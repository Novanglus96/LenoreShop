module.exports = {
  root: true,
  env: {
    node: true, // Enable Node.js global variables and scope
    browser: true, // Enable browser global variables
    es2021: true, // Enable modern JavaScript syntax
  },
  extends: [
    "plugin:vue/vue3-essential", // Essential rules for Vue 3
    "eslint:recommended", // Recommended core rules
    "prettier", // Disables conflicting rules with Prettier
  ],
  parserOptions: {
    ecmaVersion: 2021, // Support for ES2021 features
    sourceType: "module", // Use ECMAScript modules
  },
  rules: {
    "no-console": process.env.NODE_ENV === "production" ? "warn" : "off", // Warn on console in production
    "no-debugger": process.env.NODE_ENV === "production" ? "warn" : "off", // Warn on debugger in production
    "vue/valid-v-slot": [
      "error", // Validate v-slot syntax
      {
        allowModifiers: true, // Allow modifiers like `slot:header.sortable`
      },
    ],
  },
};
