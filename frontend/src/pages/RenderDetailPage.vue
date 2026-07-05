<template>
  <div class="render-detail-page">
    <div class="page-header">
      <div class="header-left">
        <button class="back-btn" @click="$router.push('/')">
          <el-icon :size="18"><ArrowLeft /></el-icon>
          <span>返回</span>
        </button>
        <h2>渲染详情</h2>
      </div>
      <div v-if="task" class="header-actions">
        <el-button
          type="primary"
          :loading="reRenderLoading"
          :disabled="!task.image_id || task.status === 'processing'"
          @click="handleReRender"
        >
          <el-icon><RefreshRight /></el-icon>
          <span>再次渲染</span>
        </el-button>
        <el-button type="danger" plain :disabled="task.status === 'processing'" @click="handleDelete">
          <el-icon><Delete /></el-icon>
          <span>删除</span>
        </el-button>
      </div>
    </div>

    <div class="status-card glass-card" :class="task ? `status-card--${task.status}` : ''">
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
        <div class="params-grid-title">
          <span>渲染参数</span>
        </div>
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
import { ref, onMounted, onUnmounted, watch } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { ElMessage, ElMessageBox } from 'element-plus'
import { ArrowLeft, RefreshRight, Delete } from '@element-plus/icons-vue'
import { getTaskStatus, deleteTask, submitRender } from '@/api/render'
import TaskStatus from '@/components/TaskStatus.vue'
import ImageCompare from '@/components/ImageCompare.vue'
import type { RenderTask } from '@/types'

const route = useRoute()
const router = useRouter()
const task = ref<RenderTask | null>(null)
let pollTimer: any = null
const reRenderLoading = ref(false)

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

const handleDelete = async () => {
  try {
    await ElMessageBox.confirm('确定删除该渲染记录？删除后不可恢复。', '删除确认', {
      confirmButtonText: '删除',
      cancelButtonText: '取消',
      type: 'warning',
    })
  } catch {
    return
  }

  const taskId = route.params.taskId as string
  try {
    const res: any = await deleteTask(taskId)
    if (res.code === 200) {
      ElMessage.success('已删除')
      stopPolling()
      router.push('/')
    }
  } catch (e: any) {
    ElMessage.error(e.message || '删除失败')
  }
}

const handleReRender = async () => {
  if (!task.value?.image_id) return
  reRenderLoading.value = true
  try {
    const res: any = await submitRender({
      mode: task.value.mode,
      image_source: {
        type: task.value.image_source || 'gallery',
        image_id: task.value.image_id,
      },
      params: task.value.params,
    })
    if (res.code === 200) {
      ElMessage.success('渲染任务已提交')
      router.push(`/render/${res.data.task_id}`)
    }
  } catch (e: any) {
    ElMessage.error(e.message || '提交失败')
  } finally {
    reRenderLoading.value = false
  }
}

onMounted(() => {
  fetchTask()
  startPolling()
})

// 监听路由参数变化（同组件跳转时 onMounted 不会重新触发）
watch(() => route.params.taskId, (newId) => {
  if (newId) {
    task.value = null
    fetchTask()
    startPolling()
  }
})

onUnmounted(stopPolling)
</script>

<style scoped>
.render-detail-page {
  max-width: 1100px;
  margin: 0 auto;
}

/* ---- Page Header ---- */
.page-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 12px;
  margin-bottom: 24px;
  flex-wrap: wrap;
}

.header-left {
  display: flex;
  align-items: center;
  gap: 12px;
  min-width: 0;
}

.back-btn {
  display: flex;
  align-items: center;
  gap: 4px;
  padding: 8px 14px;
  border-radius: var(--radius-sm);
  border: 1px solid var(--glass-border);
  background: var(--glass-bg);
  backdrop-filter: blur(12px);
  -webkit-backdrop-filter: blur(12px);
  color: var(--text-secondary);
  font-size: 14px;
  cursor: pointer;
  transition: all 0.2s ease;
  flex-shrink: 0;
}

.back-btn:hover {
  background: var(--glass-bg-hover);
  border-color: var(--glass-border-hover);
  color: var(--text-primary);
  transform: translateX(-2px);
}

.header-left h2 {
  font-size: 22px;
  font-weight: 700;
  color: var(--text-primary);
  letter-spacing: -0.02em;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

.header-actions {
  display: flex;
  gap: 8px;
  flex-shrink: 0;
}

/* ---- Status Card ---- */
.status-card {
  padding: 8px;
  margin-bottom: 20px;
  transition: all 0.3s ease;
}

.status-card--processing {
  border-color: rgba(99, 102, 241, 0.25);
  box-shadow: var(--shadow-glass), 0 0 32px rgba(99, 102, 241, 0.08);
}

.status-card--completed {
  border-color: rgba(34, 197, 94, 0.2);
}

.status-card--failed {
  border-color: rgba(239, 68, 68, 0.2);
}

/* ---- Detail Content ---- */
.detail-content {
  display: flex;
  flex-direction: column;
  gap: 20px;
}

.compare-card {
  padding: 16px;
}

/* ---- Params Grid ---- */
.params-grid {
  padding: 4px;
}

.params-grid-title {
  display: flex;
  align-items: center;
  gap: 8px;
  font-size: 16px;
  font-weight: 600;
  color: var(--text-primary);
  padding: 18px 20px 14px;
}

.params-grid-title::before {
  content: '';
  width: 3px;
  height: 16px;
  border-radius: 2px;
  background: var(--accent-primary);
  box-shadow: 0 0 8px var(--accent-primary-glow);
}

.params-grid-body {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  border: 1px solid var(--glass-border);
  border-radius: var(--radius-md);
  overflow: hidden;
  margin: 0 4px 4px;
  background: var(--el-fill-color-lighter);
}

.param-item {
  display: flex;
  flex-direction: column;
  gap: 6px;
  padding: 16px 18px;
  border-right: 1px solid var(--glass-border);
  border-bottom: 1px solid var(--glass-border);
  transition: background 0.2s ease;
}

.param-item:hover {
  background: var(--el-fill-color-light);
}

.param-item:nth-child(3n) {
  border-right: none;
}

.param-item--full {
  grid-column: 1 / -1;
  border-right: none;
}

.param-label {
  font-size: 11px;
  color: var(--text-faint);
  font-weight: 600;
  text-transform: uppercase;
  letter-spacing: 0.05em;
}

.param-value {
  font-size: 14px;
  color: var(--text-primary);
  font-weight: 500;
  line-height: 1.5;
}

/* ---- Responsive ---- */
@media (max-width: 768px) {
  .params-grid-body {
    grid-template-columns: repeat(2, 1fr);
  }

  .param-item {
    border-right: 1px solid var(--glass-border);
  }

  .param-item:nth-child(3n) {
    border-right: 1px solid var(--glass-border);
  }

  .param-item:nth-child(2n) {
    border-right: none;
  }

  .header-actions {
    width: 100%;
  }

  .header-actions :deep(.el-button) {
    flex: 1;
  }
}

@media (max-width: 480px) {
  .params-grid-body {
    grid-template-columns: 1fr;
  }

  .param-item {
    border-right: none;
  }

  .header-left h2 {
    font-size: 18px;
  }

  .header-actions :deep(.el-button) {
    padding: 8px 12px;
    min-height: 40px;
  }

  .back-btn span {
    display: none;
  }

  .back-btn {
    padding: 8px 10px;
    min-height: 40px;
  }
}

/* ---- Reduced Motion ---- */
@media (prefers-reduced-motion: reduce) {
  .back-btn:hover {
    transform: none;
  }
}
</style>
