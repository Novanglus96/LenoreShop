<template>
      <v-container>
        <v-row dense>
            <v-col cols="12">
                <span class="text-h4">{{ getShoppingListFull.name }}</span> <v-btn icon="mdi-pencil" flat @click="editMode = !editMode" v-if="!editMode"></v-btn><v-btn icon="mdi-cancel" flat @click="editMode = !editMode" v-if="editMode"></v-btn><br/>
                <span class="text-caption font-italic">{{ getShoppingListFull.store.name }}</span>
            </v-col>
        </v-row>
         <v-row dense>
              <v-col cols="12">
                <v-card 
                  density="compact"
                  v-for="aisle in getShoppingListFull.aisles"
                  :key="aisle.id"
                  >
                  <v-card-item>
                    <v-card-title>{{ aisle.name }}</v-card-title>
                  </v-card-item>
                  <v-card-text>
                    <v-table density="compact">
                      <tbody>
                        <tr
                          v-for="item in aisle.listitems"
                          :key="item.id"
                        >
                          <td width="25%"><span v-if="!editMode">{{ item.qty }}</span><v-text-field label="qty" v-if="editMode" v-model="item.qty" variant="outlined" type="number"></v-text-field></td>
                          <td><span>{{ item.item.name }}</span><br /><span class="text-caption font-italic" v-if="!editMode">{{ item.notes }}</span><v-text-field label="note" v-if="editMode" v-model="item.notes" variant="outlined" type="text"></v-text-field></td>
                          <td width="25%"><v-btn icon="mdi-check" flat v-if="!editMode"></v-btn><v-btn icon="mdi-content-save" flat v-if="editMode"></v-btn><v-btn icon="mdi-delete" flat v-if="editMode"></v-btn></td>
                        </tr>
                      </tbody>
                    </v-table>
                  </v-card-text>
                </v-card>
              </v-col>
            </v-row>
        <v-snackbar
          v-model="snackbar"
          :color="snackbarColor"
          :timeout="snackbarTimeout"
          content-class="centered-text"
        >
          {{ snackbarText }}
        </v-snackbar>
      </v-container>
</template>

<script setup>
  import { computed, ref } from 'vue';
  import { useMainStore } from '@/stores/main';

  const editMode = ref(false);
  const snackbar = ref(false);
  const snackbarText = ref('');
  const snackbarColor = ref('');
  const snackbarTimeout = ref(1500);
  
  const mainstore = useMainStore();
  const getShoppingListFull = computed(() => {
    return mainstore.getShoppingListFull;
  })

</script>