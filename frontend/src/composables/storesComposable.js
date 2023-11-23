import { useQuery, useMutation, useQueryClient } from "@tanstack/vue-query";
import axios from "axios";

async function createStore(newStore) {
  const response = await axios.post('/api/stores', newStore)
  const newAisle = {
    "name": "Uncategorized",
    "order": 0,
    "store_id": response.data.id
  }

  const aisle = await axios.post('/api/aisles', newAisle)
  return {
    storeData: response.data,
    aisleData: aisle.data
  }
}

async function updateStoreFunction(updatedStore) {
  const store = await axios.put('/api/stores/' + updatedStore.id, updatedStore)

  return store.data
}

async function deleteStoreFunction(deletedStore) {
  const store = await axios.delete('/api/stores/' + deletedStore.id)

  return store.data
}

export function useStores() {
  const queryClient = useQueryClient()

  const { data: stores, isLoading } = useQuery({
    queryKey: ['stores'],
    queryFn: () => axios.call("get", "/api/stores"),
    select: (response) => response.data
  })

  const createStoreMutation = useMutation({
    mutationFn: createStore,
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['stores'] })
    }
  })

  const updateStoreMutation = useMutation({
    mutationFn: updateStoreFunction,
    onSuccess: () => {
      console.log('Success updating store')
      queryClient.invalidateQueries({ queryKey: ['stores']})
    }
  })

  const deleteStoreMutation = useMutation({
    mutationFn: deleteStoreFunction,
    onSuccess: () => {
      console.log('Success deleting store')
      queryClient.invalidateQueries({ queryKey: ['stores']})
    }
  })

  async function addStore(newStore) {
    createStoreMutation.mutate(newStore);
  }

  async function editStore(updatedStore) {
    updateStoreMutation.mutate(updatedStore)
  }

  async function removeStore(deletedStore) {
    deleteStoreMutation.mutate(deletedStore)
  }

  return {
    stores,
    isLoading,
    addStore,
    editStore,
    removeStore
  }
}