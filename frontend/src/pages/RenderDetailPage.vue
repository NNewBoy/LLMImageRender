<template>
  <div class="render-detail-page">
    <div class="page-header">
      <el-button text @click="$router.push('/')">
        <el-icon><ArrowLeft /></el-icon> 返回
      </el-button>
      <h2>渲染详情</h2>
      <el-tag :type="tagType" size="large">{{ statusLabel }}</el-tag>
    </div>

    <TaskStatus
      :status="task?.status || 'queued'"
      :progress="task?.progress || 0"
      :error-message="task?.error_message"
    />

    <div v-if="task" class="detail-content">
      <ImageCompare
        :original-url="task.original_image_url"
        :result-url="task.result_image_url"
      />

      <el-descriptions title="渲染参数" :column="2" border class="params-desc">
        <el-descriptions-item label="渲染模式">
          {{ task.mode === 'single' ? '单品渲染' : '场景渲染' }}
        </el-descriptions-item>
        <el-descriptions-item label="风格">{{ task.params.style }}</el-descriptions-item>
        <el-descriptions-item label="光照">{{ task.params.lighting }}</el-descriptions-item>
        <el-descriptions-item label="视角">{{ task.params.view_angle }}</el-descriptions-item>
        <el-descriptions-item v-if="task.params.room_type" label="户型">
          {{ task.params.room_type }}
        </el-descriptions-item>
        <el-descriptions-item label="材质">{{ task.params.material }}</el-descriptions-item>
        <el-descriptions-item label="颜色">
          <el-color-picker :model-value="task.params.color" disabled />
        </el-descriptions-item>
        <el-descriptions-item v-if="task.mode === 'single' && task.params.background_color" label="背景颜色">
          <el-color-picker :model-value="task.params.background_color" disabled />
        </el-descriptions-item>
        <el-descriptions-item v-if="task.params.description" label="描述" :span="2">
          {{ task.params.description }}
        </el-descriptions-item>
      </el-descriptions>
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
  max-width: 1000px;
  margin: 0 auto;
}

.page-header {
  display: flex;
  align-items: center;
  gap: 12px;
  margin-bottom: 20px;
}

.page-header h2 {
  font-size: 20px;
  font-weight: 600;
  color: #303133;
  flex: 1;
}

.detail-content {
  margin-top: 20px;
}

.params-desc {
  margin-top: 24px;
}
</style>