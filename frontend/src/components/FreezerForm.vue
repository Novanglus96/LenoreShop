<template>
  <v-dialog
    v-model="show"
    persistent
    :width="isMobile ? undefined : '1024'"
    :fullscreen="isMobile"
  >
    <v-card>
      <form @submit.prevent="submit">
        <v-card-title>
          <span class="text-h5" v-if="props.isEdit == false">Add Freezer</span>
          <span class="text-h5" v-else>Edit Freezer</span>
        </v-card-title>
        <v-card-text>
          <v-container>
            <v-row>
              <v-col cols="12" sm="6" md="4">
                <v-text-field
                  label="Freezer Name*"
                  v-model="name.value.value"
                  :error-messages="name.errorMessage.value"
                ></v-text-field>
              </v-col>
              <v-col cols="12" sm="6" md="4">
                <v-text-field
                  label="Location"
                  placeholder="Garage"
                  v-model="location.value.value"
                  :error-messages="location.errorMessage.value"
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
          <v-btn color="blue-darken-1" variant="text" type="submit">Save</v-btn>
        </v-card-actions>
      </form>
    </v-card>
  </v-dialog>
</template>
<script setup>
  import { ref, defineEmits, defineProps, onMounted, watchEffect } from "vue";
  import { useDisplay } from "vuetify";
  import { useField, useForm } from "vee-validate";

  const { handleSubmit } = useForm({
    validationSchema: {
      name(value) {
        if (value) return true;

        return "Must provide a freezer name.";
      },
    },
  });

  const name = useField("name");
  const location = useField("location");
  const id = useField("id");

  const { smAndDown } = useDisplay();
  const isMobile = smAndDown;

  const props = defineProps({
    freezerFormDialog: {
      type: Boolean,
      default: false,
    },
    isEdit: {
      type: Boolean,
      default: false,
    },
    passedFormData: Object,
  });

  const show = ref(props.freezerFormDialog);
  const emit = defineEmits(["addFreezer", "editFreezer", "updateDialog"]);

  const watchPassedFormData = () => {
    watchEffect(() => {
      if (props.passedFormData) {
        id.value.value = props.passedFormData.id;
        name.value.value = props.passedFormData.name;
        location.value.value = props.passedFormData.location;
      }
    });
  };

  onMounted(() => {
    watchPassedFormData();
  });

  const submit = handleSubmit(values => {
    if (props.isEdit == false) {
      emit("addFreezer", values);
    } else {
      emit("editFreezer", values);
    }
    closeDialog();
  });

  const closeDialog = () => {
    emit("updateDialog", false);
    clearFormData();
  };

  const clearFormData = () => {
    id.value.value = null;
    name.value.value = null;
    location.value.value = null;
  };
</script>
