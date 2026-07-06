<template>
  <div class="route-progress" :class="{ 'route-progress--visible': visible }">
    <div class="route-progress__bar" :style="{ transform: `scaleX(${progress / 100})` }"></div>
  </div>
</template>

<script setup lang="ts">
import { useRouteProgress } from '@/composables/useRouteProgress'

const { progress, visible } = useRouteProgress()
</script>

<style scoped>
.route-progress {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  height: 3px;
  z-index: 9999;
  pointer-events: none;
  opacity: 0;
  transition: opacity 0.3s ease;
}

.route-progress--visible {
  opacity: 1;
}

.route-progress__bar {
  height: 100%;
  transform-origin: left;
  background: linear-gradient(
    90deg,
    var(--accent-primary),
    var(--accent-secondary)
  );
  box-shadow: 0 0 8px var(--accent-primary-glow);
  transition: transform 0.2s ease;
}
</style>
