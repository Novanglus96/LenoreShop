import { useQuery, useMutation, useQueryClient } from "@tanstack/vue-query";
import axios from "axios";

async function createShoppingList(newShoppingList) {
    const shoppingList = await axios.post('https://shopping.danielleandjohn.love/api/shoppinglists', newShoppingList)
    
    return shoppingList.data
  }
  
  export function useShoppingLists() {
    const queryClient = useQueryClient()

    const { data: shoppinglists, isLoading } = useQuery({
      queryKey: ['shoppinglists'],
      queryFn: () => axios.call("get", "https://shopping.danielleandjohn.love/api/shoppinglists"),
      select: (response) => response.data
    })
    
    const createShoppingListMutation = useMutation({
      mutationFn: createShoppingList,
      onSuccess: () => {
        console.log('Success adding shopping list', storeID)
        queryClient.invalidateQueries({ queryKey: ['shoppinglists'] })
      }
    })
  
    async function addShoppingList(newList) {
      createShoppingListMutation.mutate(newList);
    }
  
    return {
      shoppinglists,
      isLoading,
      addShoppingList
    }
  }

  export function useFullShoppingList(listID) {
    const queryClient = useQueryClient()

    const { data: fullshoppinglist, isLoading } = useQuery({
      queryKey: ['fullshoppinglist', listID],
      queryFn: () => axios.call("get", "https://shopping.danielleandjohn.love/api/shoppinglistfull/" + listID),
      select: (response) => response.data
    })

    const addListItemMutation = useMutation({
      mutationFn: addListItem,
      onSuccess: () => {
        console.log('Success adding list item', listID)
        queryClient.invalidateQueries({ queryKey: ['fullshoppinglist', listID]})
      }
    })

    async function addListItem(listItem) {
      addListItemMutation.mutate(listItem);
    }

    return {
      fullshoppinglist,
      isLoading,
      addListItem
    }
  }