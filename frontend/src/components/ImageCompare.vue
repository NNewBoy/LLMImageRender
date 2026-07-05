<template>
  <div class="image-compare">
    <div class="compare-container">
      <div class="compare-image">
        <div class="image-label">原始图片</div>
        <div class="image-container">
          <ImageViewer :src="originalUrl" alt="原始图片" />
        </div>
      </div>
      <div class="compare-image">
        <div class="image-label image-label--result">渲染结果</div>
        <div class="image-container">
          <ImageViewer v-if="resultUrl" :src="resultUrl" alt="渲染结果" />
          <div v-else class="no-result">
            <el-icon :size="32"><PictureFilled /></el-icon>
            <span>等待渲染结果...</span>
          </div>
        </div>
      </div>
    </div>
    <div v-if="resultUrl" class="compare-actions">
      <el-button type="primary" @click="downloadImage">
        <el-icon><Download /></el-icon>
        下载渲染图
      </el-button>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ElMessage } from 'element-plus'
import { PictureFilled, Download } from '@element-plus/icons-vue'
import ImageViewer from '@/components/ImageViewer.vue'

const props = defineProps<{
  originalUrl: string
  resultUrl: string | null
}>()

const downloadImage = () => {
  if (props.resultUrl) {
    const a = document.createElement('a')
    a.href = props.resultUrl
    a.download = 'render_result.png'
    a.click()
    ElMessage.success('开始下载')
  }
}
</script>

<style scoped>
.image-compare {
  width: 100%;
}

.compare-container {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 16px;
}

.compare-image {
  border-radius: var(--radius-md);
  overflow: hidden;
  border: 1px solid var(--glass-border);
  background: var(--media-bg);
}

.image-label {
  padding: 10px 14px;
  font-size: 13px;
  font-weight: 600;
  color: var(--text-muted);
  background: rgba(255, 255, 255, 0.04);
  border-bottom: 1px solid var(--glass-border);
}

.image-label--result {
  color: var(--accent-primary-light);
}

.image-container {
  height: 440px;
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 8px;
}

.no-result {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: 60px;
  color: var(--text-faint);
  gap: 8px;
  font-size: 13px;
}

.compare-actions {
  margin-top: 16px;
  text-align: center;
}

/* ---- Responsive ---- */
@media (max-width: 768px) {
  .compare-container {
    grid-template-columns: 1fr;
    gap: 12px;
  }

  .image-container {
    height: 280px;
  }
}
</style>
