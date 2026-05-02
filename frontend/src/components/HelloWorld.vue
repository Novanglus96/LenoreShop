<template>
  <div class="hello">
    <div v-if="!isLoading && stores && stores.length === 0" class="empty-state">
      <p>Welcome to LenoreShop! No stores have been set up yet.</p>
      <p>
        <router-link to="/stores" :style="{ color: '#002255' }">Add your first store</router-link>
        to get started, or load demo data to explore the app.
      </p>
      <v-btn
        color="primary"
        variant="outlined"
        prepend-icon="mdi-database-import"
        :loading="isDemoLoading"
        @click="confirmDemo = true"
      >
        Load Demo Data
      </v-btn>
      <v-dialog v-model="confirmDemo" max-width="400">
        <v-card>
          <v-card-title>Load Demo Data?</v-card-title>
          <v-card-text>
            This will create two sample stores (Grocery Store and Hardware
            Store) with aisles, items, and starter shopping lists.
          </v-card-text>
          <v-card-actions>
            <v-spacer />
            <v-btn variant="text" @click="confirmDemo = false">Cancel</v-btn>
            <v-btn color="primary" variant="text" @click="onLoadDemo">Load</v-btn>
          </v-card-actions>
        </v-card>
      </v-dialog>
    </div>
    <div v-else>
      <p>
        A simple shopping list app! To get started, setup your
        <router-link to="/stores" :style="{ color: '#002255' }">Stores</router-link>
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
      <v-chip v-if="isLoadingLists" variant="outlined" prepend-icon="mdi-loading"
        >Loading...</v-chip
      >
    </div>
  </div>
</template>

<script setup>
import { ref } from "vue";
import { useMainStore } from "@/stores/main";
import { useRouter } from "vue-router";
import { useShoppingLists } from "@/composables/listsComposable";
import { useStores } from "@/composables/storesComposable";
import { useDemo } from "@/composables/demoComposable";

const { shoppinglists, isLoading: isLoadingLists } = useShoppingLists();
const { stores, isLoading } = useStores();
const { loadDemo, isDemoLoading } = useDemo();
const localshoppinglists = ref(shoppinglists);
const confirmDemo = ref(false);

const router = useRouter();

const onLoadDemo = async () => {
  confirmDemo.value = false;
  loadDemo();
};

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

<style scoped>
h3 {
  margin: 40px 0 0;
}
.empty-state {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 16px;
  padding: 32px 0;
}
</style>
