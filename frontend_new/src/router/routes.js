
const routes = [
  {
    path: '/',
    component: () => import('layouts/MainLayout.vue'),
    children: [
      { path: '', component: () => import('pages/IndexPage.vue') },
      { path: 'stores', component: () => import('pages/StorePage.vue') },
      { path: 'aisles', component: () => import('pages/AislePage.vue') },
      { path: 'lists', component: () => import('pages/ListPage.vue') },
      { path: 'items', component: () => import('pages/ItemPage.vue') }
    ]
  },

  // Always leave this as last one,
  // but you can also remove it
  {
    path: '/:catchAll(.*)*',
    component: () => import('pages/ErrorNotFound.vue')
  }
]

export default routes
