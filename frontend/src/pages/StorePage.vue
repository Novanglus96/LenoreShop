<template>
  <q-page class="justify-center">
    <div class="q-pa-md" style="max-width: 500px">
    <q-list bordered class="rounded-borders" style="max-width: 400px">
      <q-item-label header>Stores</q-item-label>

      <q-item>
        <q-item-section avatar top>
          <q-icon name="storefront" color="black" size="24px" />
        </q-item-section>

        <q-item-section top>
          <q-item-label lines="1">
            <span class="text-weight-medium">Stop & Shop</span>
          </q-item-label>
          <q-item-label caption lines="1">
            1 Kings Highway
          </q-item-label>
        </q-item-section>

        <q-item-section top side>
          <div class="text-grey-8 q-gutter-xs">
            <q-btn class="gt-xs" size="12px" flat dense round icon="edit" />
            <q-btn class="gt-xs" size="12px" flat dense round icon="shopping_cart" />
            <q-btn class="gt-xs" size="12px" flat dense round icon="delete" />
          </div>
        </q-item-section>
      </q-item>

      <q-separator spaced />

      <q-item>
        <q-item-section avatar top>
          <q-icon name="storefront" color="black" size="24px" />
        </q-item-section>

        <q-item-section top>
          <q-item-label lines="1">
            <span class="text-weight-medium">Stop & Shop</span>
          </q-item-label>
          <q-item-label caption lines="1">
            1 Kings Highway
          </q-item-label>
        </q-item-section>

        <q-item-section top side>
          <div class="text-grey-8 q-gutter-xs">
            <q-btn class="gt-xs" size="12px" flat dense round icon="edit" />
            <q-btn class="gt-xs" size="12px" flat dense round icon="shopping_cart" />
            <q-btn class="gt-xs" size="12px" flat dense round icon="delete" />
          </div>
        </q-item-section>
      </q-item>

      <q-separator spaced />

    </q-list>
    </div>
  </q-page>
</template>

<script>
import { defineComponent } from 'vue'

export default defineComponent({
  name: 'StorePage'
})
</script>
<style lang="sass" scoped>
.my-card
  width: 100%
  max-width: 250px
</style>