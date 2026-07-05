<template>
  <div class="room-type-selector">
    <div class="room-grid">
      <div
        v-for="room in roomTypes"
        :key="room.value"
        class="room-card"
        :class="{ selected: modelValue === room.value }"
        @click="$emit('update:modelValue', room.value)"
      >
        <div class="room-icon">
          <el-icon :size="28">
            <HomeFilled v-if="room.value === 'living_room'" />
            <Moon v-else-if="room.value === 'bedroom'" />
            <KnifeFork v-else-if="room.value === 'kitchen'" />
            <Reading v-else-if="room.value === 'study'" />
            <Key v-else />
          </el-icon>
        </div>
        <div class="room-name">{{ room.label }}</div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { HomeFilled, Moon, KnifeFork, Reading, Key } from '@element-plus/icons-vue'
defineProps<{ modelValue: string }>()
defineEmits(['update:modelValue'])

const roomTypes = [
  { value: 'living_room', label: '客厅' },
  { value: 'bedroom', label: '卧室' },
  { value: 'kitchen', label: '厨房' },
  { value: 'study', label: '书房' },
  { value: 'entryway', label: '玄关' },
]
</script>

<style scoped>
.room-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(110px, 1fr));
  gap: 12px;
}

.room-card {
  padding: 20px 12px;
  text-align: center;
  border: 1px solid var(--glass-border);
  border-radius: var(--radius-md);
  cursor: pointer;
  transition: all 0.2s ease;
  background: rgba(255, 255, 255, 0.03);
}

.room-card:hover {
  border-color: var(--accent-primary-light);
  background: rgba(99, 102, 241, 0.06);
}

.room-card.selected {
  border-color: var(--accent-primary);
  background: rgba(99, 102, 241, 0.12);
  box-shadow: 0 0 12px var(--accent-primary-glow);
}

.room-icon {
  color: var(--text-muted);
  margin-bottom: 8px;
  transition: color 0.2s ease;
}

.room-card.selected .room-icon {
  color: var(--accent-primary-light);
}

.room-name {
  font-size: 13px;
  color: var(--text-secondary);
  font-weight: 500;
  transition: color 0.2s ease;
}

.room-card.selected .room-name {
  color: var(--accent-primary-light);
}

/* ---- Responsive ---- */
@media (max-width: 480px) {
  .room-grid {
    grid-template-columns: repeat(3, 1fr);
    gap: 10px;
  }

  .room-card {
    padding: 16px 8px;
  }
}
</style>
