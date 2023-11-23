import { useQuery, useMutation, useQueryClient } from "@tanstack/vue-query";
import axios from "axios";

  async function createAisle(newAisle) {
    const aisle = await axios.post('/api/aisles', newAisle)
    
    return aisle.data
  }

  async function updateAisleFunction(updatedAisle) {
    const aisle = await axios.put('/api/aisles/' + updatedAisle.id, updatedAisle)
    
    return aisle.data
  }

  async function deleteAisleFunction(deletedAisle) {
    const aisle = await axios.delete('/api/aisles/' + deletedAisle.id)
    
    return aisle.data
  }
  
  export function useAisles(storeID) {
    const queryClient = useQueryClient()

    const { data: aisles, isLoading } = useQuery({
      queryKey: ['aisles', storeID],
      queryFn: () => axios.call("get", "/api/aislesbystore/" + storeID),
      select: (response) => response.data
    })
    
    const createAisleMutation = useMutation({
      mutationFn: createAisle,
      onSuccess: () => {
        console.log('Success adding aisle', storeID)
        queryClient.invalidateQueries({ queryKey: ['aisles', storeID] })
      }
    })

    const updateAisleMutation = useMutation({
      mutationFn: updateAisleFunction,
      onSuccess: () => {
        console.log('Success updating aisle')
        queryClient.invalidateQueries({ queryKey: ['aisles', storeID]})
      }
    })

    const deleteAisleMutation = useMutation({
      mutationFn: deleteAisleFunction,
      onSuccess: () => {
        console.log('Success deleting aisle')
        queryClient.invalidateQueries({ queryKey: ['aisles', storeID]})
      }
    })
  
    async function addAisle(newAisle) {
      createAisleMutation.mutate(newAisle);
    }

    async function editAisle(updatedAisle) {
      updateAisleMutation.mutate(updatedAisle);
    }

    async function removeAisle(deletedAisle) {
      deleteAisleMutation.mutate(deletedAisle);
    }
  
    return {
      aisles,
      isLoading,
      addAisle,
      editAisle,
      removeAisle
    }
  }