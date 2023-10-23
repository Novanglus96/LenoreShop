<template>
  <q-layout view="lHh Lpr lFf">
    <q-header elevated>
      <q-toolbar>
        <q-btn
          flat
          dense
          round
          icon="menu"
          aria-label="Menu"
          @click="toggleLeftDrawer"
        />

        <q-toolbar-title>
          Shopping App
        </q-toolbar-title>

        <div>Shopping App v1</div>
      </q-toolbar>
    </q-header>

    <q-drawer
      v-model="leftDrawerOpen"
      show-if-above
      bordered
    >
      <q-list>
        <q-item-label
          header
        >
          Actions
        </q-item-label>

        <EssentialLink
          v-for="link in essentialLinks"
          v-bind="link"
          :key="link.title"
        />
      </q-list>
    </q-drawer>

    <q-page-container>
      <router-view />
    </q-page-container>
  </q-layout>
</template>

<script>
import { defineComponent, ref } from 'vue'
import EssentialLink from 'components/EssentialLink.vue'

const linksList = [
  {
    title: 'Stores',
    caption: 'available stores',
    icon: 'storefront',
    link: 'stores'
  },
  {
    title: 'Aisles',
    caption: 'aisles defined for stores',
    icon: 'view_week',
    link: 'aisles'
  },
  {
    title: 'Lists',
    caption: 'shopping lists for stores',
    icon: 'shopping_cart',
    link: 'lists'
  },
  {
    title: 'Items',
    caption: 'items to be purchased',
    icon: 'all_inclusive',
    link: 'items'
  }
]

export default defineComponent({
  name: 'MainLayout',

  components: {
    EssentialLink
  },

  setup () {
    const leftDrawerOpen = ref(false)

    return {
      essentialLinks: linksList,
      leftDrawerOpen,
      toggleLeftDrawer () {
        leftDrawerOpen.value = !leftDrawerOpen.value
      }
    }
  }
})
</script>
