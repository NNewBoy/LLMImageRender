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
  grid-template-columns: repeat(auto-fill, minmax(100px, 1fr));
  gap: 12px;
}

.room-card {
  padding: 16px;
  text-align: center;
  border: 2px solid #e4e7ed;
  border-radius: 8px;
  cursor: pointer;
  transition: all 0.3s;
}

.room-card:hover {
  border-color: #a0cfff;
  background: #ecf5ff;
}

.room-card.selected {
  border-color: #409eff;
  background: #ecf5ff;
}

.room-icon {
  color: #606266;
  margin-bottom: 8px;
}

.room-card.selected .room-icon {
  color: #409eff;
}

.room-name {
  font-size: 13px;
  color: #606266;
  font-weight: 500;
}
</style>