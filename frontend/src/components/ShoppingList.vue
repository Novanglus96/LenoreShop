<template>
  <v-list density="compact" elevation="1" :bg-color="!purchased ? 'primary' : 'grey-darken-1'">
    <div
      v-for="aisle in listitems"
      :key="aisle.id"
    >
      <v-list-subheader color="white" inset>{{ aisle.name }}</v-list-subheader>
      <v-list-item v-for="item in aisle.listitems" :key="item.id" elevation="2" :variant="!purchased ? 'flat' : 'tonal'" :color="!purchased ? 'white' : 'grey-darken-2'">
        <v-list-item-title><span :class="item.purchased ? 'text-grey text-decoration-line-through' : 'text-black'">{{ item.qty }} {{ item.item.name }}</span></v-list-item-title>
        <v-list-item-subtitle><span :class="item.purchased ? 'text-grey text-decoration-line-through' : 'text-black'">{{ item.notes }}</span></v-list-item-subtitle>
        <template v-slot:prepend>
          <v-btn variant="plain" :ripple="false" @click="purchaseItem(item)"><v-icon :icon="item.purchased ? 'mdi-checkbox-marked-outline' : 'mdi-checkbox-blank-outline' " :color="!item.purchased ? 'grey' : 'success'" flat size="x-large"></v-icon></v-btn>
        </template>
        <template v-slot:append>
          <v-btn icon="mdi-pencil" variant="plain" :ripple="false"></v-btn>
        </template>
      </v-list-item>
      <v-list-item v-if="aisle.listitems.length == 0" elevation="2" :variant="!purchased ? 'flat' : 'tonal'" :color="!purchased ? 'white' : 'grey-darken-2'">
        <v-list-item-title><span class="text-black font-italic">No Items</span></v-list-item-title>
      </v-list-item>
    </div>
    <div v-if="listitems.length == 0">
      <v-list-item elevation="2" variant="flat" color="white">
        <v-list-item-title><span class="text-black font-italic">No Items</span></v-list-item-title>
      </v-list-item>
    </div>
  </v-list>
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
    listitems: Object,
    purchased: Boolean
  })

</script>