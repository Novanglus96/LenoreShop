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
        listsbystore: [],
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
      },
      getListsByStore(state) {
        return state.listsbystore
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
        async fetchListsByStore(store) {
            try {
                const data = await axios.get('https://shopping.danielleandjohn.love/api/listsbystore/' + store)
                this.listsbystore = data.data
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
                await axios.post('https://shopping.danielleandjohn.love/api/aisles', data)
            } catch (error) {
                console.log('Error', error)
            }
        },
        async addItem(item) {
            try {
                const response = await axios.post('https://shopping.danielleandjohn.love/api/items', item)
                this.fetchItems()
                console.log(response)
            } catch (error) {
                console.log('Error', error)
            }
        },
        async addList(list) {
            try {
                const response = await axios.post('https://shopping.danielleandjohn.love/api/shoppinglists', list)
                this.fetchShoppingLists()
                console.log(response)
            } catch (error) {
                console.log('Error', error)
            }
        }
    },
    persist: true,
})