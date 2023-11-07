<template>
  <div class="items">
    <AddItemForm @form-submitted="createItem" />
    <ItemCard :items="items" :isLoading="isLoading" />
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
import ItemCard from '@/components/ItemCard.vue'
import AddItemForm from '@/components/AddItemForm.vue'
import { useItems } from '@/composables/itemsComposable'

const snackbar = ref(false);
const snackbarText = ref('');
const snackbarColor = ref('');
const snackbarTimeout = ref(1500);

const { items, isLoading, addItem } = useItems()

const createItem = async (newItem) => {
  try{
    await addItem(newItem)
    showSnackbar('Item added','success')
  } catch (error) {
    showSnackbar('Item not added','error')
  }
}

const showSnackbar = (text, color) => {
  snackbarText.value = text;
  snackbarColor.value = color;
  snackbar.value = true;
}

</script>
