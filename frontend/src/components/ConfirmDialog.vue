<template>
  <v-dialog
    :model-value="modelValue"
    max-width="420"
    @update:model-value="$emit('update:modelValue', $event)"
  >
    <v-card class="confirm">
      <header class="confirm__head">
        <v-icon
          :icon="icon"
          :class="['confirm__icon', `confirm__icon--${tone}`]"
          size="22"
        />
        <h2 class="ls-hand ls-hand--card confirm__title">{{ title }}</h2>
      </header>

      <v-card-text class="confirm__body">
        <slot />
      </v-card-text>

      <footer class="confirm__actions">
        <v-btn variant="text" @click="$emit('update:modelValue', false)">
          {{ cancelLabel }}
        </v-btn>
        <v-btn
          :color="tone === 'danger' ? 'error' : 'primary'"
          variant="flat"
          @click="$emit('confirm')"
        >
          {{ confirmLabel }}
        </v-btn>
      </footer>
    </v-card>
  </v-dialog>
</template>

<script setup>
  // One shell for every "are you sure" in the app. modelValue is declared rather
  // than left to fall through, so this can be dropped in with a plain v-model.
  defineProps({
    modelValue: {
      type: Boolean,
      default: false,
    },
    title: {
      type: String,
      required: true,
    },
    confirmLabel: {
      type: String,
      default: "Delete",
    },
    cancelLabel: {
      type: String,
      default: "Cancel",
    },
    // `danger` for anything destructive, `normal` for a confirmation that only
    // needs a second look.
    tone: {
      type: String,
      default: "danger",
    },
    icon: {
      type: String,
      default: "mdi-alert-outline",
    },
  });

  defineEmits(["update:modelValue", "confirm"]);
</script>

<style scoped>
  .confirm__head {
    display: flex;
    align-items: center;
    gap: var(--ls-space-sm);
    padding: var(--ls-space) var(--ls-space) var(--ls-space-sm);
  }

  .confirm__icon--danger {
    color: var(--ls-alert);
  }

  .confirm__icon--normal {
    color: var(--ls-navy);
  }

  .confirm__title {
    margin: 0;
  }

  .confirm__body {
    padding-top: 0 !important;
    padding-right: var(--ls-space) !important;
    padding-bottom: var(--ls-space) !important;
    padding-left: var(--ls-space) !important;
    color: var(--ls-ink-soft);
    line-height: 1.5;
  }

  .confirm__actions {
    display: flex;
    justify-content: flex-end;
    gap: var(--ls-space-sm);
    padding: var(--ls-space-sm) var(--ls-space) var(--ls-space);
    border-top: 1px solid var(--ls-rule);
  }
</style>
