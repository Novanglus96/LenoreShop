import { defineStore } from 'pinia'
import axios from "axios"

export const useMainStore = defineStore('main', {
    state: () => ({ 
        stores: [],
        aisles: [],
        items: [],
        listitems: [],
        shoppinglists: [],
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
    },
    persist: true,
})