import { defineConfig } from "vite";
import vue from "@vitejs/plugin-vue";
import { createHtmlPlugin } from "vite-plugin-html";
import vueDevTools from "vite-plugin-vue-devtools";
import { fileURLToPath, URL } from "node:url";
import eslint from "vite-plugin-eslint";
import { VitePWA } from "vite-plugin-pwa";

export default defineConfig(({ mode }) => ({
  plugins: [
    vue(),
    mode !== "production" && vueDevTools(),
    createHtmlPlugin({
      inject: {
        data: {
          title: "LenoreShop",
        },
      },
    }),
    eslint(),
    VitePWA({
      registerType: "autoUpdate",
      includeAssets: ["favicon.ico", "android-chrome-192x192.png", "android-chrome-512x512.png"],
      manifest: {
        name: "LenoreShop",
        short_name: "LenoreShop",
        description: "A simple shopping list app",
        theme_color: "#3F51B5",
        background_color: "#ffffff",
        display: "standalone",
        start_url: "/",
        scope: "/",
        icons: [
          {
            src: "/android-chrome-192x192.png",
            sizes: "192x192",
            type: "image/png",
          },
          {
            src: "/android-chrome-512x512.png",
            sizes: "512x512",
            type: "image/png",
          },
          {
            src: "/android-chrome-512x512.png",
            sizes: "512x512",
            type: "image/png",
            purpose: "maskable",
          },
        ],
      },
      workbox: {
        navigateFallbackDenylist: [/^\/admin/],
        globPatterns: ["**/*.{js,css,html,ico,png,svg,woff2}"],
        runtimeCaching: [
          {
            urlPattern: /^\/api\//,
            handler: "NetworkFirst",
            options: {
              cacheName: "api-cache",
              expiration: {
                maxEntries: 100,
                maxAgeSeconds: 60 * 60 * 24, // 24 hours
              },
              networkTimeoutSeconds: 10,
              cacheableResponse: {
                statuses: [0, 200],
              },
            },
          },
        ],
      },
    }),
  ],
  server: {
    proxy: {
      "/api": {
        target: "https://back-dev.danielleandjohn.love/api", // Backend API server
        changeOrigin: true,
        rewrite: path => path.replace(/^\/api/, ""),
      },
      "/ws": {
        target: "ws://backend:8001", // Local backend WebSocket (Docker service name)
        ws: true,
      },
    },
  },
  define: {
    __VUE_OPTIONS_API__: true,
    __VUE_PROD_DEVTOOLS__: false,
    __VUE_PROD_HYDRATION_MISMATCH_DETAILS__: false,
  },
  resolve: {
    alias: {
      "@": fileURLToPath(new URL("./src", import.meta.url)),
    },
  },
}));
