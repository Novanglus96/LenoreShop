import { useQuery, useMutation, useQueryClient } from "@tanstack/vue-query";
import axios from "axios";
import { useMainStore } from "@/stores/main";

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

async function createFreezer(newFreezer) {
  const mainstore = useMainStore();
  try {
    const response = await apiClient.post("/freezers", newFreezer);
    mainstore.showSnackbar("Freezer created successfully!", "success");
    return response.data;
  } catch (error) {
    handleApiError(error, "Freezer not created: ");
  }
}

async function updateFreezerFunction(updatedFreezer) {
  const mainstore = useMainStore();
  try {
    const response = await apiClient.put(
      "/freezers/" + updatedFreezer.id,
      updatedFreezer,
    );
    mainstore.showSnackbar("Freezer updated successfully!", "success");
    return response.data;
  } catch (error) {
    handleApiError(error, "Freezer not updated: ");
  }
}

async function deleteFreezerFunction(deletedFreezer) {
  const mainstore = useMainStore();
  try {
    const response = await apiClient.delete("/freezers/" + deletedFreezer.id);
    mainstore.showSnackbar("Freezer deleted successfully!", "success");
    return response.data;
  } catch (error) {
    handleApiError(error, "Freezer not deleted: ");
  }
}

async function getFreezersFunction() {
  try {
    const response = await apiClient.get("/freezers");
    return response.data;
  } catch (error) {
    handleApiError(error, "Freezers not fetched: ");
  }
}

async function getFreezerFullFunction(freezerID) {
  try {
    const response = await apiClient.get("/freezerfull/" + freezerID);
    return response.data;
  } catch (error) {
    handleApiError(error, "Freezer contents not fetched: ");
  }
}

async function getExpiringFunction(days) {
  try {
    const response = await apiClient.get("/freezeritemsexpiring?days=" + days);
    return response.data;
  } catch (error) {
    handleApiError(error, "Expiring foods not fetched: ");
  }
}

async function createFreezerItemFunction(newFreezerItem) {
  const mainstore = useMainStore();
  try {
    const response = await apiClient.post("/freezeritems", newFreezerItem);
    mainstore.showSnackbar("Food added successfully!", "success");
    return response.data;
  } catch (error) {
    handleApiError(error, "Food not added: ");
  }
}

async function updateFreezerItemFunction(updatedFreezerItem) {
  const mainstore = useMainStore();
  try {
    const response = await apiClient.put(
      "/freezeritems/" + updatedFreezerItem.id,
      updatedFreezerItem,
    );
    mainstore.showSnackbar("Food updated successfully!", "success");
    return response.data;
  } catch (error) {
    handleApiError(error, "Food not updated: ");
  }
}

async function deleteFreezerItemFunction(deletedFreezerItem) {
  const mainstore = useMainStore();
  try {
    const response = await apiClient.delete(
      "/freezeritems/" + deletedFreezerItem.id,
    );
    mainstore.showSnackbar("Food removed successfully!", "success");
    return response.data;
  } catch (error) {
    handleApiError(error, "Food not removed: ");
  }
}

/**
 * Surfaces the backend's own message for a rejected use or transfer.
 *
 * These two endpoints reject with something the user can act on — "Only 3 of
 * Chili in the freezer" — which is far more useful than the bare status code
 * `handleApiError` shows. Anything else falls through to the usual handler.
 *
 * @param {Object} error The axios error.
 * @param {string} message Prefix used when there is no detail to show.
 */
function handleFreezerActionError(error, message) {
  const detail = error.response?.data?.detail;
  if (!detail) {
    handleApiError(error, message);
    return;
  }
  useMainStore().showSnackbar(detail, "error");
  throw error;
}

async function useFreezerItemFunction({ id, qty }) {
  const mainstore = useMainStore();
  try {
    const response = await apiClient.post(`/freezeritems/${id}/use`, { qty });
    mainstore.showSnackbar(
      response.data.removed
        ? "Used the last of it — removed from the freezer."
        : `Used ${qty}. ${response.data.remaining} left.`,
      "success",
    );
    return response.data;
  } catch (error) {
    handleFreezerActionError(error, "Food not used: ");
  }
}

async function transferFreezerItemFunction({ id, freezer_id, qty, name }) {
  const mainstore = useMainStore();
  try {
    // qty omitted entirely means "all of it", which relocates the row rather
    // than splitting it. Sending null would fail schema validation.
    const payload = qty == null ? { freezer_id } : { freezer_id, qty };
    const response = await apiClient.post(
      `/freezeritems/${id}/transfer`,
      payload,
    );
    mainstore.showSnackbar(
      response.data.created
        ? `Moved ${qty} of ${name}. ${response.data.remaining} left behind.`
        : `Moved ${name}.`,
      "success",
    );
    return response.data;
  } catch (error) {
    handleFreezerActionError(error, "Food not moved: ");
  }
}

/**
 * Uploads or clears a freezer item's photo.
 *
 * Separate from the item PUT because a file has to go up as multipart while the
 * rest of the API is JSON.
 *
 * @param {number} freezerItemId The freezer item to attach the photo to.
 * @param {Object} image The `{ file, remove }` staged by ImagePicker.
 */
