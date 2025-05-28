<template>
  <v-card color="primary" variant="outlined">
    <v-card-text>
      {{ item.name }}
      <v-btn size="x-small" variant="outlined" @click="selectedItem(item)">
        edit
      </v-btn>
      <ItemForm
        v-model="itemFormDialog"
        @edit-item="updateItem"
        :isEdit="true"
        @update-dialog="updateDialog"
        :passedFormData="passedFormData"
      />
      <v-btn size="x-small" variant="outlined" @click="deleteDialog = true">
        delete
      </v-btn>
      <v-dialog v-model="deleteDialog" width="auto">
        <v-card>
          <v-card-text>Delete item {{ item.name }}?</v-card-text>
          <v-card-actions>
            <v-btn color="primary" @click="deleteItem(item)">Yes</v-btn>
            <v-btn color="primary" @click="deleteDialog = false">No</v-btn>
          </v-card-actions>
        </v-card>
      </v-dialog>
    </v-card-text>
  </v-card>
</template>

<script setup>
  import { defineProps, defineEmits, ref } from "vue";
  import ItemForm from "@/components/ItemForm.vue";

  const emit = defineEmits(["editItem", "removeItem"]);
  const itemFormDialog = ref(false);
  const deleteDialog = ref(false);
  const passedFormData = ref({
    id: 0,
    name: "",
    matches: "",
  });

  const selectedItem = item => {
    passedFormData.value.id = item.id;
    passedFormData.value.name = item.name;
    passedFormData.value.matches = item.matches;

    itemFormDialog.value = true;
  };

  const updateItem = async item => {
    emit("editItem", item);
  };

  const deleteItem = async item => {
    emit("removeItem", item);

    updateDialog();
  };

  const updateDialog = () => {
    itemFormDialog.value = false;
  };

  defineProps({
    item: Object,
  });
</script>
