import "vuetify/styles";
import { createVuetify } from "vuetify";
import * as components from "vuetify/components";
import * as directives from "vuetify/directives";
import { aliases, mdi } from "vuetify/iconsets/mdi";
import "@mdi/font/css/materialdesignicons.css";

// The brand colours are unchanged. `surface` and `background` shift to the warm
// off-white used by the paper surfaces so Vuetify components sit on the same
// sheet as the custom ones instead of on stark white. Keep these in sync with
// the --ls-paper* tokens in styles/tokens.css.
const myCustomLightTheme = {
  dark: false,
  colors: {
    primary: "#002255",
    secondary: "#bfe7ff",
    accent: "#ffeb3b",
    error: "#FF3407",
    warning: "#ffc107",
    info: "#795548",
    success: "#4caf50",
    background: "#f7f4ec",
    surface: "#fffdf6",
    "surface-variant": "#f7f1e2",
    "on-surface-variant": "#14263f",
  },
};

export default createVuetify({
  theme: {
    defaultTheme: "myCustomLightTheme",
    themes: {
      myCustomLightTheme,
    },
  },
  // Softer, more generous shapes across the board — the Material 3 direction —
  // applied centrally so individual components don't each carry a rounded prop.
  defaults: {
    VCard: { rounded: "lg" },
    VBtn: { rounded: "pill" },
    VTextField: { variant: "outlined", density: "comfortable" },
    VSelect: { variant: "outlined", density: "comfortable" },
    VAutocomplete: { variant: "outlined", density: "comfortable" },
    VTextarea: { variant: "outlined", density: "comfortable" },
    VChip: { rounded: "pill" },
    VDialog: { scrollable: true },
  },
  icons: {
    defaultSet: "mdi",
    aliases,
    sets: {
      mdi,
    },
  },
  components,
  directives,
});
