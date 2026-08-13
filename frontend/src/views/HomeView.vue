<template>
  <div class="dashboard">
    <!-- First run: no stores exist yet. -->
    <div v-if="showEmptyState" class="dashboard__welcome">
      <v-icon icon="mdi-cart-outline" size="56" color="primary" />
      <h1 class="ls-hand ls-hand--title">Welcome to LenoreShop!</h1>
      <p class="dashboard__welcome-text">
        No stores have been set up yet.
        <router-link to="/stores" class="dashboard__link">
          Add your first store
        </router-link>
        to get started, or load demo data to explore the app.
      </p>
      <v-btn
        color="primary"
        variant="flat"
        prepend-icon="mdi-database-import"
        :loading="isDemoLoading"
        @click="confirmDemo = true"
      >
        Load Demo Data
      </v-btn>
    </div>

    <template v-else>
      <header class="dashboard__header">
        <h1 class="ls-hand ls-hand--title">Shopping Lists</h1>
        <v-btn
          to="/lists"
          color="primary"
          variant="tonal"
          prepend-icon="mdi-playlist-plus"
          class="dashboard__manage"
        >
          Manage lists
        </v-btn>
      </header>

      <!-- Loading: placeholder sheets keep the grid from collapsing. -->
      <div v-if="isLoadingLists" class="dashboard__grid">
        <div
          v-for="placeholder in 3"
          :key="placeholder"
          class="ls-paper ls-paper--torn dashboard__skeleton"
        >
          <v-skeleton-loader type="list-item-two-line, list-item-two-line" />
        </div>
      </div>

      <!-- Stores exist, but no lists on them yet. -->
      <div v-else-if="!hasLists" class="dashboard__nolists">
        <v-icon icon="mdi-clipboard-text-outline" size="44" color="primary" />
        <p class="dashboard__welcome-text">
          Your stores are set up — now make a shopping list to fill them.
        </p>
        <v-btn to="/lists" color="primary" variant="flat" prepend-icon="mdi-plus">
          Create a list
        </v-btn>
      </div>

      <div v-else class="dashboard__grid">
        <ListNotepadCard
          v-for="(list, index) in shoppinglists"
          :key="list.id"
          :list="list"
          :style="{ '--notepad-tilt': tiltFor(index) }"
          @open="openList"
        />
      </div>

      <!-- Freezers only appear once at least one exists; the section is not a
           prompt to set one up. -->
      <section v-if="hasFreezers" class="dashboard__freezers">
        <header class="dashboard__header">
          <h2 class="ls-hand ls-hand--title">In the Freezer</h2>
          <v-btn
            to="/freezers"
            color="primary"
            variant="tonal"
            prepend-icon="mdi-snowflake"
            class="dashboard__manage"
          >
            Manage freezers
          </v-btn>
        </header>

        <p v-if="freezerAlert" class="dashboard__alert">
          <v-icon icon="mdi-alert-circle-outline" size="18" />
          {{ freezerAlert }}
        </p>

        <div class="dashboard__grid">
          <FreezerFrostCard
            v-for="freezer in freezers"
            :key="freezer.id"
            :freezer="freezer"
            @open="openFreezer"
          />
        </div>
      </section>
    </template>

    <!-- Single instance, outside any v-for. -->
    <v-dialog v-model="confirmDemo" max-width="400">
      <v-card>
        <v-card-title>Load Demo Data?</v-card-title>
        <v-card-text>
          This will create two sample stores (Grocery Store and Hardware Store)
          with aisles, items, and starter shopping lists.
        </v-card-text>
        <v-card-actions>
          <v-spacer />
          <v-btn variant="text" @click="confirmDemo = false">Cancel</v-btn>
          <v-btn color="primary" variant="text" @click="onLoadDemo">Load</v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>
  </div>
</template>

<script setup>
import { computed, ref } from "vue";
import { useRouter } from "vue-router";
import { useMainStore } from "@/stores/main";
import { useShoppingLists } from "@/composables/listsComposable";
import { useStores } from "@/composables/storesComposable";
import { useFreezers } from "@/composables/freezersComposable";
import { useDemo } from "@/composables/demoComposable";
import ListNotepadCard from "@/components/ListNotepadCard.vue";
import FreezerFrostCard from "@/components/FreezerFrostCard.vue";

