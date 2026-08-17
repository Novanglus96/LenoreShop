<template>
  <div class="frzlog">
    <div class="ls-frost-sheet ls-frost-sheet--iced frzlog__sheet">
      <span class="ls-magnet" aria-hidden="true" />

      <header class="frzlog__head">
        <h1 class="ls-hand ls-hand--title frzlog__title">Freezer History</h1>
        <p class="frzlog__blurb">
          What happened to it, and when — kept after the food is gone.
        </p>

        <v-text-field
          v-model="search"
          label="Search by name"
          placeholder="meatloaf"
          prepend-inner-icon="mdi-magnify"
          clearable
          hide-details
          density="comfortable"
          class="frzlog__search"
        ></v-text-field>

        <div class="frzlog__filters">
          <v-chip
            v-for="choice in actionChoices"
            :key="choice.value"
            :variant="action === choice.value ? 'flat' : 'outlined'"
            :color="action === choice.value ? 'primary' : undefined"
            size="small"
            @click="action = action === choice.value ? '' : choice.value"
          >
            {{ choice.label }}
          </v-chip>
        </div>
      </header>

      <div v-if="isLoading" class="frzlog__body">
        <v-skeleton-loader
          type="list-item-two-line, list-item-two-line, list-item-two-line"
        />
      </div>

      <div v-else class="frzlog__body">
        <p v-if="entries.length === 0" class="frzlog__empty">
          {{ emptyLabel }}
        </p>

        <ul v-else class="ls-rows">
          <li
            v-for="entry in entries"
            :key="entry.id"
            class="ls-frost-row frzlog__row"
          >
            <v-icon
              :icon="actionIcon(entry.action)"
              :color="actionColor(entry.action)"
              size="22"
              class="frzlog__icon"
            />

            <span class="frzlog__detail">
              <span class="frzlog__what">{{ sentence(entry) }}</span>
              <span class="frzlog__when" :title="exactLabel(entry.occurred)">
                {{ whenLabel(entry.occurred) }}
              </span>
            </span>
          </li>
        </ul>

        <div v-if="totalPages > 1" class="frzlog__pager">
          <v-pagination
            v-model="page"
            :length="totalPages"
            :total-visible="5"
            density="comfortable"
            rounded
          />
        </div>

        <p v-if="totalRecords > 0" class="frzlog__count">
          {{ totalRecords }} {{ totalRecords === 1 ? "entry" : "entries" }}
        </p>
      </div>
    </div>
  </div>
</template>

<script setup>
  import { computed, ref, watch } from "vue";
  import { useFreezerLog } from "@/composables/freezersComposable";

  const search = ref("");
  const action = ref("");
  const page = ref(1);

  const actionChoices = [
    { value: "added", label: "Added" },
    { value: "used", label: "Used" },
    { value: "moved", label: "Moved" },
    { value: "discarded", label: "Thrown out" },
  ];

  // Narrowing the list can leave the current page past the end. The backend
  // clamps rather than erroring, but resetting keeps the pager honest about
  // which page is actually showing.
  watch([search, action], () => {
    page.value = 1;
  });

  const { entries, totalPages, totalRecords, isLoading } = useFreezerLog(
    search,
    action,
    page,
  );

  const emptyLabel = computed(() => {
    if (search.value || action.value) return "Nothing matches that.";
    return "Nothing has happened in the freezers yet.";
  });

  // Past tense and the amount, so a row reads as a sentence about one event
  // rather than a table cell.
  const sentence = entry => {
    const amount = entry.unit
      ? `${entry.qty} ${entry.unit} of ${entry.name}`
      : `${entry.qty} × ${entry.name}`;

    switch (entry.action) {
      case "added":
        return `Added ${amount} to ${entry.freezer_name}`;
      case "used":
        return `Used ${amount} from ${entry.freezer_name}`;
      case "moved":
        return `Moved ${amount} from ${entry.freezer_name} to ${entry.to_freezer_name}`;
      case "discarded":
        return `Threw out ${amount} from ${entry.freezer_name}`;
      default:
        return `${entry.name} — ${entry.freezer_name}`;
    }
  };

  const actionIcon = value =>
    ({
      added: "mdi-plus-circle-outline",
      used: "mdi-silverware-fork-knife",
      moved: "mdi-swap-horizontal",
      discarded: "mdi-delete-outline",
    })[value] ?? "mdi-snowflake";

  const actionColor = value =>
    ({
      added: "var(--ls-frost-ink-soft)",
      used: "var(--ls-frost-ink-soft)",
      moved: "var(--ls-frost-ink-soft)",
      discarded: "var(--ls-alert)",
    })[value] ?? "var(--ls-frost-ink-faint)";

  // "3 days ago" is what you actually want when asking how long ago something
  // happened; the exact date is the title attribute for when it is not enough.
  const whenLabel = occurred => {
    const then = new Date(occurred);
    const days = Math.floor((Date.now() - then.getTime()) / 86400000);

    if (days <= 0) return "today";
    if (days === 1) return "yesterday";
    if (days < 30) return `${days} days ago`;

    const months = Math.floor(days / 30);
    if (months < 12) {
      return `${months} month${months === 1 ? "" : "s"} ago`;
    }

    const years = Math.floor(days / 365);
    return `${years} year${years === 1 ? "" : "s"} ago`;
  };

  const exactLabel = occurred => new Date(occurred).toLocaleString();
