import { defineStore } from 'pinia'
import { ref, computed } from 'vue'

export type ThemeMode = 'light' | 'dark'

export const useThemeStore = defineStore('theme', () => {
  /** 当前主题模式 */
  const mode = ref<ThemeMode>('dark')

  /** 是否深色模式 */
  const isDark = computed(() => mode.value === 'dark')

  /**
   * 应用主题到 documentElement
   * 切换后直接刷新 CSS 变量，无需重启页面
   */
  function applyToDOM(target: ThemeMode = mode.value) {
    const html = document.documentElement
    if (target === 'dark') {
      html.classList.add('dark')
    } else {
      html.classList.remove('dark')
    }
    // 同步 meta theme-color，适配移动端浏览器顶栏
    const meta = document.querySelector('meta[name="theme-color"]')
    if (meta) {
      meta.setAttribute('content', target === 'dark' ? '#0a0a0f' : '#eef2f8')
    }
  }

  /**
   * 设置主题（并持久化 + 应用到 DOM）
   */
  function setMode(target: ThemeMode) {
    if (target !== 'light' && target !== 'dark') return
    mode.value = target
    applyToDOM(target)
  }

  /** 切换主题 */
  function toggle() {
    setMode(mode.value === 'dark' ? 'light' : 'dark')
  }

  /**
   * 从 URL 查询参数初始化主题
   * 支持 ?theme=light 或 ?theme=dark，便于外部平台跳转特定主题
   * 优先级：URL 参数 > localStorage > 默认 dark
   * @returns 实际生效的主题
   */
  function initFromUrl(): ThemeMode {
    const params = new URLSearchParams(window.location.search)
    const fromUrl = params.get('theme')
    if (fromUrl === 'light' || fromUrl === 'dark') {
      setMode(fromUrl)
      return fromUrl
    }
    // URL 无指定时，applyToDOM 以持久化/默认值生效
    applyToDOM()
    return mode.value
  }

  return { mode, isDark, setMode, toggle, applyToDOM, initFromUrl }
}, {
  persist: {
    key: 'theme',
    paths: ['mode'],
  },
})
