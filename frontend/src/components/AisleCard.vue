<template>
      <v-container>
        <v-row dense>
          <v-col cols="12" v-for="aisle in getAisles" :key="aisle.id">
            <v-card
              color="secondary"
            >
                  <v-card-title class="text-h5">
                    <v-icon
                  icon="mdi-land-rows-vertical"
                  size="25"
                  class="me-1 pb-1"
                ></v-icon>{{aisle.name}}
                  </v-card-title>
                  <v-card-subtitle>{{aisle.store.name}}</v-card-subtitle>
                  <v-card-actions>
                    <v-btn icon="mdi-pencil" :disabled="aisle.order === 0 ? true : false"/>
                    <v-btn icon="mdi-delete" :disabled="aisle.order === 0 ? true : false"/>
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
  const getAisles = computed(() => {
    return mainstore.getAisles;
  })
</script>