<template>
  <div class="items">
    <AddItemForm @form-submitted="createItem" />
    <v-container>
      <v-row dense v-if="!isLoading">
        <v-col cols="12">
          <ItemCard v-for="item in items" :key="item.id" :item="item" />
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
