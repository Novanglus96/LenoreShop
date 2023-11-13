<template>
  <div class="lists">
    <AddListForm @form-submitted="createShoppingList" :stores="stores"/>
    <v-container>
      <ListCard v-for="shoppinglist in shoppinglists" :key="shoppinglist.id" :list="shoppinglist" :isLoading="isLoading"/>
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
import AddListForm from '@/components/AddListForm.vue'
import { useShoppingLists } from '@/composables/listsComposable'
import { useStores } from '@/composables/storesComposable'

const snackbar = ref(false);
const snackbarText = ref('');
const snackbarColor = ref('');
const snackbarTimeout = ref(1500);

const { shoppinglists, isLoading, addShoppingList } = useShoppingLists()
const { stores } = useStores()

const createShoppingList = async (newList) => {
  try{
    await addShoppingList(newList)
    showSnackbar('List added', 'success')
  } catch {
    showSnackbar('List not added','error')
  }
}

const showSnackbar = (text, color) => {
  snackbarText.value = text;
  snackbarColor.value = color;
  snackbar.value = true;
}

</script>
