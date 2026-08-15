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
      <!-- Freezer trouble is surfaced at the top of the page, because the
           freezer section itself sits below however many list cards there are
           and would otherwise be off-screen exactly when it matters. A real
           button, not a styled <p>: it scrolls down to the cards it is talking
           about, so it names a problem and then takes you to it. -->
      <button
        v-if="freezerAlert"
        type="button"
        :class="['dashboard__alert', `dashboard__alert--${freezerAlertLevel}`]"
        @click="scrollToFreezers"
      >
        <v-icon icon="mdi-alert-circle-outline" size="18" />
        <span class="dashboard__alert-text">{{ freezerAlert }}</span>
        <span class="dashboard__alert-cta">
          In the Freezer
          <v-icon icon="mdi-arrow-down" size="16" />
        </span>
      </button>

      <header class="dashboard__header">
        <h1 class="ls-hand ls-hand--title">Shopping Lists</h1>
        <v-btn
          to="/alllists"
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
        <v-btn
          to="/alllists"
          color="primary"
          variant="flat"
          prepend-icon="mdi-plus"
        >
          Create a list
        </v-btn>
      </div>

      <div v-else class="dashboard__grid">
        <ListNotepadCard
          v-for="(list, index) in visibleLists"
          :key="list.id"
          :list="list"
          :style="{ '--notepad-tilt': tiltFor(index) }"
          @open="openList"
        />
      </div>

      <!-- The dashboard stays a summary: it shows the lists most worth acting
           on and hands off the full set to /alllists, so the page height is
           bounded however many lists exist. -->
      <div v-if="hiddenListCount > 0" class="dashboard__seeall">
        <v-btn
          to="/alllists"
          variant="text"
          color="primary"
          append-icon="mdi-arrow-right"
        >
          See all {{ shoppinglists.length }} lists
        </v-btn>
      </div>

      <!-- Freezers only appear once at least one exists; the section is not a
           prompt to set one up. -->
      <section
        v-if="hasFreezers"
        ref="freezerSection"
        tabindex="-1"
        class="dashboard__freezers"
      >
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

    <!-- Single instance, outside any v-for. Not destructive, so it takes the
         normal tone rather than the red one the delete confirmations use. -->
    <ConfirmDialog
      v-model="confirmDemo"
      title="Load demo data?"
      confirm-label="Load"
      tone="normal"
      icon="mdi-database-import-outline"
      @confirm="onLoadDemo"
    >
      This will create two sample stores (Grocery Store and Hardware Store) with
      aisles, items, and starter shopping lists.
    </ConfirmDialog>
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
  import { rankShoppingLists } from "@/utils/listRanking";
  import { tiltFor } from "@/utils/paperTilt";
  import ListNotepadCard from "@/components/ListNotepadCard.vue";
  import FreezerFrostCard from "@/components/FreezerFrostCard.vue";
  import ConfirmDialog from "@/components/ConfirmDialog.vue";

  // How many list cards the dashboard shows before handing off to /alllists.
  // Roughly two rows on a laptop, so the freezer section stays reachable.
  const DASHBOARD_LIST_LIMIT = 6;

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

  // In-progress lists first, then untouched, with finished and empty last — the
  // cap below means the top few slots should go to whatever is still worth
  // opening. See utils/listRanking.js.
  const rankedLists = computed(() => rankShoppingLists(shoppinglists.value));

  const visibleLists = computed(() =>
    rankedLists.value.slice(0, DASHBOARD_LIST_LIMIT),
  );

  const hiddenListCount = computed(
    () => rankedLists.value.length - visibleLists.value.length,
  );

  const freezerCounts = computed(() => {
    const all = freezers.value ?? [];
    return {
      expired: all.reduce((sum, f) => sum + (f.totalexpired ?? 0), 0),
      expiring: all.reduce((sum, f) => sum + (f.totalexpiring ?? 0), 0),
    };
  });

  // One line summarising everything that needs attention, so a freezer problem is
  // visible without reading each card. Expired outranks expiring — food already
  // past its date is the thing to act on first.
  const freezerAlert = computed(() => {
    const { expired, expiring } = freezerCounts.value;
    const parts = [];
    if (expired > 0) {
      const noun = expired === 1 ? "item is" : "items are";
      parts.push(`${expired} ${noun} past the discard date`);
    }
    if (expiring > 0) {
      parts.push(`${expiring} to use up soon`);
    }
    return parts.join(" · ");
  });

  // Something already spoiled is a stronger signal than something approaching its
  // date, and the strip is coloured to match.
  const freezerAlertLevel = computed(() =>
    freezerCounts.value.expired > 0 ? "alert" : "warn",
  );

  const freezerSection = ref(null);

  const scrollToFreezers = () => {
    const section = freezerSection.value;
    if (!section) return;

    // The design layer zeroes --ls-duration under prefers-reduced-motion; the
    // same preference has to be honoured here, where the motion comes from the
    // scroll API rather than a transition.
    const reduceMotion = window.matchMedia(
      "(prefers-reduced-motion: reduce)",
    ).matches;
    section.scrollIntoView({
      behavior: reduceMotion ? "auto" : "smooth",
      block: "start",
    });
    // Keyboard and screen-reader users should end up where the page just went,
    // not left at the top with the focus ring on the strip.
    section.focus({ preventScroll: true });
  };

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

  .dashboard__seeall {
    display: flex;
    justify-content: center;
    margin: var(--ls-space) 0 0;
  }

  /* Separated from the lists above by space and a rule rather than a box, so the
   two sections read as one page instead of two panels. */
  .dashboard__freezers {
    margin-top: var(--ls-space-lg);
    padding-top: var(--ls-space-md);
    border-top: 1px solid var(--ls-rule);
    /* The app bar is `app`-positioned and overlays content, so scrolling this
     section to the top of the viewport would tuck its heading underneath it.
     Vuetify publishes the bar's height as --v-layout-top on the layout root. */
    scroll-margin-top: calc(var(--v-layout-top, 64px) + var(--ls-space));
  }

  /* Focused only programmatically, to move the caret after the scroll — the ring
   would otherwise appear around the whole section. */
  .dashboard__freezers:focus {
    outline: none;
  }

  .dashboard__alert {
    display: flex;
    align-items: center;
    gap: var(--ls-space-sm);
    width: 100%;
    margin-bottom: var(--ls-space);
    padding: var(--ls-space-sm) var(--ls-space);
    border: 1px solid currentcolor;
    border-radius: var(--ls-radius);
    /* A <button> does not inherit type styling the way the surrounding text does. */
    font-family: var(--ls-font-body);
    font-size: 0.875rem;
    font-weight: 500;
    text-align: left;
    cursor: pointer;
    transition:
      box-shadow var(--ls-duration) var(--ls-ease),
      transform var(--ls-duration) var(--ls-ease);
  }

  .dashboard__alert--alert {
    background: var(--ls-alert-bg);
    color: var(--ls-alert);
  }

  .dashboard__alert--warn {
    background: var(--ls-warn-bg);
    color: var(--ls-warn);
  }

  @media (hover: hover) {
    .dashboard__alert:hover {
      box-shadow: var(--ls-elev-1);
      transform: translateY(-1px);
    }
  }

  .dashboard__alert-text {
    flex: 1;
  }

  .dashboard__alert-cta {
    display: inline-flex;
    align-items: center;
    gap: 2px;
    flex-shrink: 0;
    font-size: 0.8125rem;
    font-weight: 600;
    text-decoration: underline;
    text-underline-offset: 2px;
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

    /* Not enough width for the alert text and a labelled call to action side by
     side. The whole strip is the button, so the arrow alone carries it. */
    .dashboard__alert-cta {
      font-size: 0;
      gap: 0;
    }
  }
</style>
