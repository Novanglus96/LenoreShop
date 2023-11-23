import { useQuery, useMutation, useQueryClient } from "@tanstack/vue-query";
import ShoppingService from '@/services/ShoppingService.js'

  async function createItem(newItem) {
    ShoppingService.createItem(newItem)
    .then((response) => {
      return response.data
    })
    .catch((error) => {
      console.log(error)
    })
  }

  async function updateItemFunction(updatedItem) {
    ShoppingService.updateItem(updatedItem)
      .then((response) => {
        return response.data
      })
      .catch((error) => {
        console.log(error)
      })
  }

  async function deleteItemFunction(deletedItem) {
    ShoppingService.deleteItem(deletedItem)
      .then((response) => {
        return response.data
      })
      .catch((error) => {
        console.log(error)
      })
  }
  
  export function useItems() {
    const queryClient = useQueryClient()

    const { data: items, isLoading } = useQuery({
      queryKey: ['items'],
      queryFn: () => ShoppingService.getItems(),
      select: (response) => response.data
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