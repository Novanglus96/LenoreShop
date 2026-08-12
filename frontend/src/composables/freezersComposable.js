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

  async function addFreezerItem(newFreezerItem) {
    createFreezerItemMutation.mutate(newFreezerItem);
  }

  async function editFreezerItem(updatedFreezerItem) {
    updateFreezerItemMutation.mutate(updatedFreezerItem);
  }

  async function removeFreezerItem(deletedFreezerItem) {
    deleteFreezerItemMutation.mutate(deletedFreezerItem);
  }

  return {
    freezerfull,
    isLoading,
    addFreezerItem,
    editFreezerItem,
    removeFreezerItem,
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
