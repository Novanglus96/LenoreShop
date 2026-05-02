import { useMutation, useQueryClient } from "@tanstack/vue-query";
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

async function loadDemoDataFn() {
  const response = await apiClient.post("/demo/load");
  return response.data;
}

export function useDemo() {
  const queryClient = useQueryClient();
  const mainstore = useMainStore();

  const loadDemoMutation = useMutation({
    mutationFn: loadDemoDataFn,
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ["stores"] });
      queryClient.invalidateQueries({ queryKey: ["shoppinglists"] });
      mainstore.showSnackbar("Demo data loaded!", "success");
    },
    onError: (error) => {
      const msg =
        error.response?.data?.detail || "Could not load demo data.";
      mainstore.showSnackbar(msg, "error");
    },
  });

  function loadDemo() {
    loadDemoMutation.mutate();
  }

  return {
    loadDemo,
    isDemoLoading: loadDemoMutation.isPending,
  };
}
