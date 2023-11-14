<template>
  <div>
    <h2 class="text-h6 text-primary ps-4">{{ list.name }}</h2>
    <h2 class="text-subtitle-1 text-info ps-4">{{ list.store.name }}</h2>
    <v-list density="compact" elevation="1">
      <div
        v-for="aisle in list.aisles"
        :key="aisle.id"
      >
        <v-list-subheader color="primary" inset><v-icon icon="mdi-land-rows-vertical"></v-icon> {{ aisle.name }}</v-list-subheader>
        <v-list-item v-for="item in aisle.listitems" :key="item.id" elevation="2" :variant="item.purchased ? 'tonal' : 'plain'">
          <v-list-item-title><span :class="item.purchased ? 'text-grey text-decoration-line-through' : 'text-black'">{{ item.qty }} {{ item.item.name }}</span></v-list-item-title>
          <v-list-item-subtitle><span :class="item.purchased ? 'text-grey text-decoration-line-through' : 'text-black'">{{ item.notes }}</span></v-list-item-subtitle>
          <template v-slot:prepend>
            <v-btn variant="plain" :ripple="false" @click="purchaseItem(item)"><v-icon :icon="item.purchased ? 'mdi-checkbox-marked-outline' : 'mdi-checkbox-blank-outline' " :color="!item.purchased ? 'grey' : 'success'" flat></v-icon></v-btn>
          </template>
          <template v-slot:append>
            <v-btn icon="mdi-pencil" variant="plain" :ripple="false"></v-btn>
          </template>
        </v-list-item>
      </div>
    </v-list>
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
  import { defineProps, defineEmits } from 'vue';

  const emit = defineEmits(['itemPurchased'])
  
  const purchaseItem = async (item) => {
    const itemData = {
      id: item.id,
      qty: item.qty,
      purchased: !item.purchased,
      notes: item.notes,
      purch_date: null,
      item_id: item.item_id,
      aisle_id: item.aisle_id,
      shopping_list_id: item.shopping_list_id
}
    emit('itemPurchased', itemData)
  }

  defineProps({
    list: Object,
    isLoading: Boolean
  })

</script>