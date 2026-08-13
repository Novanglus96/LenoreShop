<template>
  <button
    type="button"
    class="ls-frost-sheet ls-frost-sheet--iced ls-paper--liftable frostcard"
    :aria-label="ariaLabel"
    @click="$emit('open', freezer)"
  >
    <span class="ls-magnet" aria-hidden="true" />

    <span class="frostcard__head">
      <span class="ls-hand ls-hand--card frostcard__name">{{ freezer.name }}</span>
      <span v-if="freezer.location" class="frostcard__location">
        {{ freezer.location }}
      </span>
    </span>

    <span class="ls-frost-ruled frostcard__lines">
      <span
        v-for="(previewItem, index) in freezer.preview_items"
        :key="index"
        class="frostcard__line"
      >
        <v-icon icon="mdi-snowflake" size="13" :color="iconColor(previewItem)" />
        <span class="frostcard__item">{{ previewItem.name }}</span>
        <span :class="['frostcard__due', dueClass(previewItem)]">
          {{ dueLabel(previewItem) }}
        </span>
      </span>

      <span v-if="isEmpty" class="frostcard__line frostcard__line--empty">
        Nothing frozen yet
      </span>

      <span v-else-if="hiddenCount > 0" class="frostcard__line frostcard__more">
        +{{ hiddenCount }} more
      </span>
    </span>

    <span class="frostcard__footer">
      <span class="frostcard__count">
        {{ freezer.totalitems }} {{ freezer.totalitems === 1 ? "item" : "items" }}
      </span>
      <span class="frostcard__pills">
        <span v-if="freezer.totalexpired > 0" class="ls-pill ls-pill--alert">
          {{ freezer.totalexpired }} expired
        </span>
        <span v-if="freezer.totalexpiring > 0" class="ls-pill ls-pill--warn">
          {{ freezer.totalexpiring }} soon
        </span>
        <span v-if="isAllGood" class="ls-pill ls-pill--calm">All good</span>
      </span>
    </span>
  </button>
</template>

<script setup>
import { computed } from "vue";

const props = defineProps({
  freezer: {
    type: Object,
    required: true,
  },
});

defineEmits(["open"]);

// Matches FREEZER_SOON_DAYS in backend/backend/api.py, which decides the
// totalexpiring count these rows sit beneath.
const SOON_DAYS = 14;

const isEmpty = computed(() => props.freezer.totalitems === 0);

const isAllGood = computed(
  () =>
    props.freezer.totalitems > 0 &&
    props.freezer.totalexpired === 0 &&
    props.freezer.totalexpiring === 0,
);

const hiddenCount = computed(
  () => props.freezer.totalitems - (props.freezer.preview_items?.length ?? 0),
);

// Undated items are the common case for food already in the freezer, so they
// get a neutral dash rather than being made to look like a problem.
const dueLabel = previewItem => {
  const days = previewItem.days_until_discard;
  if (days === null || days === undefined) return "—";
  if (days < 0) return "overdue";
  if (days === 0) return "today";
  if (days < 30) return `${days}d`;
  return `${Math.round(days / 30)}mo`;
};

const dueClass = previewItem => {
  if (previewItem.is_expired) return "frostcard__due--alert";
  const days = previewItem.days_until_discard;
  if (days !== null && days !== undefined && days <= SOON_DAYS) {
    return "frostcard__due--warn";
  }
  return "";
};

const iconColor = previewItem => {
  if (previewItem.is_expired) return "var(--ls-alert)";
  const days = previewItem.days_until_discard;
  if (days !== null && days !== undefined && days <= SOON_DAYS) {
    return "var(--ls-warn)";
  }
  return "var(--ls-frost-ink-faint)";
};

const ariaLabel = computed(() => {
  const parts = [`${props.freezer.name} freezer`, `${props.freezer.totalitems} items`];
  if (props.freezer.totalexpired > 0) {
    parts.push(`${props.freezer.totalexpired} expired`);
  }
  if (props.freezer.totalexpiring > 0) {
    parts.push(`${props.freezer.totalexpiring} expiring soon`);
  }
  return parts.join(", ");
});
</script>

<style scoped>
.frostcard {
  display: flex;
  flex-direction: column;
  gap: var(--ls-space-sm);
  width: 100%;
  height: 100%;
  /* Extra top padding leaves room for the magnet. */
  padding: var(--ls-space-md) var(--ls-space) var(--ls-space);
  border: 0;
  text-align: left;
  font-family: var(--ls-font-body);
}

.frostcard__head {
  display: flex;
  flex-direction: column;
  gap: 1px;
  /* Centred under the magnet, the way a note hangs from one. */
  align-items: center;
  text-align: center;
}

.frostcard__name {
  color: var(--ls-frost-ink);
  overflow-wrap: anywhere;
}

.frostcard__location {
  font-size: 0.6875rem;
  font-weight: 600;
  letter-spacing: 0.07em;
  text-transform: uppercase;
  color: var(--ls-frost-ink-soft);
}

.frostcard__lines {
  flex: 1;
  display: flex;
  flex-direction: column;
  min-height: calc(var(--ls-rule-height) * 3);
}

.frostcard__line {
  display: flex;
  align-items: center;
  gap: 6px;
  height: var(--ls-rule-height);
  font-size: 0.875rem;
  color: var(--ls-frost-ink);
  overflow: hidden;
}

.frostcard__item {
  flex: 1;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}

.frostcard__due {
  flex-shrink: 0;
  font-size: 0.75rem;
  font-weight: 600;
  font-variant-numeric: tabular-nums;
  color: var(--ls-frost-ink-faint);
}

.frostcard__due--alert {
  color: var(--ls-alert);
}

.frostcard__due--warn {
  color: var(--ls-warn);
}

.frostcard__line--empty,
.frostcard__more {
  color: var(--ls-frost-ink-faint);
  font-style: italic;
  font-size: 0.8125rem;
}

.frostcard__footer {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: var(--ls-space-sm);
  flex-wrap: wrap;
  padding-top: var(--ls-space-xs);
}

.frostcard__count {
  font-size: 0.75rem;
  font-weight: 600;
  letter-spacing: 0.02em;
  color: var(--ls-frost-ink-soft);
  font-variant-numeric: tabular-nums;
}

.frostcard__pills {
  display: flex;
  gap: var(--ls-space-xs);
  flex-wrap: wrap;
}
</style>
