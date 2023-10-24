<template>
      <v-container>
        <v-row dense>
          <v-col cols="12" v-for="store in getStores" :key="store.id">
            <v-card
              color="secondary"
            >
                  <v-card-title class="text-h5">
                    <v-icon
                  icon="mdi-storefront"
                  size="25"
                  class="me-1 pb-1"
                ></v-icon>{{store.name}}
                  </v-card-title>
                  
                  <v-card-actions>
                    <v-btn icon="mdi-cart"/>
                    <v-btn icon="mdi-land-rows-vertical"/>
                    <v-btn icon="mdi-pencil"/>
                    <v-btn icon="mdi-delete"/>
                  </v-card-actions>
            </v-card>
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
  import { computed, ref } from 'vue';
  import { useMainStore } from '@/stores/main';

  const snackbar = ref(false);
  const snackbarText = ref('');
  const snackbarColor = ref('');
  const snackbarTimeout = ref(1500);
  
  const mainstore = useMainStore();
  const getStores = computed(() => {
    return mainstore.getStores;
  })
</script>