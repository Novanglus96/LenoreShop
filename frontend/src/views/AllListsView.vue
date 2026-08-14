<template>
  <div class="alllists">
    <header class="alllists__header">
      <div>
        <h1 class="ls-hand ls-hand--title">Shopping Lists</h1>
        <p v-if="hasLists" class="alllists__count">
          {{ shoppinglists.length }}
          {{ shoppinglists.length === 1 ? "list" : "lists" }}
        </p>
      </div>
      <v-btn
        color="primary"
        variant="flat"
        prepend-icon="mdi-plus"
        class="alllists__add"
        @click="openAdd"
      >
        Add list
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
      <p class="alllists__empty-text">
        No shopping lists yet. Make one and it'll show up here and on the
        dashboard.
      </p>
      <v-btn
        color="primary"
        variant="flat"
        prepend-icon="mdi-plus"
        @click="openAdd"
      >
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
        manageable
        :style="{ '--notepad-tilt': tiltFor(index) }"
        @open="openList"
        @edit="openEdit"
        @remove="openDelete"
      />
    </div>

    <!-- Single instances, outside every v-for. -->
    <ListForm
      v-model="listFormDialog"
      @add-list="createList"
      @edit-list="updateList"
      @update-dialog="updateDialog"
      :isEdit="isEdit"
      :passedFormData="passedFormData"
      :key="`${isEdit}-${passedFormData.id}`"
    />

    <ConfirmDialog
      v-model="deleteDialog"
      title="Delete list?"
      confirm-label="Delete"
      icon="mdi-delete-outline"
      @confirm="confirmDelete"
    >
      "{{ selectedList?.name }}" and everything on it will be removed. The store
      and its aisles stay.
    </ConfirmDialog>
  </div>
</template>

<script setup>
  import { computed, ref } from "vue";
  import { useRouter } from "vue-router";
  import { useMainStore } from "@/stores/main";
  import { useShoppingLists } from "@/composables/listsComposable";
  import { rankShoppingLists } from "@/utils/listRanking";
  import { tiltFor } from "@/utils/paperTilt";
  import ListNotepadCard from "@/components/ListNotepadCard.vue";
  import ListForm from "@/components/ListForm.vue";
  import ConfirmDialog from "@/components/ConfirmDialog.vue";
  const { shoppinglists, isLoading, addShoppingList, editList, removeList } =
    useShoppingLists();
  const router = useRouter();

  const listFormDialog = ref(false);
  const deleteDialog = ref(false);
  const isEdit = ref(false);
  const selectedList = ref(null);

  const passedFormData = ref({
    id: null,
    name: null,
    store_id: null,
  });

  const hasLists = computed(() => shoppinglists.value?.length > 0);

  const rankedLists = computed(() => rankShoppingLists(shoppinglists.value));

  const openList = list => {
    const store = useMainStore();
    store.list_id = list.id;
    store.store_id = list.store_id;
    router.push("/list");
  };

  const openAdd = () => {
    isEdit.value = false;
    selectedList.value = null;
    passedFormData.value = { id: null, name: null, store_id: null };
    listFormDialog.value = true;
  };

  const openEdit = list => {
    isEdit.value = true;
    selectedList.value = list;
    passedFormData.value = {
      id: list.id,
      name: list.name,
      store_id: list.store_id,
    };
    listFormDialog.value = true;
  };

  const openDelete = list => {
    selectedList.value = list;
    deleteDialog.value = true;
  };

  const confirmDelete = async () => {
    if (selectedList.value) await removeList(selectedList.value);
    deleteDialog.value = false;
  };

  const createList = async newList => {
    await addShoppingList(newList);
  };

  const updateList = async updatedList => {
    await editList(updatedList);
  };

  const updateDialog = () => {
    listFormDialog.value = false;
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

    .alllists__add {
      width: 100%;
    }
  }
</style>
