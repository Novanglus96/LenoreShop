import { ref } from "vue";

// Module-level rather than per-caller, so every thumbnail in the app drives one
// shared overlay. The alternative — a viewer per list — puts a dialog inside a
// v-for, which is exactly the shape that stacked into a black screen on mobile
// (see ShoppingList.vue, ec3715c).
const src = ref(null);
const caption = ref("");

export function useLightbox() {
  /**
   * Opens the overlay on a full-size image.
   *
   * @param {string} url The image to show. Falsy urls are ignored, so callers
   *   can hand over an item that may have no photo without checking first.
   * @param {string} label Shown under the image, and used as its alt text.
   */
  function openImage(url, label = "") {
    if (!url) return;
    src.value = url;
    caption.value = label;
  }

  function closeImage() {
    src.value = null;
    caption.value = "";
  }

  return { src, caption, openImage, closeImage };
}
