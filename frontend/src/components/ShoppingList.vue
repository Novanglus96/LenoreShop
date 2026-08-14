<template>
  <!-- The margin rule is drawn once down the whole block rather than per aisle,
       so it reads as the sheet's margin instead of restarting at each heading. -->
  <div class="shoplist ls-sheet-margin">
    <section v-for="aisle in listitems" :key="aisle.id" class="shoplist__aisle">
      <h3 class="shoplist__aisle-name">{{ aisle.name }}</h3>

      <ul class="ls-rows">
        <li
          v-for="listItem in aisle.listitems"
          :key="listItem.id"
          class="ls-row shoplist__row"
        >
          <!-- The whole point of the page: a target you can hit one-handed
               while holding something else. -->
          <button
            type="button"
            class="shoplist__check"
            role="checkbox"
            :aria-checked="listItem.purchased"
            :aria-label="`${listItem.item.name}, ${listItem.purchased ? 'purchased' : 'not purchased'}`"
            @click="purchaseItem(listItem)"
          >
            <v-icon
              :icon="
                listItem.purchased
                  ? 'mdi-checkbox-marked-outline'
                  : 'mdi-checkbox-blank-outline'
              "
              :color="listItem.purchased ? 'var(--ls-done)' : 'var(--ls-ink-faint)'"
              size="26"
            />
          </button>

          <span class="shoplist__body">
            <span
              :class="['shoplist__name', { 'ls-strike': listItem.purchased }]"
            >
              <span v-if="listItem.qty > 1" class="shoplist__qty">
                {{ listItem.qty }}
              </span>
              {{ listItem.item.name }}
            </span>
            <span
              v-if="listItem.notes"
              :class="['shoplist__notes', { 'ls-strike': listItem.purchased }]"
            >
              {{ listItem.notes }}
            </span>
          </span>

          <v-menu location="bottom end">
            <template v-slot:activator="{ props: menuProps }">
              <v-btn
                icon="mdi-dots-vertical"
                variant="text"
                size="small"
                density="comfortable"
                class="shoplist__menu"
                :aria-label="`Actions for ${listItem.item.name}`"
                v-bind="menuProps"
              />
            </template>
            <v-list density="compact">
              <v-list-item
                prepend-icon="mdi-pencil"
                title="Edit"
                @click="selectedItem(listItem)"
              />
              <v-list-item
                v-if="!purchased"
                prepend-icon="mdi-delete-outline"
                title="Delete"
                base-color="error"
                @click="selectedDeleteItem(listItem)"
              />
            </v-list>
          </v-menu>
        </li>
      </ul>
    </section>

    <p v-if="listitems.length === 0" class="shoplist__empty">
      {{ emptyText }}
    </p>
  </div>

  <!-- Single instances, outside every v-for. One dialog per row shares the same
       ref and opens them all at once, which stacks into a black screen on
       mobile. -->
  <ListItemForm
    v-model="listItemFormDialog"
    @edit-list-item="editListItem"
    @update-dialog="updateDialog"
    :isEdit="true"
    :passedFormData="passedFormData"
    :key="passedFormData.id"
  />

  <v-dialog v-model="deleteDialog" max-width="400">
    <v-card>
      <v-card-title>Remove item?</v-card-title>
      <v-card-text>
        "{{ passedDeleteData.name }}" will be taken off this list.
      </v-card-text>
      <v-card-actions>
        <v-spacer />
        <v-btn variant="text" @click="deleteDialog = false">Cancel</v-btn>
        <v-btn color="error" variant="text" @click="deleteItem(passedDeleteData)">
          Remove
        </v-btn>
      </v-card-actions>
    </v-card>
  </v-dialog>
</template>

<script setup>
import { ref } from "vue";
import ListItemForm from "@/components/ListItemForm.vue";

defineProps({
  listitems: {
    type: Array,
    default: () => [],
  },
  purchased: {
    type: Boolean,
    default: false,
  },
  emptyText: {
    type: String,
    default: "Nothing here yet",
  },
});

const emit = defineEmits(["itemPurchased", "editListItem", "deleteListItem"]);

