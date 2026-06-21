<template>
  <div class="history-page">
    <div class="page-header">
      <h2>渲染历史</h2>
      <span class="total-count">共 {{ total }} 条记录</span>
    </div>

    <div v-loading="loading" class="history-grid">
      <TaskCard
        v-for="task in tasks"
        :key="task.task_id"
        :task="task"
        @click="$router.push(`/render/${task.task_id}`)"
      />
    </div>

    <div v-if="!loading && tasks.length === 0" class="empty-state">
      <el-icon :size="48"><FolderOpened /></el-icon>
      <p>暂无渲染记录</p>
      <el-button type="primary" @click="$router.push('/')">开始渲染</el-button>
    </div>

    <div v-if="total > pageSize" class="pagination">
      <el-pagination
        v-model:current-page="page"
        :page-size="pageSize"
        :total="total"
        layout="prev, pager, next"
        @current-change="loadHistory"
      />
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { getHistory } from '@/api/render'
import TaskCard from '@/components/TaskCard.vue'
import type { RenderTask } from '@/types'

const tasks = ref<RenderTask[]>([])
const total = ref(0)
const loading = ref(false)
const page = ref(1)
const pageSize = 20

const loadHistory = async () => {
  loading.value = true
  try {
    const res: any = await getHistory(page.value, pageSize)
    if (res.code === 200) {
      tasks.value = res.data.items || []
      total.value = res.data.total || 0
    }
  } catch (e) {
    console.error('加载历史失败', e)
  } finally {
    loading.value = false
  }
}

onMounted(loadHistory)
</script>

<style scoped>
.history-page {
  max-width: 1000px;
  margin: 0 auto;
}

.page-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin-bottom: 20px;
}

.page-header h2 {
  font-size: 20px;
  font-weight: 600;
  color: #303133;
}

.total-count {
  font-size: 13px;
  color: #909399;
}

.history-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(220px, 1fr));
  gap: 16px;
}

.empty-state {
  text-align: center;
  padding: 60px;
  color: #c0c4cc;
}

.empty-state p {
  margin: 12px 0;
  font-size: 14px;
}

.pagination {
  margin-top: 24px;
  display: flex;
  justify-content: center;
}
</style>