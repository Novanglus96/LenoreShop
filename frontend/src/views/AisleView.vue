<template>
  <div class="aisles">
    <v-btn density="compact" @click="aisleFormDialog = true">Add Aisle</v-btn>
    <AisleForm
      v-model="aisleFormDialog"
      @add-aisle="createAisle"
      :isEdit="false"
      @update-dialog="updateDialog"
      :passedFormData="blankFormData"
    />
    <v-container fluid class="pa-0 pa-sm-2">
      <v-row dense v-if="!isLoading">
        <v-col cols="12">
          <draggable
            v-model="sortableAisles"
            item-key="id"
            handle=".drag-handle"
            @end="onReorder"
          >
            <template #item="{ element }">
              <AisleCard
                :aisle="element"
                :key="element.id"
                @edit-aisle="updateAisle"
                @remove-aisle="deleteAisle"
              />
            </template>
          </draggable>
          <AisleCard
            v-if="uncategorizedAisle"
            :aisle="uncategorizedAisle"
            :key="uncategorizedAisle.id"
            @edit-aisle="updateAisle"
            @remove-aisle="deleteAisle"
          />
        </v-col>
      </v-row>
      <v-row dense v-else>
        <v-col cols="12">
          <v-skeleton-loader type="card" color="primary"></v-skeleton-loader>
        </v-col>
      </v-row>
    </v-container>
  </div>
</template>

<script setup>
  import { ref, watch, computed } from "vue";
  import draggable from "vuedraggable";
  import AisleCard from "@/components/AisleCard.vue";
  import AisleForm from "@/components/AisleForm.vue";
  import { useAisles } from "@/composables/aislesComposable";
  import { useMainStore } from "@/stores/main";

  const store = useMainStore();
  const aisleFormDialog = ref(false);
  const updateDialog = () => {
    aisleFormDialog.value = false;
  };

  const { aisles, isLoading, addAisle, editAisle, removeAisle, reorderAisles } =
    useAisles(store.store_id);

  const sortableAisles = ref([]);

  const uncategorizedAisle = computed(() =>
    aisles.value?.find(a => a.order === 0) ?? null
  );

  watch(
    aisles,
    val => {
      sortableAisles.value = (val ?? []).filter(a => a.order !== 0);
    },
    { immediate: true }
  );

  const onReorder = () => {
    const updated = sortableAisles.value.map((aisle, index) => ({
      ...aisle,
      order: index + 1,
    }));
    reorderAisles(updated);
  };

  const createAisle = async newAisle => {
    await addAisle(newAisle);
  };

  const updateAisle = async updatedAisle => {
    await editAisle(updatedAisle);
  };

  const deleteAisle = async deletedAisle => {
    await removeAisle(deletedAisle);
  };

  const blankFormData = ref({
    id: null,
    name: null,
    store_id: store.store_id,
    order: 1,
  });
</script>
