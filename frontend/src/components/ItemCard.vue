<template>
        <v-row dense>
          <v-col cols="12">
            <v-card
              color="primary"
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
</template>

<script setup>
  import { defineProps } from 'vue';

  defineProps({
    item: Array,
    isLoading: Boolean
  })

</script>