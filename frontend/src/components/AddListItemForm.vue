<template>
    <v-dialog
      v-model="dialog"
      persistent
      width="1024"
    >
      <template v-slot:activator="{ props }">
        <v-btn v-bind="props">Add Item</v-btn>
      </template>
      <v-card>
        <v-card-title>
          <span class="text-h5">Add Item</span>
        </v-card-title>
        <v-card-text>
          <v-container>
            <v-row>
              <v-col
                sm="6"
                md="4"
              >
                <v-text-field
                  label="qty"
                  v-model="formData.qty"
                  variant="outlined"
                  type="number"
                ></v-text-field>
              </v-col>
              <v-col
                sm="6"
                md="4"
              >
                <v-select
                    label="Item*"
                    required
                    :items="props.items"
                    item-title="name"
                    item-value="id"
                    v-model="formData.item_id"  
                ></v-select>
              </v-col>
              <v-col
                sm="6"
                md="4"
              >
                <v-select
                    label="Aisle*"
                    required
                    :items="props.aisles"
                    item-title="name"
                    item-value="id"
                    v-model="formData.aisle_id"  
                ></v-select>
              </v-col>
            </v-row>
            <v-row>
              <v-col
                cols="12"
                sm="6"
                md="4"
              >
                <v-text-field
                  label="notes"
                  v-model="formData.notes"
                  variant="outlined"
                  type="text"
                ></v-text-field>
              </v-col>
            </v-row>
          </v-container>
          <small>*indicates required field</small>
        </v-card-text>
        <v-card-actions>
          <v-spacer></v-spacer>
          <v-btn
            color="blue-darken-1"
            variant="text"
            @click="dialog = false"
          >
            Close
          </v-btn>
          <v-btn
            color="blue-darken-1"
            variant="text"
            @click="submitForm"
          >
            Save
          </v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>
    
</template>
<script setup>
  import { ref, defineEmits, defineProps } from 'vue';
  import { useMainStore } from '@/stores/main';

  const store = useMainStore()

  const props = defineProps({
    items: Array,
    aisles: Array
  })

  const dialog = ref(false)
  const emit = defineEmits(['formSubmitted'])
  const formData = ref({
        qty: 1,
        purchased: false,
        notes: '',
        item_id: null,
        aisle_id: 0,
        shopping_list_id: store.list_id,
      })

  const submitForm = async () => {
    emit('formSubmitted', formData.value)
    dialog.value = false;
  }

</script>