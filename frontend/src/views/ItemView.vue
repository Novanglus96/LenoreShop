<template>
  <div class="items">
    <v-btn density="compact" @click="itemFormDialog = true">Add Item</v-btn>
    <ItemForm v-model="itemFormDialog" @add-item="createItem" @edit-item="updateItem" :isEdit="false" @update-dialog="updateDialog"/>
    <v-container>
      <v-row dense v-if="!isLoading">
        <v-col cols="12">
          <ItemCard v-for="item in items" :key="item.id" :item="item" @edit-item="updateItem" @remove-item="deleteItem"/>
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
import ItemCard from '@/components/ItemCard.vue'
import ItemForm from '@/components/ItemForm.vue'
import { useItems } from '@/composables/itemsComposable'

const itemFormDialog = ref(false);
const snackbar = ref(false);
const snackbarText = ref('');
const snackbarColor = ref('');
const snackbarTimeout = ref(1500);

const { items, isLoading, addItem, editItem, removeItem } = useItems()

const createItem = async (newItem) => {
  try{
    await addItem(newItem)
    showSnackbar('Item added','success')
  } catch (error) {
    showSnackbar('Item not added','error')
  }
}

const updateItem = async (updatedItem) => {
  try{
    await editItem(updatedItem)
    showSnackbar('Item updated','success')
  } catch (error) {
    showSnackbar('Item not updated','error')
  }
}

const deleteItem = async (deletedItem) => {
  try{
    await removeItem(deletedItem)
    showSnackbar('Item deleted','success')
  } catch (error) {
    showSnackbar('Item not deleted','error')
  }
}

const showSnackbar = (text, color) => {
  snackbarText.value = text;
  snackbarColor.value = color;
  snackbar.value = true;
}

const updateDialog = () => {
  itemFormDialog.value = false
}

</script>
