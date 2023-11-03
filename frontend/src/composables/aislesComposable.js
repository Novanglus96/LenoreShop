import { useQuery, useMutation, useQueryClient } from "@tanstack/vue-query";
import axios from "axios";

async function createAisle(newAisle) {
    const aisle = await axios.post('https://shopping.danielleandjohn.love/api/aisles', newAisle)
    
    return aisle.data
  }
  
  export function useAisles(storeID) {
    const queryClient = useQueryClient()
  
    const { data: aisles, isLoading } = useQuery({
      queryKey: ['aisles', storeID],
      queryFn: () => axios.call("get", "https://shopping.danielleandjohn.love/api/aislesbystore/" + storeID),
      select: (response) => response.data
    })
  
    const createAisleMutation = useMutation({
      mutationFn: createAisle,
      onSuccess: () => {
        console.log('Success adding aisle', storeID)
        queryClient.invalidateQueries({ queryKey: ['aisles', storeID] })
      }
    })
  
    async function addAisle(newAisle) {
      createAisleMutation.mutate(newAisle);
    }
  
    return {
      aisles,
      isLoading,
      addAisle
    }
  }