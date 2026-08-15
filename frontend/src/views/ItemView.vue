<template>
  <div class="itempage">
    <div class="ls-paper ls-paper--torn itempage__sheet">
      <header class="itempage__head">
        <h1 class="ls-hand ls-hand--title itempage__title">Items</h1>
        <p class="itempage__count">{{ countLabel }}</p>

        <v-btn
          color="primary"
          variant="flat"
          prepend-icon="mdi-plus"
          class="itempage__add"
          @click="openAdd"
        >
          Add item
        </v-btn>
      </header>

      <div v-if="isLoading" class="itempage__body">
        <v-skeleton-loader
          type="list-item-two-line, list-item-two-line, list-item-two-line"
        />
      </div>

      <div v-else class="itempage__body ls-sheet-margin">
        <p v-if="!hasItems" class="itempage__empty">
          Nothing in the catalog yet. Items you add to a shopping list end up
          here.
        </p>

        <ul v-else class="ls-rows">
          <ItemCard
            v-for="item in pageItems"
            :key="item.id"
            :item="item"
            @edit="openEdit"
            @remove="openDelete"
          />
        </ul>
      </div>
    </div>

    <v-pagination
      v-if="!isLoading && totalPages > 1"
      v-model="currentPage"
      :length="totalPages"
      density="comfortable"
      class="itempage__pages"
      @update:model-value="handlePageChange"
    />

    <!-- Single instances, outside every v-for. -->
    <ItemForm
      v-model="itemFormDialog"
      @add-item="createItem"
      @edit-item="updateItem"
      @update-dialog="updateDialog"
      :isEdit="isEdit"
      :passedFormData="passedFormData"
      :key="`${isEdit}-${passedFormData.id}`"
    />

    <ConfirmDialog
      v-model="deleteDialog"
      title="Delete item?"
      confirm-label="Delete"
      icon="mdi-delete-outline"
      @confirm="confirmDelete"
    >
      "{{ selectedItem?.name }}" will be removed from the catalog. Shopping
      lists that use it lose the entry too.
    </ConfirmDialog>
  </div>
</template>

<script setup>
  import { computed, ref } from "vue";
  import ItemCard from "@/components/ItemCard.vue";
  import ItemForm from "@/components/ItemForm.vue";
  import { useItems } from "@/composables/itemsComposable";
  import { useItemStore } from "@/stores/item";
  import ConfirmDialog from "@/components/ConfirmDialog.vue";
  const itemstore = useItemStore();

  const { items, isLoading, addItem, editItem, removeItem } = useItems(false);

  const itemFormDialog = ref(false);
  const deleteDialog = ref(false);
  const isEdit = ref(false);
  const selectedItem = ref(null);
  const currentPage = ref(itemstore.pageinfo.page ?? 1);

  const passedFormData = ref({
    id: null,
    name: null,
    matches: null,
  });

  const pageItems = computed(() => items.value?.items ?? []);
  const totalPages = computed(() => items.value?.total_pages ?? 0);
  const totalRecords = computed(() => items.value?.total_records ?? 0);
  const hasItems = computed(() => pageItems.value.length > 0);

  const countLabel = computed(() => {
    const total = totalRecords.value;
    if (total === 0) return "Nothing here yet";
    const noun = total === 1 ? "item" : "items";
    if (totalPages.value > 1) {
      return `${total} ${noun} · page ${currentPage.value} of ${totalPages.value}`;
    }
    return `${total} ${noun}`;
  });

  const openAdd = () => {
    isEdit.value = false;
    selectedItem.value = null;
    passedFormData.value = { id: null, name: null, matches: null };
    itemFormDialog.value = true;
  };

  const openEdit = item => {
    isEdit.value = true;
    selectedItem.value = item;
    passedFormData.value = {
      id: item.id,
      name: item.name,
      matches: item.matches,
    };
    itemFormDialog.value = true;
  };

  const openDelete = item => {
    selectedItem.value = item;
    deleteDialog.value = true;
  };

  const confirmDelete = async () => {
    if (selectedItem.value) await removeItem(selectedItem.value);
    deleteDialog.value = false;
  };

  const createItem = async newItem => {
    await addItem(newItem);
  };

  const updateItem = async updatedItem => {
    await editItem(updatedItem);
  };

  const updateDialog = () => {
    itemFormDialog.value = false;
  };

  const handlePageChange = page => {
    itemstore.pageinfo.page = page;
  };
</script>

<style scoped>
  .itempage {
    padding: var(--ls-space-sm) var(--ls-space) var(--ls-space-lg);
    max-width: 720px;
    margin: 0 auto;
  }

  /* Padding longhand: the shorthand would clobber the room .ls-paper--torn
   reserves for the tear. */
  .itempage__sheet {
    padding-top: var(--ls-space);
    padding-right: var(--ls-space);
    padding-left: var(--ls-space);
  }

  .itempage__head {
    display: flex;
    flex-wrap: wrap;
    align-items: baseline;
    gap: var(--ls-space-sm) var(--ls-space);
    padding-bottom: var(--ls-space);
    border-bottom: 1px solid var(--ls-rule-strong);
  }

  .itempage__title {
    margin: 0;
  }

  .itempage__count {
    flex: 1;
    margin: 0;
    font-size: 0.8125rem;
    color: var(--ls-ink-soft);
  }

  .itempage__body {
    padding-top: var(--ls-space);
  }

  .itempage__empty {
    margin: 0;
    padding: var(--ls-space) 0;
    color: var(--ls-ink-faint);
    font-style: italic;
  }

  .itempage__pages {
    margin-top: var(--ls-space);
  }

  @media (max-width: 599px) {
    .itempage {
      padding-left: var(--ls-space-sm);
      padding-right: var(--ls-space-sm);
    }

    .itempage__add {
      width: 100%;
    }
  }
</style>
