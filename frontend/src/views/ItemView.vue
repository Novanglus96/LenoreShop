<template>
  <div class="items">
    <v-btn density="compact" @click="itemFormDialog = true">Add Item</v-btn>
    <ItemForm
      v-model="itemFormDialog"
      @add-item="createItem"
      @edit-item="updateItem"
      :isEdit="false"
      @update-dialog="updateDialog"
      :passedFormData="blankFormData"
    />
    <v-container>
      <v-row dense v-if="!isLoading">
        <v-col cols="12">
          <ItemCard
            v-for="item in items.items"
            :key="item.id"
            :item="item"
            @edit-item="updateItem"
            @remove-item="deleteItem"
          />
        </v-col>
      </v-row>
      <v-row dense v-else>
        <v-col cols="12">
          <v-skeleton-loader type="card" color="primary"></v-skeleton-loader>
        </v-col>
      </v-row>
      <v-row dense v-if="!isLoading">
        <v-col cols="12">
          <v-pagination
            v-model="currentPage"
            :length="items.total_pages"
            @update:model-value="handlePageChange"
          ></v-pagination>
        </v-col>
      </v-row>
    </v-container>
  </div>
</template>

<script setup>
  import { ref } from "vue";
  import ItemCard from "@/components/ItemCard.vue";
  import ItemForm from "@/components/ItemForm.vue";
  import { useItems } from "@/composables/itemsComposable";
  import { useItemStore } from "@/stores/item";

  const itemstore = useItemStore();
  const itemFormDialog = ref(false);

  const { items, isLoading, addItem, editItem, removeItem } = useItems(false);
  const currentPage = ref(items.page);

  const createItem = async newItem => {
    await addItem(newItem);
  };

  const updateItem = async updatedItem => {
    await editItem(updatedItem);
  };

  const deleteItem = async deletedItem => {
    await removeItem(deletedItem);
  };

  const updateDialog = () => {
    itemFormDialog.value = false;
  };

  const handlePageChange = page => {
    itemstore.pageinfo.page = page;
  };

  const blankFormData = ref({
    id: null,
    name: null,
    matches: null,
  });
</script>
