import { fileURLToPath, URL } from 'node:url'

import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'
import vueJsx from '@vitejs/plugin-vue-jsx'
import vueDevTools from 'vite-plugin-vue-devtools'
import tailwindcss from 'tailwindcss'
import autoprefixer from 'autoprefixer'

// https://vite.dev/config/
export default defineConfig({
  plugins: [
    vue(),
    vueJsx(),
    vueDevTools(),
  ],
  resolve: {
    alias: {
      '@': fileURLToPath(new URL('./src', import.meta.url))
    },
  },
  server:{
    port:8080,
    proxy:{
      '/api/v1':{
        target:'http://localhost:3000/api/v1',
        changeOrigin:true, 
        rewrite: (path) => path.replace(/^\/api\/v1/, '')
        // rewrite: (path) => path.replace(/^\/api/, "")
      },
    },
  },
  css:{
    postcss: {
      plugins: [
        tailwindcss,
        autoprefixer,
      ],
    },
  }
})
