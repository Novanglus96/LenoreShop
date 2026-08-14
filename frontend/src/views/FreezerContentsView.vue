<template>
  <div class="frzpage">
    <!-- Reached by picking a freezer, so landing here without one means the
         page has nothing to show. -->
    <div v-if="!store.freezer_id" class="ls-frost-sheet frzpage__sheet frzpage__sheet--plain">
      <p class="frzpage__empty">No freezer selected.</p>
      <v-btn to="/freezers" color="primary" variant="flat" prepend-icon="mdi-snowflake">
        Pick a freezer
      </v-btn>
    </div>

    <div v-else class="ls-frost-sheet ls-frost-sheet--iced frzpage__sheet">
      <span class="ls-magnet" aria-hidden="true" />

      <header class="frzpage__head">
        <h1 class="ls-hand ls-hand--title frzpage__name">
          {{ freezerfull?.name ?? "Freezer" }}
        </h1>
        <p v-if="freezerfull?.location" class="frzpage__location">
          {{ freezerfull.location }}
        </p>

        <div class="frzpage__status">
          <span class="frzpage__count">{{ countLabel }}</span>
          <span class="frzpage__pills">
            <span v-if="expiredCount > 0" class="ls-pill ls-pill--alert">
              {{ expiredCount }} expired
            </span>
            <span v-if="expiringCount > 0" class="ls-pill ls-pill--warn">
              {{ expiringCount }} soon
            </span>
            <span v-if="isAllGood" class="ls-pill ls-pill--calm">All good</span>
          </span>
        </div>

        <v-btn
          color="primary"
          variant="flat"
          prepend-icon="mdi-plus"
          class="frzpage__add"
          @click="freezerItemFormDialog = true"
        >
          Add food
        </v-btn>
      </header>

      <div v-if="isLoading" class="frzpage__body">
        <v-skeleton-loader
          type="list-item-two-line, list-item-two-line, list-item-two-line"
        />
      </div>

      <div v-else class="frzpage__body">
        <FreezerContents
          :freezeritems="freezerfull?.freezeritems ?? []"
          :freezers="freezers"
          @edit-freezer-item="updateFreezerItem"
          @delete-freezer-item="removeFood"
        />
      </div>
    </div>

    <!-- Single instance, outside any v-for. -->
    <FreezerItemForm
      v-model="freezerItemFormDialog"
      @add-freezer-item="createFreezerItem"
      @update-dialog="updateDialog"
      :isEdit="false"
      :freezers="freezers"
      :passedFormData="blankFormData"
      :key="-1"
    />
  </div>
</template>

<script setup>
import { computed, ref } from "vue";
import FreezerContents from "@/components/FreezerContents.vue";
import FreezerItemForm from "@/components/FreezerItemForm.vue";
import { useFreezerFull, useFreezers } from "@/composables/freezersComposable";
import { useMainStore } from "@/stores/main";

// Matches FREEZER_SOON_DAYS in backend/backend/api.py.
const SOON_DAYS = 14;

const store = useMainStore();
const freezerItemFormDialog = ref(false);

const { freezers } = useFreezers();
const {
  freezerfull,
  isLoading,
  addFreezerItem,
  editFreezerItem,
  removeFreezerItem,
} = useFreezerFull(store.freezer_id);

const contents = computed(() => freezerfull.value?.freezeritems ?? []);

const totalItems = computed(() => freezerfull.value?.totalitems ?? 0);

// FreezerFull carries totalexpired but not totalexpiring, so the near-date
// count is derived from the items already on the page rather than adding a
// field for one view.
const expiredCount = computed(() => freezerfull.value?.totalexpired ?? 0);

const expiringCount = computed(
  () =>
    contents.value.filter(
      item =>
        item.days_until_discard !== null &&
        item.days_until_discard !== undefined &&
        item.days_until_discard >= 0 &&
        item.days_until_discard <= SOON_DAYS,
    ).length,
);

const isAllGood = computed(
  () =>
    totalItems.value > 0 && expiredCount.value === 0 && expiringCount.value === 0,
);

const countLabel = computed(() => {
  const total = totalItems.value;
  if (total === 0) return "Empty";
  return `${total} ${total === 1 ? "item" : "items"}`;
});

// Prefilled with today because most food is logged as it goes in. Clearing
// the field is what records "date added unknown", which is the case when
// backfilling food that was already in the freezer.
const today = new Date().toLocaleDateString("en-CA");

const blankFormData = ref({
  id: 0,
  name: null,
  qty: 1,
  unit: null,
  date_added: today,
  discard_date: null,
  notes: null,
  freezer_id: store.freezer_id,
});

const createFreezerItem = async newFood => {
  await addFreezerItem(newFood);
};

const updateFreezerItem = async updatedFood => {
  await editFreezerItem(updatedFood);
};

const removeFood = async deletedFood => {
  await removeFreezerItem(deletedFood);
};

const updateDialog = () => {
  freezerItemFormDialog.value = false;
};
</script>

<style scoped>
.frzpage {
  padding: var(--ls-space-sm) var(--ls-space) var(--ls-space-lg);
  max-width: 720px;
  margin: 0 auto;
}

/* Padding longhand: the shorthand would clobber the room
   .ls-frost-sheet--iced reserves for the icicles. Extra top padding clears the
   magnet disc pinned at the top of the sheet. */
.frzpage__sheet {
  padding-top: var(--ls-space-md);
  padding-right: var(--ls-space);
  padding-left: var(--ls-space);
}

.frzpage__sheet--plain {
  display: flex;
  flex-direction: column;
  align-items: flex-start;
  gap: var(--ls-space);
  padding-bottom: var(--ls-space);
}

.frzpage__head {
  display: flex;
  flex-direction: column;
  align-items: flex-start;
  gap: var(--ls-space-sm);
  padding-bottom: var(--ls-space);
  border-bottom: 1px solid var(--ls-frost-rule);
}

.frzpage__name {
  margin: 0;
  color: var(--ls-frost-ink);
  overflow-wrap: anywhere;
}

.frzpage__location {
  margin: 0;
  font-size: 0.8125rem;
  color: var(--ls-frost-ink-soft);
}

.frzpage__status {
  display: flex;
  flex-wrap: wrap;
  align-items: center;
  gap: var(--ls-space-sm);
}

.frzpage__count {
  font-size: 0.75rem;
  font-weight: 600;
  letter-spacing: 0.02em;
  color: var(--ls-frost-ink-soft);
}

.frzpage__pills {
  display: flex;
  flex-wrap: wrap;
  gap: var(--ls-space-xs);
}

.frzpage__add {
  align-self: stretch;
}

.frzpage__body {
  padding-top: var(--ls-space);
}

.frzpage__empty {
  margin: 0;
  color: var(--ls-frost-ink-faint);
  font-style: italic;
}

@media (min-width: 600px) {
  .frzpage__add {
    align-self: flex-start;
  }
}

@media (max-width: 599px) {
  .frzpage {
    padding-left: var(--ls-space-sm);
    padding-right: var(--ls-space-sm);
  }
}
</style>
