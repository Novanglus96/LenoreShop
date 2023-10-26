<template>
  <div class="hello">
    <h1>Shopping Lists</h1>
    <p>
      A simple shopping list app!  To get started, setup your <router-link to="/stores">Stores</router-link> here.
    </p>
    <h3>Shopping Lists</h3>
    <v-chip v-for="list in getShoppingLists" :key="list.id" @click="fetchShoppingListFull(list.id)">{{ list.store.name }} | {{ list.name }}</v-chip>
  </div>
</template>

<script setup>
  import { computed } from 'vue';
  import { useMainStore } from '@/stores/main';
  import { useRouter } from 'vue-router';

  const router = useRouter();
  const mainstore = useMainStore();
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

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
h3 {
  margin: 40px 0 0;
}
ul {
  list-style-type: none;
  padding: 0;
}
li {
  display: inline-block;
  margin: 0 10px;
}
a {
  color: #42b983;
}
</style>
