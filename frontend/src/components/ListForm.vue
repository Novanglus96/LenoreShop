<template>
  <v-dialog
    v-model="show"
    persistent
    :width="isMobile ? undefined : 520"
    :fullscreen="isMobile"
  >
    <FormSheet
      :title="props.isEdit ? 'Edit List' : 'Add List'"
      eyebrow="List"
      icon="mdi-cart-outline"
      :fullscreen="isMobile"
      required-note
      @submit="submit"
      @close="closeDialog"
    >
      <v-select
        label="Store*"
        :items="stores"
        item-title="name"
        item-value="id"
        v-model="store_id.value.value"
        :error-messages="store_id.errorMessage.value"
      ></v-select>
      <v-text-field
        label="List Name*"
        v-model="name.value.value"
        :error-messages="name.errorMessage.value"
      ></v-text-field>
    </FormSheet>
  </v-dialog>
</template>
<script setup>
  import { ref, defineEmits, defineProps, onMounted, watchEffect } from "vue";
  import { useStores } from "@/composables/storesComposable";
  import { useDisplay } from "vuetify";
  import { useField, useForm } from "vee-validate";
  import FormSheet from "@/components/FormSheet.vue";

  const { handleSubmit } = useForm({
    validationSchema: {
      name(value) {
        if (value) return true;

        return "Must provide a list name.";
      },
    },
  });

  const name = useField("name");
  const id = useField("id");
  const store_id = useField("store_id");

  const { smAndDown } = useDisplay();
  const isMobile = smAndDown;

  const { stores } = useStores();

  const props = defineProps({
    listFormDialog: {
      type: Boolean,
      default: false,
    },
    isEdit: {
      type: Boolean,
      default: false,
    },
    passedFormData: Object,
  });

  const show = ref(props.listFormDialog);
  const emit = defineEmits(["addList", "editList", "updateDialog"]);

  const watchPassedFormData = () => {
    watchEffect(() => {
      if (props.passedFormData) {
        id.value.value = props.passedFormData.id;
        name.value.value = props.passedFormData.name;
        store_id.value.value = props.passedFormData.store_id
          ? props.passedFormData.store_id
          : null;
      }
    });
  };

  onMounted(() => {
    watchPassedFormData();
  });

  const submit = handleSubmit(values => {
    if (props.isEdit == false) {
      emit("addList", values);
    } else {
      emit("editList", values);
    }

    closeDialog();
  });

  const closeDialog = () => {
    emit("updateDialog", false);
    clearFormData();
  };

  const clearFormData = () => {
    id.value.value = props.passedFormData.id;
    name.value.value = props.passedFormData.name;
    store_id.value.value = props.passedFormData.store_id;
  };
</script>
