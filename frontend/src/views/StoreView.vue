<template>
  <div class="stores">
    <AddStoreForm @form-submitted="createStore"/>
    <v-container>
      <v-row dense v-if="!isLoading">
        <v-col cols="12">
          <StoreCard v-for="store in stores" :key="store.id" :store="store"/>
        </v-col>
      </v-row>
      <v-row dense v-else>
        <v-col cols="12">
          <v-skeleton-loader type="card" color="primary"></v-skeleton-loader>
        </v-col>
      </v-row>
    </v-container>
    <v-snackbar
      v-model="snackbar"
      :color="snackbarColor"
      :timeout="snackbarTimeout"
      content-class="centered-text"
    >
      {{ snackbarText }}
    </v-snackbar>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import StoreCard from '@/components/StoreCard.vue'
import AddStoreForm from '@/components/AddStoreForm.vue'
import { useStores } from '@/composables/storesComposable'

const snackbar = ref(false);
const snackbarText = ref('');
const snackbarColor = ref('');
const snackbarTimeout = ref(1500);

const { stores, isLoading, addStore } = useStores()

const createStore = async (newStore) => {
  try{
    await addStore(newStore)
    showSnackbar('Store added', 'success')
  } catch (error) {
    showSnackbar('Store not added', 'error')
  }
}

const showSnackbar = (text, color) => {
  snackbarText.value = text;
  snackbarColor.value = color;
  snackbar.value = true;
}

</script>
