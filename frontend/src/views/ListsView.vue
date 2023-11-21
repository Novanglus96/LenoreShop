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
    <v-snackbar
      v-model="snackbar"
      :color="snackbarColor"
      :timeout="snackbarTimeout"
      content-class="centered-text"
    >
      {{ snackbarText }}
    </v-snackbar>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import ListCard from '@/components/ListCard.vue'
import ListForm from '@/components/ListForm.vue'
import { useShoppingLists } from '@/composables/listsComposable'

const listFormDialog = ref(false);
const snackbar = ref(false);
const snackbarText = ref('');
const snackbarColor = ref('');
const snackbarTimeout = ref(1500);

const { shoppinglists, isLoading, addShoppingList, editList, removeList } = useShoppingLists()

const createShoppingList = async (newList) => {
  try{
    await addShoppingList(newList)
    showSnackbar('List added', 'success')
  } catch {
    showSnackbar('List not added','error')
  }
}

const updateList = async (updatedList) => {
  try{
    await editList(updatedList)
    showSnackbar('List updated','success')
  } catch (error) {
    showSnackbar('List not updated','error')
  }
}

const deleteList = async (deletedList) => {
  try{
    await removeList(deletedList)
    showSnackbar('List deleted','success')
  } catch (error) {
    showSnackbar('List not deleted','error')
  }
}

const showSnackbar = (text, color) => {
  snackbarText.value = text;
  snackbarColor.value = color;
  snackbar.value = true;
}

const updateDialog = () => {
  listFormDialog.value = false
}


</script>
