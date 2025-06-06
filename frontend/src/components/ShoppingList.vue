<template>
  <v-list
    density="compact"
    elevation="1"
    :bg-color="!purchased ? 'primary' : 'grey-darken-1'"
  >
    <div v-for="aisle in listitems" :key="aisle.id">
      <v-list-subheader color="white" inset>{{ aisle.name }}</v-list-subheader>
      <v-list-item
        v-for="item in aisle.listitems"
        :key="item.id"
        elevation="2"
        :variant="!purchased ? 'flat' : 'tonal'"
        :color="!purchased ? 'white' : 'grey-darken-2'"
      >
        <v-list-item-title>
          <span
            :class="
              item.purchased
                ? 'text-grey text-decoration-line-through'
                : 'text-black'
            "
          >
            {{ item.qty }} {{ item.item.name }}
          </span>
        </v-list-item-title>
        <v-list-item-subtitle>
          <span
            :class="
              item.purchased
                ? 'text-grey text-decoration-line-through'
                : 'text-black'
            "
          >
            {{ item.notes }}
          </span>
        </v-list-item-subtitle>
        <template v-slot:prepend>
          <v-btn variant="plain" :ripple="false" @click="purchaseItem(item)">
            <v-icon
              :icon="
                item.purchased
                  ? 'mdi-checkbox-marked-outline'
                  : 'mdi-checkbox-blank-outline'
              "
              :color="!item.purchased ? 'grey' : 'success'"
              flat
              size="x-large"
            ></v-icon>
          </v-btn>
        </template>
        <template v-slot:append>
          <v-btn
            icon="mdi-pencil"
            variant="plain"
            :ripple="false"
            @click="selectedItem(item)"
          ></v-btn>
          <ListItemForm
            v-model="listItemFormDialog"
            @edit-list-item="editListItem"
            @update-dialog="updateDialog"
            :isEdit="true"
            :passedFormData="passedFormData"
            :key="item.id"
          />
          <v-btn
            icon="mdi-delete"
            variant="plain"
            :ripple="false"
            @click="selectedDeleteItem(item)"
          ></v-btn>
          <v-dialog v-model="deleteDialog" width="auto" :key="item.id">
            <v-card>
              <v-card-text>
                Delete item "{{ passedDeleteData.name }}" from list?
              </v-card-text>
              <v-card-actions>
                <v-btn color="primary" @click="deleteDialog = false">No</v-btn>
                <v-btn color="primary" @click="deleteItem(passedDeleteData)">
                  Yes
                </v-btn>
              </v-card-actions>
            </v-card>
          </v-dialog>
        </template>
      </v-list-item>
      <v-list-item
        v-if="aisle.listitems.length == 0"
        elevation="2"
        :variant="!purchased ? 'flat' : 'tonal'"
        :color="!purchased ? 'white' : 'grey-darken-2'"
      >
        <v-list-item-title>
          <span class="text-black font-italic">No Items</span>
        </v-list-item-title>
      </v-list-item>
    </div>
    <div v-if="listitems.length == 0">
      <v-list-item elevation="2" variant="flat" color="white">
        <v-list-item-title>
          <span class="text-black font-italic">No Items</span>
        </v-list-item-title>
      </v-list-item>
    </div>
  </v-list>
</template>

<script setup>
  import { defineProps, defineEmits, ref } from "vue";
  import ListItemForm from "@/components/ListItemForm.vue";
  //import { useFullShoppingList } from '@/composables/listsComposable'

  const emit = defineEmits(["itemPurchased", "editListItem", "deleteListItem"]);
  const passedFormData = ref({
    id: 0,
    qty: 1,
    purchased: false,
    notes: "",
    item_id: 0,
    aisle_id: 0,
    shopping_list_id: 0,
  });
  const passedDeleteData = ref({
    id: 0,
    name: null,
  });
  const listItemFormDialog = ref(false);
  const deleteDialog = ref(false);
  const updateDialog = () => {
    listItemFormDialog.value = false;
  };
  const selectedDeleteItem = item => {
    passedDeleteData.value.id = item.id;
    passedDeleteData.value.name = item.item.name;
    deleteDialog.value = true;
  };
  const selectedItem = item => {
    passedFormData.value.id = item.id;
    passedFormData.value.qty = item.qty;
    passedFormData.value.purchased = item.purchased;
    passedFormData.value.notes = item.notes;
    passedFormData.value.item = item.item_id;
    passedFormData.value.aisle_id = item.aisle_id;
    passedFormData.value.shopping_list_id = item.shopping_list_id;

    listItemFormDialog.value = true;
  };
  const editListItem = async item => {
    emit("editListItem", item);
  };
  const purchaseItem = async item => {
    const itemData = {
      id: item.id,
      qty: item.qty,
      purchased: !item.purchased,
      notes: item.notes,
      purch_date: null,
      item: item.item_id,
      aisle_id: item.aisle_id,
      shopping_list_id: item.shopping_list_id,
    };
    emit("itemPurchased", itemData);
  };
  const deleteItem = async item => {
    const itemData = {
      id: item.id,
    };
    emit("deleteListItem", itemData);
    deleteDialog.value = false;
  };
  defineProps({
    listitems: Object,
    purchased: Boolean,
  });
</script>
