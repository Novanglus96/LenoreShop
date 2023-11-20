<template>
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
      <v-btn icon="mdi-pencil" :disabled="aisle.order === 0 ? true : false" @click="selectedAisle(aisle)"/>
      <AddAisleForm v-model="aisleFormDialog" @edit-aisle="updateAisle" :isEdit="true" @update-dialog="updateDialog" :passedFormData="passedFormData" :key="aisle.id"/>
      <v-btn icon="mdi-delete" :disabled="aisle.order === 0 ? true : false"/>
    </v-card-actions>
  </v-card>
</template>

<script setup>
  import { defineProps, defineEmits, ref } from 'vue';
  import AddAisleForm from '@/components/AddAisleForm.vue'

  const emit = defineEmits(['editAisle'])
  const aisleFormDialog = ref(false)
  const passedFormData = ref({
    id: 0,
    name: '',
    store_id: 0,
    order: '1'
  })

  const selectedAisle = (aisle) => {
    passedFormData.value.id = aisle.id
    passedFormData.value.name = aisle.name
    passedFormData.value.store_id = aisle.store_id
    passedFormData.value.order = aisle.order

    aisleFormDialog.value = true
    console.log(passedFormData)
  }

  const updateAisle = async (aisle) => {
    emit('editAisle', aisle)
  }
  
  const updateDialog = () => {
    aisleFormDialog.value = false
  }

  defineProps({
    aisle: Array
  })
  
</script>