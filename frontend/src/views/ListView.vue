<template>
  <div class="lists">
    <AddListItemForm @form-submitted="createListItem" :items="items" :aisles="aisles"/>
    <ShoppingList :list="fullshoppinglist" :isLoading="isLoading"/>
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
import ShoppingList from '@/components/ShoppingList.vue'
import AddListItemForm from '@/components/AddListItemForm.vue'
import { useFullShoppingList } from '@/composables/listsComposable'
import { useItems } from '@/composables/itemsComposable'
import { useAisles } from '@/composables/aislesComposable'
import { useMainStore } from '@/stores/main'

const store = useMainStore();
const snackbar = ref(false);
const snackbarText = ref('');
const snackbarColor = ref('');
const snackbarTimeout = ref(1500);

const { aisles } = useAisles(store.store_id)
const { items } = useItems()
const { fullshoppinglist, isLoading, addListItem } = useFullShoppingList(store.list_id)

const createListItem = async (newListItem) => {
  try{
    await addListItem(newListItem)
    showSnackbar('Item added', 'success')
  } catch (error) {
    showSnackbar('Item not added', 'error')
  }
}

const showSnackbar = (text, color) => {
  snackbarText.value = text;
  snackbarColor.value = color;
  snackbar.value = true;
}

</script>
