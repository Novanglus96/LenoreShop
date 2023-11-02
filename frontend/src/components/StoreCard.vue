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
                    <v-btn icon="mdi-cart"  @click="fetchListsByStore(store.id)" />
                    <v-btn icon="mdi-land-rows-vertical" @click="fetchAislesByStore(store.id)" />
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
        <v-snackbar
          v-model="snackbar"
          :color="snackbarColor"
          :timeout="snackbarTimeout"
          content-class="centered-text"
        >
          {{ snackbarText }}
        </v-snackbar>
      </v-container>
</template>

<script setup>
  import { ref, defineProps } from 'vue';
  import { useMainStore } from '@/stores/main';
  import { useRouter } from 'vue-router';

  const props = defineProps({
    stores: Array,
    isLoading: Boolean
  })

  const router = useRouter();
  const snackbar = ref(false);
  const snackbarText = ref('');
  const snackbarColor = ref('');
  const snackbarTimeout = ref(1500);

  const fetchAislesByStore = async (store_id) => {
    try {
        const store = useMainStore();
        store.store_id = store_id;
        await store.fetchAislesByStore(store_id);
        router.push('/aisles')
    } catch (error) {
        console.log(error)
    }
  }

  const fetchListsByStore = async (store_id) => {
    try {
        const store = useMainStore();
        store.store_id=store_id;
        await store.fetchListsByStore(store_id);
        router.push('/lists')
    } catch (error) {
        console.log(error)
    }
  }
</script>