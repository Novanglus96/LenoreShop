<template>
  <div class="hello">
    <p>
      A simple shopping list app! To get started, setup your
      <router-link to="/stores" :style="{ color: '#002255' }"
        >Stores</router-link
      >
      here.
    </p>
    <h3>Shopping Lists</h3>
    <v-chip
      v-for="list in localshoppinglists"
      :key="list.id"
      @click="fetchShoppingListFull(list.id, list.store_id)"
      variant="outlined"
      prepend-icon="mdi-cart"
      >{{ list.store.name }} &bull; {{ list.name }}</v-chip
    >
    <v-chip v-if="isLoading" variant="outlined" prepend-icon="mdi-loading"
      >Loading...</v-chip
    >
  </div>
</template>

<script setup>
import { ref } from "vue";
import { useMainStore } from "@/stores/main";
import { useRouter } from "vue-router";
import { useShoppingLists } from "@/composables/listsComposable";

const { shoppinglists, isLoading } = useShoppingLists();
const localshoppinglists = ref(shoppinglists);

const router = useRouter();

const fetchShoppingListFull = async (list_id, store_id) => {
  try {
    const store = useMainStore();
    store.list_id = list_id;
    store.store_id = store_id;
    router.push("/list");
  } catch (error) {
    console.log(error);
  }
};
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
h3 {
  margin: 40px 0 0;
}
ul {
  list-style-type: none;
  padding: 0;
}
li {
  display: inline-block;
  margin: 0 10px;
}
a {
  color: #42b983;
}
</style>
