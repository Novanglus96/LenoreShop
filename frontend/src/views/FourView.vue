<template>
  <div class="notfound">
    <header class="bg-white shadow">
      <div class="mx-auto max-w-7xl px-4 py-6 sm:px-6 lg:px-8">
        <h1 class="text-3xl font-bold tracking-tight text-gray-900">404 Page Not Found</h1>
      </div>
    </header>
    <main>
      <div class="mx-auto max-w-7xl py-6 sm:px-6 lg:px-8">
        <NotFound/>
      </div>
    </main>
  </div>
</template>

<script>
// @ is an alias to /src
import NotFound from '@/components/NotFound.vue'

export default {
  name: 'ListView',
  components: {
    NotFound
  }
}
</script>
