<template>
      <v-container>
        <v-row dense v-if="!isLoading">
          <v-col cols="12" v-for="store in props.stores" :key="store.id">
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
                    <v-btn icon="mdi-cart"  @click="showShoppingList(store.id)" />
                    <v-btn icon="mdi-land-rows-vertical" @click="showAisle(store.id)" />
                    <v-btn icon="mdi-pencil"/>
                    <v-btn icon="mdi-delete"/>
                  </v-card-actions>
            </v-card>
          </v-col>
        </v-row>
        <v-row dense v-else>
          <v-col cols="12">
            <v-skeleton-loader type="card" color="primary"></v-skeleton-loader>
          </v-col>
        </v-row>
      </v-container>
</template>

<script setup>
  import { defineProps } from 'vue';
  import { useMainStore } from '@/stores/main';
  import { useRouter } from 'vue-router';

  const props = defineProps({
    stores: Array,
    isLoading: Boolean
  })

  const router = useRouter();

  const showShoppingList = async (store_id) => {
    const store = useMainStore()
    store.store_id = store_id
    router.push('/lists')
  }

  const showAisle = async (store_id) => {
    const store = useMainStore()
    store.store_id = store_id
    router.push('/aisles')
  }

</script>