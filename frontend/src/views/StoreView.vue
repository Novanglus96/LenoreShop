<template>
  <div class="stores">
    <AddStoreForm @form-submitted="createStore"/>
    <StoreCard :stores="stores" :isLoading="isLoading"/>
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

const createStore = (newStore) => {
  try{
    addStore(newStore)
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
