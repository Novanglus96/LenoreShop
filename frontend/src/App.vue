<template>
    <v-app>
        <AppNavigation/>
        <v-main>
            <v-container fluid-class="pa-2">
                <router-view />
            </v-container>
            <v-snackbar
                v-model="store.snackbar"
                :color="store.snackbarColor"
                :timeout="store.snackbarTimeout"
                content-class="centered-text"
            >
                {{ store.snackbarText }}
            </v-snackbar>
        </v-main>
    </v-app>
</template>
<script setup>
import AppNavigation from "@/components/AppNavigation.vue";
import { useMainStore } from '@/stores/main'

const store = useMainStore();

</script>
