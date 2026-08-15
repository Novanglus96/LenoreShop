<template>
  <v-dialog
    v-model="show"
    persistent
    :width="isMobile ? undefined : 520"
    :fullscreen="isMobile"
  >
    <FormSheet
      :title="props.isEdit ? 'Edit Freezer' : 'Add Freezer'"
      eyebrow="Freezer"
      icon="mdi-snowflake"
      :fullscreen="isMobile"
      required-note
      @submit="submit"
      @close="closeDialog"
    >
      <v-text-field
        label="Freezer Name*"
        v-model="name.value.value"
        :error-messages="name.errorMessage.value"
      ></v-text-field>
      <v-text-field
        label="Location"
        placeholder="Garage"
        v-model="location.value.value"
        :error-messages="location.errorMessage.value"
      ></v-text-field>
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

        return "Must provide a freezer name.";
      },
    },
  });

  const name = useField("name");
  const location = useField("location");
  const id = useField("id");

  const { smAndDown } = useDisplay();
  const isMobile = smAndDown;

  const props = defineProps({
    freezerFormDialog: {
      type: Boolean,
      default: false,
    },
    isEdit: {
      type: Boolean,
      default: false,
    },
    passedFormData: Object,
  });

  const show = ref(props.freezerFormDialog);
  const emit = defineEmits(["addFreezer", "editFreezer", "updateDialog"]);

  const watchPassedFormData = () => {
    watchEffect(() => {
      if (props.passedFormData) {
        id.value.value = props.passedFormData.id;
        name.value.value = props.passedFormData.name;
        location.value.value = props.passedFormData.location;
      }
    });
  };

  onMounted(() => {
    watchPassedFormData();
  });

  const submit = handleSubmit(values => {
    if (props.isEdit == false) {
      emit("addFreezer", values);
    } else {
      emit("editFreezer", values);
    }
    closeDialog();
  });

  const closeDialog = () => {
    emit("updateDialog", false);
    clearFormData();
  };

  // Reset to the defaults the parent supplied. The watchEffect above only
  // re-runs when passedFormData changes, so clearing to hardcoded blanks would
  // discard any prefill for the life of the view — see FreezerItemForm, where
  // exactly that lost the selected freezer and the date_added default.
  const clearFormData = () => {
    const defaults = props.passedFormData ?? {};
    id.value.value = defaults.id ?? null;
    name.value.value = defaults.name ?? null;
    location.value.value = defaults.location ?? null;
  };
</script>
