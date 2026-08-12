<template>
  <div class="freezer">
    <v-btn
      density="compact"
      @click="freezerItemFormDialog = true"
      :disabled="!store.freezer_id"
    >
      Add Food
    </v-btn>
    <FreezerItemForm
      v-model="freezerItemFormDialog"
      @add-freezer-item="createFreezerItem"
      @update-dialog="updateDialog"
      :isEdit="false"
      :freezers="freezers"
      :passedFormData="blankFormData"
      :key="-1"
    />
    <v-container fluid class="pa-0">
      <v-row dense v-if="!store.freezer_id">
        <v-col cols="12">
          <v-card color="primary" variant="outlined">
            <v-card-text class="font-italic">
              No freezer selected. Pick one from the Freezers page.
            </v-card-text>
            <v-card-actions>
              <v-btn size="small" variant="outlined" to="/freezers">
                Freezers
              </v-btn>
            </v-card-actions>
          </v-card>
        </v-col>
      </v-row>
      <template v-else>
        <v-row dense v-if="!isLoading">
          <v-col cols="12">
            <h2 class="text-h6 text-primary ps-4">{{ freezerfull?.name }}</h2>
            <h2
              v-if="freezerfull?.location"
              class="text-subtitle-1 text-info ps-4"
            >
              {{ freezerfull?.location }}
            </h2>
            <h2 class="text-subtitle-2 text-grey ps-4">
              {{ freezerfull?.totalitems }} items
              <span v-if="freezerfull?.totalexpired" class="text-error">
                &middot; {{ freezerfull?.totalexpired }} past their throw out
                date
              </span>
            </h2>
          </v-col>
        </v-row>
        <v-row dense v-if="!isLoading">
          <v-col cols="12">
            <FreezerContents
              :freezeritems="freezerfull?.freezeritems"
              :freezers="freezers"
              @edit-freezer-item="updateFreezerItem"
              @delete-freezer-item="removeFood"
            />
          </v-col>
        </v-row>
        <v-row dense v-else>
          <v-col cols="12">
            <v-skeleton-loader type="card" color="primary"></v-skeleton-loader>
          </v-col>
        </v-row>
      </template>
    </v-container>
  </div>
</template>

<script setup>
  import { ref } from "vue";
  import FreezerContents from "@/components/FreezerContents.vue";
  import FreezerItemForm from "@/components/FreezerItemForm.vue";
  import {
    useFreezerFull,
    useFreezers,
  } from "@/composables/freezersComposable";
  import { useMainStore } from "@/stores/main";

  const store = useMainStore();
  const freezerItemFormDialog = ref(false);

  const { freezers } = useFreezers();
  const {
    freezerfull,
    isLoading,
    addFreezerItem,
    editFreezerItem,
    removeFreezerItem,
  } = useFreezerFull(store.freezer_id);

  // Prefilled with today because most food is logged as it goes in. Clearing
  // the field is what records "date added unknown", which is the case when
  // backfilling food that was already in the freezer.
  const today = new Date().toLocaleDateString("en-CA");

  const blankFormData = ref({
    id: 0,
    name: null,
    qty: 1,
    unit: null,
    date_added: today,
    discard_date: null,
    notes: null,
    freezer_id: store.freezer_id,
  });

  const createFreezerItem = async newFood => {
    await addFreezerItem(newFood);
  };

  const updateFreezerItem = async updatedFood => {
    await editFreezerItem(updatedFood);
  };

  const removeFood = async deletedFood => {
    await removeFreezerItem(deletedFood);
  };

  const updateDialog = () => {
    freezerItemFormDialog.value = false;
  };
</script>