const passedFormData = ref({
  id: 0,
  qty: 1,
  purchased: false,
  notes: "",
  item_id: 0,
  aisle_id: 0,
  shopping_list_id: 0,
});
const passedDeleteData = ref({
  id: 0,
  name: null,
});
const listItemFormDialog = ref(false);
const deleteDialog = ref(false);

const updateDialog = () => {
  listItemFormDialog.value = false;
};

const selectedDeleteItem = listItem => {
  passedDeleteData.value.id = listItem.id;
  passedDeleteData.value.name = listItem.item.name;
  deleteDialog.value = true;
};

const selectedItem = listItem => {
  passedFormData.value.id = listItem.id;
  passedFormData.value.qty = listItem.qty;
  passedFormData.value.purchased = listItem.purchased;
  passedFormData.value.notes = listItem.notes;
  passedFormData.value.item = listItem.item_id;
  passedFormData.value.aisle_id = listItem.aisle_id;
  passedFormData.value.shopping_list_id = listItem.shopping_list_id;

  listItemFormDialog.value = true;
};

const editListItem = async listItem => {
  emit("editListItem", listItem);
};

const purchaseItem = async listItem => {
  emit("itemPurchased", {
    id: listItem.id,
    qty: listItem.qty,
    purchased: !listItem.purchased,
    notes: listItem.notes,
    purch_date: null,
    item: listItem.item_id,
    aisle_id: listItem.aisle_id,
    shopping_list_id: listItem.shopping_list_id,
  });
};

const deleteItem = async listItem => {
  emit("deleteListItem", { id: listItem.id });
  deleteDialog.value = false;
};
</script>

<style scoped>
.shoplist__aisle + .shoplist__aisle {
  margin-top: var(--ls-space-md);
}

/* Aisles are wayfinding, not content — small and quiet, so the item names stay
   the thing your eye lands on. */
.shoplist__aisle-name {
  display: flex;
  align-items: center;
  gap: var(--ls-space-sm);
  margin: 0 0 var(--ls-space-xs);
  font-size: 0.75rem;
  font-weight: 700;
  letter-spacing: 0.08em;
  text-transform: uppercase;
  color: var(--ls-ink-soft);
}

.shoplist__aisle-name::after {
  content: "";
  flex: 1;
  height: 1px;
  background: var(--ls-rule);
}

.shoplist__row {
  display: flex;
  align-items: center;
  gap: var(--ls-space-sm);
  /* Two ruled lines tall, which is also comfortably over the 44px a thumb
     needs. Rows with notes grow past it and rule themselves — see .ls-rows. */
  min-height: calc(var(--ls-rule-height) * 2);
  padding: var(--ls-space-xs) 0;
}

.shoplist__check {
  display: flex;
  align-items: center;
  justify-content: center;
  flex-shrink: 0;
  width: 44px;
  height: 44px;
  margin-left: -10px;
  border: 0;
  border-radius: var(--ls-radius-pill);
  background: transparent;
  cursor: pointer;
  transition: background var(--ls-duration) var(--ls-ease);
}

@media (hover: hover) {
  .shoplist__check:hover {
    background: var(--ls-paper-shade);
  }
}

.shoplist__check:focus-visible {
  outline: 3px solid var(--ls-navy);
  outline-offset: -3px;
}

.shoplist__body {
  flex: 1;
  display: flex;
  flex-direction: column;
  gap: 1px;
  min-width: 0;
}

.shoplist__name {
  font-size: 1rem;
  line-height: 1.3;
  color: var(--ls-ink);
  overflow-wrap: anywhere;
}

/* A quantity of one is the default and says nothing, so only a real count is
   worth the ink. */
.shoplist__qty {
  display: inline-block;
  min-width: 1.5rem;
  margin-right: 2px;
  padding: 0 5px;
  border-radius: var(--ls-radius-sm);
  background: var(--ls-powder);
  color: var(--ls-navy);
  font-size: 0.8125rem;
  font-weight: 700;
  text-align: center;
}

.shoplist__notes {
  font-size: 0.8125rem;
  line-height: 1.35;
  color: var(--ls-ink-soft);
  overflow-wrap: anywhere;
}

.shoplist__menu {
  flex-shrink: 0;
  color: var(--ls-ink-faint);
}

.shoplist__empty {
  margin: 0;
  padding: var(--ls-space) 0;
  color: var(--ls-ink-faint);
  font-style: italic;
}
</style>
