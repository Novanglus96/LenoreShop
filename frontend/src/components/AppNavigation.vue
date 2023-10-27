<template>
    <v-app-bar
        color="primary"
        density=compact
        app
    >
        <v-menu>
            <template v-slot:activator="{ props }">
                <v-btn icon="mdi-menu" v-bind="props"></v-btn>
            </template>
            <v-list>
                <v-list-item
                    v-for="(menu, i) in menus"
                    :key="i"
                    :to="menu.url"
                >
                <template v-slot:prepend>
                    <v-icon :icon="menu.icon"></v-icon>
                </template>
                    <v-list-item-title>{{ menu.title }}</v-list-item-title>
                </v-list-item>
            </v-list>
            <v-list>
                <v-list-item
                    v-for="list in getShoppingLists"
                    :key="list.id"
                    @click="fetchShoppingListFull(list.id)"
                    prepend-icon="mdi-cart"
                >
                    <v-list-item-title>{{ list.store.name }} | {{ list.name }}</v-list-item-title>
                </v-list-item>
                <v-list-item v-if="getShoppingLists.length === 0">
                    <v-list-item-title>No Lists</v-list-item-title>
                </v-list-item>
            </v-list>
        </v-menu>
        <v-app-bar-title>Shopping</v-app-bar-title>
        <v-menu
            v-model="menu"
            :close-on-content-click="false"
            location="end"
        >
            <template v-slot:activator="{ props }">
                <v-btn icon="mdi-dots-vertical" v-bind="props"></v-btn>
            </template>

            <v-list>
                <v-list-item
                    to="/profile"
                    prepend-icon="mdi-account"
                >
                    <v-list-item-title>Profile</v-list-item-title>
                </v-list-item>
                <v-list-item
                    as="a"
                    href="/admin"
                    prepend-icon="mdi-security"
                >
                    <v-list-item-title>Admin</v-list-item-title>
                </v-list-item>
                <v-list-item
                    to="/logout"
                    prepend-icon="mdi-logout"
                >
                    <v-list-item-title>Logout</v-list-item-title>
                </v-list-item>
            </v-list>
        </v-menu>
    </v-app-bar>
</template>

<script setup>
    import { ref, computed } from 'vue';
    import { useMainStore } from '@/stores/main';
    import { useRouter } from 'vue-router';

    const router = useRouter();
    const mainstore = useMainStore();

    const menus = [
        { title: 'Home', url: '/', icon: 'mdi-home' },
        { title: 'Stores', url: '/stores', icon: 'mdi-storefront-outline' },
        { title: 'Shopping Lists', url: '/alllists', icon: 'mdi-cart-outline' },
        { title: 'Items', url: '/items', icon: 'mdi-food-apple-outline' },
      ]

    const menu = ref(false);

    const getShoppingLists = computed(() => {
        return mainstore.getShoppingLists;
    }) 

    const fetchShoppingListFull = async (list) => {
        try {
            const store = useMainStore();
            await store.fetchShoppingListFull(list);
            router.push('/list')
        } catch (error) {
            console.log(error)
        }
    }

</script>

<style scoped>
</style>