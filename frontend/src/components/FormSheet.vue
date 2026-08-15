<template>
  <!-- The <form> wraps the <v-card>, not the other way round. Vuetify's
       scrollable dialog only matches `.v-overlay__content > form > .v-card >
       .v-card-text`, so a card-outside-form nesting silently loses the ability
       to scroll a tall form on a short screen. -->
  <form class="formsheet" @submit.prevent="$emit('submit')">
    <v-card
      :class="['formsheet__card', { 'formsheet__card--full': fullscreen }]"
    >
      <header class="formsheet__head">
        <span class="ls-tab">
          <v-icon :icon="icon" size="14" />
          <span class="ls-tab__text">{{ eyebrow }}</span>
        </span>
        <h2 class="ls-hand ls-hand--card formsheet__title">{{ title }}</h2>
      </header>

      <v-card-text class="formsheet__body">
        <div class="ls-form-grid">
          <slot />
        </div>

        <p v-if="requiredNote" class="formsheet__required">
          <span aria-hidden="true">*</span>
          required
        </p>
      </v-card-text>

      <footer class="formsheet__actions">
        <v-btn variant="text" @click="$emit('close')">Cancel</v-btn>
        <v-btn color="primary" variant="flat" type="submit">
          {{ submitLabel }}
        </v-btn>
      </footer>
    </v-card>
  </form>
</template>

<script setup>
  // The shared shell for every add/edit dialog: the paper surface, the folded tab
  // and handwritten heading, the field grid and the actions row. Each form keeps
  // its own v-dialog, vee-validate fields and submit handler, so the dialog's
  // modelValue fallthrough is untouched.
  defineProps({
    title: {
      type: String,
      required: true,
    },
    // The short word on the folded tab — what kind of thing is being edited.
    eyebrow: {
      type: String,
      required: true,
    },
    icon: {
      type: String,
      default: "mdi-pencil-outline",
    },
    submitLabel: {
      type: String,
      default: "Save",
    },
    // Mirrors the dialog's own fullscreen state; a class rather than a media
    // query because Vuetify's smAndDown breakpoint is not the one the design
    // layer uses elsewhere.
    fullscreen: {
      type: Boolean,
      default: false,
    },
    requiredNote: {
      type: Boolean,
      default: false,
    },
  });

  defineEmits(["submit", "close"]);
</script>

<style scoped>
  .formsheet {
    width: 100%;
  }

  /* The card already paints --ls-paper: the Vuetify theme's `surface` is set to
   the same warm off-white, so no override is needed here. */
  .formsheet__card {
    display: flex;
    flex-direction: column;
  }

  .formsheet__card--full {
    border-radius: 0;
    min-height: 100%;
  }

  .formsheet__head {
    display: flex;
    flex-direction: column;
    align-items: flex-start;
    gap: var(--ls-space-xs);
    /* Left padding matches --ls-space so .ls-tab's negative margin tucks it into
     the sheet's edge the way it does on a card. */
    padding: var(--ls-space) var(--ls-space) var(--ls-space-sm);
    border-bottom: 1px solid var(--ls-rule-strong);
  }

  .formsheet__title {
    margin: 0;
  }

  .formsheet__body {
    /* Longhand so the top rhythm is not inherited from Vuetify's card padding. */
    padding-top: var(--ls-space) !important;
    padding-right: var(--ls-space) !important;
    padding-bottom: var(--ls-space) !important;
    padding-left: var(--ls-space) !important;
  }

  .formsheet__required {
    margin: var(--ls-space-sm) 0 0;
    font-size: 0.75rem;
    color: var(--ls-ink-faint);
  }

  .formsheet__actions {
    display: flex;
    justify-content: flex-end;
    gap: var(--ls-space-sm);
    padding: var(--ls-space-sm) var(--ls-space) var(--ls-space);
    border-top: 1px solid var(--ls-rule);
    /* Stays put while the body scrolls, so Save is always reachable. */
    background: var(--ls-paper);
  }

  /* On a phone the dialog is fullscreen, so the actions become the bar you reach
   for with a thumb. */
  .formsheet__card--full .formsheet__actions {
    margin-top: auto;
  }
</style>
