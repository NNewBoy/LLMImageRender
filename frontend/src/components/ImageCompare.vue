<template>
  <div class="image-compare">
    <div class="compare-container">
      <div class="compare-image compare-original">
        <div class="image-label">原始图片</div>
        <img :src="originalUrl" alt="原始图片" />
      </div>
      <div class="compare-image compare-result">
        <div class="image-label">渲染结果</div>
        <img v-if="resultUrl" :src="resultUrl" alt="渲染结果" />
        <div v-else class="no-result">
          <el-icon :size="32"><PictureFilled /></el-icon>
          <span>等待渲染结果...</span>
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
  border-radius: 8px;
  overflow: hidden;
  border: 1px solid #e4e7ed;
  background: #fafafa;
}

.image-label {
  padding: 8px 12px;
  font-size: 13px;
  font-weight: 600;
  color: #606266;
  background: #f5f7fa;
  border-bottom: 1px solid #e4e7ed;
}

.compare-image img {
  width: 100%;
  max-height: 400px;
  object-fit: contain;
  display: block;
}

.no-result {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: 60px;
  color: #c0c4cc;
  gap: 8px;
  font-size: 13px;
}

.compare-actions {
  margin-top: 16px;
  text-align: center;
}
</style>