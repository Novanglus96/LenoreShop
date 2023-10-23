<template>
    <v-app>
        <v-main>
            <v-container fluid-class="pa-2">
                <router-view />
            </v-container>
        </v-main>
    </v-app>
</template>
<script setup>
import { onMounted } from 'vue';
import { useMainStore } from '@/stores/main';

const mainstore = useMainStore();

onMounted(() => {
    mainstore.fetchAll();
})

</script>
