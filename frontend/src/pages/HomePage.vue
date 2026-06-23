<template>
  <div class="home-page">
    <!-- Hero -->
    <section class="hero-section">
      <div class="hero-badge glass">AI 驱动 · 真实感 3D 渲染</div>
      <h1 class="hero-title">柜子家具 3D 渲染平台</h1>
      <p class="hero-desc">上传柜子图片，AI 智能渲染，生成真实感 3D 效果图</p>
    </section>

    <!-- Mode cards -->
    <section class="mode-section">
      <h2 class="section-title">选择渲染模式</h2>
      <div class="mode-cards">
        <div class="mode-card glass-card" @click="$router.push('/render/single')">
          <div class="mode-icon mode-icon--blue">
            <el-icon :size="40"><PictureFilled /></el-icon>
          </div>
          <h3>单品渲染</h3>
          <p>对单个柜子家具进行真实感渲染，支持多种风格和光照</p>
          <span class="mode-cta">
            开始渲染
            <el-icon><ArrowRight /></el-icon>
          </span>
        </div>
        <div class="mode-card glass-card" @click="$router.push('/render/scene')">
          <div class="mode-icon mode-icon--purple">
            <el-icon :size="40"><HomeFilled /></el-icon>
          </div>
          <h3>场景渲染</h3>
          <p>将柜子布置在客厅、卧室等典型户型中进行场景化渲染</p>
          <span class="mode-cta">
            开始渲染
            <el-icon><ArrowRight /></el-icon>
          </span>
        </div>
      </div>
    </section>

    <!-- Recent tasks -->
    <section v-if="recentTasks.length > 0" class="recent-section">
      <div class="section-header">
        <h2 class="section-title">近期渲染任务</h2>
        <button class="view-all-btn" @click="$router.push('/history')">
          <span>查看全部</span>
          <el-icon><ArrowRight /></el-icon>
        </button>
      </div>
      <div class="recent-grid">
        <TaskCard
          v-for="task in recentTasks"
          :key="task.task_id"
          :task="task"
          @click="$router.push(`/render/${task.task_id}`)"
        />
      </div>
    </section>
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

/* Hero */
.hero-section {
  text-align: center;
  padding: 48px 0 40px;
}

.hero-badge {
  display: inline-block;
  padding: 6px 16px;
  border-radius: 100px;
  font-size: 13px;
  font-weight: 500;
  color: var(--accent-primary-light);
  margin-bottom: 20px;
}

.hero-title {
  font-size: 36px;
  font-weight: 800;
  color: var(--text-primary);
  margin-bottom: 12px;
  letter-spacing: -0.03em;
  line-height: 1.2;
}

.hero-desc {
  font-size: 16px;
  color: var(--text-muted);
  max-width: 480px;
  margin: 0 auto;
  line-height: 1.6;
}

/* Section */
.section-title {
  font-size: 18px;
  font-weight: 600;
  color: var(--text-primary);
  margin-bottom: 20px;
}

.section-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin-bottom: 20px;
}

.view-all-btn {
  display: inline-flex;
  align-items: center;
  gap: 4px;
  padding: 8px 16px;
  border: 1px solid var(--glass-border);
  border-radius: 100px;
  background: var(--glass-bg);
  color: var(--text-secondary);
  font-size: 14px;
  font-weight: 500;
  cursor: pointer;
  transition: all 0.2s ease;
}

.view-all-btn:hover {
  color: var(--accent-primary-light);
  background: rgba(99, 102, 241, 0.1);
  border-color: rgba(99, 102, 241, 0.3);
  gap: 8px;
}

/* Mode cards */
.mode-cards {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 24px;
  margin-bottom: 48px;
}

.mode-card {
  padding: 32px 28px;
  text-align: center;
  cursor: pointer;
}

.mode-icon {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  width: 72px;
  height: 72px;
  border-radius: 20px;
  margin-bottom: 20px;
}

.mode-icon--blue {
  color: var(--accent-primary-light);
  background: rgba(99, 102, 241, 0.12);
}

.mode-icon--purple {
  color: #a78bfa;
  background: rgba(139, 92, 246, 0.12);
}

.mode-card h3 {
  font-size: 20px;
  font-weight: 700;
  color: var(--text-primary);
  margin-bottom: 8px;
}

.mode-card p {
  font-size: 14px;
  color: var(--text-muted);
  margin-bottom: 20px;
  line-height: 1.6;
}

.mode-cta {
  display: inline-flex;
  align-items: center;
  gap: 6px;
  font-size: 14px;
  font-weight: 600;
  color: var(--accent-primary-light);
  transition: gap 0.2s ease;
}

.mode-card:hover .mode-cta {
  gap: 10px;
}

/* Recent grid */
.recent-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(220px, 1fr));
  gap: 16px;
}

/* ---- Responsive ---- */
@media (max-width: 768px) {
  .hero-section {
    padding: 32px 0 28px;
  }

  .hero-title {
    font-size: 26px;
  }

  .hero-desc {
    font-size: 15px;
  }

  .mode-cards {
    grid-template-columns: 1fr;
    gap: 16px;
    margin-bottom: 32px;
  }

  .mode-card {
    padding: 24px 20px;
  }

  .recent-grid {
    grid-template-columns: repeat(auto-fill, minmax(160px, 1fr));
    gap: 12px;
  }
}

@media (max-width: 375px) {
  .hero-title {
    font-size: 22px;
  }

  .recent-grid {
    grid-template-columns: 1fr 1fr;
  }
}
</style>
