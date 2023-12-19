<template>
  <div class="lists">
    <v-btn density="compact" @click="listFormDialog = true">Add List</v-btn>
    <ListForm v-model="listFormDialog" @add-list="createShoppingList" :isEdit="false" @update-dialog="updateDialog"/>
    <v-container>
      <v-row dense v-if="!isLoading">
        <v-col cols="12">
          <ListCard v-for="shoppinglist in shoppinglists" :key="shoppinglist.id" :list="shoppinglist" @edit-list="updateList" @remove-list="deleteList" />
        </v-col>
      </v-row>
      <v-row dense v-else>
        <v-col cols="12">
          <v-skeleton-loader type="card" color="primary"></v-skeleton-loader>
        </v-col>
      </v-row>
    </v-container>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import ListCard from '@/components/ListCard.vue'
import ListForm from '@/components/ListForm.vue'
import { useShoppingLists } from '@/composables/listsComposable'

const listFormDialog = ref(false);

const { shoppinglists, isLoading, addShoppingList, editList, removeList } = useShoppingLists()

const createShoppingList = async (newList) => {
  await addShoppingList(newList)
}

const updateList = async (updatedList) => {
  await editList(updatedList)
}

const deleteList = async (deletedList) => {
  await removeList(deletedList)
}

const updateDialog = () => {
  listFormDialog.value = false
}


</script>
