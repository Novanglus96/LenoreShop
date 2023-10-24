<template>
      <v-container>
        <v-row dense>
          <v-col cols="12" v-for="item in getItems" :key="item.id">
            <v-card
              color="secondary"
            >
                  <v-card-title class="text-h5">
                    <v-icon
                  icon="mdi-food-apple"
                  size="25"
                  class="me-1 pb-1"
                ></v-icon>{{item.name}}
                  </v-card-title>
                  
                  <v-card-actions>
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
  const getItems = computed(() => {
    return mainstore.getItems;
  })
</script>