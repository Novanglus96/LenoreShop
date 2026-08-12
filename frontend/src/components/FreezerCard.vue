<template>
  <v-card color="primary" variant="outlined" class="mb-2">
    <v-card-title class="text-h6">
      {{ freezer.name }}
      <span v-if="freezer.location" class="text-caption text-grey">
        &mdash; {{ freezer.location }}
      </span>
    </v-card-title>

    <v-card-actions>
      <v-btn
        size="x-small"
        variant="outlined"
        @click="showContents(freezer.id)"
      >
        contents
      </v-btn>
      <v-btn size="x-small" variant="outlined" @click="emit('select', freezer)">
        edit
      </v-btn>
      <v-btn
        size="x-small"
        variant="outlined"
        @click="emit('selectDelete', freezer)"
      >
        delete
      </v-btn>
    </v-card-actions>
  </v-card>
</template>

<script setup>
  import { defineProps, defineEmits } from "vue";
  import { useMainStore } from "@/stores/main";
  import { useRouter } from "vue-router";

  // Both dialogs live in FreezerView, outside its v-for. Rendering them here
  // would create one hidden dialog per card, which is what caused the mobile
  // black screen in ShoppingList.vue.
  const emit = defineEmits(["select", "selectDelete"]);

  defineProps({
    freezer: Object,
  });

  const router = useRouter();

  const showContents = async freezer_id => {
    const store = useMainStore();
    store.freezer_id = freezer_id;
    router.push("/freezer");
  };
</script>
