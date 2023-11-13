<template>
  <v-card
    color="primary"
  >
        <v-card-title class="text-h5">
          <v-icon
        icon="mdi-cart"
        size="25"
        class="me-1 pb-1"
      ></v-icon>{{list.name}}
        </v-card-title>
        <v-card-subtitle>{{list.store.name}}</v-card-subtitle>
        
        <v-card-actions>
          <v-btn icon="mdi-pencil" @click="fetchShoppingListFull(list.id, list.store_id)" />
          <v-btn icon="mdi-delete"/>
        </v-card-actions>
  </v-card>
</template>

<script setup>
  import { defineProps } from 'vue';
  import { useMainStore } from '@/stores/main';
  import { useRouter } from 'vue-router';

  defineProps({
    list: Array
  })

  const router = useRouter();

  const fetchShoppingListFull = async (list_id, store_id) => {
    try {
        const store = useMainStore();
        store.list_id = list_id
        store.store_id = store_id
        router.push('/list')
    } catch (error) {
        console.log(error)
    }
  }
</script>