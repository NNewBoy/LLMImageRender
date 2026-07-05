<template>
  <div class="task-status">
    <div class="status-indicator">
      <el-icon :size="48" :class="[statusClass, { 'is-loading': status === 'processing' }]">
        <Clock v-if="status === 'queued'" />
        <Loading v-else-if="status === 'processing'" />
        <CircleCheck v-else-if="status === 'completed'" />
        <CircleClose v-else />
      </el-icon>
      <div class="status-text">{{ statusText }}</div>
    </div>
    <el-progress
      v-if="status === 'processing'"
      :percentage="progress"
      :stroke-width="8"
      :color="'#6366f1'"
    />
    <div v-if="errorMessage" class="error-message">
      <el-alert :title="errorMessage" type="error" :closable="false" />
    </div>
  </div>
</template>

<script setup lang="ts">
import { computed } from 'vue'
import { Clock, Loading, CircleCheck, CircleClose } from '@element-plus/icons-vue'

const props = defineProps<{
  status: string
  progress: number
  errorMessage?: string | null
}>()

const statusText = computed(() => {
  const map: Record<string, string> = {
    queued: '排队中，请稍候...',
    processing: `渲染中... ${props.progress}%`,
    completed: '渲染完成',
    failed: '渲染失败',
    cancelled: '已取消',
  }
  return map[props.status] || props.status
})

const statusClass = computed(() => {
  const map: Record<string, string> = {
    queued: 'status-queued',
    processing: 'status-processing',
    completed: 'status-completed',
    failed: 'status-failed',
  }
  return map[props.status] || ''
})
</script>

<style scoped>
.task-status {
  text-align: center;
  padding: 24px;
}

.status-indicator {
  margin-bottom: 16px;
}

.status-text {
  margin-top: 12px;
  font-size: 16px;
  font-weight: 600;
  color: var(--text-primary);
}

.status-queued {
  color: var(--accent-warning);
}
.status-processing {
  color: var(--accent-primary-light);
}
.status-completed {
  color: var(--accent-success);
}
.status-failed {
  color: var(--accent-danger);
}

.error-message {
  margin-top: 16px;
  text-align: left;
}
</style>
