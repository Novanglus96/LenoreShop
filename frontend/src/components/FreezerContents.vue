<template>
  <v-list density="compact" elevation="1" bg-color="primary">
    <v-list-item
      v-for="item in freezeritems"
      :key="item.id"
      elevation="2"
      variant="flat"
      color="white"
    >
      <v-list-item-title>
        <span class="text-black">
          {{ item.qty }}
          <span v-if="item.unit">{{ item.unit }}</span>
          {{ item.name }}
        </span>
      </v-list-item-title>
      <v-list-item-subtitle>
        <span :class="discardClass(item)">{{ discardLabel(item) }}</span>
        <span class="text-grey">&middot; {{ addedLabel(item) }}</span>
        <span v-if="item.notes" class="text-black">
          &middot; {{ item.notes }}
        </span>
      </v-list-item-subtitle>
      <template v-slot:prepend>
        <v-icon
          :icon="discardIcon(item)"
          :color="discardColor(item)"
          size="large"
        ></v-icon>
      </template>
      <template v-slot:append>
        <v-btn
          icon="mdi-pencil"
          variant="plain"
          :ripple="false"
          @click="selectedItem(item)"
        ></v-btn>
        <v-btn
          icon="mdi-delete"
          variant="plain"
          :ripple="false"
          @click="selectedDeleteItem(item)"
        ></v-btn>
      </template>
    </v-list-item>
    <v-list-item
      v-if="!freezeritems || freezeritems.length == 0"
      elevation="2"
      variant="flat"
      color="white"
    >
      <v-list-item-title>
        <span class="text-black font-italic">Nothing in this freezer</span>
      </v-list-item-title>
    </v-list-item>
  </v-list>
  <FreezerItemForm
    v-model="freezerItemFormDialog"
    @edit-freezer-item="editFreezerItem"
    @update-dialog="updateDialog"
    :isEdit="true"
    :freezers="freezers"
    :passedFormData="passedFormData"
    :key="passedFormData.id"
  />
  <v-dialog v-model="deleteDialog" width="auto">
    <v-card>
      <v-card-text>
        Remove "{{ passedDeleteData.name }}" from the freezer?
      </v-card-text>
      <v-card-actions>
        <v-btn color="primary" @click="deleteDialog = false">No</v-btn>
        <v-btn color="primary" @click="deleteItem(passedDeleteData)">Yes</v-btn>
      </v-card-actions>
    </v-card>
  </v-dialog>
</template>

<script setup>
  import { defineProps, defineEmits, ref } from "vue";
  import FreezerItemForm from "@/components/FreezerItemForm.vue";

  const emit = defineEmits(["editFreezerItem", "deleteFreezerItem"]);

  // A single form and a single delete dialog, both rendered outside the v-for
  // above. One instance per row would share these refs and open together.
  const passedFormData = ref({
    id: 0,
    name: "",
    qty: 1,
    unit: null,
    date_added: null,
    discard_date: null,
    notes: "",
    freezer_id: 0,
  });
  const passedDeleteData = ref({
    id: 0,
    name: null,
  });
  const freezerItemFormDialog = ref(false);
  const deleteDialog = ref(false);

  const updateDialog = () => {
    freezerItemFormDialog.value = false;
  };

  const selectedItem = item => {
    passedFormData.value = {
      id: item.id,
      name: item.name,
      qty: item.qty,
      unit: item.unit,
      date_added: item.date_added,
      discard_date: item.discard_date,
      notes: item.notes,
      freezer_id: item.freezer_id,
    };

    freezerItemFormDialog.value = true;
  };

  const selectedDeleteItem = item => {
    passedDeleteData.value.id = item.id;
    passedDeleteData.value.name = item.name;
    deleteDialog.value = true;
  };

  const editFreezerItem = async item => {
    emit("editFreezerItem", item);
  };

  const deleteItem = async item => {
    emit("deleteFreezerItem", { id: item.id });
    deleteDialog.value = false;
  };

  const addedLabel = item => {
    if (!item.date_added) return "date added unknown";
    return `frozen ${item.date_added}`;
  };

  const discardLabel = item => {
    if (item.days_until_discard === null) return "No throw out date";
    const days = item.days_until_discard;
    if (days < 0) return `Throw out - ${Math.abs(days)} days overdue`;
    if (days === 0) return "Throw out today";
    if (days === 1) return "Throw out tomorrow";
    return `Throw out in ${days} days`;
  };

  const discardColor = item => {
    if (item.days_until_discard === null) return "grey";
    if (item.days_until_discard < 0) return "error";
    if (item.days_until_discard <= 14) return "warning";
    return "success";
  };

  const discardClass = item => {
    if (item.days_until_discard === null) return "text-grey";
    if (item.days_until_discard < 0) return "text-error font-weight-bold";
    if (item.days_until_discard <= 14) return "text-warning";
    return "text-success";
  };

  const discardIcon = item => {
    if (item.days_until_discard === null) return "mdi-snowflake";
    if (item.days_until_discard < 0) return "mdi-alert-circle";
    if (item.days_until_discard <= 14) return "mdi-clock-alert-outline";
    return "mdi-snowflake";
  };

  defineProps({
    freezeritems: Array,
    freezers: {
      type: Array,
      default: () => [],
    },
  });
</script>
