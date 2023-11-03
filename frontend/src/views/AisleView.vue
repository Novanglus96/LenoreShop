<template>
  <div class="aisles">
    <AddAisleForm @form-submitted="createAisle"/>
    <AisleCard :aisles="aisles" :isLoading="isLoading"/>
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
import AisleCard from '@/components/AisleCard.vue'
import AddAisleForm from '@/components/AddAisleForm.vue'
import { useAisles } from '@/composables/aislesComposable'
import { useMainStore } from '@/stores/main';

const store = useMainStore();
const snackbar = ref(false);
const snackbarText = ref('');
const snackbarColor = ref('');
const snackbarTimeout = ref(1500);

const { aisles, isLoading, addAisle } = useAisles(store.store_id)

const createAisle = (newAisle) => {
  try{
    addAisle(newAisle)
    showSnackbar('Aisle added', 'success')
  } catch (error) {
    showSnackbar('Aisle not added', 'error')
  }
}

const showSnackbar = (text, color) => {
  snackbarText.value = text;
  snackbarColor.value = color;
  snackbar.value = true;
}

</script>
