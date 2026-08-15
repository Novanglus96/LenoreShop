<template>
  <v-app-bar color="secondary" density="compact" app flat class="appbar">
    <v-menu location="bottom start" offset="8">
      <template v-slot:activator="{ props }">
        <v-btn
          icon="mdi-menu"
          aria-label="Open navigation menu"
          v-bind="props"
        ></v-btn>
      </template>

      <!-- A torn sheet rather than a plain menu panel, so the navigation reads
           as part of the same notepad as the pages it leads to. -->
      <div class="ls-paper ls-paper--torn navmenu">
        <span class="ls-tab navmenu__tab">
          <v-icon icon="mdi-cart-outline" size="14" />
          <span class="ls-tab__text">LenoreShop</span>
        </span>

        <v-list
          class="navmenu__list"
          density="compact"
          bg-color="transparent"
          nav
        >
          <v-list-item
            v-for="(menu, i) in menus"
            :key="i"
            :to="menu.url"
            class="navmenu__item"
          >
            <template v-slot:prepend>
              <v-icon :icon="menu.icon" size="20"></v-icon>
            </template>
            <v-list-item-title>{{ menu.title }}</v-list-item-title>
          </v-list-item>

          <v-divider class="navmenu__rule" />

          <v-list-item href="/admin/" class="navmenu__item">
            <template v-slot:prepend>
              <v-icon icon="mdi-security" size="20"></v-icon>
            </template>
            <v-list-item-title>Admin</v-list-item-title>
          </v-list-item>
        </v-list>

        <p class="navmenu__version">v{{ version }}</p>
      </div>
    </v-menu>

    <v-img :width="201" aspect-ratio="1/1" src="logov2.png" inline></v-img>
  </v-app-bar>
</template>

<script setup>
  import { version } from "../../package.json";

  const menus = [
    { title: "Home", url: "/", icon: "mdi-home-outline" },
    { title: "Stores", url: "/stores", icon: "mdi-storefront-outline" },
    { title: "Shopping Lists", url: "/alllists", icon: "mdi-cart-outline" },
    { title: "Items", url: "/items", icon: "mdi-food-apple-outline" },
    { title: "Freezers", url: "/freezers", icon: "mdi-snowflake" },
  ];
</script>

<style scoped>
  /* A hairline instead of an elevation shadow — the sheets below carry their own,
   and two competing shadows muddied the top of the screen. */
  .appbar {
    border-bottom: 1px solid rgba(0, 34, 85, 0.12);
  }

  .navmenu {
    min-width: 224px;
    /* Longhand: the shorthand would clobber the room .ls-paper--torn reserves for
     the tear and let the version line run into it. */
    padding-top: var(--ls-space);
    padding-right: var(--ls-space-sm);
    padding-left: var(--ls-space-sm);
  }

  /* .ls-tab hangs off the sheet's edge by --ls-space, which assumes a card with
   that much padding; this sheet is tighter, so the offset is restated. */
  .navmenu__tab {
    margin-left: calc(var(--ls-space-sm) * -1);
    margin-bottom: var(--ls-space-sm);
  }

  .navmenu__list {
    padding: 0;
  }

  .navmenu__item {
    min-height: 40px;
    border-radius: var(--ls-radius-sm);
    color: var(--ls-ink);
  }

  .navmenu__item :deep(.v-list-item-title) {
    font-size: 0.9375rem;
    font-weight: 500;
  }

  /* The page you are on, marked the way a pen would: a yellow swash behind it. */
  .navmenu__item.v-list-item--active {
    background: var(--ls-yellow-soft);
    color: var(--ls-navy);
  }

  .navmenu__item.v-list-item--active :deep(.v-list-item-title) {
    font-weight: 700;
  }

  .navmenu__rule {
    margin: var(--ls-space-xs) 0;
    border-color: var(--ls-rule);
  }

  .navmenu__version {
    margin: var(--ls-space-xs) 0 0;
    text-align: center;
    font-size: 0.6875rem;
    color: var(--ls-ink-faint);
  }
</style>
