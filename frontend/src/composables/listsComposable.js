import { useQuery, useMutation, useQueryClient } from "@tanstack/vue-query";
import axios from "axios";

  async function createShoppingList(newShoppingList) {
    const shoppingList = await axios.post('/api/shoppinglists', newShoppingList)
    
    return shoppingList.data
  }

  async function createListItem(newListItem) {
    const listitem = await axios.post('/api/listitems', newListItem)
    
    return listitem.data
  }

  async function updateListItemFunction(updatedListItem) {
    const listitem = await axios.put('/api/listitems/' + updatedListItem.id, updatedListItem)
    
    return listitem.data
  }

  async function clearListFunction(shoppinglistID) {
    const shoppinglist = await axios.delete('/api/listitems/deleteall/' + shoppinglistID)

    return shoppinglist
  }

  async function clearPurchasedListFunction(shoppinglistID) {
    const shoppinglist = await axios.delete('/api/listitems/deletepurchased/' + shoppinglistID)

    return shoppinglist
  }

  async function updateListFunction(updatedList) {
    const list = await axios.put('/api/shoppinglists/' + updatedList.id, updatedList)
    
    return list.data
  }

  async function deleteListFunction(deletedList) {
    const list = await axios.delete('/api/shoppinglists/' + deletedList.id)
    
    return list.data
  }
  
  export function useShoppingLists() {
    const queryClient = useQueryClient()

    const { data: shoppinglists, isLoading } = useQuery({
      queryKey: ['shoppinglists'],
      queryFn: () => axios.call("get", "/api/shoppinglists"),
      select: (response) => response.data
    })
    
    const createShoppingListMutation = useMutation({
      mutationFn: createShoppingList,
      onSuccess: () => {
        console.log('Success adding shopping list')
        queryClient.invalidateQueries({ queryKey: ['shoppinglists'] })
      }
    })

    const updateListMutation = useMutation({
      mutationFn: updateListFunction,
      onSuccess: () => {
        console.log('Success updating shopping list')
        queryClient.invalidateQueries({ queryKey: ['shoppinglists'] })
      }
    })

    const deleteListMutation = useMutation({
      mutationFn: deleteListFunction,
      onSuccess: () => {
        console.log('Success deleting shopping list')
        queryClient.invalidateQueries({ queryKey: ['shoppinglists'] })
      }
    })
  
    async function addShoppingList(newList) {
      createShoppingListMutation.mutate(newList);
    }

    async function editList(updatedList) {
      updateListMutation.mutate(updatedList);
    }

    async function removeList(deletedList) {
      deleteListMutation.mutate(deletedList);
    }
  
    return {
      shoppinglists,
      isLoading,
      addShoppingList,
      editList,
      removeList
    }
  }

  export function useFullShoppingList(listID) {
    const queryClient = useQueryClient()

    const { data: fullshoppinglist, isLoading } = useQuery({
      queryKey: ['fullshoppinglist', listID],
      queryFn: () => axios.call("get", "/api/shoppinglistfull/" + listID),
      select: (response) => response.data
    })

    const addListItemMutation = useMutation({
      mutationFn: createListItem,
      onSuccess: () => {
        console.log('Success adding list item', listID)
        queryClient.invalidateQueries({ queryKey: ['fullshoppinglist', listID]})
      }
    })

    const updateListItemMutation = useMutation({
      mutationFn: updateListItemFunction,
      onSuccess: () => {
        console.log('Success updating list item')
        queryClient.invalidateQueries({ queryKey: ['fullshoppinglist', listID]})
      }
    })

    const clearListMutation = useMutation({
      mutationFn: clearListFunction,
      onSuccess: () => {
        console.log('Sucess clearing list')
        queryClient.invalidateQueries({ queryKey: ['fullshoppinglist', listID]})
      }
    })

    const clearPurchasedListMutation = useMutation({
      mutationFn: clearPurchasedListFunction,
      onSuccess: () => {
        console.log('Success clearing purchased list')
        queryClient.invalidateQueries({ queryKey: ['fullshoppinglist', listID]})
      }
    })

    async function addListItem(listItem) {
      addListItemMutation.mutate(listItem);
    }

    async function updateListItem(listItem) {
      updateListItemMutation.mutate(listItem);
    }

    async function clearList(shoppinglistID) {
      clearListMutation.mutate(shoppinglistID);
    }

    async function clearPurchasedList(shoppinglistID) {
      clearPurchasedListMutation.mutate(shoppinglistID);
    }

    return {
      fullshoppinglist,
      isLoading,
      addListItem,
      updateListItem,
      clearList,
      clearPurchasedList
    }
  }