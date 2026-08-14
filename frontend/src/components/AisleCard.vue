<template>
  <li :class="['ls-row', 'aislerow', { 'aislerow--fixed': isUncategorized }]">
    <!-- Uncategorized is where items land when they have no aisle, so it has no
         position to drag and nothing to rename. -->
    <span v-if="isUncategorized" class="aislerow__handle aislerow__handle--fixed">
      <v-icon icon="mdi-tray-arrow-down" size="20" />
    </span>
    <span v-else class="drag-handle aislerow__handle" aria-hidden="true">
      <v-icon icon="mdi-drag-horizontal-variant" size="20" />
    </span>

    <span class="aislerow__body">
      <span class="aislerow__name">{{ aisle.name }}</span>
      <span v-if="isUncategorized" class="aislerow__note">
        Always last · items with no aisle
      </span>
    </span>

    <span v-if="!isUncategorized" class="aislerow__order">{{ aisle.order }}</span>

    <v-menu v-if="!isUncategorized" location="bottom end">
      <template v-slot:activator="{ props: menuProps }">
        <v-btn
          icon="mdi-dots-vertical"
          variant="text"
          size="small"
          density="comfortable"
          class="aislerow__menu"
          :aria-label="`Actions for ${aisle.name}`"
          v-bind="menuProps"
        />
      </template>
      <v-list density="compact">
        <v-list-item
          prepend-icon="mdi-pencil"
          title="Edit"
          @click="$emit('edit', aisle)"
        />
        <v-list-item
          prepend-icon="mdi-delete-outline"
          title="Delete"
          base-color="error"
          @click="$emit('remove', aisle)"
        />
      </v-list>
    </v-menu>
  </li>
</template>

<script setup>
import { computed } from "vue";

// Presentational only. The edit form and delete confirmation live once in
// AisleView, driven by a selected-aisle ref, rather than once per row.
const props = defineProps({
  aisle: {
    type: Object,
    required: true,
  },
});

defineEmits(["edit", "remove"]);

const isUncategorized = computed(() => props.aisle.order === 0);
</script>

<style scoped>
.aislerow {
  display: flex;
  align-items: center;
  gap: var(--ls-space-sm);
  min-height: calc(var(--ls-rule-height) * 2);
  padding: var(--ls-space-xs) 0;
  background: var(--ls-paper);
}

.aislerow--fixed {
  opacity: 0.75;
}

.aislerow__handle {
  display: flex;
  align-items: center;
  justify-content: center;
  flex-shrink: 0;
  width: 36px;
  height: 44px;
  margin-left: -8px;
  color: var(--ls-ink-faint);
  cursor: grab;
  touch-action: none;
}

.aislerow__handle:active {
  cursor: grabbing;
}

.aislerow__handle--fixed {
  cursor: default;
}

.aislerow__body {
  flex: 1;
  display: flex;
  flex-direction: column;
  gap: 1px;
  min-width: 0;
}

.aislerow__name {
  font-size: 1rem;
  line-height: 1.3;
  color: var(--ls-ink);
  overflow-wrap: anywhere;
}

.aislerow__note {
  font-size: 0.75rem;
  line-height: 1.35;
  color: var(--ls-ink-faint);
  font-style: italic;
}

/* The number is the point of this page — it's the order you walk the store in. */
.aislerow__order {
  flex-shrink: 0;
  min-width: 1.75rem;
  padding: 1px 6px;
  border-radius: var(--ls-radius-sm);
  background: var(--ls-powder);
  color: var(--ls-navy);
  font-size: 0.8125rem;
  font-weight: 700;
  text-align: center;
}

.aislerow__menu {
  flex-shrink: 0;
  color: var(--ls-ink-faint);
}
</style>
