<template>
    <v-dialog
      v-model="dialog"
      persistent
      width="1024"
    >
      <template v-slot:activator="{ props }">
        <v-btn v-bind="props">Add Aisle</v-btn>
      </template>
      <v-card>
        <v-card-title>
          <span class="text-h5">Add Aisle</span>
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
                    :items="getStores"
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
                  label="Aisle Name*"
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
      <v-snackbar
        v-model="snackbar"
        :color="snackbarColor"
        :timeout="snackbarTimeout"
        content-class="centered-text"
      >
        {{ snackbarText }}
      </v-snackbar>
    </v-dialog>
    
</template>
<script setup>
  import { ref, computed } from 'vue';
  import { useMainStore } from '@/stores/main';

  const snackbar = ref(false);
  const snackbarText = ref('');
  const snackbarColor = ref('');
  const snackbarTimeout = ref(1500);
  const mainstore = useMainStore();
  const dialog = ref(false)
  const formData = ref({
        name: '',
        store_id: mainstore.store_id,
        order: 1,
      })
  const getStores = computed(() => {
    return mainstore.getStores;
  })
  
  const submitForm = async () => {
    try {
      mainstore.addAisle(formData.value);
      dialog.value = false;
      showSnackbar('Aisle added successfully!', 'success');
    } catch (error) {
      // Handle errors (e.g., show an error message)
      console.log('Error:', error);
      showSnackbar('Aisle not added!', 'error');
    }
  };
  const showSnackbar = (text, color) => {
    snackbarText.value = text;
    snackbarColor.value = color;
    snackbar.value = true;
  }
</script>