<template>
  <v-dialog
    v-model="show"
    persistent
    :width="isMobile ? undefined : 680"
    :fullscreen="isMobile"
  >
    <FormSheet
      :title="props.isEdit ? 'Edit Food' : 'Add Food'"
      eyebrow="Food"
      icon="mdi-food-drumstick-outline"
      :fullscreen="isMobile"
      required-note
      @submit="submit"
      @close="closeDialog"
    >
      <v-text-field
        label="Food*"
        placeholder="Chicken breasts"
        v-model="name.value.value"
        :error-messages="name.errorMessage.value"
      ></v-text-field>
      <v-text-field
        class="ls-form-half"
        label="Amount*"
        v-model="qty.value.value"
        type="number"
        min="1"
        :error-messages="qty.errorMessage.value"
      ></v-text-field>
      <v-text-field
        class="ls-form-half"
        label="Unit"
        placeholder="lbs"
        v-model="unit.value.value"
        :error-messages="unit.errorMessage.value"
      ></v-text-field>
      <v-select
        label="Freezer*"
        v-model="freezer_id.value.value"
        :items="freezers"
        item-title="name"
        item-value="id"
        :error-messages="freezer_id.errorMessage.value"
      ></v-select>
      <v-text-field
        class="ls-form-half"
        label="Date Added"
        type="date"
        v-model="date_added.value.value"
        :error-messages="date_added.errorMessage.value"
        hint="Leave blank if unknown"
        persistent-hint
      ></v-text-field>
      <v-text-field
        class="ls-form-half"
        label="Throw Out By"
        type="date"
        v-model="discard_date.value.value"
        :error-messages="discard_date.errorMessage.value"
        hint="Leave blank if it does not expire"
        persistent-hint
      ></v-text-field>
      <v-textarea
        label="Notes"
        rows="2"
        v-model="notes.value.value"
        :error-messages="notes.errorMessage.value"
      ></v-textarea>
    </FormSheet>
  </v-dialog>
</template>
<script setup>
  import { ref, defineEmits, defineProps, onMounted, watchEffect } from "vue";
  import { useDisplay } from "vuetify";
  import { useField, useForm } from "vee-validate";
  import FormSheet from "@/components/FormSheet.vue";

  const { handleSubmit } = useForm({
    validationSchema: {
      name(value) {
        if (value) return true;

        return "Must provide a food name.";
      },
      qty(value) {
        if (value > 0) return true;

        return "Amount must be greater than 0.";
      },
      freezer_id(value) {
        if (value) return true;

        return "Must choose a freezer.";
      },
      discard_date(value) {
        // An empty discard date is valid - not everything expires.
        if (!value) return true;
        if (!date_added.value.value) return true;
        if (value >= date_added.value.value) return true;

        return "Throw out date cannot be before the date added.";
      },
    },
  });

  const name = useField("name");
  const qty = useField("qty");
  const unit = useField("unit");
  const date_added = useField("date_added");
  const discard_date = useField("discard_date");
  const notes = useField("notes");
  const freezer_id = useField("freezer_id");
  const id = useField("id");

  const { smAndDown } = useDisplay();
  const isMobile = smAndDown;

  const props = defineProps({
    freezerItemFormDialog: {
      type: Boolean,
      default: false,
    },
    isEdit: {
      type: Boolean,
      default: false,
    },
    freezers: {
      type: Array,
      default: () => [],
    },
    passedFormData: Object,
  });

  const show = ref(props.freezerItemFormDialog);
  const emit = defineEmits([
    "addFreezerItem",
    "editFreezerItem",
    "updateDialog",
  ]);

  const watchPassedFormData = () => {
    watchEffect(() => {
      if (props.passedFormData) {
        id.value.value = props.passedFormData.id;
        name.value.value = props.passedFormData.name;
        qty.value.value = props.passedFormData.qty;
        unit.value.value = props.passedFormData.unit;
        date_added.value.value = props.passedFormData.date_added;
        discard_date.value.value = props.passedFormData.discard_date;
        notes.value.value = props.passedFormData.notes;
        freezer_id.value.value = props.passedFormData.freezer_id;
      }
    });
  };

  onMounted(() => {
    watchPassedFormData();
  });

  const submit = handleSubmit(values => {
    const payload = {
      ...values,
      qty: Number(values.qty),
      // The API treats null as "not set"; empty strings from a cleared date
      // input would fail date parsing.
      unit: values.unit || null,
      date_added: values.date_added || null,
      discard_date: values.discard_date || null,
      notes: values.notes || null,
    };
    if (props.isEdit == false) {
      emit("addFreezerItem", payload);
    } else {
      emit("editFreezerItem", payload);
    }
    closeDialog();
  });

  const closeDialog = () => {
    emit("updateDialog", false);
    clearFormData();
  };

  const clearFormData = () => {
    id.value.value = null;
    name.value.value = null;
    qty.value.value = 1;
    unit.value.value = null;
    date_added.value.value = null;
    discard_date.value.value = null;
    notes.value.value = null;
    freezer_id.value.value = null;
  };
</script>
