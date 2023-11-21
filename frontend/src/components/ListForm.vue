<template>
  <v-dialog
    v-model="show"
    persistent
    width="1024"
  >
    <v-card v-if="formData">
      <v-card-title>
        <span class="text-h5" v-if="props.isEdit == false">Add List</span>
        <span class="text-h5" v-else>Add List</span>
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
                  :items="stores"
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
          @click="closeDialog"
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
  import { ref, defineEmits, defineProps, onMounted, watchEffect } from 'vue';
  import { useMainStore } from '@/stores/main';
  import { useStores } from '@/composables/storesComposable'


  const { stores } = useStores()
  const mainstore = useMainStore();
  const formData = ref({
        id: 0,
        name: '',
        store_id: mainstore.store_id,
      })
  
  const props = defineProps({
    listFormDialog: {
      type: Boolean,
      default: false
    },
    isEdit: {
      type: Boolean,
      default: false
    },
    passedFormData: Array
  })

  const show = ref(props.listFormDialog)
  const emit = defineEmits(['addList', 'editList', 'updateDialog'])
 
  const watchPassedFormData = () => {
      watchEffect(() => {
        formData.value.id = props.passedFormData.id;
        formData.value.name = props.passedFormData.name;
        formData.value.store_id = props.passedFormData.store_id;
      })
    }

    onMounted(() => {
      watchPassedFormData();
    })

    const submitForm = async () => {
      if (props.isEdit == false) {
        emit('addList', formData.value)
      } else {
        emit('editList', formData.value)
      }
      
      closeDialog()
    }

    const closeDialog = () => {
      emit('updateDialog', false);
    };
</script>