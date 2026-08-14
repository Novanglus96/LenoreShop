<template>
  <div class="listpage">
    <div class="ls-paper ls-paper--torn listpage__sheet">
      <header class="listpage__head">
        <span class="ls-tab">
          <v-icon icon="mdi-storefront-outline" size="14" />
          <span class="ls-tab__text">
            {{ fullshoppinglist?.store?.name ?? "—" }}
          </span>
        </span>

        <h1 class="ls-hand ls-hand--title listpage__name">
          {{ fullshoppinglist?.name ?? "Shopping List" }}
        </h1>

        <div class="listpage__progress">
          <span class="listpage__count">{{ countLabel }}</span>
          <span class="ls-progress listpage__bar">
            <span
              :class="[
                'ls-progress__fill',
                { 'ls-progress__fill--done': isComplete },
              ]"
              :style="{ width: percentComplete + '%' }"
            />
          </span>
        </div>

        <div class="listpage__actions">
          <v-btn
            color="primary"
            variant="flat"
            prepend-icon="mdi-plus"
            :disabled="isOffline"
            @click="listItemFormDialog = true"
          >
            Add item
          </v-btn>

          <!-- Clearing is rare and destructive, so it lives a level down rather
               than sitting next to the button you press on every visit. -->
          <v-menu location="bottom end">
            <template v-slot:activator="{ props: menuProps }">
              <v-btn
                icon="mdi-dots-vertical"
                variant="text"
                :disabled="isOffline"
                aria-label="More list actions"
                v-bind="menuProps"
              />
            </template>
            <v-list density="compact">
              <v-list-item
                prepend-icon="mdi-broom"
                title="Clear purchased"
                :disabled="!hasPurchased"
                @click="clear_purchased_dialog = true"
              />
              <v-list-item
                prepend-icon="mdi-delete-sweep-outline"
                title="Clear all"
                base-color="error"
                :disabled="isEmpty"
                @click="clear_full_dialog = true"
              />
            </v-list>
          </v-menu>
        </div>
      </header>

      <div v-if="isLoading" class="listpage__body">
        <v-skeleton-loader
          type="list-item-two-line, list-item-two-line, list-item-two-line"
        />
      </div>

      <div v-else class="listpage__body">
        <!-- Everything bought: say so, rather than showing an empty region
             above a long purchased list. -->
        <p v-if="isComplete" class="listpage__done">
          <v-icon icon="mdi-check-circle-outline" size="20" />
          All done — nothing left to pick up.
        </p>

        <ShoppingList
          v-else
          :listitems="fullshoppinglist?.aisles ?? []"
          :purchased="false"
          empty-text="Nothing on this list yet."
          @edit-list-item="editListItem"
          @delete-list-item="removeListItem"
          @item-purchased="purchaseItem"
        />

        <!-- Collapsed by default: while shopping, the things still to find are
             the page's job, and this section only grows as you work. -->
        <section v-if="hasPurchased" class="listpage__purchased">
          <button
            type="button"
            class="listpage__toggle"
            :aria-expanded="showPurchased"
            @click="showPurchased = !showPurchased"
          >
            <v-icon
              :icon="showPurchased ? 'mdi-chevron-down' : 'mdi-chevron-right'"
              size="20"
            />
            In the cart ({{ fullshoppinglist.totalpurchased }})
          </button>

          <div v-if="showPurchased" class="listpage__purchased-body">
            <ShoppingList
              :listitems="fullshoppinglist?.purchased_aisles ?? []"
              :purchased="true"
              @edit-list-item="editListItem"
              @item-purchased="purchaseItem"
            />
          </div>
        </section>
      </div>
    </div>

    <!-- Single instances, outside any v-for. -->
    <ListItemForm
      v-model="listItemFormDialog"
      @add-list-item="createListItem"
      @update-dialog="updateDialog"
      :passedFormData="blankFormData"
      :isEdit="false"
      :key="-1"
    />

    <v-dialog v-model="clear_purchased_dialog" max-width="400">
      <v-card>
        <v-card-title>Clear purchased items?</v-card-title>
        <v-card-text>
          The {{ fullshoppinglist?.totalpurchased }} item{{
            fullshoppinglist?.totalpurchased === 1 ? "" : "s"
          }}
          you have already picked up will be removed from this list.
        </v-card-text>
        <v-card-actions>
          <v-spacer />
          <v-btn variant="text" @click="clear_purchased_dialog = false">
            Cancel
          </v-btn>
          <v-btn
            color="error"
            variant="text"
            @click="clearPurchasedListFunction(fullshoppinglist?.id)"
          >
            Clear
          </v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>

    <v-dialog v-model="clear_full_dialog" max-width="400">
      <v-card>
        <v-card-title>Clear the whole list?</v-card-title>
        <v-card-text>
          All {{ fullshoppinglist?.totalitems }} items will be removed,
          purchased or not. The list itself stays.
        </v-card-text>
        <v-card-actions>
          <v-spacer />
          <v-btn variant="text" @click="clear_full_dialog = false">
            Cancel
          </v-btn>
          <v-btn
            color="error"
            variant="text"
            @click="clearListFunction(fullshoppinglist?.id)"
          >
            Clear all
          </v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>
  </div>
