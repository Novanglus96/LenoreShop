<template>
  <div class="frzcontents">
    <ul v-if="hasItems" class="ls-rows">
      <li
        v-for="item in freezeritems"
        :key="item.id"
        class="ls-frost-row frzcontents__row"
      >
        <v-icon
          :icon="discardIcon(item)"
          :color="discardColor(item)"
          size="22"
          class="frzcontents__icon"
        />

        <!-- No placeholder: an empty frame beside every unphotographed row
             would be clutter on a freezer you are digging through. -->
        <ItemThumb
          :thumbnail-url="item.thumbnail_url"
          :image-url="item.image_url"
          :name="item.name"
          variant="frost"
        />

        <span class="frzcontents__body">
          <span class="frzcontents__name">
            <span v-if="showQty(item)" class="frzcontents__qty">
              {{ item.qty }}
              <template v-if="item.unit">{{ item.unit }}</template>
            </span>
            {{ item.name }}
          </span>

          <span class="frzcontents__meta">
            <span :class="['frzcontents__discard', discardClass(item)]">
              {{ discardLabel(item) }}
            </span>
            <span class="frzcontents__added">· {{ addedLabel(item) }}</span>
          </span>

          <span v-if="item.notes" class="frzcontents__notes">
            {{ item.notes }}
          </span>
        </span>

        <v-menu location="bottom end">
          <template v-slot:activator="{ props: menuProps }">
            <v-btn
              icon="mdi-dots-vertical"
              variant="text"
              size="small"
              density="comfortable"
              class="frzcontents__menu"
              :aria-label="`Actions for ${item.name}`"
              v-bind="menuProps"
            />
          </template>
          <v-list density="compact">
            <v-list-item
              prepend-icon="mdi-pencil"
              title="Edit"
              @click="selectedItem(item)"
            />
            <v-list-item
              prepend-icon="mdi-delete-outline"
              title="Remove"
              base-color="error"
              @click="selectedDeleteItem(item)"
            />
          </v-list>
        </v-menu>
      </li>
    </ul>

    <p v-else class="frzcontents__empty">Nothing in this freezer yet.</p>
  </div>

  <!-- A single form and a single delete dialog, both rendered outside the
       v-for above. One instance per row would share these refs and open
       together. -->
  <FreezerItemForm
    v-model="freezerItemFormDialog"
    @edit-freezer-item="editFreezerItem"
    @update-dialog="updateDialog"
    :isEdit="true"
    :freezers="freezers"
    :passedFormData="passedFormData"
    :key="passedFormData.id"
  />

  <ConfirmDialog
    v-model="deleteDialog"
    title="Remove from freezer?"
    confirm-label="Remove"
    icon="mdi-delete-outline"
    @confirm="deleteItem(passedDeleteData)"
  >
    "{{ passedDeleteData.name }}" will no longer be tracked as being in this
    freezer.
  </ConfirmDialog>
</template>

