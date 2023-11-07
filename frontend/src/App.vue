<template>
    <v-app>
        <AppNavigation/>
        <v-main>
            <v-container fluid-class="pa-2">
                <router-view />
            </v-container>
        </v-main>
    </v-app>
</template>
<script setup>
import AppNavigation from "@/components/AppNavigation.vue";

</script>
