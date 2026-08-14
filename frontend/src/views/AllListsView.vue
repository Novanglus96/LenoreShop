<template>
  <div class="alllists">
    <header class="alllists__header">
      <div>
        <h1 class="ls-hand ls-hand--title">All Lists</h1>
        <p v-if="hasLists" class="alllists__count">
          {{ shoppinglists.length }}
          {{ shoppinglists.length === 1 ? "list" : "lists" }}
        </p>
      </div>
      <v-btn
        to="/lists"
        color="primary"
        variant="tonal"
        prepend-icon="mdi-playlist-edit"
        class="alllists__manage"
      >
        Manage lists
      </v-btn>
    </header>

    <div v-if="isLoading" class="alllists__grid">
      <div
        v-for="placeholder in 6"
        :key="placeholder"
        class="ls-paper ls-paper--torn alllists__skeleton"
      >
        <v-skeleton-loader type="list-item-two-line, list-item-two-line" />
      </div>
    </div>

    <div v-else-if="!hasLists" class="alllists__empty">
      <v-icon icon="mdi-clipboard-text-outline" size="44" color="primary" />
      <p class="alllists__empty-text">No shopping lists yet.</p>
      <v-btn to="/lists" color="primary" variant="flat" prepend-icon="mdi-plus">
        Create a list
      </v-btn>
    </div>

    <!-- Same ranking as the dashboard, so a list does not move when you follow
         "See all" — this page just stops capping it. -->
    <div v-else class="alllists__grid">
      <ListNotepadCard
        v-for="(list, index) in rankedLists"
        :key="list.id"
        :list="list"
        :style="{ '--notepad-tilt': tiltFor(index) }"
        @open="openList"
      />
    </div>
  </div>
</template>

<script setup>
import { computed } from "vue";
import { useRouter } from "vue-router";
import { useMainStore } from "@/stores/main";
import { useShoppingLists } from "@/composables/listsComposable";
import { rankShoppingLists } from "@/utils/listRanking";
import { tiltFor } from "@/utils/paperTilt";
import ListNotepadCard from "@/components/ListNotepadCard.vue";

const { shoppinglists, isLoading } = useShoppingLists();
const router = useRouter();

const hasLists = computed(() => shoppinglists.value?.length > 0);

const rankedLists = computed(() => rankShoppingLists(shoppinglists.value));

const openList = list => {
  const store = useMainStore();
  store.list_id = list.id;
  store.store_id = list.store_id;
  router.push("/list");
};
</script>

<style scoped>
.alllists {
  padding: var(--ls-space-sm) var(--ls-space) var(--ls-space-lg);
  max-width: 1200px;
  margin: 0 auto;
}

.alllists__header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: var(--ls-space);
  flex-wrap: wrap;
  margin-bottom: var(--ls-space-md);
}

.alllists__header h1 {
  margin: 0;
}

.alllists__count {
  margin: 0;
  font-size: 0.875rem;
  color: var(--ls-ink-soft);
}

.alllists__grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(240px, 1fr));
  gap: var(--ls-space-md) var(--ls-space);
  align-items: stretch;
}

.alllists__skeleton {
  padding: var(--ls-space);
  opacity: 0.6;
}

.alllists__empty {
  display: flex;
  flex-direction: column;
  align-items: center;
  text-align: center;
  gap: var(--ls-space);
  padding: var(--ls-space-lg) var(--ls-space);
  max-width: 32rem;
  margin: 0 auto;
}

.alllists__empty-text {
  margin: 0;
  color: var(--ls-ink-soft);
  line-height: 1.6;
}

/* Phones: one sheet per row, tilt dropped so edges stay parallel at full width. */
@media (max-width: 599px) {
  .alllists {
    padding-left: var(--ls-space-sm);
    padding-right: var(--ls-space-sm);
  }

  .alllists__grid {
    grid-template-columns: 1fr;
    gap: var(--ls-space);
  }

  .alllists__grid :deep(.notepad) {
    --notepad-tilt: 0deg;
  }

  .alllists__manage {
    width: 100%;
  }
}
</style>