<script setup>
  import { computed, ref } from "vue";
  import FreezerItemForm from "@/components/FreezerItemForm.vue";

  // Matches FREEZER_SOON_DAYS in backend/backend/api.py, which decides the
  // totalexpiring count shown on the freezer cards.
  const SOON_DAYS = 14;
  import ConfirmDialog from "@/components/ConfirmDialog.vue";
  import ItemThumb from "@/components/ItemThumb.vue";
  const props = defineProps({
    freezeritems: {
      type: Array,
      default: () => [],
    },
    freezers: {
      type: Array,
      default: () => [],
    },
  });

  const emit = defineEmits(["editFreezerItem", "deleteFreezerItem"]);

  const passedFormData = ref({
    id: 0,
    name: "",
    qty: 1,
    unit: null,
    date_added: null,
    discard_date: null,
    notes: "",
    freezer_id: 0,
    thumbnail_url: null,
  });
  const passedDeleteData = ref({
    id: 0,
    name: null,
  });
  const freezerItemFormDialog = ref(false);
  const deleteDialog = ref(false);

  const hasItems = computed(() => (props.freezeritems?.length ?? 0) > 0);

  const updateDialog = () => {
    freezerItemFormDialog.value = false;
  };

  const selectedItem = item => {
    passedFormData.value = {
      id: item.id,
      name: item.name,
      qty: item.qty,
      unit: item.unit,
      date_added: item.date_added,
      discard_date: item.discard_date,
      notes: item.notes,
      freezer_id: item.freezer_id,
      // ImagePicker shows this as the existing photo, and only calls for a
      // delete when there was one to begin with.
      thumbnail_url: item.thumbnail_url,
    };

    freezerItemFormDialog.value = true;
  };

  const selectedDeleteItem = item => {
    passedDeleteData.value.id = item.id;
    passedDeleteData.value.name = item.name;
    deleteDialog.value = true;
  };

  const editFreezerItem = async item => {
    emit("editFreezerItem", item);
  };

  const deleteItem = async item => {
    emit("deleteFreezerItem", { id: item.id });
    deleteDialog.value = false;
  };

  // A single unitless portion is the default and says nothing; anything else is
  // worth showing.
  const showQty = item => item.qty > 1 || Boolean(item.unit);

  const addedLabel = item => {
    if (!item.date_added) return "date added unknown";
    return `frozen ${item.date_added}`;
  };

  const discardLabel = item => {
    const days = item.days_until_discard;
    if (days === null || days === undefined) return "No throw out date";
    if (days < 0) {
      return `${Math.abs(days)} day${Math.abs(days) === 1 ? "" : "s"} overdue`;
    }
    if (days === 0) return "Throw out today";
    if (days === 1) return "Throw out tomorrow";
    return `Throw out in ${days} days`;
  };

  const discardColor = item => {
    const days = item.days_until_discard;
    if (days === null || days === undefined) return "var(--ls-frost-ink-faint)";
    if (days < 0) return "var(--ls-alert)";
    if (days <= SOON_DAYS) return "var(--ls-warn)";
    return "var(--ls-frost-ink-faint)";
  };

  const discardClass = item => {
    const days = item.days_until_discard;
    if (days === null || days === undefined)
      return "frzcontents__discard--none";
    if (days < 0) return "frzcontents__discard--alert";
    if (days <= SOON_DAYS) return "frzcontents__discard--warn";
    return "frzcontents__discard--calm";
  };

  const discardIcon = item => {
    const days = item.days_until_discard;
    if (days === null || days === undefined) return "mdi-snowflake";
    if (days < 0) return "mdi-alert-circle";
    if (days <= SOON_DAYS) return "mdi-clock-alert-outline";
    return "mdi-snowflake";
  };
</script>

<style scoped>
  .frzcontents__row {
    display: flex;
    align-items: center;
    gap: var(--ls-space-sm);
    min-height: calc(var(--ls-rule-height) * 2);
    padding: var(--ls-space-xs) 0;
  }

  .frzcontents__icon {
    flex-shrink: 0;
  }

  .frzcontents__body {
    flex: 1;
    display: flex;
    flex-direction: column;
    gap: 1px;
    min-width: 0;
  }

  .frzcontents__name {
    font-size: 1rem;
    line-height: 1.3;
    color: var(--ls-frost-ink);
    overflow-wrap: anywhere;
  }

  .frzcontents__qty {
    display: inline-block;
    margin-right: 2px;
    padding: 0 6px;
    border-radius: var(--ls-radius-sm);
    background: var(--ls-frost-edge);
    color: var(--ls-frost-ink);
    font-size: 0.8125rem;
    font-weight: 700;
  }

  .frzcontents__meta {
    display: flex;
    flex-wrap: wrap;
    gap: 4px;
    font-size: 0.8125rem;
    line-height: 1.35;
  }

  .frzcontents__discard--alert {
    color: var(--ls-alert);
    font-weight: 700;
  }

  .frzcontents__discard--warn {
    color: var(--ls-warn);
    font-weight: 600;
  }

  .frzcontents__discard--calm,
  .frzcontents__discard--none {
    color: var(--ls-frost-ink-soft);
  }

  .frzcontents__added {
    color: var(--ls-frost-ink-faint);
  }

  .frzcontents__notes {
    font-size: 0.8125rem;
    line-height: 1.35;
    color: var(--ls-frost-ink-soft);
    overflow-wrap: anywhere;
  }

  .frzcontents__menu {
    flex-shrink: 0;
    color: var(--ls-frost-ink-faint);
  }

  .frzcontents__empty {
    margin: 0;
    padding: var(--ls-space) 0;
    color: var(--ls-frost-ink-faint);
    font-style: italic;
  }
</style>