async function saveFreezerItemImage(freezerItemId, image) {
  if (!freezerItemId || !image) return;

  try {
    if (image.file) {
      const body = new FormData();
      body.append("image", image.file);
      // See itemsComposable: apiClient defaults to application/json, and axios
      // turns a FormData body into JSON when it sees that, silently dropping
      // the file. The browser replaces this value with the multipart boundary.
      await apiClient.post(`/freezeritems/${freezerItemId}/image`, body, {
        headers: { "Content-Type": "multipart/form-data" },
      });
    } else if (image.remove) {
      await apiClient.delete(`/freezeritems/${freezerItemId}/image`);
    }
  } catch (error) {
    handleApiError(error, "Photo not saved: ");
  }
}

export function useFreezers() {
  const queryClient = useQueryClient();

  const { data: freezers, isLoading } = useQuery({
    queryKey: ["freezers"],
    queryFn: getFreezersFunction,
    select: response => response,
    client: queryClient,
  });

  const createFreezerMutation = useMutation({
    mutationFn: createFreezer,
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ["freezers"] });
    },
  });

  const updateFreezerMutation = useMutation({
    mutationFn: updateFreezerFunction,
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ["freezers"] });
      queryClient.invalidateQueries({ queryKey: ["freezerfull"] });
    },
  });

  const deleteFreezerMutation = useMutation({
    mutationFn: deleteFreezerFunction,
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ["freezers"] });
      queryClient.invalidateQueries({ queryKey: ["freezerfull"] });
    },
  });

  async function addFreezer(newFreezer) {
    createFreezerMutation.mutate(newFreezer);
  }

  async function editFreezer(updatedFreezer) {
    updateFreezerMutation.mutate(updatedFreezer);
  }

  async function removeFreezer(deletedFreezer) {
    deleteFreezerMutation.mutate(deletedFreezer);
  }

  return {
    freezers,
    isLoading,
    addFreezer,
    editFreezer,
    removeFreezer,
  };
}

export function useFreezerFull(freezerID) {
  const queryClient = useQueryClient();

  const { data: freezerfull, isLoading } = useQuery({
    queryKey: ["freezerfull", freezerID],
    queryFn: () => getFreezerFullFunction(freezerID),
    select: response => response,
    client: queryClient,
  });

  function invalidate() {
    queryClient.invalidateQueries({ queryKey: ["freezerfull", freezerID] });
    queryClient.invalidateQueries({ queryKey: ["freezeritems"] });
    // The freezer list carries the dashboard's item and expiry counts, so
    // changing an item's contents or its discard date changes them too.
    queryClient.invalidateQueries({ queryKey: ["freezers"] });
  }

  const createFreezerItemMutation = useMutation({
    mutationFn: createFreezerItemFunction,
    onSuccess: invalidate,
  });

  const updateFreezerItemMutation = useMutation({
    mutationFn: updateFreezerItemFunction,
    onSuccess: invalidate,
  });

  const deleteFreezerItemMutation = useMutation({
    mutationFn: deleteFreezerItemFunction,
    onSuccess: invalidate,
  });

  const useFreezerItemMutation = useMutation({
    mutationFn: useFreezerItemFunction,
    onSuccess: invalidate,
  });

  const transferFreezerItemMutation = useMutation({
    mutationFn: transferFreezerItemFunction,
    // A transfer changes two freezers, and `invalidate` is scoped to the one
    // being viewed, so refresh the target's contents as well.
    onSuccess: (data, variables) => {
      invalidate();
      queryClient.invalidateQueries({
        queryKey: ["freezerfull", variables.freezer_id],
      });
    },
  });

  // A photo is saved on its own request after the food itself, because a new
  // freezer item has no id to upload against until it has been created.
  // `image` is the ImagePicker's staged `{ file, remove }`.
  async function saveImageFor(freezerItemId, image) {
    if (!freezerItemId || !(image?.file || image?.remove)) return;
    await saveFreezerItemImage(freezerItemId, image);
    invalidate();
  }

  async function addFreezerItem(newFreezerItem) {
    const { image, ...fields } = newFreezerItem;
    const created = await createFreezerItemMutation.mutateAsync(fields);
    await saveImageFor(created?.id, image);
  }

  async function editFreezerItem(updatedFreezerItem) {
    const { image, ...fields } = updatedFreezerItem;
    await updateFreezerItemMutation.mutateAsync(fields);
    await saveImageFor(fields.id, image);
  }

  async function removeFreezerItem(deletedFreezerItem) {
    deleteFreezerItemMutation.mutate(deletedFreezerItem);
  }

  // Rejections are already reported to the user by the mutation function, so
  // swallow them here rather than leaving an unhandled rejection behind.
  async function useFreezerItem(freezerItem, qty) {
    try {
      await useFreezerItemMutation.mutateAsync({ id: freezerItem.id, qty });
    } catch {
      /* reported via snackbar */
    }
  }

  // `qty` omitted moves the whole row.
  async function transferFreezerItem(freezerItem, freezerId, qty) {
    try {
      await transferFreezerItemMutation.mutateAsync({
        id: freezerItem.id,
        freezer_id: freezerId,
        qty,
        name: freezerItem.name,
      });
    } catch {
      /* reported via snackbar */
    }
  }

  return {
    freezerfull,
    isLoading,
    addFreezerItem,
    editFreezerItem,
    removeFreezerItem,
    useFreezerItem,
    transferFreezerItem,
  };
}

export function useExpiringFreezerItems(days = 14) {
  const queryClient = useQueryClient();

  const { data: expiringItems, isLoading } = useQuery({
    queryKey: ["freezeritems", "expiring", days],
    queryFn: () => getExpiringFunction(days),
    select: response => response,
    client: queryClient,
  });

  return {
    expiringItems,
    isLoading,
  };
}
