<template>
  <v-card
    color="primary"
  >
        <v-card-title class="text-h5">
          <v-icon
        icon="mdi-storefront"
        size="25"
        class="me-1 pb-1"
      ></v-icon>{{store.name}}
        </v-card-title>
        
        <v-card-actions>
          <v-btn icon="mdi-land-rows-vertical" @click="showAisle(store.id)" />
          <v-btn icon="mdi-pencil"/>
          <v-btn icon="mdi-delete"/>
        </v-card-actions>
  </v-card>
</template>

<script setup>
  import { defineProps } from 'vue';
  import { useMainStore } from '@/stores/main';
  import { useRouter } from 'vue-router';

  defineProps({
    store: Array
  })

  const router = useRouter();

  const showAisle = async (store_id) => {
    const store = useMainStore()
    store.store_id = store_id
    router.push('/aisles')
  }

</script>