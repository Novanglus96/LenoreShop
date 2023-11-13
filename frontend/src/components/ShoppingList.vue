<template>
  <div>
    <h2 class="text-h6 text-primary ps-4">{{ list.name }}</h2>
    <h2 class="text-subtitle-1 text-info ps-4">{{ list.store.name }}</h2>
    <div
      v-for="aisle in list.aisles"
      :key="aisle.id"
    >
      <v-divider class="mt-4"></v-divider>

      <v-row class="my-1" align="center">
        <strong class="mx-4 text-primary-darken-2"> {{ aisle.name }}</strong>
      </v-row>

      <v-divider class="mb-4"></v-divider>

      <v-card>
        <v-slide-y-transition class="py-0" group tag="v-list">
          <template v-for="(item, i) in aisle.listitems" :key="`${i}-${item.item.name}`">
            <v-divider v-if="i !== 0" :key="`${i}-divider`"></v-divider>

            <v-list-item @click="item.purchased = !item.purchased">
              <template v-slot:prepend>
                <v-checkbox-btn v-model="item.purchased" color="grey"></v-checkbox-btn>
              </template>

              <v-list-item-title>
                <span :class="item.purchased ? 'text-grey' : 'text-primary'"
                  >({{ item.qty }}) {{ item.item.name }}</span
                >
              </v-list-item-title>
              <v-list-item-subtitle>
                {{ item.notes }}
              </v-list-item-subtitle>

              <template v-slot:append>
                <v-expand-x-transition>
                  <v-icon v-if="item.purchased" color="success"> mdi-check </v-icon>
                </v-expand-x-transition>
              </template>
            </v-list-item>
          </template>
        </v-slide-y-transition>
      </v-card>
    </div>
    <v-row dense align="center">
      <v-col cols="12" align="center">
        <v-img
          :width="300"
          aspect-ratio="16/9"
          cover
          src="Simple_shopping_cart.svg"
          v-ripple
        >
        </v-img>
      </v-col>
    </v-row>
  </div>
</template>

<script setup>
  import { defineProps } from 'vue';

  defineProps({
    list: Object,
    isLoading: Boolean
  })

</script>