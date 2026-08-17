<template>
  <v-dialog
    v-model="show"
    persistent
    :width="isMobile ? undefined : 520"
    :fullscreen="isMobile"
  >
    <FormSheet
      title="Use Food"
      eyebrow="Use"
      icon="mdi-silverware-fork-knife"
      submit-label="Use"
      :fullscreen="isMobile"
      @submit="submit"
      @close="closeDialog"
    >
      <p class="usefood__what">
        <span class="usefood__name">{{ props.passedFormData.name }}</span>
        <span class="usefood__stock">{{ stockLabel }}</span>
      </p>

      <v-text-field
        label="How many?"
        v-model="qty.value.value"
        type="number"
        min="1"
        :max="available"
        :suffix="props.passedFormData.unit || undefined"
        :error-messages="qty.errorMessage.value"
      ></v-text-field>

      <v-btn
        v-if="available > 1 && !usesTheLastOfIt"
        variant="text"
        size="small"
        class="usefood__all"
        @click="qty.value.value = available"
      >
        Use all {{ available }}
      </v-btn>

      <!-- Worth saying plainly: this is the one path that removes a row
           without going through the delete confirmation. -->
      <p v-if="usesTheLastOfIt" class="usefood__note">
        <v-icon icon="mdi-information-outline" size="16" />
        That is all of it — it will be taken out of the freezer.
      </p>
    </FormSheet>
  </v-dialog>
</template>

<script setup>
  // Remounted per row by its :key, the same way FreezerItemForm is, so the
  // quantity always starts fresh instead of carrying over from the last food.
  import { computed, ref } from "vue";
  import { useDisplay } from "vuetify";
  import { useField, useForm } from "vee-validate";
  import FormSheet from "@/components/FormSheet.vue";

  const props = defineProps({
    useFormDialog: {
      type: Boolean,
      default: false,
    },
    // The row being used. `qty` is the ceiling on what can be taken.
    passedFormData: {
      type: Object,
      default: () => ({ id: 0, name: "", qty: 1, unit: null }),
    },
  });

  const emit = defineEmits(["useFreezerItem", "updateDialog"]);

  const show = ref(props.useFormDialog);
  const { smAndDown } = useDisplay();
  const isMobile = smAndDown;

  const available = computed(() => props.passedFormData?.qty ?? 1);

  const { handleSubmit } = useForm({
    validationSchema: {
      qty(value) {
        if (!(value > 0)) return "Amount must be greater than 0.";
        if (Number(value) > available.value) {
          return `Only ${available.value} in the freezer.`;
        }

        return true;
      },
    },
  });

  const qty = useField("qty", undefined, { initialValue: 1 });

  const usesTheLastOfIt = computed(
    () => Number(qty.value.value) === available.value,
  );

  const stockLabel = computed(() => {
    const unit = props.passedFormData?.unit;
    if (unit) return `${available.value} ${unit} in the freezer`;
    return `${available.value} in the freezer`;
  });

  const closeDialog = () => {
    show.value = false;
    emit("updateDialog");
  };

  const submit = handleSubmit(values => {
    emit("useFreezerItem", props.passedFormData, Number(values.qty));
    closeDialog();
  });
</script>

<style scoped>
  .usefood__what {
    display: flex;
    flex-direction: column;
    gap: 2px;
    margin: 0;
  }

  .usefood__name {
    font-size: 1.0625rem;
    color: var(--ls-ink);
    overflow-wrap: anywhere;
  }

  .usefood__stock {
    font-size: 0.8125rem;
    color: var(--ls-ink-faint);
  }

  .usefood__all {
    align-self: flex-start;
  }

  .usefood__note {
    display: flex;
    align-items: center;
    gap: var(--ls-space-xs);
    margin: 0;
    font-size: 0.8125rem;
    color: var(--ls-warn);
  }
</style>
