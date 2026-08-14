<template>
  <div
    :class="[
      'ls-paper',
      'ls-paper--torn',
      'ls-paper--liftable',
      'notepad',
      { 'notepad--manageable': manageable },
    ]"
  >
    <!-- The sheet is a wrapper rather than the button itself, so the manage
         menu can sit beside the open action instead of nested inside it. -->
    <button
      type="button"
      class="notepad__open"
      :aria-label="ariaLabel"
      @click="$emit('open', list)"
    >
      <span class="ls-tab">
        <v-icon icon="mdi-storefront-outline" size="14" />
        <span class="ls-tab__text">{{ list.store.name }}</span>
      </span>

      <span class="ls-hand ls-hand--card notepad__name">{{ list.name }}</span>

      <span class="ls-ruled ls-ruled--margin notepad__lines">
        <span
          v-for="(previewItem, index) in list.preview_items"
          :key="index"
          class="notepad__line"
        >
          <v-icon
            :icon="
              previewItem.purchased
                ? 'mdi-check-circle'
                : 'mdi-checkbox-blank-circle-outline'
            "
            :color="
              previewItem.purchased ? 'var(--ls-done)' : 'var(--ls-ink-faint)'
            "
            size="15"
          />
          <span
            :class="['notepad__item', { 'ls-strike': previewItem.purchased }]"
          >
            {{ previewItem.name }}
          </span>
        </span>

        <span v-if="isEmpty" class="notepad__line notepad__line--empty">
          Nothing on this list yet
        </span>

        <span v-else-if="hiddenCount > 0" class="notepad__line notepad__more">
          +{{ hiddenCount }} more
        </span>
      </span>

      <span class="notepad__footer">
        <span class="notepad__count">{{ countLabel }}</span>
        <span class="ls-progress notepad__progress">
          <span
            :class="[
              'ls-progress__fill',
              { 'ls-progress__fill--done': isComplete },
            ]"
            :style="{ width: percentComplete + '%' }"
          />
        </span>
      </span>
    </button>

    <v-menu v-if="manageable" location="bottom end">
      <template v-slot:activator="{ props: menuProps }">
        <v-btn
          icon="mdi-dots-vertical"
          variant="text"
          size="small"
          density="comfortable"
          class="notepad__menu"
          :aria-label="`Actions for ${list.name}`"
          v-bind="menuProps"
        />
      </template>
      <v-list density="compact">
        <v-list-item
          prepend-icon="mdi-pencil"
          title="Edit"
          @click="$emit('edit', list)"
        />
        <v-list-item
          prepend-icon="mdi-delete-outline"
          title="Delete"
          base-color="error"
          @click="$emit('remove', list)"
        />
      </v-list>
    </v-menu>
  </div>
</template>

<script setup>
  import { computed } from "vue";

  const props = defineProps({
    list: {
      type: Object,
      required: true,
    },
    // The dashboard shows these read-only; the lists page adds the manage menu.
    manageable: {
      type: Boolean,
      default: false,
    },
  });

  defineEmits(["open", "edit", "remove"]);

  const isEmpty = computed(() => props.list.totalitems === 0);

  const isComplete = computed(
    () =>
      props.list.totalitems > 0 &&
      props.list.totalpurchased === props.list.totalitems,
  );

  // The API caps preview_items, so anything beyond what came back is summarised.
  const hiddenCount = computed(
    () => props.list.totalitems - (props.list.preview_items?.length ?? 0),
  );

  const percentComplete = computed(() =>
    props.list.totalitems === 0
      ? 0
      : Math.round((props.list.totalpurchased / props.list.totalitems) * 100),
  );

  const countLabel = computed(() => {
    if (isEmpty.value) return "Empty";
    if (isComplete.value) return "All done!";
    return `${props.list.totalpurchased} of ${props.list.totalitems}`;
  });

  const ariaLabel = computed(
    () =>
      `${props.list.name} at ${props.list.store.name}, ${props.list.totalpurchased} of ${props.list.totalitems} items purchased`,
  );
</script>

<style scoped>
  .notepad {
    position: relative;
    width: 100%;
    height: 100%;
    /* Longhand on purpose: the padding shorthand would also set padding-bottom,
     clobbering the room .ls-paper--torn reserves for the tear and letting the
     last ruled line run into the torn edge. */
    padding-top: var(--ls-space);
    padding-right: var(--ls-space);
    padding-left: var(--ls-space);
    /* Sheets sit at very slightly different angles so a grid of them reads as
     loose paper rather than a table. Overridden per-card by the dashboard. */
    transform: rotate(var(--notepad-tilt, 0deg));
  }

  .notepad__open {
    display: flex;
    flex-direction: column;
    gap: var(--ls-space-sm);
    width: 100%;
    height: 100%;
    padding: 0;
    border: 0;
    background: transparent;
    text-align: left;
    font-family: var(--ls-font-body);
    cursor: pointer;
  }

  /* The ring goes on the button, not the sheet — the sheet is a plain div now,
   and the torn mask would clip an outline drawn on it anyway. */
  .notepad__open:focus-visible {
    outline: 3px solid var(--ls-navy);
    outline-offset: 2px;
  }

  /* Pinned to the corner so adding it does not change the card's layout, and
   sitting above the tab, which occupies the opposite corner. */
  .notepad__menu {
    position: absolute;
    top: 4px;
    right: 4px;
    color: var(--ls-ink-faint);
  }

  /* The tab and the menu share the top line, so give the tab back the width the
   menu takes or a long store name runs underneath it. */
  .notepad--manageable .ls-tab {
    max-width: calc(100% - 36px);
  }

  @media (hover: hover) {
    /* Straighten on hover — the sheet being picked up and looked at. */
    .notepad:hover {
      transform: translateY(-3px) rotate(0deg);
    }
  }

  .notepad__name {
    display: block;
    /* Room for two lines of a long list name without the card jumping height. */
    min-height: 2.2rem;
    overflow-wrap: anywhere;
  }

  .notepad__lines {
    flex: 1;
    display: flex;
    flex-direction: column;
    /* Each row is exactly one ruled line tall so the text sits on the ruling. */
    min-height: calc(var(--ls-rule-height) * 3);
  }

  .notepad__line {
    display: flex;
    align-items: center;
    gap: 6px;
    height: var(--ls-rule-height);
    font-size: 0.875rem;
    color: var(--ls-ink);
    overflow: hidden;
  }

  .notepad__item {
    overflow: hidden;
    text-overflow: ellipsis;
    white-space: nowrap;
  }

  .notepad__line--empty,
  .notepad__more {
    color: var(--ls-ink-faint);
    font-style: italic;
    font-size: 0.8125rem;
  }

  .notepad__footer {
    display: flex;
    align-items: center;
    gap: var(--ls-space-sm);
    padding-top: var(--ls-space-xs);
  }

  .notepad__count {
    flex-shrink: 0;
    font-size: 0.75rem;
    font-weight: 600;
    letter-spacing: 0.02em;
    color: var(--ls-ink-soft);
  }

  .notepad__progress {
    flex: 1;
  }
</style>
