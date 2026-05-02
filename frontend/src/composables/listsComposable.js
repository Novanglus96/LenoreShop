import { useQuery, useMutation, useQueryClient } from "@tanstack/vue-query";
import { watch } from "vue";
import axios from "axios";
import { useMainStore } from "@/stores/main";
import {
  isOffline,
  savePendingUpdate,
  removePendingUpdate,
  loadPendingUpdates,
} from "@/composables/offlineComposable";

const apiClient = axios.create({
  baseURL: "/api",
  withCredentials: false,
  headers: {
    Accept: "application/json",
    "Content-Type": "application/json",
  },
});

function handleApiError(error, message) {
  const mainstore = useMainStore();
  if (error.response) {
    console.error("Response error:", error.response.data);
    console.error("Status code:", error.response.status);
    console.error("Headers", error.response.headers);
  } else if (error.request) {
    console.error("No response received:", error.request);
  } else {
    console.error("Error during request setup:", error.message);
  }
  mainstore.showSnackbar(message + "Error #" + error.response.status, "error");
  throw error;
}

async function createShoppingList(newShoppingList) {
  const mainstore = useMainStore();
  try {
    const response = await apiClient.post("/shoppinglists", newShoppingList);
    mainstore.showSnackbar("List created successfully!", "success");
    return response.data;
  } catch (error) {
    handleApiError(error, "List not created: ");
  }
}

async function updateListFunction(updatedList) {
  const mainstore = useMainStore();
  try {
    const response = await apiClient.put(
      "/shoppinglists/" + updatedList.id,
      updatedList,
    );
    mainstore.showSnackbar("List updated successfully!", "success");
    return response.data;
  } catch (error) {
    handleApiError(error, "List not updated: ");
  }
}

async function deleteListFunction(deletedList) {
  const mainstore = useMainStore();
  try {
    const response = await apiClient.delete("/shoppinglists/" + deletedList.id);
    mainstore.showSnackbar("List deleted successfully!", "success");
    return response.data;
  } catch (error) {
    handleApiError(error, "List not deleted: ");
  }
}

async function getShoppingListsFunction() {
  try {
    const response = await apiClient.get("/shoppinglists");
    return response.data;
  } catch (error) {
    handleApiError(error, "Lists not fetched: ");
  }
}

async function createListItem(newListItem) {
  const mainstore = useMainStore();
  try {
    const data = {
      qty: newListItem.qty,
      purchased: false,
      notes: newListItem.notes,
      item_id: newListItem.item.id,
      aisle_id: newListItem.aisle_id,
      shopping_list_id: newListItem.shopping_list_id,
    };
    const response = await apiClient.post("/listitems", data);
    mainstore.showSnackbar("List Item created successfully!", "success");
    return response.data;
  } catch (error) {
    handleApiError(error, "List Item not created: ");
  }
}

async function deleteListItemFunction(deleteListItem) {
  const mainstore = useMainStore();
  try {
    const response = await apiClient.delete("/listitems/" + deleteListItem.id);
    mainstore.showSnackbar("List Item deleted successfully!", "success");
    return response.data;
  } catch (error) {
    handleApiError(error, "List Item not deleted: ");
  }
}

async function updateListItemFunction(updatedListItem) {
  const mainstore = useMainStore();
  try {
    const data = {
      id: updatedListItem.id,
      qty: updatedListItem.qty,
      purchased: updatedListItem.purchased,
      notes: updatedListItem.notes,
      item_id: updatedListItem.item,
      aisle_id: updatedListItem.aisle_id,
      shopping_list_id: updatedListItem.shopping_list_id,
    };
    const response = await apiClient.put(
      "/listitems/" + updatedListItem.id,
      data,
    );
    mainstore.showSnackbar("List Item updated successfully!", "success");
    return response.data;
  } catch (error) {
    handleApiError(error, "List Item not updated: ");
  }
}

