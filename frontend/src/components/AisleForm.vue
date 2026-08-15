<template>
  <v-dialog
    v-model="show"
    persistent
    :width="isMobile ? undefined : 520"
    :fullscreen="isMobile"
  >
    <FormSheet
      :title="props.isEdit ? 'Edit Aisle' : 'Add Aisle'"
      eyebrow="Aisle"
      icon="mdi-view-list-outline"
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
        label="Aisle Name*"
        required
        v-model="name.value.value"
        :error-messages="name.errorMessage.value"
      ></v-text-field>
      <v-text-field
        label="Order*"
        v-model="order.value.value"
        :error-messages="order.errorMessage.value"
        type="number"
      ></v-text-field>
    </FormSheet>
  </v-dialog>
</template>
<script setup>
  import { ref, defineEmits, defineProps, onMounted, watchEffect } from "vue";
  import { useMainStore } from "@/stores/main";
  import { useStores } from "@/composables/storesComposable";
  import { useDisplay } from "vuetify";
  import { useField, useForm } from "vee-validate";
  import FormSheet from "@/components/FormSheet.vue";

  const { handleSubmit } = useForm({
    validationSchema: {
      name(value) {
        if (value) return true;

        return "Must provide an aisle name.";
      },
    },
  });

  const name = useField("name");
  const id = useField("id");
  const store_id = useField("store_id");
  const order = useField("order");

  const { smAndDown } = useDisplay();
  const isMobile = smAndDown;

  const { stores } = useStores();
  const props = defineProps({
    aisleFormDialog: {
      type: Boolean,
      default: false,
    },
    isEdit: {
      type: Boolean,
      default: false,
    },
    passedFormData: Object,
  });

  const mainstore = useMainStore();
  const show = ref(props.aisleFormDialog);
  const emit = defineEmits(["addAisle", "editAisle", "updateDialog"]);

  const watchPassedFormData = () => {
    watchEffect(() => {
      if (props.passedFormData) {
        id.value.value = props.passedFormData.id;
        name.value.value = props.passedFormData.name;
        store_id.value.value = props.passedFormData.store_id
          ? props.passedFormData.store_id
          : mainstore.store_id;
        order.value.value = props.passedFormData.order;
      }
    });
  };

  onMounted(() => {
    watchPassedFormData();
  });

  const submit = handleSubmit(values => {
    if (props.isEdit == false) {
      emit("addAisle", values);
    } else {
      emit("editAisle", values);
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
    store_id.value.value = mainstore.store_id;
    order.value.value = props.passedFormData.order;
  };
</script>
