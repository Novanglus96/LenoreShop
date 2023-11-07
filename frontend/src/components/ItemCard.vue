<template>
      <v-container>
        <v-row dense>
          <v-col cols="12" v-for="item in props.items" :key="item.id">
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
      </v-container>
</template>

<script setup>
  import { defineProps } from 'vue';

  const props = defineProps({
    items: Array,
    isLoading: Boolean
  })

</script>