async function clearListFunction(shoppinglistID) {
  const mainstore = useMainStore();
  try {
    const response = await apiClient.delete(
      "/listitems/deleteall/" + shoppinglistID,
    );
    mainstore.showSnackbar("List cleared successfully!", "success");
    return response.data;
  } catch (error) {
    handleApiError(error, "List not cleared: ");
  }
}

async function clearPurchasedListFunction(shoppinglistID) {
  const mainstore = useMainStore();
  try {
    const response = await apiClient.delete(
      "/listitems/deletepurchased/" + shoppinglistID,
    );
    mainstore.showSnackbar("Purchased Items cleared successfully!", "success");
    return response.data;
  } catch (error) {
    handleApiError(error, "Purchased Items not cleared: ");
  }
}

async function getFullListFunction() {
  const mainstore = useMainStore();
  try {
    const response = await apiClient.get(
      "/shoppinglistfull/" + mainstore.list_id,
    );
    return response.data;
  } catch (error) {
    handleApiError(error, "Full List not fetched: ");
  }
}

export function useShoppingLists() {
  const queryClient = useQueryClient();

  const { data: shoppinglists, isLoading } = useQuery({
    queryKey: ["shoppinglists"],
    queryFn: getShoppingListsFunction,
    select: response => response,
    client: queryClient,
  });

  const createShoppingListMutation = useMutation({
    mutationFn: createShoppingList,
    onSuccess: () => {
      console.log("Success adding shopping list");
      queryClient.invalidateQueries({ queryKey: ["shoppinglists"] });
    },
  });

  const updateListMutation = useMutation({
    mutationFn: updateListFunction,
    onSuccess: () => {
      console.log("Success updating shopping list");
      queryClient.invalidateQueries({ queryKey: ["shoppinglists"] });
    },
  });

  const deleteListMutation = useMutation({
    mutationFn: deleteListFunction,
    onSuccess: () => {
      console.log("Success deleting shopping list");
      queryClient.invalidateQueries({ queryKey: ["shoppinglists"] });
    },
  });

  async function addShoppingList(newList) {
    createShoppingListMutation.mutate(newList);
  }

  async function editList(updatedList) {
    updateListMutation.mutate(updatedList);
  }

  async function removeList(deletedList) {
    deleteListMutation.mutate(deletedList);
  }

  return {
    shoppinglists,
    isLoading,
    addShoppingList,
    editList,
    removeList,
  };
}

// Move item between aisles/purchased_aisles in the cached full list
function applyOptimisticPurchase(old, updatedListItem) {
  if (!old) return old;
  const { id, purchased } = updatedListItem;

  const removeFromAisles = (aisles) => {
    let removedItem = null;
    let sourceAisle = null;
    const updated = aisles.map((aisle) => {
      const idx = aisle.listitems.findIndex((i) => i.id === id);
      if (idx !== -1) {
        removedItem = { ...aisle.listitems[idx], purchased };
        sourceAisle = aisle;
        return { ...aisle, listitems: aisle.listitems.filter((i) => i.id !== id) };
      }
      return aisle;
    });
    return { updated, removedItem, sourceAisle };
  };

  const addToAisles = (aisles, item, sourceAisle) => {
    const existing = aisles.find((a) => a.id === sourceAisle.id);
    if (existing) {
      return aisles.map((a) =>
        a.id === sourceAisle.id
          ? { ...a, listitems: [...a.listitems, item] }
          : a,
      );
    }
    return [...aisles, { ...sourceAisle, listitems: [item] }];
  };

  if (purchased) {
    const { updated: newAisles, removedItem, sourceAisle } = removeFromAisles(old.aisles);
    if (!removedItem) return old;
    return {
      ...old,
      aisles: newAisles,
      purchased_aisles: addToAisles(old.purchased_aisles, removedItem, sourceAisle),
      totalpurchased: old.totalpurchased + 1,
    };
  } else {
    const { updated: newPurchasedAisles, removedItem, sourceAisle } = removeFromAisles(old.purchased_aisles);
    if (!removedItem) return old;
    return {
      ...old,
      aisles: addToAisles(old.aisles, removedItem, sourceAisle),
      purchased_aisles: newPurchasedAisles,
      totalpurchased: Math.max(0, old.totalpurchased - 1),
    };
  }
}

