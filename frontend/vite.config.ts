import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'
import Components from 'unplugin-vue-components/vite'
import { ElementPlusResolver } from 'unplugin-vue-components/resolvers'
import { resolve } from 'path'

export default defineConfig({
  plugins: [
    vue(),
    // Element Plus 按需引入：模板中使用的 el-* 组件与 v-loading 指令自动导入并附带样式
    Components({
      resolvers: [ElementPlusResolver()],
      dts: 'src/components.d.ts',
    }),
  ],
  base: '/llmimagerender/',
  resolve: {
    alias: {
      '@': resolve(__dirname, 'src'),
    },
  },
  server: {
    port: 5175,
    proxy: {
      '/api': {
        target: 'http://localhost:8000',
        changeOrigin: true,
      },
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
