<template>
  <div class="storepage">
    <div class="ls-paper ls-paper--torn storepage__sheet">
      <header class="storepage__head">
        <h1 class="ls-hand ls-hand--title storepage__title">Stores</h1>
        <p class="storepage__hint">
          Each store keeps its own aisles and shopping lists.
        </p>

        <v-btn
          color="primary"
          variant="flat"
          prepend-icon="mdi-plus"
          class="storepage__add"
          @click="openAdd"
        >
          Add store
        </v-btn>
      </header>

      <div v-if="isLoading" class="storepage__body">
        <v-skeleton-loader type="list-item, list-item, list-item" />
      </div>

      <div v-else class="storepage__body ls-sheet-margin">
        <p v-if="!hasStores" class="storepage__empty">
          No stores yet. Add one to start building lists.
        </p>

        <ul v-else class="ls-rows">
          <StoreCard
            v-for="store in stores"
            :key="store.id"
            :store="store"
            @edit="openEdit"
            @remove="openDelete"
          />
        </ul>
      </div>
    </div>

    <!-- Single instances, outside every v-for. -->
    <StoreForm
      v-model="storeFormDialog"
      @add-store="createStore"
      @edit-store="updateStore"
      @update-dialog="updateDialog"
      :isEdit="isEdit"
      :passedFormData="passedFormData"
      :key="`${isEdit}-${passedFormData.id}`"
    />

    <v-dialog v-model="deleteDialog" max-width="400">
      <v-card>
        <v-card-title>Delete store?</v-card-title>
        <v-card-text>
          "{{ selectedStore?.name }}" will be removed, along with its aisles and
          every shopping list belonging to it.
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
import { computed, ref } from "vue";
import StoreCard from "@/components/StoreCard.vue";
import StoreForm from "@/components/StoreForm.vue";
import { useStores } from "@/composables/storesComposable";

const { stores, isLoading, addStore, editStore, removeStore } = useStores();

const storeFormDialog = ref(false);
const deleteDialog = ref(false);
const isEdit = ref(false);
const selectedStore = ref(null);

const passedFormData = ref({
  id: null,
  name: null,
});

const hasStores = computed(() => (stores.value?.length ?? 0) > 0);

const openAdd = () => {
  isEdit.value = false;
  selectedStore.value = null;
  passedFormData.value = { id: null, name: null };
  storeFormDialog.value = true;
};

const openEdit = store => {
  isEdit.value = true;
  selectedStore.value = store;
  passedFormData.value = { id: store.id, name: store.name };
  storeFormDialog.value = true;
};

const openDelete = store => {
  selectedStore.value = store;
  deleteDialog.value = true;
};

const confirmDelete = async () => {
  if (selectedStore.value) await removeStore(selectedStore.value);
  deleteDialog.value = false;
};

const createStore = async newStore => {
  await addStore(newStore);
};

const updateStore = async updatedStore => {
  await editStore(updatedStore);
};

const updateDialog = () => {
  storeFormDialog.value = false;
};
</script>

<style scoped>
.storepage {
  padding: var(--ls-space-sm) var(--ls-space) var(--ls-space-lg);
  max-width: 720px;
  margin: 0 auto;
}

/* Padding longhand: the shorthand would clobber the room .ls-paper--torn
   reserves for the tear. */
.storepage__sheet {
  padding-top: var(--ls-space);
  padding-right: var(--ls-space);
  padding-left: var(--ls-space);
}

.storepage__head {
  display: flex;
  flex-direction: column;
  align-items: flex-start;
  gap: var(--ls-space-sm);
  padding-bottom: var(--ls-space);
  border-bottom: 1px solid var(--ls-rule-strong);
}

.storepage__title {
  margin: 0;
}

.storepage__hint {
  margin: 0;
  font-size: 0.8125rem;
  line-height: 1.45;
  color: var(--ls-ink-soft);
}

.storepage__add {
  align-self: stretch;
}

.storepage__body {
  padding-top: var(--ls-space);
}

.storepage__empty {
  margin: 0;
  padding: var(--ls-space) 0;
  color: var(--ls-ink-faint);
  font-style: italic;
}

@media (min-width: 600px) {
  .storepage__add {
    align-self: flex-start;
  }
}

@media (max-width: 599px) {
  .storepage {
    padding-left: var(--ls-space-sm);
    padding-right: var(--ls-space-sm);
  }
}
</style>
