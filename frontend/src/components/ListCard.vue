<template>
  <v-card
    color="primary"
    variant="outlined"
  >
        <v-card-title class="text-h6">
          {{list.name}}
        </v-card-title>
        <v-card-subtitle>{{list.store.name}}</v-card-subtitle>
        
        <v-card-actions>
          <v-btn size="x-small" variant="outlined" @click="fetchShoppingListFull(list.id, list.store_id)">shop</v-btn>
          <v-btn size="x-small" variant="outlined" @click="selectedList(list)">edit</v-btn>
          <ListForm v-model="listFormDialog" @edit-list="updateList" :isEdit="true" @update-dialog="updateDialog" :passedFormData="passedFormData"/>
          <v-btn size="x-small" variant="outlined" @click="deleteDialog = true">delete</v-btn>
          <v-dialog
            v-model="deleteDialog"
            width="auto"
          >
            <v-card>
              <v-card-text>
                Delete list {{ list.name }}?
              </v-card-text>
              <v-card-actions>
                <v-btn color="primary" @click="deleteList(list)">Yes</v-btn>
                <v-btn color="primary" @click="deleteDialog = false">No</v-btn>
              </v-card-actions>
            </v-card>
          </v-dialog>
        </v-card-actions>
  </v-card>
</template>

<script setup>
  import { defineProps, defineEmits, ref } from 'vue';
  import { useMainStore } from '@/stores/main';
  import { useRouter } from 'vue-router';
  import ListForm from '@/components/ListForm.vue'

  const emit = defineEmits(['editList', 'removeList'])
  const listFormDialog = ref(false)
  const deleteDialog = ref(false)
  const passedFormData = ref({
    id: 0,
    name: '',
    store_id: 0
  })

  const selectedList = (list) => {
    passedFormData.value.id = list.id
    passedFormData.value.name = list.name
    passedFormData.value.store_id = list.store_id

    listFormDialog.value = true
  }

  const updateList = async (list) => {
    emit('editList', list)
  }

  const deleteList = async (list) => {
    emit('removeList', list)

    updateDialog()
  }

  const updateDialog = () => {
    listFormDialog.value = false
  }

  defineProps({
    list: Array
  })

  const router = useRouter();

  const fetchShoppingListFull = async (list_id, store_id) => {
    try {
        const store = useMainStore();
        store.list_id = list_id
        store.store_id = store_id
        router.push('/list')
    } catch (error) {
        console.log(error)
    }
  }
</script>