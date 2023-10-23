<template>
  <div class="hello">
    <h1>Shopping Lists</h1>
    <p>
      A simple shopping list app!  To get started, setup your <router-link to="/stores">Stores</router-link> here.
    </p>
    <h3>Pages</h3>
    <ul>
      <li><router-link to="/stores">Stores</router-link></li>
      <li><router-link to="/lists">Shopping Lists</router-link></li>
      <li><router-link to="/items">Items</router-link></li>
    </ul>
  </div>
</template>

<script>
export default {
  name: 'HelloWorld',
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
