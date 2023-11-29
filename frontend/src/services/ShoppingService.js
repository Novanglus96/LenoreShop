import axios from 'axios'

const apiClient = axios.create({
  baseURL: '/api',
  withCredentials: false,
  headers: {
    Accept: 'application/json',
    'Content-Type': 'application/json'
  }
})

export default {
    createItem(newItem) {
        return apiClient.post('/items', newItem)
    },
    updateItem(updatedItem) {
        return apiClient.put('/items/' + updatedItem.id, updatedItem)
    },
    deleteItem(deletedItem) {
        return apiClient.delete('/items/' + deletedItem.id)
    },
    getItems() {
        return apiClient.call("get", "/items")
    }
}