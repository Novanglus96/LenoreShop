<template>
  <div class="stores">
    <v-btn density="compact" @click="storeFormDialog = true">Add Store</v-btn>
    <StoreForm v-model="storeFormDialog" @add-store="createStore" @edit-store="updateStore" :isEdit="false" @update-dialog="updateDialog"/>
    <v-container>
      <v-row dense v-if="!isLoading">
        <v-col cols="12">
          <StoreCard v-for="store in stores" :key="store.id" :store="store" @edit-store="updateStore" @remove-store="deleteStore"/>
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
import StoreForm from '@/components/StoreForm.vue'
import { useStores } from '@/composables/storesComposable'

const storeFormDialog = ref(false);
const snackbar = ref(false);
const snackbarText = ref('');
const snackbarColor = ref('');
const snackbarTimeout = ref(1500);

const { stores, isLoading, addStore, editStore, removeStore } = useStores()

const createStore = async (newStore) => {
  try{
    await addStore(newStore)
    showSnackbar('Store added', 'success')
  } catch (error) {
    showSnackbar('Store not added', 'error')
  }
}

const updateStore = async (updatedStore) => {
  try{
    await editStore(updatedStore)
    showSnackbar('Store updated','success')
  } catch (error) {
    showSnackbar('Store not updated','error')
  }
}

const deleteStore = async (deletedStore) => {
  try{
    await removeStore(deletedStore)
    showSnackbar('Store deleted','success')
  } catch (error) {
    showSnackbar('Store not deleted','error')
  }
}

const showSnackbar = (text, color) => {
  snackbarText.value = text;
  snackbarColor.value = color;
  snackbar.value = true;
}

const updateDialog = () => {
  storeFormDialog.value = false
}

</script>
