<template>
  <v-dialog
    v-model="show"
    persistent
    :width="isMobile ? undefined : 460"
    :fullscreen="isMobile"
  >
    <FormSheet
      :title="props.isEdit ? 'Edit Item' : 'Add Item'"
      eyebrow="Item"
      icon="mdi-food-apple-outline"
      :fullscreen="isMobile"
      required-note
      @submit="submit"
      @close="closeDialog"
    >
      <v-text-field
        label="Item Name*"
        v-model="name.value.value"
        :error-messages="name.errorMessage.value"
      ></v-text-field>

      <ImagePicker
        v-model="image.value.value"
        :current-url="props.passedFormData?.thumbnail_url"
      />
    </FormSheet>
  </v-dialog>
</template>
<script setup>
  import { ref, defineEmits, defineProps, onMounted, watchEffect } from "vue";
  import { useDisplay } from "vuetify";
  import { useField, useForm } from "vee-validate";
  import FormSheet from "@/components/FormSheet.vue";
  import ImagePicker from "@/components/ImagePicker.vue";

  // What ImagePicker starts from, and what it is reset to on cancel. A fresh
  // object each time, so two dialogs never share one staged photo.
  const noImageChange = () => ({ file: null, remove: false });

  const { handleSubmit } = useForm({
    validationSchema: {
      name(value) {
        if (value) return true;

        return "Must provide an item name.";
      },
    },
  });

  const name = useField("name");
  const id = useField("id");
  const matches = useField("matches");
  const image = useField("image", undefined, { initialValue: noImageChange() });

  const { smAndDown } = useDisplay();
  const isMobile = smAndDown;

  const props = defineProps({
    itemFormDialog: {
      type: Boolean,
      default: false,
    },
    isEdit: {
      type: Boolean,
      default: false,
    },
    passedFormData: Object,
  });

  const show = ref(props.itemFormDialog);
  const emit = defineEmits(["addItem", "editItem", "updateDialog"]);

  const watchPassedFormData = () => {
    watchEffect(() => {
      if (props.passedFormData) {
        id.value.value = props.passedFormData.id;
        name.value.value = props.passedFormData.name;
        matches.value.value = props.passedFormData.matches;
      }
    });
  };

  onMounted(() => {
    watchPassedFormData();
  });

  const submit = handleSubmit(values => {
    if (props.isEdit == false) {
      emit("addItem", values);
    } else {
      emit("editItem", values);
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
    matches.value.value = props.passedFormData.matches;
    // Cancelling has to drop a staged photo too, or reopening the dialog would
    // show a preview of a file the user backed out of.
    image.value.value = noImageChange();
  };
</script>
