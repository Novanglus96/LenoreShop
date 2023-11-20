<template>
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
          <v-btn icon="mdi-pencil" @click="selectedItem(item)"/>
          <AddItemForm v-model="itemFormDialog" @edit-item="updateItem" :isEdit="true" @update-dialog="updateDialog" :passedFormData="passedFormData"/>
          <v-btn icon="mdi-delete" @click="deleteDialog = true"/>
            <v-dialog
              v-model="deleteDialog"
              width="auto"
            >
              <v-card>
                <v-card-text>
                  Delete item {{ item.name }}?
                </v-card-text>
                <v-card-actions>
                  <v-btn color="primary" @click="deleteItem(item)">Yes</v-btn>
                  <v-btn color="primary" @click="deleteDialog = false">No</v-btn>
                </v-card-actions>
              </v-card>
            </v-dialog>
        </v-card-actions>
  </v-card>
</template>

<script setup>
  import { defineProps, defineEmits, ref } from 'vue';
  import AddItemForm from '@/components/AddItemForm.vue'

  const emit = defineEmits(['editItem', 'removeItem'])
  const itemFormDialog = ref(false)
  const deleteDialog = ref(false)
  const passedFormData = ref({
    id: 0,
    name: '',
    matches: ''
  })

  const selectedItem = (item) => {
    passedFormData.value.id = item.id
    passedFormData.value.name = item.name
    passedFormData.value.matches = item.matches

    itemFormDialog.value = true
  }

  const updateItem = async (item) => {
    emit('editItem', item)
  }

  const deleteItem = async (item) => {
    emit('removeItem', item)

    updateDialog()
  }

  const updateDialog = () => {
    itemFormDialog.value = false
  }

  defineProps({
    item: Array
  })

</script>