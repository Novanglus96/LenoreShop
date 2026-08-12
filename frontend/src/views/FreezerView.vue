<template>
  <div class="freezers">
    <v-btn density="compact" @click="freezerFormDialog = true">
      Add Freezer
    </v-btn>
    <FreezerForm
      v-model="freezerFormDialog"
      @add-freezer="createFreezer"
      :isEdit="false"
      @update-dialog="updateDialog"
      :passedFormData="blankFormData"
    />
    <v-container fluid class="pa-0">
      <v-row dense v-if="!isLoading">
        <v-col cols="12">
          <FreezerCard
            v-for="freezer in freezers"
            :key="freezer.id"
            :freezer="freezer"
            @select="selectedFreezer"
            @select-delete="selectedDeleteFreezer"
          />
          <v-card
            v-if="!freezers || freezers.length == 0"
            color="primary"
            variant="outlined"
          >
            <v-card-text class="font-italic">
              No freezers yet. Add one to start tracking frozen food.
            </v-card-text>
          </v-card>
        </v-col>
      </v-row>
      <v-row dense v-else>
        <v-col cols="12">
          <v-skeleton-loader type="card" color="primary"></v-skeleton-loader>
        </v-col>
      </v-row>
    </v-container>

    <!-- One edit form and one delete dialog for the whole list, kept outside
         the v-for above so a click opens exactly one of each. -->
    <FreezerForm
      v-model="editFreezerFormDialog"
      @edit-freezer="updateFreezer"
      :isEdit="true"
      @update-dialog="updateEditDialog"
      :passedFormData="passedFormData"
      :key="passedFormData.id"
    />
    <v-dialog v-model="deleteDialog" width="auto">
      <v-card>
        <v-card-text>
          Delete freezer {{ passedDeleteData.name }} and everything in it?
        </v-card-text>
        <v-card-actions>
          <v-btn color="primary" @click="deleteDialog = false">No</v-btn>
          <v-btn color="primary" @click="deleteFreezer(passedDeleteData)">
            Yes
          </v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>
  </div>
</template>

<script setup>
  import { ref } from "vue";
  import FreezerCard from "@/components/FreezerCard.vue";
  import FreezerForm from "@/components/FreezerForm.vue";
  import { useFreezers } from "@/composables/freezersComposable";

  const freezerFormDialog = ref(false);
  const editFreezerFormDialog = ref(false);
  const deleteDialog = ref(false);

  const { freezers, isLoading, addFreezer, editFreezer, removeFreezer } =
    useFreezers();

  const createFreezer = async newFreezer => {
    await addFreezer(newFreezer);
  };

  const updateFreezer = async updatedFreezer => {
    await editFreezer(updatedFreezer);
  };

  const deleteFreezer = async deletedFreezer => {
    await removeFreezer(deletedFreezer);
    deleteDialog.value = false;
  };

  const passedFormData = ref({
    id: 0,
    name: "",
    location: "",
  });

  const passedDeleteData = ref({
    id: 0,
    name: null,
  });

  const selectedFreezer = freezer => {
    passedFormData.value = {
      id: freezer.id,
      name: freezer.name,
      location: freezer.location,
    };
    editFreezerFormDialog.value = true;
  };

  const selectedDeleteFreezer = freezer => {
    passedDeleteData.value.id = freezer.id;
    passedDeleteData.value.name = freezer.name;
    deleteDialog.value = true;
  };

  const updateDialog = () => {
    freezerFormDialog.value = false;
  };

  const updateEditDialog = () => {
    editFreezerFormDialog.value = false;
  };

  const blankFormData = ref({
    id: null,
    name: null,
    location: null,
  });
</script>
