<template>
  <header class="app-header">
    <div class="header-left">
      <router-link to="/" class="logo">
        <el-icon :size="28"><PictureFilled /></el-icon>
        <span class="logo-text">LLMImageRender</span>
      </router-link>
    </div>
    <div class="header-right">
      <el-menu mode="horizontal" :default-active="activeMenu" router :ellipsis="false">
        <el-menu-item index="/">
          <el-icon><HomeFilled /></el-icon>
          <span>首页</span>
        </el-menu-item>
        <el-menu-item index="/gallery">
          <el-icon><Grid /></el-icon>
          <span>图库</span>
        </el-menu-item>
        <el-menu-item index="/history">
          <el-icon><Clock /></el-icon>
          <span>历史</span>
        </el-menu-item>
      </el-menu>
    </div>
  </header>
</template>

<script setup lang="ts">
import { computed } from 'vue'
import { useRoute } from 'vue-router'

const route = useRoute()
const activeMenu = computed(() => {
  if (route.path.startsWith('/render')) return '/'
  return route.path
})
</script>

<style scoped>
.app-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 0 24px;
  height: 60px;
  background: #fff;
  border-bottom: 1px solid #e4e7ed;
  box-shadow: 0 1px 4px rgba(0, 0, 0, 0.05);
  position: sticky;
  top: 0;
  z-index: 100;
}

.logo {
  display: flex;
  align-items: center;
  gap: 8px;
  text-decoration: none;
  color: #409eff;
}

.logo-text {
  font-size: 20px;
  font-weight: 700;
  color: #303133;
}

.header-right {
  flex: 1;
  display: flex;
  justify-content: flex-end;
}

.el-menu {
  border-bottom: none;
}
</style>