<template>
  <div class="lists">
    <v-btn density="compact" @click="listItemFormDialog = true">Add Item</v-btn>
    <ListItemForm v-model="listItemFormDialog" @add-list-item="createListItem" @update-dialog="updateDialog" :isEdit="false"/>
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
          <v-btn density="compact" variant="outlined" prepend-icon="mdi-delete-sweep-outline" @click="clearPurchasedListFunction(fullshoppinglist.id)">Clear Purchased</v-btn><v-btn density="compact" variant="outlined" prepend-icon="mdi-delete-sweep-outline" @click="clearListFunction(fullshoppinglist.id)">Clear All</v-btn>
        </v-col>
      </v-row>
      <v-row dense v-if="!isLoading">
        <v-col cols="12">
          <ShoppingList @edit-list-item="editListItem" @item-purchased="purchaseItem" :listitems="fullshoppinglist.aisles" :purchased="false"/>
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
          <ShoppingList @edit-list-item="editListItem" @item-purchased="purchaseItem" :listitems="fullshoppinglist.purchased_aisles" :purchased="true"/>
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
  </div>
</template>

<script setup>
import { ref } from 'vue'
import ShoppingList from '@/components/ShoppingList.vue'
import ListItemForm from '@/components/ListItemForm.vue'
import { useFullShoppingList } from '@/composables/listsComposable'
import { useMainStore } from '@/stores/main'

const store = useMainStore();
const listItemFormDialog = ref(false);
const updateDialog = () => {
  listItemFormDialog.value = false
}

const { fullshoppinglist, isLoading, addListItem, updateListItem, clearList, clearPurchasedList } = useFullShoppingList(store.list_id)

const editListItem = async (listItem) => {
  await updateListItem(listItem)
}

const createListItem = async (newListItem) => {
  await addListItem(newListItem)
}

const purchaseItem = async (listItem) => {
  await updateListItem(listItem)
}

const clearListFunction = async (shoppinglistID) => {
  await clearList(shoppinglistID)
}

const clearPurchasedListFunction = async (shoppinglistID) => {
  await clearPurchasedList(shoppinglistID)
}

</script>
