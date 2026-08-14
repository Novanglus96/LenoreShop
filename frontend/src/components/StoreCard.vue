<template>
  <li class="ls-row storerow">
    <!-- The row itself goes to the store's aisles, which is the only thing a
         store really contains. Edit and delete sit in the menu beside it, as
         siblings rather than nested inside the button. -->
    <button type="button" class="storerow__main" @click="showAisles">
      <v-icon icon="mdi-storefront-outline" size="20" class="storerow__icon" />
      <span class="storerow__name">{{ store.name }}</span>
      <span class="storerow__go">
        Aisles
        <v-icon icon="mdi-chevron-right" size="18" />
      </span>
    </button>

    <v-menu location="bottom end">
      <template v-slot:activator="{ props: menuProps }">
        <v-btn
          icon="mdi-dots-vertical"
          variant="text"
          size="small"
          density="comfortable"
          class="storerow__menu"
          :aria-label="`Actions for ${store.name}`"
          v-bind="menuProps"
        />
      </template>
      <v-list density="compact">
        <v-list-item
          prepend-icon="mdi-pencil"
          title="Edit"
          @click="$emit('edit', store)"
        />
        <v-list-item
          prepend-icon="mdi-delete-outline"
          title="Delete"
          base-color="error"
          @click="$emit('remove', store)"
        />
      </v-list>
    </v-menu>
  </li>
</template>

<script setup>
import { useRouter } from "vue-router";
import { useMainStore } from "@/stores/main";

// Presentational apart from the navigation. The edit form and the delete
// confirmation live once in StoreView, driven by a selected-store ref.
const props = defineProps({
  store: {
    type: Object,
    required: true,
  },
});

defineEmits(["edit", "remove"]);

const router = useRouter();

const showAisles = () => {
  const mainStore = useMainStore();
  mainStore.store_id = props.store.id;
  router.push("/aisles");
};
</script>

<style scoped>
.storerow {
  display: flex;
  align-items: center;
  gap: var(--ls-space-sm);
  min-height: calc(var(--ls-rule-height) * 2);
}

.storerow__main {
  flex: 1;
  display: flex;
  align-items: center;
  gap: var(--ls-space-sm);
  min-width: 0;
  padding: var(--ls-space-sm) 0;
  border: 0;
  background: transparent;
  font-family: var(--ls-font-body);
  text-align: left;
  cursor: pointer;
}

.storerow__main:focus-visible {
  outline: 3px solid var(--ls-navy);
  outline-offset: 2px;
}

.storerow__icon {
  flex-shrink: 0;
  color: var(--ls-navy-300);
}

.storerow__name {
  flex: 1;
  min-width: 0;
  font-size: 1rem;
  color: var(--ls-ink);
  overflow-wrap: anywhere;
}

.storerow__go {
  display: inline-flex;
  align-items: center;
  gap: 1px;
  flex-shrink: 0;
  font-size: 0.75rem;
  font-weight: 600;
  letter-spacing: 0.03em;
  text-transform: uppercase;
  color: var(--ls-navy-300);
}

@media (hover: hover) {
  .storerow__main:hover .storerow__go,
  .storerow__main:hover .storerow__icon {
    color: var(--ls-navy);
  }
}

.storerow__menu {
  flex-shrink: 0;
  color: var(--ls-ink-faint);
}
</style>
