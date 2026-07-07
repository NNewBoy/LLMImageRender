import { createApp } from 'vue'
import { createPinia } from 'pinia'
import piniaPluginPersistedstate from 'pinia-plugin-persistedstate'
// Element Plus 按需引入：el-* 组件与 v-loading 指令由 unplugin-vue-components 自动导入
// 仅需全局引入暗色模式 CSS 变量、基础变量，以及以 JS API 形式调用的 ElMessage / ElMessageBox 样式
import 'element-plus/theme-chalk/dark/css-vars.css'
import 'element-plus/theme-chalk/base.css'
import 'element-plus/theme-chalk/el-message.css'
import 'element-plus/theme-chalk/el-message-box.css'
import './styles/theme.css'
import App from './App.vue'
import router from './router'
import { useThemeStore } from '@/stores/theme'
import { recordVisit } from '@/api/visit'

const app = createApp(App)

const pinia = createPinia()
pinia.use(piniaPluginPersistedstate)
app.use(pinia)

// 在应用挂载前，根据 URL 参数 / localStorage 初始化主题
// index.html 内联脚本已提前设置 .dark 类以避免闪烁，
// 这里将持久化状态与 URL 参数同步到 store，并再次应用到 DOM
const themeStore = useThemeStore(pinia)
themeStore.initFromUrl()

app.use(router)

app.mount('#app')

// 记录访客量
recordVisit('LLM柜子3D模型渲染器')
