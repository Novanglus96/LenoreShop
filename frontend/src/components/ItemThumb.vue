<template>
  <button
    v-if="thumbnailUrl"
    type="button"
    :class="['itemthumb', `itemthumb--${variant}`]"
    :aria-label="`View photo of ${name}`"
    @click.stop="open"
  >
    <!-- Decorative here: the button's aria-label already names the item, so an
         alt would say the same thing twice to a screen reader. -->
    <img :src="thumbnailUrl" alt="" class="itemthumb__img" loading="lazy" />
  </button>

  <span
    v-else-if="placeholder"
    :class="['itemthumb', 'itemthumb--empty', `itemthumb--${variant}`]"
    aria-hidden="true"
  >
    <v-icon icon="mdi-camera-outline" size="16" />
  </span>
</template>

<script setup>
  // The thumbnail on a row. Renders nothing at all when there is no photo and
  // no placeholder was asked for, so list rows that predate this feature keep
  // exactly the layout they had.
  import { useLightbox } from "@/composables/lightboxComposable";

  const props = defineProps({
    thumbnailUrl: {
      type: String,
      default: null,
    },
    // The full-size rendition. Falls back to the thumbnail so a row still opens
    // something if only the small one came back.
    imageUrl: {
      type: String,
      default: null,
    },
    name: {
      type: String,
      default: "",
    },
    // Shows a camera outline when there is no photo. On for the catalog, where
    // the gap is a prompt to add one; off on a shopping list, where it would
    // just be noise next to every unphotographed row.
    placeholder: {
      type: Boolean,
      default: false,
    },
    // "frost" swaps the paper palette for the freezer one.
    variant: {
      type: String,
      default: "paper",
    },
  });

  const { openImage } = useLightbox();

  const open = () => {
    openImage(props.imageUrl || props.thumbnailUrl, props.name);
  };
</script>

<style scoped>
  .itemthumb {
    flex-shrink: 0;
    display: flex;
    align-items: center;
    justify-content: center;
    width: 40px;
    height: 40px;
    padding: 0;
    overflow: hidden;
    border: 1px solid var(--ls-rule-strong);
    border-radius: var(--ls-radius-sm);
    background: var(--ls-paper-shade);
  }

  .itemthumb__img {
    width: 100%;
    height: 100%;
    object-fit: cover;
    display: block;
  }

  .itemthumb--empty {
    border-style: dashed;
    border-color: var(--ls-rule);
    color: var(--ls-ink-faint);
    background: transparent;
  }

  .itemthumb--frost {
    border-color: var(--ls-frost-rule);
    background: var(--ls-frost-shade);
  }

  .itemthumb--frost.itemthumb--empty {
    color: var(--ls-frost-ink-faint);
    background: transparent;
  }
</style>
