import { useQuery, useMutation, useQueryClient } from "@tanstack/vue-query";
import axios from "axios";

async function createStore(newStore) {
  const response = await axios.post('https://shopping.danielleandjohn.love/api/stores', newStore)
  const newAisle = {
    "name": "Uncategorized",
    "order": 0,
    "store_id": response.data.id
  }

  const aisle = await axios.post('https://shopping.danielleandjohn.love/api/aisles', newAisle)
  return {
    storeData: response.data,
    aisleData: aisle.data
  }
}

export function useStores() {
  const queryClient = useQueryClient()

  const { data: stores, isLoading } = useQuery({
    queryKey: ['stores'],
    queryFn: () => axios.call("get", "https://shopping.danielleandjohn.love/api/stores"),
    select: (response) => response.data
  })

  const createStoreMutation = useMutation({
    mutationFn: createStore,
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['stores'] })
    }
  })

  async function addStore(newStore) {
    createStoreMutation.mutate(newStore);
  }

  return {
    stores,
    isLoading,
    addStore
  }
}