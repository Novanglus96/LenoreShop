<template>
  <v-dialog
    v-model="show"
    persistent
    width="1024"
  >
    <v-card>
      <v-card-title>
        <span class="text-h5">Add Item</span>
      </v-card-title>
      <v-card-text>
        <v-container>
          <v-row>
            <v-col
              cols="12"
              sm="6"
              md="4"
            >
              <v-text-field
                label="Item Name*"
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

  const formData = ref({
        if: 0,
        name: '',
        matches: '',
      })

   const props = defineProps({
    itemFormDialog: {
      type: Boolean,
      default: false
    },
    isEdit: {
      type: Boolean,
      default: false
    },
    passedFormData: Array
  })

  const show = ref(props.itemFormDialog)
  const emit = defineEmits(['addItem', 'editItem', 'updateDialog'])
 
  const watchPassedFormData = () => {
      watchEffect(() => {
        formData.value.id = props.passedFormData.id;
        formData.value.name = props.passedFormData.name;
        formData.value.matches = props.passedFormData.matches;
      })
    }

    onMounted(() => {
      watchPassedFormData();
    })

    const submitForm = async () => {
      if (props.isEdit == false) {
        emit('addItem', formData.value)
      } else {
        emit('editItem', formData.value)
      }
      
      closeDialog()
    }

    const closeDialog = () => {
      emit('updateDialog', false);
    };
  
</script>