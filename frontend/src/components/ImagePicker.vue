<template>
  <div class="imagepicker">
    <span class="imagepicker__label">Photo</span>

    <div class="imagepicker__row">
      <span class="imagepicker__preview">
        <img
          v-if="previewUrl"
          :src="previewUrl"
          alt=""
          class="imagepicker__img"
        />
        <v-icon v-else icon="mdi-camera-outline" size="22" />
      </span>

      <div class="imagepicker__actions">
        <!-- Two inputs, because one cannot do both jobs. `capture` sends the
             OS straight to the camera; without it the picker opens the photo
             library. Relying on a single bare input to offer a choice sheet
             does not hold up on device — tested on mobile, only the library
             was offered and the camera was unreachable. Each source therefore
             gets its own control. -->
        <input
          ref="cameraInput"
          type="file"
          accept="image/*"
          capture="environment"
          class="imagepicker__input"
          @change="pick"
        />
        <input
          ref="libraryInput"
          type="file"
          accept="image/*"
          class="imagepicker__input"
          @change="pick"
        />

        <v-btn
          v-if="canCapture"
          variant="tonal"
          size="small"
          prepend-icon="mdi-camera-outline"
          @click="cameraInput.click()"
        >
          {{ previewUrl ? "Retake" : "Take photo" }}
        </v-btn>

        <v-btn
          variant="tonal"
          size="small"
          prepend-icon="mdi-image-outline"
          @click="libraryInput.click()"
        >
          {{ previewUrl ? "Choose another" : "Choose photo" }}
        </v-btn>

        <v-btn
          v-if="previewUrl"
          variant="text"
          size="small"
          color="error"
          prepend-icon="mdi-close"
          @click="clear"
        >
          Remove
        </v-btn>
      </div>
    </div>

    <p v-if="error" class="imagepicker__error">{{ error }}</p>
    <p v-else class="imagepicker__hint">
      Helps you spot the right one on the shelf.
    </p>
  </div>
</template>

<script setup>
  // Stages a photo choice rather than uploading it. The file only goes to the
  // server after the form is saved, because a new item has no id to upload
  // against until it has been created.
  //
  // v-model is `{ file, remove }`:
  //   file   - a File to upload once the row exists, or null.
  //   remove - true when an existing photo should be deleted on save.
  import { computed, onBeforeUnmount, ref, watch } from "vue";

  const props = defineProps({
    modelValue: {
      type: Object,
      default: () => ({ file: null, remove: false }),
    },
    // The photo already stored on the record, if any.
    currentUrl: {
      type: String,
      default: null,
    },
  });

  const emit = defineEmits(["update:modelValue"]);

  const cameraInput = ref(null);
  const libraryInput = ref(null);
  const localUrl = ref(null);
  const error = ref("");

  // A coarse pointer means a phone or tablet, which is where a camera intent
  // makes sense and where this feature is actually used. Deliberately a
  // capability query rather than a viewport breakpoint: a narrow desktop window
  // is still a desktop. Defaults to showing the button if matchMedia is
  // missing, since losing the camera is the worse failure.
  const canCapture =
    typeof window === "undefined" || !window.matchMedia
      ? true
      : window.matchMedia("(pointer: coarse)").matches;

  // Mirrors the backend's own ceiling, so an oversized photo is caught before
  // it is uploaded rather than after a round trip.
  const MAX_BYTES = 12 * 1024 * 1024;

  const previewUrl = computed(() => {
    if (localUrl.value) return localUrl.value;
    if (props.modelValue?.remove) return null;
    return props.currentUrl;
  });

  const releaseLocalUrl = () => {
    if (localUrl.value) {
      // Object URLs pin the file in memory until revoked, and a form can be
      // reopened many times in a session.
      URL.revokeObjectURL(localUrl.value);
      localUrl.value = null;
    }
  };

  // An input holds on to its last selection, so picking the same file twice
  // fires no change event. Clearing after every read keeps re-picking working,
  // and covers switching between the camera and the library.
  const resetInputs = () => {
    if (cameraInput.value) cameraInput.value.value = "";
    if (libraryInput.value) libraryInput.value.value = "";
  };

  const pick = event => {
    const file = event.target.files?.[0];
    resetInputs();
    if (!file) return;

    if (!file.type.startsWith("image/")) {
      error.value = "That file is not an image.";
      return;
    }
    if (file.size > MAX_BYTES) {
      error.value = "That photo is larger than 12MB.";
      return;
    }

    error.value = "";
    releaseLocalUrl();
    localUrl.value = URL.createObjectURL(file);
    emit("update:modelValue", { file, remove: false });
  };

  const clear = () => {
    error.value = "";
    releaseLocalUrl();
    resetInputs();
    // Only worth a delete call if there was something stored to begin with.
    emit("update:modelValue", {
      file: null,
      remove: Boolean(props.currentUrl),
    });
  };

  // The parent resets modelValue when the dialog is reopened for a different
  // record; drop the stale preview with it.
  watch(
    () => props.modelValue,
    value => {
      if (!value?.file) releaseLocalUrl();
    },
  );

  onBeforeUnmount(releaseLocalUrl);
</script>

<style scoped>
  .imagepicker {
    display: flex;
    flex-direction: column;
    gap: var(--ls-space-xs);
  }

  .imagepicker__label {
    font-size: 0.75rem;
    color: var(--ls-ink-soft);
  }

  .imagepicker__row {
    display: flex;
    align-items: center;
    gap: var(--ls-space);
  }

  .imagepicker__preview {
    flex-shrink: 0;
    display: flex;
    align-items: center;
    justify-content: center;
    width: 64px;
    height: 64px;
    overflow: hidden;
    border: 1px dashed var(--ls-rule-strong);
    border-radius: var(--ls-radius-sm);
    color: var(--ls-ink-faint);
  }

  .imagepicker__img {
    width: 100%;
    height: 100%;
    object-fit: cover;
    display: block;
  }

  .imagepicker__actions {
    display: flex;
    flex-wrap: wrap;
    gap: var(--ls-space-sm);
  }

  .imagepicker__input {
    display: none;
  }

  .imagepicker__hint {
    margin: 0;
    font-size: 0.75rem;
    color: var(--ls-ink-faint);
  }

  .imagepicker__error {
    margin: 0;
    font-size: 0.75rem;
    color: var(--ls-alert);
  }
</style>
