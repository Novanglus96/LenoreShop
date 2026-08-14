<template>
  <div class="aislepage">
    <div class="ls-paper ls-paper--torn aislepage__sheet">
      <header class="aislepage__head">
        <span v-if="storeName" class="ls-tab">
          <v-icon icon="mdi-storefront-outline" size="14" />
          <span class="ls-tab__text">{{ storeName }}</span>
        </span>

        <h1 class="ls-hand ls-hand--title aislepage__title">Aisles</h1>
        <p class="aislepage__hint">
          Drag to match the order you actually walk the store — shopping lists
          are grouped this way.
        </p>

        <v-btn
          color="primary"
          variant="flat"
          prepend-icon="mdi-plus"
          class="aislepage__add"
          @click="openAdd"
        >
          Add aisle
        </v-btn>
      </header>

      <div v-if="isLoading" class="aislepage__body">
        <v-skeleton-loader
          type="list-item, list-item, list-item, list-item"
        />
      </div>

      <div v-else class="aislepage__body ls-sheet-margin">
        <p v-if="!hasAisles" class="aislepage__empty">
          No aisles yet. Add the sections of this store so lists can be sorted
          by them.
        </p>

        <template v-else>
          <draggable
            v-model="sortableAisles"
            item-key="id"
            handle=".drag-handle"
            tag="ul"
            class="ls-rows"
            ghost-class="aislepage__ghost"
            @end="onReorder"
          >
            <template #item="{ element }">
              <AisleCard
                :aisle="element"
                @edit="openEdit"
                @remove="openDelete"
              />
            </template>
          </draggable>

          <!-- Outside the draggable: its position is fixed, so it must not be a
               drop target either. -->
          <ul v-if="uncategorizedAisle" class="ls-rows aislepage__catchall">
            <AisleCard
              :aisle="uncategorizedAisle"
              :key="uncategorizedAisle.id"
            />
          </ul>
        </template>
      </div>
    </div>

    <!-- Single instances, outside every v-for. -->
    <AisleForm
      v-model="aisleFormDialog"
      @add-aisle="createAisle"
      @edit-aisle="updateAisle"
      @update-dialog="updateDialog"
      :isEdit="isEdit"
      :passedFormData="passedFormData"
      :key="`${isEdit}-${passedFormData.id}`"
    />

    <v-dialog v-model="deleteDialog" max-width="400">
      <v-card>
        <v-card-title>Delete aisle?</v-card-title>
        <v-card-text>
          "{{ selectedAisle?.name }}" will be removed from this store. Items
          filed under it fall back to Uncategorized.
        </v-card-text>
        <v-card-actions>
          <v-spacer />
          <v-btn variant="text" @click="deleteDialog = false">Cancel</v-btn>
          <v-btn color="error" variant="text" @click="confirmDelete">
            Delete
          </v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>
  </div>
</template>

<script setup>
import { computed, ref, watch } from "vue";
import draggable from "vuedraggable";
import AisleCard from "@/components/AisleCard.vue";
import AisleForm from "@/components/AisleForm.vue";
import { useAisles } from "@/composables/aislesComposable";
import { useMainStore } from "@/stores/main";

const store = useMainStore();

const { aisles, isLoading, addAisle, editAisle, removeAisle, reorderAisles } =
  useAisles(store.store_id);

const aisleFormDialog = ref(false);
const deleteDialog = ref(false);
const isEdit = ref(false);
const selectedAisle = ref(null);
const sortableAisles = ref([]);

const passedFormData = ref({
  id: null,
  name: null,
  store_id: store.store_id,
  order: 1,
});

// order === 0 marks the catch-all aisle, which always sorts last and cannot be
// renamed, moved or deleted.
const uncategorizedAisle = computed(
  () => aisles.value?.find(a => a.order === 0) ?? null,
);

const hasAisles = computed(() => (aisles.value?.length ?? 0) > 0);

const storeName = computed(() => aisles.value?.[0]?.store?.name ?? "");

watch(
  aisles,
  val => {
    sortableAisles.value = (val ?? []).filter(a => a.order !== 0);
  },
  { immediate: true },
);

const onReorder = () => {
  const updated = sortableAisles.value.map((aisle, index) => ({
    ...aisle,
    order: index + 1,
  }));
  reorderAisles(updated);
};

const openAdd = () => {
  isEdit.value = false;
  selectedAisle.value = null;
  passedFormData.value = {
    id: null,
    name: null,
    store_id: store.store_id,
    // New aisles land after everything that already has a position.
    order: sortableAisles.value.length + 1,
  };
  aisleFormDialog.value = true;
};

const openEdit = aisle => {
  isEdit.value = true;
  selectedAisle.value = aisle;
  passedFormData.value = {
    id: aisle.id,
    name: aisle.name,
    store_id: aisle.store_id,
    order: aisle.order,
  };
  aisleFormDialog.value = true;
};

const openDelete = aisle => {
  selectedAisle.value = aisle;
  deleteDialog.value = true;
};

const confirmDelete = async () => {
  if (selectedAisle.value) await removeAisle(selectedAisle.value);
  deleteDialog.value = false;
};

const createAisle = async newAisle => {
  await addAisle(newAisle);
};

const updateAisle = async updatedAisle => {
  await editAisle(updatedAisle);
};

const updateDialog = () => {
  aisleFormDialog.value = false;
};
</script>

<style scoped>
.aislepage {
  padding: var(--ls-space-sm) var(--ls-space) var(--ls-space-lg);
  max-width: 720px;
  margin: 0 auto;
}

/* Padding longhand: the shorthand would clobber the room .ls-paper--torn
   reserves for the tear. */
.aislepage__sheet {
  padding-top: var(--ls-space);
  padding-right: var(--ls-space);
  padding-left: var(--ls-space);
}

.aislepage__head {
  display: flex;
  flex-direction: column;
  align-items: flex-start;
  gap: var(--ls-space-sm);
  padding-bottom: var(--ls-space);
  border-bottom: 1px solid var(--ls-rule-strong);
}

.aislepage__title {
  margin: 0;
}

.aislepage__hint {
  margin: 0;
  font-size: 0.8125rem;
  line-height: 1.45;
  color: var(--ls-ink-soft);
}

.aislepage__add {
  align-self: stretch;
}

.aislepage__body {
  padding-top: var(--ls-space);
}

.aislepage__empty {
  margin: 0;
  padding: var(--ls-space) 0;
  color: var(--ls-ink-faint);
  font-style: italic;
}

/* .ls-row drops its border on the last row of a group, so the draggable list
   ends flush against this one; put the separator back. */
.aislepage__catchall {
  border-top: 1px solid var(--ls-rule);
}

/* The gap the dragged row will drop into. */
.aislepage__ghost {
  opacity: 0.4;
  background: var(--ls-powder-soft);
}

@media (min-width: 600px) {
  .aislepage__add {
    align-self: flex-start;
  }
}
</style>
