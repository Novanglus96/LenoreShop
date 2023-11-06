import { useQuery, useMutation, useQueryClient } from "@tanstack/vue-query";
import axios from "axios";

async function createItem(newItem) {
    const item = await axios.post('https://shopping.danielleandjohn.love/api/items', newItem)
    
    return item.data
  }
  
  export function useItems() {
    const queryClient = useQueryClient()

    const { data: items, isLoading } = useQuery({
      queryKey: ['items'],
      queryFn: () => axios.call("get", "https://shopping.danielleandjohn.love/api/items"),
      select: (response) => response.data
    })
    
    const createItemMutation = useMutation({
      mutationFn: createItem,
      onSuccess: () => {
        console.log('Success adding item')
        queryClient.invalidateQueries({ queryKey: ['items'] })
      }
    })
  
    async function addItem(newItem) {
      createItemMutation.mutate(newItem);
    }
  
    return {
      items,
      isLoading,
      addItem
    }
  }