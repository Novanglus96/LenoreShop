import { createRouter, createWebHistory } from 'vue-router'
import HomeView from '../views/HomeView.vue'
import FourView from '../views/FourView.vue'
import StoreView from '@/views/StoreView.vue'
import ListsView from '@/views/ListsView.vue'
import ItemView from '@/views/ItemView.vue'
import AisleView from '@/views/AisleView.vue'
import ListView from '@/views/ListView.vue'

const routes = [
  {
    path: '/',
    name: 'home',
    component: HomeView
  },
  {
    path: '/stores',
    name: 'stores',
    component: StoreView
  },
  {
    path: '/lists',
    name: 'lists',
    component: ListsView
  },
  {
    path: '/lists/:store',
    name: 'listfilter',
    component: ListsView
  },
  {
    path: '/list/:list',
    name: 'listview',
    component: ListView
  },
  {
    path: '/items',
    name: 'items',
    component: ItemView
  },
  {
    path: '/aisles',
    name: 'aisles',
    component: AisleView
  },
  {
    path: '/aisles/:store',
    name: 'aislefilter',
    component: AisleView
  },
  { 
    path: '/:catchAll(.*)', 
    component: FourView,
    name: 'NotFound'
  }
]

const router = createRouter({
  history: createWebHistory(process.env.BASE_URL),
  routes
})

export default router
