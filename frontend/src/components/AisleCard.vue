<template>
      <v-row dense v-if="!isLoading">
          <v-col cols="12">
            <v-card
              color="primary"
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
            <v-row dense v-else>
              <v-col cols="12">
                <v-skeleton-loader type="card" color="primary"></v-skeleton-loader>
              </v-col>
            </v-row>
</template>

<script setup>
  import { defineProps } from 'vue';

  defineProps({
    aisle: Array,
    isLoading: Boolean
  })
  
</script>