import { defineStore } from 'pinia'
import axios from "axios"

export const useMainStore = defineStore('main', {
    state: () => ({ 
        stores: [],
        aisles: [],
        items: [],
        listitems: [],
        shoppinglists: [],
        shoppinglistfull: [],
        aislesbystore: [],
    }),
    getters: {
      getStores(state){
        return state.stores
      },
      getAisles(state){
        return state.aisles
      },
      getItems(state){
        return state.items
      },
      getListItems(state){
        return state.listitems
      },
      getShoppingLists(state){
        return state.shoppinglists
      },
      getShoppingListFull(state){
        return state.shoppinglistfull
      },
      getAislesByStore(state) {
        return state.aislesbystore
      }
    },
    actions: {
        async fetchAll() {
            try {
                this.fetchStores()
                this.fetchAisles()
                this.fetchItems()
                this.fetchListItems()
                this.fetchShoppingLists()
            }
            catch (error) {
                console.log(error)
            }
        },
        async fetchStores() {
            try {
                const data = await axios.get('https://shopping.danielleandjohn.love/api/stores')
                this.stores = data.data
            }
            catch (error) {
                console.log(error)
            }
        },
        async fetchAisles() {
            try {
                const data = await axios.get('https://shopping.danielleandjohn.love/api/aisles')
                this.aisles = data.data
            }
            catch (error) {
                console.log(error)
            }
        },
        async fetchItems() {
            try {
                const data = await axios.get('https://shopping.danielleandjohn.love/api/items')
                this.items = data.data
            }
            catch (error) {
                console.log(error)
            }
        },
        async fetchListItems() {
            try {
                const data = await axios.get('https://shopping.danielleandjohn.love/api/listitems')
                this.listitems = data.data
            }
            catch (error) {
                console.log(error)
            }
        },
        async fetchShoppingLists() {
            try {
                const data = await axios.get('https://shopping.danielleandjohn.love/api/shoppinglists')
                this.shoppinglists = data.data
            }
            catch (error) {
                console.log(error)
            }
        },
        async fetchShoppingListFull(list) {
            try {
                const data = await axios.get('https://shopping.danielleandjohn.love/api/shoppinglistfull/' + list)
                this.shoppinglistfull = data.data
            }
            catch (error) {
                console.log(error)
            }
        },
        async fetchAislesByStore(store) {
            try {
                const data = await axios.get('https://shopping.danielleandjohn.love/api/aislesbystore/' + store)
                this.aislesbystore = data.data
            }
            catch (error) {
                console.log(error)
            }
        },
        async addStore(store) {
            try {
                const response = await axios.post('https://shopping.danielleandjohn.love/api/stores', store)
                this.fetchStores()
                const data = {
                    "name": "Uncategorized",
                    "order": 0,
                    "store_id": response.data.id
                  }
                  console.log(response.data.id, data)
                await axios.post('https://shopping.danielleandjohn.love/api/aisles', data)
            } catch (error) {
                console.log('Error', error)
            }
        }
    },
    persist: true,
})