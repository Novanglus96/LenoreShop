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
        error: '#FF3407',
        warning: '#ffc107',
        info: '#795548',
        success: '#4caf50',
        area1: '#BBDEFB',
        area2: '#90CAF9',
        area3: '#64B5F6',
        area4: '#42A5F5',
        area5: '#1E88E5',
        area6: '#1976D2',
        user1: '#E91E63',
        user2: '#3F51B5',
        user3: '#009688',
        user4: '#CDDC39',
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