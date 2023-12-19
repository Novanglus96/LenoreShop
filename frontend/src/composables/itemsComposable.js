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

async function createItem(newItem) {
  const mainstore = useMainStore();
  try {
    const response = await apiClient.post('/items', newItem)
    mainstore.showSnackbar('Item created successfully!', 'success')
    return response.data
  } catch (error) {
    handleApiError(error, 'Item not created: ')
  }
}

async function updateItemFunction(updatedItem) {
  const mainstore = useMainStore();
  try {
    const response = await apiClient.put('/items/' + updatedItem.id, updatedItem)
    mainstore.showSnackbar('Item updated successfully!', 'success')
    return response.data
  } catch (error) {
    handleApiError(error, 'Item not updated: ')
  }
}

async function deleteItemFunction(deletedItem) {
  const mainstore = useMainStore();
  try {
    const response = await apiClient.delete('/items/' + deletedItem.id)
    mainstore.showSnackbar('Item deleted successfully!', 'success')
    return response.data
  } catch (error) {
    handleApiError(error, 'Item not deleted: ')
  }
}

async function getItemsFunction() {
  try {
    const response = await apiClient.get('/items')
    return response.data
  } catch (error) {
    handleApiError(error, 'Items not fetched: ')
  }
}

export function useItems() {
  const queryClient = useQueryClient()

  const { data: items, isLoading } = useQuery({
    queryKey: ['items'],
    queryFn: getItemsFunction,
    select: (response) => response,
    client: queryClient
  })
  
  const createItemMutation = useMutation({
    mutationFn: createItem,
    onSuccess: (data) => {
      console.log('Success adding item', data)
      queryClient.invalidateQueries({ queryKey: ['items'] })
      return data
    }
  })

  const updateItemMutation = useMutation({
    mutationFn: updateItemFunction,
    onSuccess: () => {
      console.log('Success updating item')
      queryClient.invalidateQueries({ queryKey: ['items']})
    }
  })

  const deleteItemMutation = useMutation({
    mutationFn: deleteItemFunction,
    onSuccess: () => {
      console.log('Success deleting item')
      queryClient.invalidateQueries({ queryKey: ['items']})
    }
  })

  async function addItem(newItem) {
    const item = await createItemMutation.mutateAsync(newItem)
    return item
  }

  async function editItem(updatedItem) {
    updateItemMutation.mutate(updatedItem);
  }

  async function removeItem(deletedItem) {
    deleteItemMutation.mutate(deletedItem);
  }

  return {
    items,
    isLoading,
    addItem,
    editItem,
    removeItem
  }
}