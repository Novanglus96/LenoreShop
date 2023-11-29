import axios from 'axios'

const apiClient = axios.create({
  baseURL: 'https://dev.danielleandjohn.love',
  withCredentials: false,
  headers: {
    Accept: 'application/json',
    'Content-Type': 'application/json'
  }
})

export default {
    createItem(newItem) {
        return apiClient.post('/api/items', newItem)
    },
    updateItem(updatedItem) {
        return apiClient.put('/api/items/' + updatedItem.id, updatedItem)
    },
    deleteItem(deletedItem) {
        return apiClient.delete('/api/items/' + deletedItem.id)
    },
    getItems() {
        return apiClient.call("get", "/api/items")
    }
}