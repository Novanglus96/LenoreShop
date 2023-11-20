<template>
  <div class="lists">
    <ListForm @form-submitted="createShoppingList" :stores="stores"/>
    <v-container>
      <v-row dense v-if="!isLoading">
        <v-col cols="12">
          <ListCard v-for="shoppinglist in shoppinglists" :key="shoppinglist.id" :list="shoppinglist" />
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
