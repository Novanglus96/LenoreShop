<template>
  <v-dialog
    v-model="show"
    persistent
    :width="isMobile ? undefined : 560"
    :fullscreen="isMobile"
  >
    <FormSheet
      title="Move Food"
      eyebrow="Move"
      icon="mdi-swap-horizontal"
      submit-label="Move"
      :fullscreen="isMobile"
      required-note
      @submit="submit"
      @close="closeDialog"
    >
      <p class="movefood__what">
        <span class="movefood__name">{{ props.passedFormData.name }}</span>
        <span class="movefood__stock">{{ stockLabel }}</span>
      </p>

      <v-select
        label="Move to*"
        v-model="freezer_id.value.value"
        :items="destinations"
        item-title="name"
        item-value="id"
        :error-messages="freezer_id.errorMessage.value"
        :no-data-text="'No other freezer to move it to.'"
      ></v-select>

      <v-radio-group v-model="mode" hide-details density="compact">
        <v-radio :label="`Move all ${available}`" value="all"></v-radio>
        <v-radio label="Move some of it" value="some"></v-radio>
      </v-radio-group>

      <v-text-field
        v-if="mode === 'some'"
        label="How many?"
        v-model="qty.value.value"
        type="number"
        min="1"
        :max="available - 1"
        :suffix="props.passedFormData.unit || undefined"
        :error-messages="qty.errorMessage.value"
      ></v-text-field>

      <p class="movefood__note">
        <v-icon icon="mdi-information-outline" size="16" />
        {{ outcomeLabel }}
      </p>
    </FormSheet>
  </v-dialog>
</template>

<script setup>
  // Remounted per row by its :key, the same way FreezerItemForm is, so the
  // destination and amount always start fresh.
  import { computed, ref, watch } from "vue";
  import { useDisplay } from "vuetify";
  import { useField, useForm } from "vee-validate";
  import FormSheet from "@/components/FormSheet.vue";

  const props = defineProps({
    transferFormDialog: {
      type: Boolean,
      default: false,
    },
    // The row being moved. `qty` is the ceiling, `freezer_id` the freezer it is
    // leaving — excluded from the destination list.
    passedFormData: {
      type: Object,
      default: () => ({ id: 0, name: "", qty: 1, unit: null, freezer_id: 0 }),
    },
    freezers: {
      type: Array,
      default: () => [],
    },
  });

  const emit = defineEmits(["transferFreezerItem", "updateDialog"]);

  const show = ref(props.transferFormDialog);
  const { smAndDown } = useDisplay();
  const isMobile = smAndDown;

  // "all" is the common case — most of the time a whole bag is being shifted —
  // so it is the default and needs no number typed.
  const mode = ref("all");

  const available = computed(() => props.passedFormData?.qty ?? 1);

  // Moving food to the freezer it is already in is rejected by the backend, so
  // never offer it.
  const destinations = computed(() =>
    props.freezers.filter(
      freezer => freezer.id !== props.passedFormData?.freezer_id,
    ),
  );

  const { handleSubmit } = useForm({
    validationSchema: {
      freezer_id(value) {
        if (value) return true;

        return "Must choose a freezer.";
      },
      qty(value) {
        // Only meaningful in "some" mode; "all" sends no quantity at all.
        if (mode.value !== "some") return true;
        if (!(value > 0)) return "Amount must be greater than 0.";
        if (Number(value) >= available.value) {
          return `Choose "Move all" to move every one of them.`;
        }

        return true;
      },
    },
  });

  const freezer_id = useField("freezer_id");
  const qty = useField("qty", undefined, { initialValue: 1 });

  // A single portion cannot be split, so the choice would be a dead control.
  watch(
    available,
    value => {
      if (value <= 1) mode.value = "all";
    },
    { immediate: true },
  );

  const stockLabel = computed(() => {
    const unit = props.passedFormData?.unit;
    if (unit) return `${available.value} ${unit} to move`;
    return `${available.value} to move`;
  });

  const outcomeLabel = computed(() => {
    if (mode.value === "all") {
      return "The whole row moves across, photo and dates included.";
    }
    const left = available.value - Number(qty.value.value || 0);
    if (!(left > 0)) return "The whole row moves across.";
    return `${left} stays behind as its own row.`;
  });

  const closeDialog = () => {
    show.value = false;
    emit("updateDialog");
  };

  const submit = handleSubmit(values => {
    emit(
      "transferFreezerItem",
      props.passedFormData,
      values.freezer_id,
      // undefined, not null: the backend reads a missing qty as "all of it",
      // and relocates the row rather than splitting it.
      mode.value === "all" ? undefined : Number(values.qty),
    );
    closeDialog();
  });
</script>

<style scoped>
  .movefood__what {
    display: flex;
    flex-direction: column;
    gap: 2px;
    margin: 0;
  }

  .movefood__name {
    font-size: 1.0625rem;
    color: var(--ls-ink);
    overflow-wrap: anywhere;
  }

  .movefood__stock {
    font-size: 0.8125rem;
    color: var(--ls-ink-faint);
  }

  .movefood__note {
    display: flex;
    align-items: center;
    gap: var(--ls-space-xs);
    margin: 0;
    font-size: 0.8125rem;
    color: var(--ls-ink-faint);
  }
</style>
