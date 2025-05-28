<template>
  <v-dialog
    v-model="show"
    persistent
    :width="isMobile ? undefined : '1024'"
    :fullscreen="isMobile"
  >
    <v-card>
      <form @submit.prevent="submit">
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
                  v-model="qty.value.value"
                  variant="outlined"
                  type="number"
                  :error-messages="qty.errorMessage.value"
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
                  :items="items.items"
                  item-title="name"
                  item-value="id"
                  v-model="item.value.value"
                  :return-object="true"
                  :error-messages="item.errorMessage.value"
                  chips
                  @update:model-value="itemSelected()"
                ></v-autocomplete>
              </v-col>
            </v-row>
            <v-row>
              <v-col>
                <v-autocomplete
                  label="Aisle*"
                  :items="aisles"
                  item-title="name"
                  item-value="id"
                  v-model="aisle_id.value.value"
                  :error-messages="aisle_id.errorMessage.value"
                ></v-autocomplete>
              </v-col>
            </v-row>
            <v-row>
              <v-col>
                <v-text-field
                  label="notes"
                  v-model="notes.value.value"
                  variant="outlined"
                  type="text"
                  :error-messages="notes.errorMessage.value"
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
          <v-btn color="blue-darken-1" variant="text" type="submit">Save</v-btn>
        </v-card-actions>
      </form>
    </v-card>
  </v-dialog>
</template>
<script setup>
  import { ref, defineEmits, defineProps, onMounted, watchEffect } from "vue";
  import { useMainStore } from "@/stores/main";
  import { useItems } from "@/composables/itemsComposable";
  import { useAisles } from "@/composables/aislesComposable";
  import { useDisplay } from "vuetify";
  import { useField, useForm } from "vee-validate";

  const { handleSubmit } = useForm({
    validationSchema: {
      item(value) {
        if (value !== null) {
          return true;
        }

        return "Must choose an item.";
      },
      aisle_id(value) {
        if (value) return true;

        return "Must provide an aisle.";
      },
      qty(value) {
        if (value) return true;

        return "Must provide a quantity.";
      },
    },
  });

  const id = useField("id");
  const qty = useField("qty");
  const purchased = useField("purchased");
  const notes = useField("notes");
  const item = useField("item");
  const aisle_id = useField("aisle_id");
  const shopping_list_id = useField("shopping_list_id");

  const { smAndDown } = useDisplay();
  const isMobile = smAndDown;

  const newItemField = ref("");
  const store = useMainStore();
  const { aisles } = useAisles(store.store_id);
  const { addItem, items } = useItems(true);
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

  const watchPassedFormData = () => {
    watchEffect(() => {
      if (props.passedFormData) {
        id.value.value = props.passedFormData.id;
        qty.value.value = props.passedFormData.qty;
        purchased.value.value = props.passedFormData.purchased;
        notes.value.value = props.passedFormData.notes;
        item.value.value = props.passedFormData.item;
        aisle_id.value.value = props.passedFormData.aisle_id;
        shopping_list_id.value.value = store ? store.list_id : null;
      }
    });
  };

  onMounted(() => {
    watchPassedFormData();
    clearFormData();
  });

  const clearFormData = () => {
    id.value.value = null;
    qty.value.value = 1;
    purchased.value.value = false;
    notes.value.value = "";
    item.value.value = null;
    aisle_id.value.value = null;
    shopping_list_id.value.value = store.list_id;
  };

  const submit = handleSubmit(values => {
    if (props.isEdit == false) {
      emit("addListItem", values);
    } else {
      emit("editListItem", values);
    }

    closeDialog();
    clearFormData();
  });

  const itemSelected = () => {
    if (item.value.value && item.value.value.aisle) {
      if (item.value.value.aisle.store.id === store.store_id) {
        aisle_id.value.value = item.value.value.aisle.id;
      }
    }
  };

  const closeDialog = () => {
    emit("updateDialog", false);
  };

  const itemChanged = async () => {
    const newItem = {
      name: newItemField.value,
    };
    const newItemID = await createItem(newItem);
    item.value.value = newItemID;
    newItemField.value = "";
  };
</script>
