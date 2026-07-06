<template>
  <div class="task-card glass-card" @click="$emit('click')">
    <div class="task-thumbnail">
      <ImageViewer
        :src="task.thumbnail_url || task.result_image_url || task.original_image_url"
        :alt="task.result_image_url ? '渲染结果' : '原始图片'"
        :preview="false"
      />
      <div class="task-status-badge" :class="task.status">
        {{ statusLabel }}
      </div>
    </div>
    <div class="task-info">
      <div class="task-mode">{{ task.mode === 'single' ? '单品渲染' : '场景渲染' }}</div>
      <div class="task-time">{{ formatTime(task.created_at) }}</div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { computed } from 'vue'
import ImageViewer from '@/components/ImageViewer.vue'
import type { RenderTask } from '@/types'

const props = defineProps<{ task: RenderTask }>()
defineEmits(['click'])

const statusLabels: Record<string, string> = {
  queued: '排队中',
  processing: '处理中',
  completed: '已完成',
  failed: '失败',
}

const statusLabel = computed(() => statusLabels[props.task.status] || props.task.status)

const formatTime = (time: string) => {
  if (!time) return ''
  const d = new Date(time)
  const now = new Date()
  const diff = now.getTime() - d.getTime()
  if (diff < 60000) return '刚刚'
  if (diff < 3600000) return `${Math.floor(diff / 60000)}分钟前`
  if (diff < 86400000) return `${Math.floor(diff / 3600000)}小时前`
  return d.toLocaleDateString('zh-CN')
}
</script>

<style scoped>
.task-card {
  overflow: hidden;
  cursor: pointer;
}

.task-thumbnail {
  position: relative;
  height: 180px;
  overflow: hidden;
  background: var(--media-bg);
}

.task-thumbnail :deep(img) {
  width: 100%;
  height: 100%;
  object-fit: cover;
  transition: transform 0.3s ease;
}

.task-card:hover .task-thumbnail :deep(img) {
  transform: scale(1.05);
}

.task-status-badge {
  position: absolute;
  top: 8px;
  right: 8px;
  padding: 3px 10px;
  border-radius: 100px;
  font-size: 11px;
  font-weight: 600;
  color: #fff;
  backdrop-filter: blur(8px);
}

.task-status-badge.completed {
  background: rgba(34, 197, 94, 0.85);
}
.task-status-badge.processing {
  background: rgba(99, 102, 241, 0.85);
}
.task-status-badge.queued {
  background: rgba(245, 158, 11, 0.85);
}
.task-status-badge.failed {
  background: rgba(239, 68, 68, 0.85);
}

.task-info {
  padding: 12px 14px;
}

.task-mode {
  font-size: 14px;
  font-weight: 600;
  color: var(--text-primary);
}

.task-time {
  font-size: 12px;
  color: var(--text-faint);
  margin-top: 4px;
}
</style>
