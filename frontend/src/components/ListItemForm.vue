<template>
  <v-dialog v-model="show" persistent width="1024">
    <v-card>
      <v-card-title>
        <span class="text-h5" v-if="props.isEdit == false">Add Item</span>
        <span class="text-h5" v-else>Edit Item</span>
      </v-card-title>
      <v-card-text>
        <v-container>
          <v-row>
            <v-col>
              <v-text-field
                label="qty"
                v-model="formData.qty"
                variant="outlined"
                type="number"
              ></v-text-field>
            </v-col>
          </v-row>
          <v-row>
            <v-col>
              <v-text-field
                label="new item"
                variant="outlined"
                v-model="newItemField"
              ></v-text-field>
            </v-col>
            <v-col cols="1">
              <v-btn
                icon="mdi-plus"
                variant="plain"
                @click="itemChanged"
              ></v-btn>
            </v-col>
          </v-row>
          <v-row>
            <v-col>
              <v-autocomplete
                clearable
                label="Item*"
                required
                :items="items"
                item-title="name"
                item-value="id"
                v-model="formData.item_id"
                :return-object="false"
                chips
              ></v-autocomplete>
            </v-col>
          </v-row>
          <v-row>
            <v-col>
              <v-select
                label="Aisle*"
                required
                :items="aisles"
                item-title="name"
                item-value="id"
                v-model="formData.aisle_id"
              ></v-select>
            </v-col>
          </v-row>
          <v-row>
            <v-col>
              <v-text-field
                label="notes"
                v-model="formData.notes"
                variant="outlined"
                type="text"
              ></v-text-field>
            </v-col>
          </v-row>
        </v-container>
        <small>*indicates required field</small>
      </v-card-text>
      <v-card-actions>
        <v-spacer></v-spacer>
        <v-btn color="blue-darken-1" variant="text" @click="closeDialog()">
          Close
        </v-btn>
        <v-btn color="blue-darken-1" variant="text" @click="submitForm">
          Save
        </v-btn>
      </v-card-actions>
    </v-card>
  </v-dialog>
</template>
<script setup>
import { ref, defineEmits, defineProps, onMounted, watchEffect } from "vue";
import { useMainStore } from "@/stores/main";
import { useItems } from "@/composables/itemsComposable";
import { useAisles } from "@/composables/aislesComposable";

const newItemField = ref("");
const store = useMainStore();
const { aisles } = useAisles(store.store_id);
const { addItem, items } = useItems();
const props = defineProps({
  listItemFormDialog: {
    type: Boolean,
    default: false,
  },
  isEdit: {
    type: Boolean,
    default: false,
  },
  passedFormData: Array,
});

const createItem = async newItem => {
  try {
    const data = await addItem(newItem);
    return data;
  } catch (error) {
    console.log("Item not added", error);
  }
};

const show = ref(props.listItemFormDialog);
const emit = defineEmits(["addListItem", "editListItem", "updateDialog"]);
const formData = ref({
  id: null,
  qty: 1,
  purchased: false,
  notes: "",
  item_id: null,
  aisle_id: null,
  shopping_list_id: store.list_id,
});

const watchPassedFormData = () => {
  watchEffect(() => {
    if (props.passedFormData) {
      formData.value.id = props.passedFormData.id;
      formData.value.qty = props.passedFormData.qty;
      formData.value.purchased = props.passedFormData.purchased;
      formData.value.notes = props.passedFormData.notes;
      formData.value.item_id = props.passedFormData.item_id;
      formData.value.aisle_id = props.passedFormData.aisle_id;
      formData.value.shopping_list_id = props.passedFormData.shopping_list_id;
    }
  });
};

onMounted(() => {
  watchPassedFormData();
  clearFormData();
});

const clearFormData = () => {
  formData.value.id = null;
  formData.value.qty = 1;
  formData.value.purchased = false;
  formData.value.notes = "";
  formData.value.item_id = null;
  formData.value.aisle_id = null;
  formData.value.shopping_list_id = store.list_id;
};
const submitForm = async () => {
  if (props.isEdit == false) {
    emit("addListItem", formData.value);
  } else {
    emit("editListItem", formData.value);
  }

  closeDialog();
};

const closeDialog = () => {
  emit("updateDialog", false);
};

const itemChanged = async () => {
  const newItem = {
    name: newItemField.value,
  };
  const newItemID = await createItem(newItem);
  formData.value.item_id = newItemID.id;
  newItemField.value = "";
};
</script>
