import { useQuery, useMutation, useQueryClient } from "@tanstack/vue-query";
import axios from "axios";
import { useMainStore } from "@/stores/main";
import { useItemStore } from "@/stores/item";

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

async function createItem(newItem) {
  const mainstore = useMainStore();
  try {
    const response = await apiClient.post("/items", newItem);
    mainstore.showSnackbar("Item created successfully!", "success");
    return response.data;
  } catch (error) {
    handleApiError(error, "Item not created: ");
  }
}

async function updateItemFunction(updatedItem) {
  const mainstore = useMainStore();
  try {
    const response = await apiClient.put(
      "/items/" + updatedItem.id,
      updatedItem,
    );
    mainstore.showSnackbar("Item updated successfully!", "success");
    return response.data;
  } catch (error) {
    handleApiError(error, "Item not updated: ");
  }
}

async function deleteItemFunction(deletedItem) {
  const mainstore = useMainStore();
  try {
    const response = await apiClient.delete("/items/" + deletedItem.id);
    mainstore.showSnackbar("Item deleted successfully!", "success");
    return response.data;
  } catch (error) {
    handleApiError(error, "Item not deleted: ");
  }
}

/**
 * Uploads or clears an item's photo.
 *
 * Kept separate from updateItemFunction because the rest of the API is JSON and
 * a file has to go up as multipart — and because saving a rename should not
 * re-send a photo that has not changed.
 *
 * @param {number} itemId The item to attach the photo to.
 * @param {Object} image The `{ file, remove }` staged by ImagePicker.
 */
async function saveItemImage(itemId, image) {
  if (!itemId || !image) return;

  try {
    if (image.file) {
      const body = new FormData();
      body.append("image", image.file);
      // The Content-Type override is load-bearing, not decoration. apiClient
      // defaults to application/json, and axios silently converts a FormData
      // body to JSON when it sees a JSON content type — the file would be
      // dropped with no error. The value set here is then replaced by the
      // browser with the same type plus the multipart boundary.
      await apiClient.post(`/items/${itemId}/image`, body, {
        headers: { "Content-Type": "multipart/form-data" },
      });
    } else if (image.remove) {
      await apiClient.delete(`/items/${itemId}/image`);
    }
  } catch (error) {
    handleApiError(error, "Photo not saved: ");
  }
}

async function getItemsFunction(pageinfo, full) {
  try {
    let params =
      "?page=" +
      pageinfo.page +
      "&page_size=" +
      pageinfo.page_size +
      "&full=" +
      full;
    const response = await apiClient.get("/items" + params);
    return response.data;
  } catch (error) {
    handleApiError(error, "Items not fetched: ");
  }
}

/**
 * Just the photo half of an item, with no items query attached.
 *
 * The shopping list needs to save a photo but has no use for the paginated
 * catalog that useItems() fetches, and taking useItems() there would run that
 * query on the page you use most.
 */
export function useItemImage() {
  const queryClient = useQueryClient();

  // A photo is saved on its own request, separately from the item, because a
  // new item has no id to upload against until it has been created. `image` is
  // the ImagePicker's staged `{ file, remove }`.
  async function saveImageFor(itemId, image) {
    if (!itemId || !(image?.file || image?.remove)) return;
    await saveItemImage(itemId, image);
    // A photo lives on the catalog item, so it shows up on the catalog page and
    // on every list row using that item. Both sets of keys have to drop.
    queryClient.invalidateQueries({ queryKey: ["items"] });
    queryClient.invalidateQueries({ queryKey: ["fullshoppinglist"] });
  }

  return { saveImageFor };
}

export function useItems(full) {
  const queryClient = useQueryClient();
  const itemstore = useItemStore();
  const { saveImageFor } = useItemImage();
  const { data: items, isLoading } = useQuery({
    queryKey: ["items", itemstore.pageinfo, full],
    queryFn: () => getItemsFunction(itemstore.pageinfo, full),
    select: response => response,
    client: queryClient,
  });

  const createItemMutation = useMutation({
    mutationFn: createItem,
    onSuccess: data => {
      console.log("Success adding item", data);
      queryClient.invalidateQueries({ queryKey: ["items"] });
      return data;
    },
  });

  const updateItemMutation = useMutation({
    mutationFn: updateItemFunction,
    onSuccess: () => {
      console.log("Success updating item");
      queryClient.invalidateQueries({ queryKey: ["items"] });
    },
  });

  const deleteItemMutation = useMutation({
    mutationFn: deleteItemFunction,
    onSuccess: () => {
      console.log("Success deleting item");
      queryClient.invalidateQueries({ queryKey: ["items"] });
    },
  });

  async function addItem(newItem) {
    const { image, ...fields } = newItem;
    const item = await createItemMutation.mutateAsync(fields);
    await saveImageFor(item?.id, image);
    return item;
  }

  async function editItem(updatedItem) {
    const { image, ...fields } = updatedItem;
    await updateItemMutation.mutateAsync(fields);
    await saveImageFor(fields.id, image);
  }

  async function removeItem(deletedItem) {
    deleteItemMutation.mutate(deletedItem);
  }

  return {
    items,
    isLoading,
    addItem,
    editItem,
    removeItem,
  };
}