const { shoppinglists, isLoading: isLoadingLists } = useShoppingLists();
const { stores, isLoading: isLoadingStores } = useStores();
const { freezers } = useFreezers();
const { loadDemo, isDemoLoading } = useDemo();

const router = useRouter();
const confirmDemo = ref(false);

const showEmptyState = computed(
  () => !isLoadingStores.value && stores.value && stores.value.length === 0,
);

const hasLists = computed(() => shoppinglists.value?.length > 0);

const hasFreezers = computed(() => freezers.value?.length > 0);

// One line summarising everything that needs attention, so a freezer problem is
// visible without reading each card. Expired outranks expiring — food already
// past its date is the thing to act on first.
const freezerAlert = computed(() => {
  if (!freezers.value) return "";
  const expired = freezers.value.reduce((sum, f) => sum + f.totalexpired, 0);
  const expiring = freezers.value.reduce((sum, f) => sum + f.totalexpiring, 0);
  const parts = [];
  if (expired > 0) {
    parts.push(`${expired} item${expired === 1 ? "" : "s"} past its discard date`);
  }
  if (expiring > 0) {
    parts.push(`${expiring} to use up soon`);
  }
  return parts.join(" · ");
});

// A repeating set of small angles, so the sheets look dropped on the page
// rather than laid out on a grid. Deterministic, so cards don't jump on
// re-render the way a random tilt would.
const TILTS = ["-0.7deg", "0.5deg", "-0.3deg", "0.8deg", "-0.5deg"];
const tiltFor = index => TILTS[index % TILTS.length];

const onLoadDemo = () => {
  confirmDemo.value = false;
  loadDemo();
};

const openList = list => {
  const store = useMainStore();
  store.list_id = list.id;
  store.store_id = list.store_id;
  router.push("/list");
};

const openFreezer = freezer => {
  const store = useMainStore();
  store.freezer_id = freezer.id;
  router.push("/freezer");
};
</script>

<style scoped>
.dashboard {
  padding: var(--ls-space-sm) var(--ls-space) var(--ls-space-lg);
  max-width: 1200px;
  margin: 0 auto;
}

.dashboard__header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: var(--ls-space);
  flex-wrap: wrap;
  margin-bottom: var(--ls-space-md);
}

.dashboard__header h1 {
  margin: 0;
}

/* auto-fill rather than auto-fit: a single list keeps its card width instead of
   stretching across the whole desktop viewport. */
.dashboard__grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(240px, 1fr));
  gap: var(--ls-space-md) var(--ls-space);
  align-items: stretch;
}

.dashboard__skeleton {
  padding: var(--ls-space);
  opacity: 0.6;
}

/* Separated from the lists above by space and a rule rather than a box, so the
   two sections read as one page instead of two panels. */
.dashboard__freezers {
  margin-top: var(--ls-space-lg);
  padding-top: var(--ls-space-md);
  border-top: 1px solid var(--ls-rule);
}

.dashboard__alert {
  display: flex;
  align-items: center;
  gap: 6px;
  margin: 0 0 var(--ls-space);
  font-size: 0.875rem;
  font-weight: 500;
  color: var(--ls-alert);
}

.dashboard__welcome,
.dashboard__nolists {
  display: flex;
  flex-direction: column;
  align-items: center;
  text-align: center;
  gap: var(--ls-space);
  padding: var(--ls-space-lg) var(--ls-space);
  max-width: 32rem;
  margin: 0 auto;
}

.dashboard__welcome h1 {
  margin: 0;
}

.dashboard__welcome-text {
  margin: 0;
  color: var(--ls-ink-soft);
  line-height: 1.6;
}

.dashboard__link {
  color: var(--ls-navy);
  font-weight: 600;
}

/* Phones: one sheet per row, and drop the tilt so edges stay parallel to the
   screen at full width. */
@media (max-width: 599px) {
  .dashboard {
    padding-left: var(--ls-space-sm);
    padding-right: var(--ls-space-sm);
  }

  .dashboard__grid {
    grid-template-columns: 1fr;
    gap: var(--ls-space);
  }

  .dashboard__grid :deep(.notepad) {
    --notepad-tilt: 0deg;
  }

  .dashboard__manage {
    width: 100%;
  }
}
</style>
