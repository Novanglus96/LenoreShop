<template>
  <v-dialog v-model="show" persistent width="1024">
    <v-card>
      <v-card-title>
        <span class="text-h5" v-if="props.isEdit == false">Add Store</span>
        <span class="text-h5" v-else>Edit Store</span>
      </v-card-title>
      <v-card-text>
        <v-container>
          <v-row>
            <v-col cols="12" sm="6" md="4">
              <v-text-field
                label="Store Name*"
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
        <v-btn color="blue-darken-1" variant="text" @click="closeDialog">
          Close
        </v-btn>
        <v-btn color="blue-darken-1" variant="text" @click="submitForm">
          Save
        </v-btn>
      </v-card-actions>
    </v-card>
  </v-dialog>
</template>
<script setup>
import { ref, defineEmits, defineProps, onMounted, watchEffect } from "vue";

const formData = ref({
  name: "",
});

const props = defineProps({
  storeFormDialog: {
    type: Boolean,
    default: false,
  },
  isEdit: {
    type: Boolean,
    default: false,
  },
  passedFormData: Array,
});

const show = ref(props.storeFormDialog);
const emit = defineEmits(["addStore", "editStore", "updateDialog"]);

const watchPassedFormData = () => {
  watchEffect(() => {
    if (props.passedFormData) {
      formData.value.id = props.passedFormData.id;
      formData.value.name = props.passedFormData.name;
    }
  });
};

onMounted(() => {
  watchPassedFormData();
});

const submitForm = async () => {
  if (props.isEdit == false) {
    emit("addStore", formData.value);
  } else {
    emit("editStore", formData.value);
  }
  closeDialog();
};

const closeDialog = () => {
  emit("updateDialog", false);
};
</script>
