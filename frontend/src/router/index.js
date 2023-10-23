import { createRouter, createWebHistory } from 'vue-router'
import HomeView from '../views/HomeView.vue'
import FourView from '../views/FourView.vue'
import StoreView from '@/views/StoreView.vue'
import ListView from '@/views/ListView.vue'
import ItemView from '@/views/ItemView.vue'

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
    component: ListView
  },
  {
    path: '/items',
    name: 'items',
    component: ItemView
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
