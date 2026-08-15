<template>
  <li class="ls-row itemrow">
    <!-- Placeholder shown here but not on a shopping list: in the catalog the
         empty frame is the hint that an item can have a photo. -->
    <ItemThumb
      :thumbnail-url="item.thumbnail_url"
      :image-url="item.image_url"
      :name="item.name"
      placeholder
    />

    <span class="itemrow__body">
      <span class="itemrow__name">{{ item.name }}</span>
      <span v-if="item.aisle" class="itemrow__aisle">
        {{ item.aisle.name }} · {{ item.aisle.store.name }}
      </span>
      <span v-else class="itemrow__aisle itemrow__aisle--none">
        Not filed under an aisle yet
      </span>
      <span v-if="item.matches" class="itemrow__matches">
        also matches: {{ item.matches }}
      </span>
    </span>

    <v-menu location="bottom end">
      <template v-slot:activator="{ props: menuProps }">
        <v-btn
          icon="mdi-dots-vertical"
          variant="text"
          size="small"
          density="comfortable"
          class="itemrow__menu"
          :aria-label="`Actions for ${item.name}`"
          v-bind="menuProps"
        />
      </template>
      <v-list density="compact">
        <v-list-item
          prepend-icon="mdi-pencil"
          title="Edit"
          @click="$emit('edit', item)"
        />
        <v-list-item
          prepend-icon="mdi-delete-outline"
          title="Delete"
          base-color="error"
          @click="$emit('remove', item)"
        />
      </v-list>
    </v-menu>
  </li>
</template>

<script setup>
  // Presentational only. The edit form and the delete confirmation live once in
  // ItemView, driven by a selected-item ref — a dialog per row is the shape that
  // caused the mobile black screen, and it mounts one dialog per visible item.
  // The photo overlay follows the same rule: ItemThumb calls a shared lightbox
  // mounted once in App.vue rather than rendering an overlay per row.
  import ItemThumb from "@/components/ItemThumb.vue";

  defineProps({
    item: {
      type: Object,
      required: true,
    },
  });

  defineEmits(["edit", "remove"]);
</script>

<style scoped>
  .itemrow {
    display: flex;
    align-items: center;
    gap: var(--ls-space-sm);
    min-height: calc(var(--ls-rule-height) * 2);
    padding: var(--ls-space-xs) 0;
  }

  .itemrow__body {
    flex: 1;
    display: flex;
    flex-direction: column;
    gap: 1px;
    min-width: 0;
  }

  .itemrow__name {
    font-size: 1rem;
    line-height: 1.3;
    color: var(--ls-ink);
    overflow-wrap: anywhere;
  }

  .itemrow__aisle {
    font-size: 0.8125rem;
    line-height: 1.35;
    color: var(--ls-ink-soft);
  }

  .itemrow__aisle--none {
    color: var(--ls-ink-faint);
    font-style: italic;
  }

  .itemrow__matches {
    font-size: 0.75rem;
    line-height: 1.35;
    color: var(--ls-ink-faint);
    overflow-wrap: anywhere;
  }

  .itemrow__menu {
    flex-shrink: 0;
    color: var(--ls-ink-faint);
  }
</style>
