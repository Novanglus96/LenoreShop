<template>
  <v-card color="primary" variant="outlined">
    <v-card-title class="text-h6">
      {{ store.name }}
    </v-card-title>

    <v-card-actions>
      <v-btn size="x-small" variant="outlined" @click="showAisle(store.id)">
        aisles
      </v-btn>
      <v-btn size="x-small" variant="outlined" @click="selectedStore(store)">
        edit
      </v-btn>
      <StoreForm
        v-model="storeFormDialog"
        @edit-store="updateStore"
        :isEdit="true"
        @update-dialog="updateDialog"
        :passedFormData="passedFormData"
      />
      <v-btn size="x-small" variant="outlined" @click="deleteDialog = true">
        delete
      </v-btn>
      <v-dialog v-model="deleteDialog" width="auto">
        <v-card>
          <v-card-text>Delete store {{ store.name }}?</v-card-text>
          <v-card-actions>
            <v-btn color="primary" @click="deleteStore(store)">Yes</v-btn>
            <v-btn color="primary" @click="deleteDialog = false">No</v-btn>
          </v-card-actions>
        </v-card>
      </v-dialog>
    </v-card-actions>
  </v-card>
</template>

<script setup>
  import { defineProps, defineEmits, ref } from "vue";
  import { useMainStore } from "@/stores/main";
  import { useRouter } from "vue-router";
  import StoreForm from "@/components/StoreForm.vue";

  const emit = defineEmits(["editStore", "removeStore"]);
  const storeFormDialog = ref(false);
  const deleteDialog = ref(false);
  const passedFormData = ref({
    id: 0,
    name: "",
  });

  const selectedStore = store => {
    passedFormData.value.id = store.id;
    passedFormData.value.name = store.name;

    storeFormDialog.value = true;
  };

  const updateStore = async store => {
    emit("editStore", store);
  };

  const deleteStore = async store => {
    emit("removeStore", store);

    updateDialog();
  };

  const updateDialog = () => {
    storeFormDialog.value = false;
  };

  defineProps({
    store: Object,
  });

  const router = useRouter();

  const showAisle = async store_id => {
    const store = useMainStore();
    store.store_id = store_id;
    router.push("/aisles");
  };
</script>
