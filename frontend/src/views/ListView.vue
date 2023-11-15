<template>
  <div class="lists">
    <AddListItemForm @form-submitted="createListItem" :items="items" :aisles="aisles"/>
    <v-container>
      <v-row dense v-if="!isLoading">
        <v-col cols="12">
          <h2 class="text-h6 text-primary ps-4">{{ fullshoppinglist.name }}</h2>
          <h2 class="text-subtitle-1 text-info ps-4">{{ fullshoppinglist.store.name }}</h2>
          <h2 class="text-subtitle-2 text-grey ps-4">{{ fullshoppinglist.totalpurchased }} of {{ fullshoppinglist.totalitems }} purchased</h2>
        </v-col>
      </v-row>
      <v-row dense>
        <v-col class="d-flex justify-center">
          <v-btn density="compact" variant="outlined" prepend-icon="mdi-delete-sweep-outline">Clear Purchased</v-btn><v-btn density="compact" variant="outlined" prepend-icon="mdi-delete-sweep-outline">Clear All</v-btn>
        </v-col>
      </v-row>
      <v-row dense v-if="!isLoading">
        <v-col cols="12">
          <ShoppingList @item-purchased="purchaseItem" :listitems="fullshoppinglist.aisles" :purchased="false"/>
        </v-col>
      </v-row>
      <v-row dense v-else>
        <v-col cols="12">
          <v-skeleton-loader
            type="list-item-two-line"
          ></v-skeleton-loader>
          <v-skeleton-loader
            type="list-item-avatar-two-line"
          ></v-skeleton-loader>
        </v-col>
      </v-row>
      <v-row dense>
        <v-col cols="12">
          <h2 class="text-subtitle-1 text-info ps-4">Purchased Items</h2>
        </v-col>
      </v-row>
      <v-row dense v-if="!isLoading">
        <v-col cols="12">
          <ShoppingList @item-purchased="purchaseItem" :listitems="fullshoppinglist.purchased_aisles" :purchased="true"/>
        </v-col>
      </v-row>
      <v-row dense v-else>
        <v-col cols="12">
          <v-skeleton-loader
            type="list-item-two-line"
          ></v-skeleton-loader>
          <v-skeleton-loader
            type="list-item-avatar-two-line"
          ></v-skeleton-loader>
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
const { fullshoppinglist, isLoading, addListItem, updateListItem } = useFullShoppingList(store.list_id)

const createListItem = async (newListItem) => {
  try{
    await addListItem(newListItem)
    showSnackbar('Item added', 'success')
  } catch (error) {
    showSnackbar('Item not added', 'error')
  }
}

const purchaseItem = async (listItem) => {
  try{
    await updateListItem(listItem)
  } catch {
    showSnackbar('Item not purchased', 'error')
  }
}

const showSnackbar = (text, color) => {
  snackbarText.value = text;
  snackbarColor.value = color;
  snackbar.value = true;
}

</script>
