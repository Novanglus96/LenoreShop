<template>
  <v-dialog
    v-model="show"
    persistent
    :width="isMobile ? undefined : 460"
    :fullscreen="isMobile"
  >
    <FormSheet
      :title="props.isEdit ? 'Edit Store' : 'Add Store'"
      eyebrow="Store"
      icon="mdi-storefront-outline"
      :fullscreen="isMobile"
      required-note
      @submit="submit"
      @close="closeDialog"
    >
      <v-text-field
        label="Store Name*"
        v-model="name.value.value"
        :error-messages="name.errorMessage.value"
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

        return "Must provide a store name.";
      },
    },
  });

  const name = useField("name");
  const id = useField("id");

  const { smAndDown } = useDisplay();
  const isMobile = smAndDown;

  const props = defineProps({
    storeFormDialog: {
      type: Boolean,
      default: false,
    },
    isEdit: {
      type: Boolean,
      default: false,
    },
    passedFormData: Object,
  });

  const show = ref(props.storeFormDialog);
  const emit = defineEmits(["addStore", "editStore", "updateDialog"]);

  const watchPassedFormData = () => {
    watchEffect(() => {
      if (props.passedFormData) {
        id.value.value = props.passedFormData.id;
        name.value.value = props.passedFormData.name;
      }
    });
  };

  onMounted(() => {
    watchPassedFormData();
  });

  const submit = handleSubmit(values => {
    if (props.isEdit == false) {
      emit("addStore", values);
    } else {
      emit("editStore", values);
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
  };
</script>
