import { useQuery, useMutation, useQueryClient } from "@tanstack/vue-query";
import axios from "axios";

  async function createItem(newItem) {
    const item = await axios.post('/api/items', newItem)
    return item.data
  }

  async function updateItemFunction(updatedItem) {
    const item = await axios.put('/api/items/' + updatedItem.id, updatedItem)
    
    return item.data
  }

  async function deleteItemFunction(deletedItem) {
    const item = await axios.delete('/api/items/' + deletedItem.id)
    
    return item.data
  }
  
  export function useItems() {
    const queryClient = useQueryClient()

    const { data: items, isLoading } = useQuery({
      queryKey: ['items'],
      queryFn: () => axios.call("get", "/api/items"),
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