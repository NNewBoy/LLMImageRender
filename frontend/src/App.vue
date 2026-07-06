<template>
  <div id="app-layout">
    <!-- 路由跳转进度条 -->
    <RouteProgress />

    <!-- Animated gradient background -->
    <div class="bg-gradient" aria-hidden="true">
      <div class="bg-orb bg-orb--1"></div>
      <div class="bg-orb bg-orb--2"></div>
      <div class="bg-orb bg-orb--3"></div>
    </div>

    <el-scrollbar class="app-scroll">
      <AppHeader />
      <main class="main-content">
        <router-view v-slot="{ Component }">
          <transition name="page" mode="out-in">
            <component :is="Component" />
          </transition>
        </router-view>
      </main>
    </el-scrollbar>
  </div>
</template>

<script setup lang="ts">
import AppHeader from './components/AppHeader.vue'
import RouteProgress from './components/RouteProgress.vue'
</script>

<style>
#app-layout {
  position: relative;
  height: 100vh;
  display: flex;
  flex-direction: column;
  overflow: hidden;
}

/* 内容滚动区：用 ElScrollbar 接管滚动，不再使用系统滚动条 */
.app-scroll {
  flex: 1;
  min-height: 0;
  position: relative;
  z-index: 1;
}

/* Animated background orbs */
.bg-gradient {
  position: fixed;
  inset: 0;
  z-index: 0;
  overflow: hidden;
  pointer-events: none;
}

.bg-orb {
  position: absolute;
  border-radius: 50%;
  filter: blur(100px);
  opacity: 0.4;
  animation: float 20s ease-in-out infinite;
}

.bg-orb--1 {
  width: 500px;
  height: 500px;
  background: radial-gradient(circle, #6366f1, transparent 70%);
  top: -150px;
  left: -100px;
}

.bg-orb--2 {
  width: 400px;
  height: 400px;
  background: radial-gradient(circle, #8b5cf6, transparent 70%);
  bottom: -100px;
  right: -80px;
  animation-delay: -7s;
}

.bg-orb--3 {
  width: 350px;
  height: 350px;
  background: radial-gradient(circle, #3b82f6, transparent 70%);
  top: 40%;
  left: 50%;
  transform: translateX(-50%);
  animation-delay: -14s;
}

@keyframes float {
  0%,
  100% {
    transform: translate(0, 0) scale(1);
  }
  33% {
    transform: translate(30px, -40px) scale(1.05);
  }
  66% {
    transform: translate(-20px, 30px) scale(0.95);
  }
}

.main-content {
  position: relative;
  z-index: 1;
  flex: 1;
  max-width: 1280px;
  width: 100%;
  margin: 0 auto;
  padding: 24px 24px 48px;
}

/* Page transition */
.page-enter-active,
.page-leave-active {
  transition: opacity 0.25s ease, transform 0.25s ease;
}

.page-enter-from {
  opacity: 0;
  transform: translateY(12px);
}

.page-leave-to {
  opacity: 0;
  transform: translateY(-12px);
}

/* ---- Responsive ---- */
@media (max-width: 768px) {
  .main-content {
    padding: 16px 16px 32px;
  }

  .bg-orb {
    filter: blur(80px);
    opacity: 0.3;
  }

  .bg-orb--1 {
    width: 300px;
    height: 300px;
  }

  .bg-orb--2 {
    width: 250px;
    height: 250px;
  }

  .bg-orb--3 {
    width: 200px;
    height: 200px;
  }
}

@media (prefers-reduced-motion: reduce) {
  .bg-orb {
    animation: none;
  }
}
</style>
