<template>
      <v-container>
        <v-row dense>
          <v-col cols="12" v-for="list in getShoppingLists" :key="list.id">
            <v-card
              color="secondary"
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
                    <v-btn icon="mdi-pencil" @click="fetchShoppingListFull(list.id)" />
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
  import { useRouter } from 'vue-router';

  const router = useRouter();
  const snackbar = ref(false);
  const snackbarText = ref('');
  const snackbarColor = ref('');
  const snackbarTimeout = ref(1500);
  
  const mainstore = useMainStore();
  const getShoppingLists = computed(() => {
    return mainstore.getShoppingLists;
  })

  const fetchShoppingListFull = async (list) => {
    try {
        const store = useMainStore();
        await store.fetchShoppingListFull(list);
        router.push('/list/' + list)
    } catch (error) {
        console.log(error)
    }
  }
</script>