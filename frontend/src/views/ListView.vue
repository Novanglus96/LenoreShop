<template>
  <div class="lists">
    <v-btn density="compact" @click="listItemFormDialog = true">Add Item</v-btn>
    <ListItemForm
      v-model="listItemFormDialog"
      @add-list-item="createListItem"
      @update-dialog="updateDialog"
      :passedFormData="blankFormData"
      :isEdit="false"
      :key="-1"
    />
    <v-container>
      <v-row dense v-if="!isLoading">
        <v-col cols="12">
          <h2 class="text-h6 text-primary ps-4">{{ fullshoppinglist.name }}</h2>
          <h2 class="text-subtitle-1 text-info ps-4">
            {{ fullshoppinglist.store.name }}
          </h2>
          <h2 class="text-subtitle-2 text-grey ps-4">
            {{ fullshoppinglist.totalpurchased }} of
            {{ fullshoppinglist.totalitems }} purchased
          </h2>
        </v-col>
      </v-row>
      <v-row dense>
        <v-col class="d-flex justify-center">
          <v-dialog v-model="clear_purchased_dialog" max-width="400" persistent>
            <template v-slot:activator="{ props: activatorProps }">
              <v-btn
                density="compact"
                variant="outlined"
                prepend-icon="mdi-delete-sweep-outline"
                v-bind="activatorProps"
              >
                Clear Purchased
              </v-btn>
            </template>
            <v-card
              prepend-icon="mdi-alert"
              text="Are you sure you want to clear purchased items?"
              title="Confirm Clear Purchased"
            >
              <template v-slot:actions>
                <v-spacer></v-spacer>
                <v-btn @click="clear_purchased_dialog = false">No</v-btn>
                <v-btn @click="clearPurchasedListFunction(fullshoppinglist.id)">
                  Yes
                </v-btn>
              </template>
            </v-card>
          </v-dialog>
          <v-dialog v-model="clear_full_dialog" max-width="400" persistent>
            <template v-slot:activator="{ props: activatorProps }">
              <v-btn
                density="compact"
                variant="outlined"
                prepend-icon="mdi-delete-sweep-outline"
                v-bind="activatorProps"
              >
                Clear All
              </v-btn>
            </template>
            <v-card
              prepend-icon="mdi-alert"
              text="Are you sure you want to clear all items?"
              title="Confirm Clear All"
            >
              <template v-slot:actions>
                <v-spacer></v-spacer>
                <v-btn @click="clear_full_dialog = false">No</v-btn>
                <v-btn @click="clearListFunction(fullshoppinglist.id)">
                  Yes
                </v-btn>
              </template>
            </v-card>
          </v-dialog>
        </v-col>
      </v-row>
      <v-row dense v-if="!isLoading">
        <v-col cols="12">
          <ShoppingList
            @edit-list-item="editListItem"
            @delete-list-item="removeListItem"
            @item-purchased="purchaseItem"
            :listitems="fullshoppinglist.aisles"
            :purchased="false"
          />
        </v-col>
      </v-row>
      <v-row dense v-else>
        <v-col cols="12">
          <v-skeleton-loader type="list-item-two-line"></v-skeleton-loader>
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
          <ShoppingList
            @edit-list-item="editListItem"
            @item-purchased="purchaseItem"
            :listitems="fullshoppinglist.purchased_aisles"
            :purchased="true"
          />
        </v-col>
      </v-row>
      <v-row dense v-else>
        <v-col cols="12">
          <v-skeleton-loader type="list-item-two-line"></v-skeleton-loader>
          <v-skeleton-loader
            type="list-item-avatar-two-line"
          ></v-skeleton-loader>
        </v-col>
      </v-row>
    </v-container>
  </div>
</template>

<script setup>
  import { ref } from "vue";
  import ShoppingList from "@/components/ShoppingList.vue";
  import ListItemForm from "@/components/ListItemForm.vue";
  import { useFullShoppingList } from "@/composables/listsComposable";
  import { useMainStore } from "@/stores/main";

  const store = useMainStore();
  const clear_full_dialog = ref(false);
  const clear_purchased_dialog = ref(false);
  const listItemFormDialog = ref(false);
  const updateDialog = () => {
    listItemFormDialog.value = false;
  };

  const blankFormData = ref({
    id: 0,
    qty: 1,
    purchased: false,
    notes: "",
    item: null,
    aisle_id: null,
    shopping_list_id: 0,
  });

  const {
    fullshoppinglist,
    isLoading,
    addListItem,
    deleteListItem,
    updateListItem,
    clearList,
    clearPurchasedList,
  } = useFullShoppingList(store.list_id);

  const editListItem = async listItem => {
    await updateListItem(listItem);
  };

  const createListItem = async newListItem => {
    await addListItem(newListItem);
  };

  const removeListItem = async deletedListItem => {
    await deleteListItem(deletedListItem);
  };

  const purchaseItem = async listItem => {
    await updateListItem(listItem);
  };

  const clearListFunction = async shoppinglistID => {
    await clearList(shoppinglistID);
    clear_full_dialog.value = false;
  };

  const clearPurchasedListFunction = async shoppinglistID => {
    await clearPurchasedList(shoppinglistID);
    clear_purchased_dialog.value = false;
  };
</script>
