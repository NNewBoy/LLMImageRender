<template>
  <header class="app-header">
    <div class="header-inner glass">
      <router-link to="/" class="logo">
        <el-icon :size="24" class="logo-icon"><PictureFilled /></el-icon>
        <span class="logo-text">LLMImageRender</span>
      </router-link>

      <!-- Desktop nav -->
      <nav class="nav-desktop">
        <router-link
          v-for="item in menuItems"
          :key="item.path"
          :to="item.path"
          class="nav-link"
          :class="{ active: isActive(item.path) }"
        >
          <el-icon :size="18"><component :is="item.icon" /></el-icon>
          <span>{{ item.label }}</span>
        </router-link>

        <!-- 主题切换 -->
        <button
          class="theme-toggle"
          @click="themeStore.toggle()"
          :aria-label="themeStore.isDark ? '切换到浅色模式' : '切换到深色模式'"
          :title="themeStore.isDark ? '切换到浅色模式' : '切换到深色模式'"
        >
          <el-icon :size="18" class="theme-icon">
            <Sunny v-if="themeStore.isDark" />
            <Moon v-else />
          </el-icon>
        </button>
      </nav>

      <!-- Mobile actions: theme toggle + menu toggle -->
      <div class="nav-mobile-actions">
        <button
          class="theme-toggle"
          @click="themeStore.toggle()"
          :aria-label="themeStore.isDark ? '切换到浅色模式' : '切换到深色模式'"
          :title="themeStore.isDark ? '切换到浅色模式' : '切换到深色模式'"
        >
          <el-icon :size="18" class="theme-icon">
            <Sunny v-if="themeStore.isDark" />
            <Moon v-else />
          </el-icon>
        </button>

        <!-- Mobile menu toggle -->
        <button
          class="nav-toggle"
          :class="{ open: mobileOpen }"
          @click="mobileOpen = !mobileOpen"
          aria-label="切换菜单"
        >
          <span></span>
          <span></span>
          <span></span>
        </button>
      </div>
    </div>

    <!-- Mobile dropdown -->
    <transition name="dropdown">
      <nav v-if="mobileOpen" class="nav-mobile glass">
        <router-link
          v-for="item in menuItems"
          :key="item.path"
          :to="item.path"
          class="nav-mobile-link"
          :class="{ active: isActive(item.path) }"
          @click="mobileOpen = false"
        >
          <el-icon :size="20"><component :is="item.icon" /></el-icon>
          <span>{{ item.label }}</span>
        </router-link>
      </nav>
    </transition>
  </header>
</template>

<script setup lang="ts">
import { ref, watch } from 'vue'
import { useRoute } from 'vue-router'
import { HomeFilled, Grid, Clock, PictureFilled, Sunny, Moon } from '@element-plus/icons-vue'
import { useThemeStore } from '@/stores/theme'

const route = useRoute()
const mobileOpen = ref(false)
const themeStore = useThemeStore()

const menuItems = [
  { path: '/', label: '首页', icon: HomeFilled },
  { path: '/gallery', label: '图库', icon: Grid },
  { path: '/history', label: '历史', icon: Clock },
]

const isActive = (path: string) => {
  if (path === '/') return route.path === '/' || route.path.startsWith('/render')
  return route.path.startsWith(path)
}

watch(() => route.path, () => {
  mobileOpen.value = false
})
</script>

<style scoped>
.app-header {
  position: sticky;
  top: 0;
  z-index: 100;
  padding: 16px 24px;
}

.header-inner {
  display: flex;
  align-items: center;
  justify-content: space-between;
  max-width: 1280px;
  margin: 0 auto;
  padding: 10px 20px;
  border-radius: 16px;
}

.logo {
  display: flex;
  align-items: center;
  gap: 10px;
  text-decoration: none;
  cursor: pointer;
}

.logo-icon {
  color: var(--accent-primary-light);
  filter: drop-shadow(0 0 8px var(--accent-primary-glow));
}