export function useFullShoppingList(listID) {
  const queryClient = useQueryClient();

  const { data: fullshoppinglist, isLoading } = useQuery({
    queryKey: ["fullshoppinglist", listID],
    queryFn: getFullListFunction,
    select: response => response,
    client: queryClient,
  });

  const addListItemMutation = useMutation({
    mutationFn: createListItem,
    onSuccess: () => {
      console.log("Success adding list item", listID);
      queryClient.invalidateQueries({ queryKey: ["fullshoppinglist", listID] });
    },
  });

  const deleteListItemMutation = useMutation({
    mutationFn: deleteListItemFunction,
    onSuccess: () => {
      console.log("Success deleting list item", listID);
      queryClient.invalidateQueries({ queryKey: ["fullshoppinglist", listID] });
    },
  });

  const updateListItemMutation = useMutation({
    mutationFn: updateListItemFunction,
    onMutate: async (updatedListItem) => {
      await queryClient.cancelQueries({ queryKey: ["fullshoppinglist", listID] });
      const previousList = queryClient.getQueryData(["fullshoppinglist", listID]);
      queryClient.setQueryData(["fullshoppinglist", listID], (old) =>
        applyOptimisticPurchase(old, updatedListItem),
      );
      return { previousList };
    },
    onError: (err, updatedListItem, context) => {
      if (!navigator.onLine) {
        // Keep the optimistic state, queue for sync when back online
        savePendingUpdate(updatedListItem);
        return;
      }
      if (context?.previousList) {
        queryClient.setQueryData(["fullshoppinglist", listID], context.previousList);
      }
      console.error("Error updating list item");
    },
    onSuccess: (data, updatedListItem) => {
      removePendingUpdate(updatedListItem.id);
      queryClient.invalidateQueries({ queryKey: ["fullshoppinglist", listID] });
    },
  });

  const clearListMutation = useMutation({
    mutationFn: clearListFunction,
    onSuccess: () => {
      console.log("Sucess clearing list");
      queryClient.invalidateQueries({ queryKey: ["fullshoppinglist", listID] });
    },
  });

  const clearPurchasedListMutation = useMutation({
    mutationFn: clearPurchasedListFunction,
    onSuccess: () => {
      console.log("Success clearing purchased list");
      queryClient.invalidateQueries({ queryKey: ["fullshoppinglist", listID] });
    },
  });

  // Flush pending updates when connection is restored
  watch(isOffline, async (offline) => {
    if (offline) return;
    const pending = loadPendingUpdates();
    for (const item of pending) {
      try {
        await updateListItemFunction(item);
        removePendingUpdate(item.id);
      } catch {
        // Will retry on next reconnect
      }
    }
    if (pending.length > 0) {
      queryClient.invalidateQueries({ queryKey: ["fullshoppinglist", listID] });
    }
  });

  async function addListItem(listItem) {
    addListItemMutation.mutate(listItem);
  }

  async function deleteListItem(listItem) {
    deleteListItemMutation.mutate(listItem);
  }

  async function updateListItem(listItem) {
    updateListItemMutation.mutate(listItem);
  }

  async function clearList(shoppinglistID) {
    clearListMutation.mutate(shoppinglistID);
  }

  async function clearPurchasedList(shoppinglistID) {
    clearPurchasedListMutation.mutate(shoppinglistID);
  }

  return {
    fullshoppinglist,
    isLoading,
    addListItem,
    updateListItem,
    clearList,
    clearPurchasedList,
    deleteListItem,
  };
}
