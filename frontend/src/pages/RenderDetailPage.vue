<template>
  <div class="render-detail-page">
    <div class="page-header">
      <button class="back-btn" @click="$router.push('/')">
        <el-icon :size="18"><ArrowLeft /></el-icon>
        <span>返回</span>
      </button>
      <h2>渲染详情</h2>
      <el-tag :type="tagType" size="large" effect="dark" round>{{ statusLabel }}</el-tag>
    </div>

    <div class="status-card glass-card">
      <TaskStatus
        :status="task?.status || 'queued'"
        :progress="task?.progress || 0"
        :error-message="task?.error_message"
      />
    </div>

    <div v-if="task" class="detail-content">
      <div class="compare-card glass-card">
        <ImageCompare
          :original-url="task.original_image_url"
          :result-url="task.result_image_url"
        />
      </div>

      <div class="params-grid glass-card">
        <div class="params-grid-title">渲染参数</div>
        <div class="params-grid-body">
          <div class="param-item">
            <span class="param-label">渲染模式</span>
            <span class="param-value">{{ task.mode === 'single' ? '单品渲染' : '场景渲染' }}</span>
          </div>
          <div class="param-item">
            <span class="param-label">风格</span>
            <span class="param-value">{{ task.params.style }}</span>
          </div>
          <div class="param-item">
            <span class="param-label">光照</span>
            <span class="param-value">{{ task.params.lighting }}</span>
          </div>
          <div class="param-item">
            <span class="param-label">视角</span>
            <span class="param-value">{{ task.params.view_angle }}</span>
          </div>
          <div v-if="task.params.room_type" class="param-item">
            <span class="param-label">户型</span>
            <span class="param-value">{{ task.params.room_type }}</span>
          </div>
          <div class="param-item">
            <span class="param-label">材质</span>
            <span class="param-value">{{ task.params.material }}</span>
          </div>
          <div class="param-item">
            <span class="param-label">颜色</span>
            <span class="param-value"><el-color-picker :model-value="task.params.color" disabled /></span>
          </div>
          <div v-if="task.mode === 'single' && task.params.background_color" class="param-item">
            <span class="param-label">背景颜色</span>
            <span class="param-value"><el-color-picker :model-value="task.params.background_color" disabled /></span>
          </div>
          <div v-if="task.params.description" class="param-item param-item--full">
            <span class="param-label">描述</span>
            <span class="param-value">{{ task.params.description }}</span>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted, onUnmounted } from 'vue'
import { useRoute } from 'vue-router'
import { getTaskStatus } from '@/api/render'
import TaskStatus from '@/components/TaskStatus.vue'
import ImageCompare from '@/components/ImageCompare.vue'
import type { RenderTask } from '@/types'

const route = useRoute()
const task = ref<RenderTask | null>(null)
let pollTimer: any = null

const statusLabel = computed(() => {
  const map: Record<string, string> = {
    queued: '排队中',
    processing: '处理中',
    completed: '已完成',
    failed: '失败',
  }
  return map[task.value?.status || ''] || ''
})

const tagType = computed(() => {
  const map: Record<string, string> = {
    queued: 'warning',
    processing: 'primary',
    completed: 'success',
    failed: 'danger',
  }
  return (map[task.value?.status || ''] || 'info') as any
})

const fetchTask = async () => {
  const taskId = route.params.taskId as string
  try {
    const res: any = await getTaskStatus(taskId)
    if (res.code === 200) {
      task.value = res.data
      if (res.data.status === 'completed' || res.data.status === 'failed') {
        stopPolling()
      }
    }
  } catch (e) {
    console.error('获取任务状态失败', e)
  }
}

const startPolling = () => {
  stopPolling()
  pollTimer = setInterval(fetchTask, 3000)
}

const stopPolling = () => {
  if (pollTimer) {
    clearInterval(pollTimer)
    pollTimer = null
  }
}

onMounted(() => {
  fetchTask()
  startPolling()
})

onUnmounted(stopPolling)
</script>

<style scoped>
.render-detail-page {
  max-width: 1100px;
  margin: 0 auto;
}

.page-header {
  display: flex;
  align-items: center;
  gap: 12px;
  margin-bottom: 20px;
}

.back-btn {
  display: flex;
  align-items: center;
  gap: 4px;
  padding: 8px 14px;
  border-radius: 10px;
  border: 1px solid var(--glass-border);
  background: var(--glass-bg);
  color: var(--text-secondary);
  font-size: 14px;
  cursor: pointer;
  transition: all 0.2s ease;
}

.back-btn:hover {
  background: var(--glass-bg-hover);
  border-color: var(--glass-border-hover);
  color: var(--text-primary);
}

.page-header h2 {
  font-size: 20px;
  font-weight: 700;
  color: var(--text-primary);
  flex: 1;
}

.status-card {
  padding: 8px;
  margin-bottom: 20px;
}

.detail-content {
  display: flex;
  flex-direction: column;
  gap: 20px;
}

.compare-card {
  padding: 16px;
}

.params-grid {
  padding: 4px;
}

.params-grid-title {
  font-size: 16px;
  font-weight: 600;
  color: var(--text-primary);
  padding: 16px 20px 12px;
}

.params-grid-body {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  border: 1px solid rgba(255, 255, 255, 0.15);
  border-radius: var(--radius-md);
  overflow: hidden;
  margin: 0 4px 4px;
}

.param-item {
  display: flex;
  flex-direction: column;
  gap: 6px;
  padding: 14px 16px;
  border-right: 1px solid rgba(255, 255, 255, 0.15);
  border-bottom: 1px solid rgba(255, 255, 255, 0.15);
}

.param-item:nth-child(3n) {
  border-right: none;
}

.param-item--full {
  grid-column: 1 / -1;
  border-right: none;
}

.param-label {
  font-size: 12px;
  color: var(--text-muted);
  font-weight: 500;
}

.param-value {
  font-size: 14px;
  color: var(--text-primary);
  font-weight: 500;
}

/* ---- Responsive ---- */
@media (max-width: 768px) {
  .params-grid-body {
    grid-template-columns: repeat(2, 1fr);
  }

  .param-item {
    border-right: 1px solid rgba(255, 255, 255, 0.15);
  }

  .param-item:nth-child(3n) {
    border-right: 1px solid rgba(255, 255, 255, 0.15);
  }

  .param-item:nth-child(2n) {
    border-right: none;
  }
}

@media (max-width: 480px) {
  .params-grid-body {
    grid-template-columns: 1fr;
  }

  .param-item {
    border-right: none;
  }
}
</style>
