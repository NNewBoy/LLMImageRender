import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'
import { resolve } from 'path'

export default defineConfig({
  plugins: [vue()],
  base: '/llmimagerender/',
  resolve: {
    alias: {
      '@': resolve(__dirname, 'src'),
    },
  },
  server: {
    port: 5175,
    proxy: {
      '/render_api': {
        target: 'http://localhost:8002',
        changeOrigin: true,
      },
      '/render_static': {
        target: 'http://localhost:8002',
        changeOrigin: true,
      },
    },
  },
})
