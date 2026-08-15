<template>
  <v-dialog
    :model-value="isOpen"
    fullscreen
    transition="fade-transition"
    scrim="black"
    @update:model-value="closeImage"
  >
    <!-- Clicking anywhere dismisses. On a phone this is a photo you opened to
         squint at for a second, so the whole surface is the way out rather than
         a small target in a corner. -->
    <div class="lightbox" @click="closeImage">
      <v-btn
        icon="mdi-close"
        variant="text"
        size="large"
        class="lightbox__close"
        aria-label="Close photo"
      />

      <img
        v-if="src"
        :src="src"
        :alt="caption || 'Item photo'"
        class="lightbox__image"
      />

      <p v-if="caption" class="lightbox__caption">{{ caption }}</p>
    </div>
  </v-dialog>
</template>

<script setup>
  // Mounted once, in App.vue. Anything with a photo calls openImage() from the
  // lightbox composable instead of owning an overlay of its own.
  import { computed } from "vue";
  import { useLightbox } from "@/composables/lightboxComposable";

  const { src, caption, closeImage } = useLightbox();

  const isOpen = computed(() => Boolean(src.value));
</script>

<style scoped>
  .lightbox {
    position: relative;
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    gap: var(--ls-space);
    width: 100%;
    height: 100%;
    padding: var(--ls-space);
    background: rgba(0, 0, 0, 0.92);
  }

  .lightbox__close {
    position: absolute;
    top: env(safe-area-inset-top, 0px);
    right: 0;
    color: #fff;
  }

  .lightbox__image {
    max-width: 100%;
    /* Leaves room for the caption without letting a tall photo push it off. */
    max-height: 80%;
    object-fit: contain;
    border-radius: var(--ls-radius-sm);
  }

  .lightbox__caption {
    margin: 0;
    color: #fff;
    font-size: 0.9375rem;
    text-align: center;
    overflow-wrap: anywhere;
  }
</style>
