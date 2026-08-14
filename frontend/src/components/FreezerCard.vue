<template>
  <li class="ls-frost-row freezerrow">
    <button type="button" class="freezerrow__main" @click="showContents">
      <v-icon icon="mdi-snowflake" size="20" class="freezerrow__icon" />

      <span class="freezerrow__body">
        <span class="freezerrow__name">{{ freezer.name }}</span>
        <span class="freezerrow__meta">
          <span v-if="freezer.location">{{ freezer.location }} ·</span>
          {{ freezer.totalitems }}
          {{ freezer.totalitems === 1 ? "item" : "items" }}
        </span>
      </span>

      <!-- The same counts the dashboard card shows, so the two agree at a
           glance about which freezer needs attention. -->
      <span class="freezerrow__pills">
        <span v-if="freezer.totalexpired > 0" class="ls-pill ls-pill--alert">
          {{ freezer.totalexpired }} expired
        </span>
        <span v-if="freezer.totalexpiring > 0" class="ls-pill ls-pill--warn">
          {{ freezer.totalexpiring }} soon
        </span>
      </span>

      <v-icon icon="mdi-chevron-right" size="18" class="freezerrow__chevron" />
    </button>

    <v-menu location="bottom end">
      <template v-slot:activator="{ props: menuProps }">
        <v-btn
          icon="mdi-dots-vertical"
          variant="text"
          size="small"
          density="comfortable"
          class="freezerrow__menu"
          :aria-label="`Actions for ${freezer.name}`"
          v-bind="menuProps"
        />
      </template>
      <v-list density="compact">
        <v-list-item
          prepend-icon="mdi-pencil"
          title="Edit"
          @click="$emit('select', freezer)"
        />
        <v-list-item
          prepend-icon="mdi-delete-outline"
          title="Delete"
          base-color="error"
          @click="$emit('selectDelete', freezer)"
        />
      </v-list>
    </v-menu>
  </li>
</template>

<script setup>
  import { useRouter } from "vue-router";
  import { useMainStore } from "@/stores/main";

  // Both dialogs live in FreezerView, outside its v-for. Rendering them here
  // would create one hidden dialog per row, which is what caused the mobile
  // black screen in ShoppingList.vue.
  const props = defineProps({
    freezer: {
      type: Object,
      required: true,
    },
  });

  defineEmits(["select", "selectDelete"]);

  const router = useRouter();

  const showContents = () => {
    const store = useMainStore();
    store.freezer_id = props.freezer.id;
    router.push("/freezer");
  };
</script>

<style scoped>
  .freezerrow {
    display: flex;
    align-items: center;
    gap: var(--ls-space-sm);
    min-height: calc(var(--ls-rule-height) * 2);
  }

  .freezerrow__main {
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

  .freezerrow__main:focus-visible {
    outline: 3px solid var(--ls-frost-ink);
    outline-offset: 2px;
  }

  .freezerrow__icon {
    flex-shrink: 0;
    color: var(--ls-frost-ink-faint);
  }

  .freezerrow__body {
    flex: 1;
    display: flex;
    flex-direction: column;
    gap: 1px;
    min-width: 0;
  }

  .freezerrow__name {
    font-size: 1rem;
    line-height: 1.3;
    color: var(--ls-frost-ink);
    overflow-wrap: anywhere;
  }

  .freezerrow__meta {
    font-size: 0.8125rem;
    line-height: 1.35;
    color: var(--ls-frost-ink-soft);
  }

  .freezerrow__pills {
    display: flex;
    flex-wrap: wrap;
    justify-content: flex-end;
    gap: var(--ls-space-xs);
    flex-shrink: 0;
  }

  .freezerrow__chevron {
    flex-shrink: 0;
    color: var(--ls-frost-ink-faint);
  }

  .freezerrow__menu {
    flex-shrink: 0;
    color: var(--ls-frost-ink-faint);
  }
</style>