</template>

<script setup>
  import { computed, ref } from "vue";
  import ShoppingList from "@/components/ShoppingList.vue";
  import ListItemForm from "@/components/ListItemForm.vue";
  import { useFullShoppingList } from "@/composables/listsComposable";
  import { useMainStore } from "@/stores/main";
  import { useOffline } from "@/composables/offlineComposable";

  const store = useMainStore();
  const { isOffline } = useOffline();

  const clear_full_dialog = ref(false);
  const clear_purchased_dialog = ref(false);
  const listItemFormDialog = ref(false);
  const showPurchased = ref(false);

  const updateDialog = () => {
    listItemFormDialog.value = false;
  };

  const blankFormData = ref({
    id: 0,
    qty: 1,
    purchased: false,
    notes: "",
    item: null,
    aisle_id: null,
    shopping_list_id: 0,
  });

  const {
    fullshoppinglist,
    isLoading,
    addListItem,
    deleteListItem,
    updateListItem,
    clearList,
    clearPurchasedList,
  } = useFullShoppingList(store.list_id);

  const totalItems = computed(() => fullshoppinglist.value?.totalitems ?? 0);
  const totalPurchased = computed(
    () => fullshoppinglist.value?.totalpurchased ?? 0,
  );

  const isEmpty = computed(() => totalItems.value === 0);

  const hasPurchased = computed(() => totalPurchased.value > 0);

  const isComplete = computed(
    () => totalItems.value > 0 && totalPurchased.value === totalItems.value,
  );

  const percentComplete = computed(() =>
    isEmpty.value
      ? 0
      : Math.round((totalPurchased.value / totalItems.value) * 100),
  );

  const countLabel = computed(() => {
    if (isEmpty.value) return "Empty list";
    return `${totalPurchased.value} of ${totalItems.value} purchased`;
  });

  const editListItem = async listItem => {
    await updateListItem(listItem);
  };

  const createListItem = async newListItem => {
    await addListItem(newListItem);
  };

  const removeListItem = async deletedListItem => {
    await deleteListItem(deletedListItem);
  };

  const purchaseItem = async listItem => {
    await updateListItem(listItem);
  };

  const clearListFunction = async shoppinglistID => {
    await clearList(shoppinglistID);
    clear_full_dialog.value = false;
  };

  const clearPurchasedListFunction = async shoppinglistID => {
    await clearPurchasedList(shoppinglistID);
    clear_purchased_dialog.value = false;
  };
</script>

<style scoped>
  .listpage {
    padding: var(--ls-space-sm) var(--ls-space) var(--ls-space-lg);
    max-width: 720px;
    margin: 0 auto;
  }

  /* Padding longhand on purpose: the shorthand would also set padding-bottom,
   clobbering the room .ls-paper--torn reserves for the tear and letting the
   last row run into the torn edge. */
  .listpage__sheet {
    padding-top: var(--ls-space);
    padding-right: var(--ls-space);
    padding-left: var(--ls-space);
  }

  .listpage__head {
    display: flex;
    flex-direction: column;
    gap: var(--ls-space-sm);
    padding-bottom: var(--ls-space);
    border-bottom: 1px solid var(--ls-rule-strong);
  }

  .listpage__name {
    margin: 0;
    overflow-wrap: anywhere;
  }

  .listpage__progress {
    display: flex;
    align-items: center;
    gap: var(--ls-space-sm);
  }

  .listpage__count {
    flex-shrink: 0;
    font-size: 0.75rem;
    font-weight: 600;
    letter-spacing: 0.02em;
    color: var(--ls-ink-soft);
  }

  .listpage__bar {
    flex: 1;
  }

  .listpage__actions {
    display: flex;
    align-items: center;
    gap: var(--ls-space-sm);
    padding-top: var(--ls-space-xs);
  }

  .listpage__actions .v-btn:first-child {
    flex: 1;
  }

  .listpage__body {
    padding-top: var(--ls-space);
  }

  .listpage__done {
    display: flex;
    align-items: center;
    gap: var(--ls-space-sm);
    margin: 0;
    padding: var(--ls-space) 0;
    color: var(--ls-done);
    font-weight: 600;
  }

  .listpage__purchased {
    margin-top: var(--ls-space-md);
    padding-top: var(--ls-space-sm);
    border-top: 1px solid var(--ls-rule);
  }

  .listpage__toggle {
    display: flex;
    align-items: center;
    gap: var(--ls-space-xs);
    width: 100%;
    padding: var(--ls-space-sm) 0;
    border: 0;
    background: transparent;
    color: var(--ls-ink-soft);
    font-family: var(--ls-font-body);
    font-size: 0.8125rem;
    font-weight: 700;
    letter-spacing: 0.06em;
    text-transform: uppercase;
    text-align: left;
    cursor: pointer;
  }

  .listpage__toggle:focus-visible {
    outline: 3px solid var(--ls-navy);
    outline-offset: 2px;
  }

  .listpage__purchased-body {
    /* Faded back so the cart reads as done business next to what is still to do. */
    opacity: 0.72;
  }

  @media (max-width: 599px) {
    .listpage {
      padding-left: var(--ls-space-sm);
      padding-right: var(--ls-space-sm);
    }
  }
</style>