.logo-text {
  font-size: 18px;
  font-weight: 700;
  color: var(--text-primary);
  letter-spacing: -0.02em;
}

.nav-desktop {
  display: flex;
  align-items: center;
  gap: 4px;
}

.nav-link {
  display: flex;
  align-items: center;
  gap: 6px;
  padding: 8px 16px;
  border-radius: 10px;
  text-decoration: none;
  font-size: 14px;
  font-weight: 500;
  color: var(--text-muted);
  transition: all 0.2s ease;
  cursor: pointer;
}

.nav-link:hover {
  color: var(--text-primary);
  background: rgba(255, 255, 255, 0.06);
}

.nav-link.active {
  color: var(--accent-primary-light);
  background: rgba(99, 102, 241, 0.12);
}

/* Theme toggle */
.theme-toggle {
  display: flex;
  align-items: center;
  justify-content: center;
  width: 36px;
  height: 36px;
  margin-left: 4px;
  padding: 0;
  border-radius: 10px;
  border: 1px solid transparent;
  background: transparent;
  color: var(--text-muted);
  cursor: pointer;
  transition: all 0.2s ease;
}

.theme-toggle:hover {
  color: var(--accent-primary-light);
  background: rgba(99, 102, 241, 0.1);
  border-color: rgba(99, 102, 241, 0.15);
}

.theme-icon {
  transition: transform 0.3s ease;
}

.theme-toggle:hover .theme-icon {
  transform: rotate(30deg);
}

/* Mobile actions (theme + hamburger) */
.nav-mobile-actions {
  display: none;
  align-items: center;
  gap: 4px;
}

/* Mobile hamburger */
.nav-toggle {
  display: none;
  flex-direction: column;
  justify-content: center;
  gap: 5px;
  width: 40px;
  height: 40px;
  padding: 0;
  background: transparent;
  border: none;
  cursor: pointer;
}

.nav-toggle span {
  display: block;
  width: 22px;
  height: 2px;
  margin: 0 auto;
  background: var(--text-secondary);
  border-radius: 2px;
  transition: all 0.25s ease;
}

.nav-toggle.open span:nth-child(1) {
  transform: translateY(7px) rotate(45deg);
}

.nav-toggle.open span:nth-child(2) {
  opacity: 0;
}

.nav-toggle.open span:nth-child(3) {
  transform: translateY(-7px) rotate(-45deg);
}

/* Mobile dropdown */
.nav-mobile {
  position: absolute;
  top: 72px;
  left: 24px;
  right: 24px;
  border-radius: 16px;
  padding: 8px;
  display: flex;
  flex-direction: column;
  gap: 4px;
}

.nav-mobile-link {
  display: flex;
  align-items: center;
  gap: 10px;
  padding: 12px 16px;
  border-radius: 10px;
  text-decoration: none;
  font-size: 15px;
  font-weight: 500;
  color: var(--text-secondary);
  transition: all 0.2s ease;
  cursor: pointer;
}

.nav-mobile-link:hover {
  color: var(--text-primary);
  background: rgba(255, 255, 255, 0.06);
}

.nav-mobile-link.active {
  color: var(--accent-primary-light);
  background: rgba(99, 102, 241, 0.12);
}

/* Dropdown transition */
.dropdown-enter-active,
.dropdown-leave-active {
  transition: all 0.2s ease;
}

.dropdown-enter-from,
.dropdown-leave-to {
  opacity: 0;
  transform: translateY(-8px);
}

/* ---- Responsive ---- */
@media (max-width: 768px) {
  .app-header {
    padding: 12px 16px;
  }

  .header-inner {
    padding: 8px 16px;
  }

  .nav-desktop {
    display: none;
  }

  .nav-mobile-actions {
    display: flex;
  }

  .nav-toggle {
    display: flex;
  }

  .nav-mobile {
    left: 16px;
    right: 16px;
  }
}
</style>
