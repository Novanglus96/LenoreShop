<template>
  <div class="aisles">
    <v-btn density="compact" @click="aisleFormDialog = true">Add Aisle</v-btn>
    <AddAisleForm v-model="aisleFormDialog" @add-aisle="createAisle" :isEdit="false" @update-dialog="updateDialog"/>
    <v-container>
      <v-row dense v-if="!isLoading">
        <v-col cols="12">
          <AisleCard v-for="aisle in aisles" :aisle="aisle" :key="aisle.id" @edit-aisle="updateAisle"/>
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
import AisleCard from '@/components/AisleCard.vue'
import AddAisleForm from '@/components/AddAisleForm.vue'
import { useAisles } from '@/composables/aislesComposable'
import { useMainStore } from '@/stores/main'

const aisleFormDialog = ref(false);
const store = useMainStore();
const snackbar = ref(false);
const snackbarText = ref('');
const snackbarColor = ref('');
const snackbarTimeout = ref(1500);
const updateDialog = () => {
  aisleFormDialog.value = false
}

const { aisles, isLoading, addAisle, editAisle } = useAisles(store.store_id)

const createAisle = async (newAisle) => {
  try{
    await addAisle(newAisle)
    showSnackbar('Aisle added', 'success')
  } catch (error) {
    showSnackbar('Aisle not added', 'error')
  }
}

const updateAisle = async (updatedAisle) => {
  try{
    await editAisle(updatedAisle)
    showSnackbar('Aisle updated', 'success')
  } catch {
    showSnackbar('Aisle not updated', 'error')
  }
}

const showSnackbar = (text, color) => {
  snackbarText.value = text;
  snackbarColor.value = color;
  snackbar.value = true;
}

</script>
