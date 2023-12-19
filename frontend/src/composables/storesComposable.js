import { useQuery, useMutation, useQueryClient } from "@tanstack/vue-query";
import axios from "axios";
import { useMainStore } from "@/stores/main";

const apiClient = axios.create({
  baseURL: '/api',
  withCredentials: false,
  headers: {
    Accept: 'application/json',
    'Content-Type': 'application/json'
  }
})

function handleApiError(error, message) {
  const mainstore = useMainStore();
  if (error.response) {
    console.error('Response error:', error.response.data)
    console.error('Status code:', error.response.status)
    console.error('Headers', error.response.headers)
  } else if (error.request){
    console.error('No response received:', error.request)
  } else {
    console.error('Error during request setup:', error.message)
  }
  mainstore.showSnackbar(message + 'Error #' + error.response.status, 'error')
  throw error
}

async function createStore(newStore) {
  const mainstore = useMainStore();
  try {
    const response = await apiClient.post('/stores', newStore)
    mainstore.showSnackbar('Store created successfully!', 'success')
    const newAisle = {
      "name": "Uncategorized",
      "order": 0,
      "store_id": response.data.id
    }
    const aisle = await apiClient.post('/aisles', newAisle)
    return {
    storeData: response.data,
    aisleData: aisle.data
    }
  } catch (error) {
    handleApiError(error, 'Store not created: ')
  }
}

async function updateStoreFunction(updatedStore) {
  const mainstore = useMainStore();
  try {
    const response = await apiClient.put('/stores/' + updatedStore.id, updatedStore)
    mainstore.showSnackbar('Store updated successfully!', 'success')
    return response.data
  } catch (error) {
    handleApiError(error, 'Store not updated: ')
  }
}

async function deleteStoreFunction(deletedStore) {
  const mainstore = useMainStore();
  try {
    const response = await apiClient.delete('/stores/' + deletedStore.id)
    mainstore.showSnackbar('Store deleted successfully!', 'success')
    return response.data
  } catch (error) {
    handleApiError(error, 'Store not deleted: ')
  }
}

async function getStoresFunction() {
  try {
    const response = await apiClient.get('/stores')
    return response.data
  } catch (error) {
    handleApiError(error, 'Stores not fetched: ')
  }
}

export function useStores() {
  const queryClient = useQueryClient()

  const { data: stores, isLoading } = useQuery({
    queryKey: ['stores'],
    queryFn: getStoresFunction,
    select: (response) => response,
    client: queryClient
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