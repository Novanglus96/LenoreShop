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
          <span class="text-h5" v-if="props.isEdit == false">Add List</span>
          <span class="text-h5" v-else>Add List</span>
        </v-card-title>
        <v-card-text>
          <v-container>
            <v-row>
              <v-col cols="12" sm="6" md="4">
                <v-select
                  label="Store*"
                  :items="stores"
                  item-title="name"
                  item-value="id"
                  v-model="store_id.value.value"
                  :error-messages="store_id.errorMessage.value"
                ></v-select>
              </v-col>
            </v-row>
            <v-row>
              <v-col cols="12" sm="6" md="4">
                <v-text-field
                  label="List Name*"
                  v-model="name.value.value"
                  :error-messages="name.errorMessage.value"
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
  import { useStores } from "@/composables/storesComposable";
  import { useDisplay } from "vuetify";
  import { useField, useForm } from "vee-validate";

  const { handleSubmit } = useForm({
    validationSchema: {
      name(value) {
        if (value) return true;

        return "Must provide a list name.";
      },
    },
  });

  const name = useField("name");
  const id = useField("id");
  const store_id = useField("store_id");

  const { smAndDown } = useDisplay();
  const isMobile = smAndDown;

  const { stores } = useStores();

  const props = defineProps({
    listFormDialog: {
      type: Boolean,
      default: false,
    },
    isEdit: {
      type: Boolean,
      default: false,
    },
    passedFormData: Object,
  });

  const show = ref(props.listFormDialog);
  const emit = defineEmits(["addList", "editList", "updateDialog"]);

  const watchPassedFormData = () => {
    watchEffect(() => {
      if (props.passedFormData) {
        id.value.value = props.passedFormData.id;
        name.value.value = props.passedFormData.name;
        store_id.value.value = props.passedFormData.store_id
          ? props.passedFormData.store_id
          : null;
      }
    });
  };

  onMounted(() => {
    watchPassedFormData();
  });

  const submit = handleSubmit(values => {
    if (props.isEdit == false) {
      emit("addList", values);
    } else {
      emit("editList", values);
    }

    closeDialog();
  });

  const closeDialog = () => {
    emit("updateDialog", false);
    clearFormData();
  };

  const clearFormData = () => {
    id.value.value = props.passedFormData.id;
    name.value.value = props.passedFormData.name;
    store_id.value.value = props.passedFormData.store_id;
  };
</script>
