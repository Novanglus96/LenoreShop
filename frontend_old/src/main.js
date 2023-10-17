import { createApp } from 'vue'
import { createPinia } from 'pinia'
import App from './App.vue'
import router from './router'
import { loadFonts } from './plugins/webfontloader'
import PrimeVue from 'primevue/config'

loadFonts()

const pinia = createPinia()
const app = createApp(App)

app.use(router)
app.use(pinia)
app.use(PrimeVue)
app.mount('#app')
  