</script>

<style scoped>
  .frzlog {
    padding: var(--ls-space-sm) var(--ls-space) var(--ls-space-lg);
    max-width: 720px;
    margin: 0 auto;
  }

  /* Padding longhand: the shorthand would clobber the room
   .ls-frost-sheet--iced reserves for the icicles. */
  .frzlog__sheet {
    padding-top: var(--ls-space-md);
    padding-right: var(--ls-space);
    padding-left: var(--ls-space);
  }

  .frzlog__head {
    display: flex;
    flex-direction: column;
    align-items: stretch;
    gap: var(--ls-space-sm);
    padding-bottom: var(--ls-space);
    border-bottom: 1px solid var(--ls-frost-rule);
  }

  .frzlog__title {
    margin: 0;
    color: var(--ls-frost-ink);
  }

  .frzlog__blurb {
    margin: 0;
    font-size: 0.8125rem;
    color: var(--ls-frost-ink-soft);
  }

  .frzlog__filters {
    display: flex;
    flex-wrap: wrap;
    gap: var(--ls-space-xs);
  }

  .frzlog__body {
    padding-top: var(--ls-space);
  }

  .frzlog__row {
    display: flex;
    align-items: center;
    gap: var(--ls-space-sm);
    min-height: calc(var(--ls-rule-height) * 2);
    padding: var(--ls-space-xs) 0;
  }

  .frzlog__icon {
    flex-shrink: 0;
  }

  .frzlog__detail {
    flex: 1;
    display: flex;
    flex-direction: column;
    gap: 1px;
    min-width: 0;
  }

  .frzlog__what {
    font-size: 1rem;
    line-height: 1.3;
    color: var(--ls-frost-ink);
    overflow-wrap: anywhere;
  }

  .frzlog__when {
    font-size: 0.8125rem;
    line-height: 1.35;
    color: var(--ls-frost-ink-faint);
  }

  .frzlog__pager {
    padding-top: var(--ls-space);
  }

  .frzlog__count {
    margin: 0;
    padding-top: var(--ls-space-sm);
    font-size: 0.75rem;
    text-align: center;
    color: var(--ls-frost-ink-faint);
  }

  .frzlog__empty {
    margin: 0;
    padding: var(--ls-space) 0;
    color: var(--ls-frost-ink-faint);
    font-style: italic;
  }

  @media (max-width: 599px) {
    .frzlog {
      padding-left: var(--ls-space-sm);
      padding-right: var(--ls-space-sm);
    }
  }
</style>
