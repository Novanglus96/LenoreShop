<template>
  <v-dialog
    v-model="show"
    persistent
    :width="isMobile ? undefined : 560"
    :fullscreen="isMobile"
  >
    <FormSheet
      :title="props.isEdit ? 'Edit Item' : 'Add Item'"
      eyebrow="Item"
      icon="mdi-cart-plus"
      :fullscreen="isMobile"
      required-note
      @submit="submit"
      @close="closeDialog"
    >
      <!-- Picking the item comes first: choosing one fills in its usual aisle,
           so the field below is normally already correct. -->
      <v-autocomplete
        clearable
        chips
        label="Item*"
        :items="items.items"
        item-title="name"
        item-value="id"
        v-model="item.value.value"
        :return-object="true"
        :error-messages="item.errorMessage.value"
        @update:model-value="itemSelected()"
      ></v-autocomplete>

      <v-autocomplete
        label="Aisle*"
        :items="aisles"
        item-title="name"
        item-value="id"
        v-model="aisle_id.value.value"
        :error-messages="aisle_id.errorMessage.value"
      ></v-autocomplete>

      <v-text-field
        class="ls-form-half"
        label="Quantity*"
        type="number"
        min="1"
        v-model="qty.value.value"
        :error-messages="qty.errorMessage.value"
      ></v-text-field>

      <v-text-field
        class="ls-form-half"
        label="Notes"
        v-model="notes.value.value"
        :error-messages="notes.errorMessage.value"
      ></v-text-field>

      <!-- The escape hatch for something not in the catalog yet. The add
           button is an affordance on the field itself rather than a separate
           icon button in its own grid column. -->
      <v-text-field
        label="Not in the list? Add a new item"
        v-model="newItemField"
        append-inner-icon="mdi-plus-circle"
        hint="Adds it to the catalog and selects it above"
        persistent-hint
        @update:model-value="newItemTextChanged()"
        @click:append-inner="itemChanged"
        @keydown.enter.prevent="itemChanged"
      ></v-text-field>
    </FormSheet>
  </v-dialog>
</template>
<script setup>
  import { ref, defineEmits, defineProps, onMounted, watchEffect } from "vue";
  import { useMainStore } from "@/stores/main";
  import { useItems } from "@/composables/itemsComposable";
  import { useAisles } from "@/composables/aislesComposable";
  import { useDisplay } from "vuetify";
  import { useField, useForm } from "vee-validate";
  import FormSheet from "@/components/FormSheet.vue";

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

  const newItemEntered = ref(false);
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
    passedFormData: Object,
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
    newItemField.value = null;
    id.value.value = props.passedFormData.id;
    qty.value.value = props.passedFormData.qty;
    purchased.value.value = props.passedFormData.purchased;
    notes.value.value = props.passedFormData.notes;
    item.value.value = props.passedFormData.item;
    aisle_id.value.value = props.passedFormData.aisle_id;
    shopping_list_id.value.value = store ? store.list_id : null;
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
    clearFormData();
  };

  const newItemTextChanged = () => {
    if (newItemField.value && newItemField.value != "") {
      newItemEntered.value = true;
    } else {
      newItemEntered.value = false;
    }
  };

  const itemChanged = async () => {
    // The add affordance lives on the field itself now, so it can be triggered
    // with nothing typed; the old separate button was disabled instead.
    if (!newItemEntered.value) return;

    const newItem = {
      name: newItemField.value,
    };
    const newItemID = await createItem(newItem);
    item.value.value = newItemID;
    newItemField.value = "";
    newItemEntered.value = false;
  };
</script>
