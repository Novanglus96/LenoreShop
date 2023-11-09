<template>
      <v-container>
        <v-row dense>
            <v-col cols="12">
                <span class="text-h4">{{ props.list.name }}</span> <v-btn icon="mdi-pencil" flat @click="editMode = !editMode" v-if="!editMode"></v-btn><v-btn icon="mdi-cancel" flat @click="editMode = !editMode" v-if="editMode"></v-btn><br/>
                <span class="text-caption font-italic">{{ props.list.store.name }}</span>
            </v-col>
        </v-row>
         <v-row dense>
              <v-col cols="12">
                <v-card 
                  density="compact"
                  v-for="aisle in props.list.aisles"
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
      </v-container>
</template>

<script setup>
  import { defineProps, ref } from 'vue';

  const editMode = ref(false);
  const props = defineProps({
    list: Object,
    isLoading: Boolean
  })

</script>