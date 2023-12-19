<template>
    <v-dialog
      v-model="show"
      persistent
      width="1024"
    >
      <v-card>
        <v-card-title>
          <span class="text-h5" v-if="props.isEdit == false">Add Aisle</span>
          <span class="text-h5" v-else>Edit Aisle</span>
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
                  label="Aisle Name*"
                  required
                  v-model="formData.name"
                ></v-text-field>
              </v-col>
            </v-row>
            <v-row v-if="props.isEdit == true">
              <v-col
                cols="12"
                sm="6"
                md="4"
              >
                <v-text-field
                  label="Order*"
                  v-model="formData.order"
                  type="number"
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
  const props = defineProps({
    aisleFormDialog: {
      type: Boolean,
      default: false
    },
    isEdit: {
      type: Boolean,
      default: false
    },
    passedFormData: Array
  })

  const mainstore = useMainStore();
  const show = ref(props.aisleFormDialog)
  const emit = defineEmits(['addAisle', 'editAisle', 'updateDialog'])
  const formData = ref({
        id: 0,
        name: '',
        store_id: mainstore.store_id,
        order: 1,
      })

  const watchPassedFormData = () => {
    watchEffect(() => {
      if (props.passedFormData) {
        formData.value.id = props.passedFormData.id;
        formData.value.name = props.passedFormData.name;
        formData.value.store_id = props.passedFormData.store_id;
        formData.value.order = props.passedFormData.order;
      }
    })
  }

  onMounted(() => {
    watchPassedFormData();
  })

  const submitForm = async () => {
    if (props.isEdit == false) {
      emit('addAisle', formData.value)
    } else {
      emit('editAisle', formData.value)
    }
    
    closeDialog()
  }

  const closeDialog = () => {
    emit('updateDialog', false);
  };
</script>