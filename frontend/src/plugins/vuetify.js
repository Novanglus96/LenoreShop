import 'vuetify/styles'
import { createVuetify } from 'vuetify'
import * as components from 'vuetify/components'
import * as directives from 'vuetify/directives'
import { aliases, mdi } from 'vuetify/iconsets/mdi'
import '@mdi/font/css/materialdesignicons.css'

const myCustomLightTheme = {
    dark: false,
    colors: {
        primary: '#2196f3',
        secondary: '#00bcd4',
        accent: '#ffeb3b',
        error: '#ffc107',
        warning: '#ff9800',
        info: '#795548',
        success: '#4caf50',
    },
}

export default createVuetify({
    theme: {
      defaultTheme: 'myCustomLightTheme',
      themes: {
        myCustomLightTheme,
      },
    },
    icons: {
        defaultSet: 'mdi',
        aliases,
        sets: {
          mdi,
        },
    },
    components,
    directives,
  })