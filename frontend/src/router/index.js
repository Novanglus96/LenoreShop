import { createRouter, createWebHistory } from "vue-router";
import HomeView from "../views/HomeView.vue";
import FourView from "../views/FourView.vue";
import StoreView from "@/views/StoreView.vue";
import ListView from "@/views/ListView.vue";
import ItemView from "@/views/ItemView.vue";
import AisleView from "@/views/AisleView.vue";
import ListsStoreView from "@/views/ListsStoreView.vue";
import ListsView from "@/views/ListsView.vue";

const routes = [
  {
    path: "/",
    name: "home",
    component: HomeView,
  },
  {
    path: "/stores",
    name: "stores",
    component: StoreView,
  },
  {
    path: "/alllists",
    name: "alllists",
    component: ListsStoreView,
  },
  {
    path: "/lists",
    name: "lists",
    component: ListsView,
  },
  {
    path: "/list",
    name: "listview",
    component: ListView,
  },
  {
    path: "/items",
    name: "items",
    component: ItemView,
  },
  {
    path: "/aisles",
    name: "aisles",
    component: AisleView,
  },
  {
    path: "/aisles/:store",
    name: "aislefilter",
    component: AisleView,
  },
  {
    path: "/:catchAll(.*)",
    component: FourView,
    name: "NotFound",
  },
];

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes,
});

// Add a global beforeEach guard
router.beforeEach((to, from, next) => {
  const isPageReload = sessionStorage.getItem("isPageReload");
  sessionStorage.removeItem("isPageReload");

  if (isPageReload && to.fullPath !== "/") {
    next("/");
  } else {
    next();
  }
});

// Set a flag to detect page reload
window.addEventListener("beforeunload", () => {
  sessionStorage.setItem("isPageReload", "true");
});

export default router;
