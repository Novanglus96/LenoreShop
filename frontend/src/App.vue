<template>
  <v-app>
    <VueQueryDevtools />
    <AppNavigation />
    <v-main>
      <v-container fluid-class="pa-2">
        <router-view />
      </v-container>
      <v-snackbar
        v-model="store.snackbar"
        :color="store.snackbarColor"
        :timeout="store.snackbarTimeout"
        content-class="centered-text"
      >
        {{ store.snackbarText }}
      </v-snackbar>
      <v-snackbar
        v-model="showBanner"
        color="secondary"
        location="top"
        timeout="-1"
        :multi-line="true"
      >
        There's been an update to the application. Click refresh to get the new
        changes!
        <template v-slot:actions>
          <v-btn color="primary" variant="text" @click="showBanner = false">
            Close
          </v-btn>
          <v-btn color="primary" variant="text" @click="reloadPage"
            >Refresh</v-btn
          >
        </template>
      </v-snackbar>
    </v-main>
  </v-app>
</template>
<script setup>
import AppNavigation from "@/components/AppNavigation.vue";
import { useMainStore } from "@/stores/main";
import { onMounted, computed, ref, watch, onUnmounted } from "vue";
import { VueQueryDevtools } from "@tanstack/vue-query-devtools";
import { useVersion } from "@/composables/versionComposable";

const reloadPage = () => {
  window.location.reload();
};
const store = useMainStore();
const { prefetchVersion, version } = useVersion();
const showBanner = ref(false);

const checkVersion = computed(() => {
  return version.value && version.value.version_number !== "1.6.19";
});

const updateBanner = () => {
  showBanner.value = checkVersion.value;
};

onMounted(() => {
  prefetchVersion();

  // Check version initially
  updateBanner();

  const handleVisibilityChange = () => {
    if (!document.hidden) {
      prefetchVersion().then(() => {
        updateBanner();
      });
    }
  };

  document.addEventListener("visibilitychange", handleVisibilityChange);

  // Clean up the event listener when the component is unmounted
  onUnmounted(() => {
    document.removeEventListener("visibilitychange", handleVisibilityChange);
  });
});

// Watch for changes in the computed property
watch(checkVersion, newValue => {
  showBanner.value = newValue;
});
</script>
