<template>
  <div class="task-card" @click="$emit('click')">
    <div class="task-thumbnail">
      <ImageViewer
        :src="task.result_image_url || task.original_image_url"
        :alt="task.result_image_url ? '渲染结果' : '原始图片'"
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
  border-radius: 8px;
  overflow: hidden;
  border: 1px solid #e4e7ed;
  cursor: pointer;
  transition: box-shadow 0.3s;
  background: #fff;
}

.task-card:hover {
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
}

.task-thumbnail {
  position: relative;
  height: 180px;
  overflow: hidden;
  background: #f5f7fa;
}

.task-thumbnail img {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.task-status-badge {
  position: absolute;
  top: 8px;
  right: 8px;
  padding: 2px 8px;
  border-radius: 4px;
  font-size: 11px;
  color: #fff;
}

.task-status-badge.completed { background: #67c23a; }
.task-status-badge.processing { background: #409eff; }
.task-status-badge.queued { background: #e6a23c; }
.task-status-badge.failed { background: #f56c6c; }

.task-info {
  padding: 10px 12px;
}

.task-mode {
  font-size: 13px;
  font-weight: 600;
  color: #303133;
}

.task-time {
  font-size: 12px;
  color: #c0c4cc;
  margin-top: 4px;
}
</style>