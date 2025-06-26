<template>
  <v-app-bar color="secondary" density="compact" app>
    <v-menu>
      <template v-slot:activator="{ props }">
        <v-btn icon="mdi-menu" v-bind="props"></v-btn>
      </template>
      <v-list>
        <v-list-item v-for="(menu, i) in menus" :key="i" :to="menu.url">
          <template v-slot:prepend>
            <v-icon :icon="menu.icon"></v-icon>
          </template>
          <v-list-item-title>{{ menu.title }}</v-list-item-title>
        </v-list-item>
      </v-list>
    </v-menu>
    <v-img :width="201" aspect-ratio="1/1" src="logov2.png" inline></v-img>
    <span class="text-subtitle-2 font-italic text-grey-darken-1">v1.6.19</span>
    <v-spacer></v-spacer>
    <v-menu v-model="menu" :close-on-content-click="false" location="end">
      <template v-slot:activator="{ props }">
        <v-btn icon="mdi-dots-vertical" v-bind="props"></v-btn>
      </template>

      <v-list>
        <v-list-item as="a" href="/admin" prepend-icon="mdi-security">
          <v-list-item-title>Admin</v-list-item-title>
        </v-list-item>
        <!--<v-list-item to="/logout" prepend-icon="mdi-logout">
          <v-list-item-title>Logout</v-list-item-title>
        </v-list-item>-->
      </v-list>
    </v-menu>
  </v-app-bar>
</template>

<script setup>
  import { ref } from "vue";

  const menus = [
    { title: "Home", url: "/", icon: "mdi-home-outline" },
    { title: "Stores", url: "/stores", icon: "mdi-storefront-outline" },
    { title: "Shopping Lists", url: "/lists", icon: "mdi-cart-outline" },
    { title: "Items", url: "/items", icon: "mdi-food-apple-outline" },
  ];

  const menu = ref(false);
</script>

<style scoped></style>
