<template>
  <!-- Bound straight to the prop rather than mirrored into a local ref, so the
       dialog and the parent's flag cannot drift apart if Vuetify closes it. -->
  <v-dialog
    :model-value="props.modelValue"
    persistent
    :width="isMobile ? undefined : 460"
    :fullscreen="isMobile"
    @update:model-value="value => !value && close()"
  >
    <FormSheet
      :title="props.itemName || 'Photo'"
      eyebrow="Photo"
      icon="mdi-camera-outline"
      :fullscreen="isMobile"
      submit-label="Save photo"
      @submit="submit"
      @close="close"
    >
      <ImagePicker v-model="staged" :current-url="props.currentUrl" />

      <!-- Worth saying plainly: the photo is on the catalog item, not on this
           row, so it turns up wherever that item appears. -->
      <p class="itemphoto__note">
        Photos belong to the item itself, so this one shows on every list that
        uses it.
      </p>
    </FormSheet>
  </v-dialog>
</template>

<script setup>
  // Adding a photo from a shopping list row, which is where you are actually
  // stood in front of the product. Rendered once by ShoppingList, outside the
  // v-for, and driven by a selected-item ref.
  import { ref, watch } from "vue";
  import { useDisplay } from "vuetify";
  import FormSheet from "@/components/FormSheet.vue";
  import ImagePicker from "@/components/ImagePicker.vue";

  const props = defineProps({
    modelValue: {
      type: Boolean,
      default: false,
    },
    itemId: {
      type: Number,
      default: null,
    },
    itemName: {
      type: String,
      default: "",
    },
    currentUrl: {
      type: String,
      default: null,
    },
  });

  const emit = defineEmits(["update:modelValue", "save"]);

  const { smAndDown } = useDisplay();
  const isMobile = smAndDown;

  const noImageChange = () => ({ file: null, remove: false });
  const staged = ref(noImageChange());

  watch(
    () => props.modelValue,
    value => {
      // Reopening for a different row must not inherit the last row's staged
      // file. Reset on open rather than on close, so a save that is still in
      // flight keeps the file it is uploading.
      if (value) staged.value = noImageChange();
    },
  );

  const close = () => {
    emit("update:modelValue", false);
  };

  const submit = () => {
    emit("save", { itemId: props.itemId, image: staged.value });
    close();
  };
</script>

<style scoped>
  .itemphoto__note {
    margin: 0;
    font-size: 0.75rem;
    color: var(--ls-ink-faint);
  }
</style>
