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
          <span class="text-h5" v-if="props.isEdit == false">Add Food</span>
          <span class="text-h5" v-else>Edit Food</span>
        </v-card-title>
        <v-card-text>
          <v-container>
            <v-row>
              <v-col cols="12" sm="6" md="4">
                <v-text-field
                  label="Food*"
                  placeholder="Chicken breasts"
                  v-model="name.value.value"
                  :error-messages="name.errorMessage.value"
                ></v-text-field>
              </v-col>
              <v-col cols="6" sm="3" md="2">
                <v-text-field
                  label="Amount*"
                  v-model="qty.value.value"
                  type="number"
                  min="1"
                  :error-messages="qty.errorMessage.value"
                ></v-text-field>
              </v-col>
              <v-col cols="6" sm="3" md="2">
                <v-text-field
                  label="Unit"
                  placeholder="lbs"
                  v-model="unit.value.value"
                  :error-messages="unit.errorMessage.value"
                ></v-text-field>
              </v-col>
              <v-col cols="12" sm="6" md="4">
                <v-select
                  label="Freezer*"
                  v-model="freezer_id.value.value"
                  :items="freezers"
                  item-title="name"
                  item-value="id"
                  :error-messages="freezer_id.errorMessage.value"
                ></v-select>
              </v-col>
              <v-col cols="12" sm="6" md="4">
                <v-text-field
                  label="Date Added"
                  type="date"
                  v-model="date_added.value.value"
                  :error-messages="date_added.errorMessage.value"
                  hint="Leave blank if unknown"
                  persistent-hint
                ></v-text-field>
              </v-col>
              <v-col cols="12" sm="6" md="4">
                <v-text-field
                  label="Throw Out By"
                  type="date"
                  v-model="discard_date.value.value"
                  :error-messages="discard_date.errorMessage.value"
                  hint="Leave blank if it does not expire"
                  persistent-hint
                ></v-text-field>
              </v-col>
              <v-col cols="12">
                <v-textarea
                  label="Notes"
                  rows="2"
                  v-model="notes.value.value"
                  :error-messages="notes.errorMessage.value"
                ></v-textarea>
              </v-col>
            </v-row>
          </v-container>
          <small>*indicates required field</small>
        </v-card-text>
        <v-card-actions>
          <v-spacer></v-spacer>
          <v-btn color="blue-darken-1" variant="text" @click="closeDialog">
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
  import { useDisplay } from "vuetify";
  import { useField, useForm } from "vee-validate";

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
