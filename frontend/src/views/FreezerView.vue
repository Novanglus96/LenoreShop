<template>
  <div class="freezerpage">
    <div class="ls-frost-sheet ls-frost-sheet--iced freezerpage__sheet">
      <span class="ls-magnet" aria-hidden="true" />

      <header class="freezerpage__head">
        <h1 class="ls-hand ls-hand--title freezerpage__title">Freezers</h1>
        <p class="freezerpage__hint">
          Track what's frozen, and what needs using up before it goes.
        </p>

        <v-btn
          color="primary"
          variant="flat"
          prepend-icon="mdi-plus"
          class="freezerpage__add"
          @click="freezerFormDialog = true"
        >
          Add freezer
        </v-btn>
      </header>

      <div v-if="isLoading" class="freezerpage__body">
        <v-skeleton-loader type="list-item, list-item" />
      </div>

      <div v-else class="freezerpage__body">
        <p v-if="!hasFreezers" class="freezerpage__empty">
          No freezers yet. Add one to start tracking frozen food.
        </p>

        <ul v-else class="ls-rows">
          <FreezerCard
            v-for="freezer in freezers"
            :key="freezer.id"
            :freezer="freezer"
            @select="selectedFreezer"
            @select-delete="selectedDeleteFreezer"
          />
        </ul>
      </div>
    </div>

    <!-- One add form, one edit form and one delete dialog for the whole list,
         all kept outside the v-for above. -->
    <FreezerForm
      v-model="freezerFormDialog"
      @add-freezer="createFreezer"
      @update-dialog="updateDialog"
      :isEdit="false"
      :passedFormData="blankFormData"
    />

    <FreezerForm
      v-model="editFreezerFormDialog"
      @edit-freezer="updateFreezer"
      @update-dialog="updateEditDialog"
      :isEdit="true"
      :passedFormData="passedFormData"
      :key="passedFormData.id"
    />

    <v-dialog v-model="deleteDialog" max-width="400">
      <v-card>
        <v-card-title>Delete freezer?</v-card-title>
        <v-card-text>
          "{{ passedDeleteData.name }}" will be removed, along with everything
          recorded as being in it.
        </v-card-text>
        <v-card-actions>
          <v-spacer />
          <v-btn variant="text" @click="deleteDialog = false">Cancel</v-btn>
          <v-btn
            color="error"
            variant="text"
            @click="deleteFreezer(passedDeleteData)"
          >
            Delete
          </v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>
  </div>
</template>

<script setup>
  import { computed, ref } from "vue";
  import FreezerCard from "@/components/FreezerCard.vue";
  import FreezerForm from "@/components/FreezerForm.vue";
  import { useFreezers } from "@/composables/freezersComposable";

  const freezerFormDialog = ref(false);
  const editFreezerFormDialog = ref(false);
  const deleteDialog = ref(false);

  const { freezers, isLoading, addFreezer, editFreezer, removeFreezer } =
    useFreezers();

  const hasFreezers = computed(() => (freezers.value?.length ?? 0) > 0);

  const createFreezer = async newFreezer => {
    await addFreezer(newFreezer);
  };

  const updateFreezer = async updatedFreezer => {
    await editFreezer(updatedFreezer);
  };

  const deleteFreezer = async deletedFreezer => {
    await removeFreezer(deletedFreezer);
    deleteDialog.value = false;
  };

  const passedFormData = ref({
    id: 0,
    name: "",
    location: "",
  });

  const passedDeleteData = ref({
    id: 0,
    name: null,
  });

  const selectedFreezer = freezer => {
    passedFormData.value = {
      id: freezer.id,
      name: freezer.name,
      location: freezer.location,
    };
    editFreezerFormDialog.value = true;
  };

  const selectedDeleteFreezer = freezer => {
    passedDeleteData.value.id = freezer.id;
    passedDeleteData.value.name = freezer.name;
    deleteDialog.value = true;
  };

  const updateDialog = () => {
    freezerFormDialog.value = false;
  };

  const updateEditDialog = () => {
    editFreezerFormDialog.value = false;
  };

  const blankFormData = ref({
    id: null,
    name: null,
    location: null,
  });
</script>

<style scoped>
  .freezerpage {
    padding: var(--ls-space-sm) var(--ls-space) var(--ls-space-lg);
    max-width: 720px;
    margin: 0 auto;
  }

  /* Padding longhand: the shorthand would clobber the room
   .ls-frost-sheet--iced reserves for the icicles. Extra top padding clears the
   magnet disc pinned at the top of the sheet. */
  .freezerpage__sheet {
    padding-top: var(--ls-space-md);
    padding-right: var(--ls-space);
    padding-left: var(--ls-space);
  }

  .freezerpage__head {
    display: flex;
    flex-direction: column;
    align-items: flex-start;
    gap: var(--ls-space-sm);
    padding-bottom: var(--ls-space);
    border-bottom: 1px solid var(--ls-frost-rule);
  }

  .freezerpage__title {
    margin: 0;
    color: var(--ls-frost-ink);
  }

  .freezerpage__hint {
    margin: 0;
    font-size: 0.8125rem;
    line-height: 1.45;
    color: var(--ls-frost-ink-soft);
  }

  .freezerpage__add {
    align-self: stretch;
  }

  .freezerpage__body {
    padding-top: var(--ls-space);
  }

  .freezerpage__empty {
    margin: 0;
    padding: var(--ls-space) 0;
    color: var(--ls-frost-ink-faint);
    font-style: italic;
  }

  @media (min-width: 600px) {
    .freezerpage__add {
      align-self: flex-start;
    }
  }

  @media (max-width: 599px) {
    .freezerpage {
      padding-left: var(--ls-space-sm);
      padding-right: var(--ls-space-sm);
    }
  }
</style>
