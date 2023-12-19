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

async function createAisle(newAisle) {
  const mainstore = useMainStore();
  try {
    const aisle = await apiClient.post('/aisles', newAisle)
    mainstore.showSnackbar('Aisle created successfully!', 'success')
    return aisle.data
  } catch (error) {
    handleApiError(error, 'Aisle not created: ')
  }
}

async function updateAisleFunction(updatedAisle) {
  const mainstore = useMainStore();
  try {
    const aisle = await apiClient.put('/aisles/' + updatedAisle.id, updatedAisle)
    mainstore.showSnackbar('Aisle updated successfully!', 'success')
    return aisle.data
  } catch (error) {
    handleApiError(error, 'Aisle not updated: ')
  }
}

async function deleteAisleFunction(deletedAisle) {
  const mainstore = useMainStore();
  try {
    const aisle = await apiClient.delete('/aisles/' + deletedAisle.id)
    mainstore.showSnackbar('Aisle deleted successfully!', 'success')
    return aisle.data
  } catch (error) {
    handleApiError(error, 'Aisle not deleted: ')
  }
}

async function getAislesByStoreFunction() {
  const mainstore = useMainStore();
  try {
    const response = await apiClient.get('/aislesbystore/' + mainstore.store_id)
    return response.data
  } catch (error) {
    handleApiError(error, 'Aisles not fetched: ')
  }
}

//async function getAislesFunction() {
//  try {
//    const response = await apiClient.get('/aisles')
//    return response.data
//  } catch (error) {
//    handleApiError(error, 'Aisles not fetched: ')
//  }
//}
  
export function useAisles(storeID) {
  const queryClient = useQueryClient()

  const { data: aisles, isLoading } = useQuery({
    queryKey: ['aisles', storeID],
    queryFn: getAislesByStoreFunction,
    select: (response) => response,
    client: queryClient
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