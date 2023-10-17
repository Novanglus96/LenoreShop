import { createApp } from 'vue'
import { createPinia } from 'pinia'
import App from './App.vue'
import router from './router'
import store from './store'
import vuetify from './plugins/vuetify'
import { loadFonts } from './plugins/webfontloader'

loadFonts()

const pinia = createPinia()
const app = createApp(App)

app.use(router)
app.use(store)
app.use(pinia)
app.use(vuetify)
app.mount('#app')
  