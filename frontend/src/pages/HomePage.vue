<template>
  <div class="home-page">
    <div class="hero-section">
      <h1 class="hero-title">柜子家具3D渲染平台</h1>
      <p class="hero-desc">上传柜子图片，AI 智能渲染，生成真实感3D效果图</p>
    </div>

    <div class="mode-section">
      <h2 class="section-title">选择渲染模式</h2>
      <div class="mode-cards">
        <div class="mode-card" @click="$router.push('/render/single')">
          <div class="mode-icon">
            <el-icon :size="48"><PictureFilled /></el-icon>
          </div>
          <h3>单品渲染</h3>
          <p>对单个柜子家具进行真实感渲染，支持多种风格和光照</p>
          <el-button type="primary" size="large">开始渲染</el-button>
        </div>
        <div class="mode-card" @click="$router.push('/render/scene')">
          <div class="mode-icon">
            <el-icon :size="48"><HomeFilled /></el-icon>
          </div>
          <h3>场景渲染</h3>
          <p>将柜子布置在客厅、卧室等典型户型中进行场景化渲染</p>
          <el-button type="success" size="large">开始渲染</el-button>
        </div>
      </div>
    </div>

    <div v-if="recentTasks.length > 0" class="recent-section">
      <div class="section-header">
        <h2 class="section-title">近期渲染任务</h2>
        <el-button text type="primary" @click="$router.push('/history')">查看全部</el-button>
      </div>
      <div class="recent-grid">
        <TaskCard
          v-for="task in recentTasks"
          :key="task.task_id"
          :task="task"
          @click="$router.push(`/render/${task.task_id}`)"
        />
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { getHistory } from '@/api/render'
import TaskCard from '@/components/TaskCard.vue'
import type { RenderTask } from '@/types'

const recentTasks = ref<RenderTask[]>([])

onMounted(async () => {
  try {
    const res: any = await getHistory(1, 6)
    if (res.code === 200) {
      recentTasks.value = res.data.items || []
    }
  } catch (e) {
    console.error('加载历史失败', e)
  }
})
</script>

<style scoped>
.home-page {
  max-width: 1000px;
  margin: 0 auto;
}

.hero-section {
  text-align: center;
  padding: 40px 0 20px;
}

.hero-title {
  font-size: 32px;
  font-weight: 700;
  color: #303133;
  margin-bottom: 12px;
}

.hero-desc {
  font-size: 16px;
  color: #909399;
}

.section-title {
  font-size: 20px;
  font-weight: 600;
  color: #303133;
  margin-bottom: 20px;
}

.mode-cards {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 24px;
  margin-bottom: 40px;
}

.mode-card {
  padding: 32px;
  text-align: center;
  border: 2px solid #e4e7ed;
  border-radius: 12px;
  cursor: pointer;
  transition: all 0.3s;
  background: #fff;
}

.mode-card:hover {
  border-color: #409eff;
  box-shadow: 0 4px 20px rgba(64, 158, 255, 0.15);
  transform: translateY(-2px);
}

.mode-icon {
  color: #409eff;
  margin-bottom: 16px;
}

.mode-card h3 {
  font-size: 20px;
  font-weight: 600;
  color: #303133;
  margin-bottom: 8px;
}

.mode-card p {
  font-size: 14px;
  color: #909399;
  margin-bottom: 20px;
  line-height: 1.6;
}

.section-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin-bottom: 20px;
}

.recent-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(220px, 1fr));
  gap: 16px;
}
</style>