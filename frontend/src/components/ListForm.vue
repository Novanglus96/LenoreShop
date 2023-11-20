<template>
    <v-dialog
      v-model="dialog"
      persistent
      width="1024"
    >
      <template v-slot:activator="{ props }">
        <v-btn v-bind="props">Add List</v-btn>
      </template>
      <v-card>
        <v-card-title>
          <span class="text-h5">Add List</span>
        </v-card-title>
        <v-card-text>
          <v-container>
            <v-row>
              <v-col
                cols="12"
                sm="6"
                md="4"
              >
                <v-select
                    label="Store*"
                    required
                    :items="props.stores"
                    item-title="name"
                    item-value="id"
                    v-model="formData.store_id"  
                >
                </v-select>
              </v-col>
            </v-row>
            <v-row>
              <v-col
                cols="12"
                sm="6"
                md="4"
              >
                <v-text-field
                  label="List Name*"
                  required
                  v-model="formData.name"
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

  const mainstore = useMainStore();
  const dialog = ref(false)
  const formData = ref({
        name: '',
        store_id: mainstore.store_id,
      })
  const props = defineProps({
    stores: Array
  })
  

  const emit = defineEmits(['formSubmitted'])
  const submitForm = async () => {
    emit('formSubmitted', formData.value)
    dialog.value = false;
  }
</script>