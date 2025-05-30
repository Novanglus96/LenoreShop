<template>
  <div class="stores">
    <v-btn density="compact" @click="storeFormDialog = true">Add Store</v-btn>
    <StoreForm
      v-model="storeFormDialog"
      @add-store="createStore"
      @edit-store="updateStore"
      :isEdit="false"
      @update-dialog="updateDialog"
      :passedFormData="blankFormData"
    />
    <v-container>
      <v-row dense v-if="!isLoading">
        <v-col cols="12">
          <StoreCard
            v-for="store in stores"
            :key="store.id"
            :store="store"
            @edit-store="updateStore"
            @remove-store="deleteStore"
          />
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
  import { ref } from "vue";
  import StoreCard from "@/components/StoreCard.vue";
  import StoreForm from "@/components/StoreForm.vue";
  import { useStores } from "@/composables/storesComposable";

  const storeFormDialog = ref(false);

  const { stores, isLoading, addStore, editStore, removeStore } = useStores();
  const createStore = async newStore => {
    await addStore(newStore);
  };

  const updateStore = async updatedStore => {
    await editStore(updatedStore);
  };

  const deleteStore = async deletedStore => {
    await removeStore(deletedStore);
  };

  const updateDialog = () => {
    storeFormDialog.value = false;
  };

  const blankFormData = ref({
    id: null,
    name: null,
  });
</script>
