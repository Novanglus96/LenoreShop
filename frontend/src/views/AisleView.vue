<template>
  <div class="aisles">
    <v-btn density="compact" @click="aisleFormDialog = true">Add Aisle</v-btn>
    <AisleForm v-model="aisleFormDialog" @add-aisle="createAisle" :isEdit="false" @update-dialog="updateDialog"/>
    <v-container>
      <v-row dense v-if="!isLoading">
        <v-col cols="12">
          <AisleCard v-for="aisle in aisles" :aisle="aisle" :key="aisle.id" @edit-aisle="updateAisle" @remove-aisle="deleteAisle"/>
        </v-col>
      </v-row>
      <v-row dense v-else>
        <v-col cols="12">
          <v-skeleton-loader type="card" color="primary"></v-skeleton-loader>
        </v-col>
      </v-row>
    </v-container>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import AisleCard from '@/components/AisleCard.vue'
import AisleForm from '@/components/AisleForm.vue'
import { useAisles } from '@/composables/aislesComposable'
import { useMainStore } from '@/stores/main'

const store = useMainStore();
const aisleFormDialog = ref(false);
const updateDialog = () => {
  aisleFormDialog.value = false
}

const { aisles, isLoading, addAisle, editAisle, removeAisle } = useAisles(store.store_id)
const createAisle = async (newAisle) => {
  await addAisle(newAisle)
}

const updateAisle = async (updatedAisle) => {
  await editAisle(updatedAisle)
}

const deleteAisle = async (deletedAisle) => {
  await removeAisle(deletedAisle)
}

</script>
