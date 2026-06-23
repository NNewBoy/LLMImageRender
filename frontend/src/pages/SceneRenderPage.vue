<template>
  <div class="scene-render-page">
    <div class="page-header">
      <button class="back-btn" @click="$router.push('/')">
        <el-icon :size="18"><ArrowLeft /></el-icon>
        <span>返回</span>
      </button>
      <h2>场景渲染</h2>
    </div>

    <div class="render-content">
      <el-card class="image-card glass-card">
        <el-tabs v-model="activeTab" type="border-card">
          <el-tab-pane label="上传图片" name="upload">
            <ImageUploader @uploaded="onImageUploaded" />
          </el-tab-pane>
          <el-tab-pane label="从图库选择" name="gallery">
            <GalleryPicker @selected="onGallerySelected" />
          </el-tab-pane>
        </el-tabs>
        <div v-if="renderStore.selectedImageUrl" class="preview-section">
          <el-divider />
          <div class="preview-title">已选图片</div>
          <div class="preview-container">
            <ImageViewer :src="renderStore.selectedImageUrl" alt="已选图片" />
          </div>
          <div class="selected-name">{{ renderStore.selectedImageName }}</div>
        </div>
      </el-card>

      <el-card class="room-card glass-card" header="选择户型">
        <RoomTypeSelector
          :model-value="renderStore.params.room_type || 'living_room'"
          @update:model-value="onRoomChange"
        />
      </el-card>

      <el-card class="params-card glass-card">
        <ParamPanel :show-room-type="true" />
      </el-card>

      <div class="submit-section">
        <SubmitBar />
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { useRoute } from 'vue-router'
import { ElMessage } from 'element-plus'
import { useRenderStore } from '@/stores/render'
import ImageUploader from '@/components/ImageUploader.vue'
import GalleryPicker from '@/components/GalleryPicker.vue'
import ImageViewer from '@/components/ImageViewer.vue'
import RoomTypeSelector from '@/components/RoomTypeSelector.vue'
import ParamPanel from '@/components/ParamPanel.vue'
import SubmitBar from '@/components/SubmitBar.vue'
import { parseUrlParams, applyExternalImage } from '@/utils/urlParams'

const route = useRoute()
const renderStore = useRenderStore()
const activeTab = ref('upload')

onMounted(async () => {
  renderStore.setMode('scene')

  const urlResult = parseUrlParams(route.query, route.hash)

  // 应用 URL 中的渲染参数
  if (Object.keys(urlResult.params).length > 0) {
    renderStore.updateParams(urlResult.params)
  }

  // 应用外部图片
  if (urlResult.hasExternalImage) {
    const ok = await applyExternalImage(renderStore, urlResult.imageUrl, urlResult.imageBase64, urlResult.imageId)
    if (ok) {
      ElMessage.success('外部图片已加载')
    } else if (urlResult.imageId) {
      ElMessage.error(`图库中未找到该图片（image_id: ${urlResult.imageId}）`)
    } else {
      ElMessage.error('外部图片加载失败')
    }
  }
})

const onImageUploaded = (data: any) => {
  console.log('图片已上传', data)
}

const onGallerySelected = (data: any) => {
  console.log('图库图片已选择', data)
}

const onRoomChange = (val: string) => {
  renderStore.updateParams({ room_type: val })
}
</script>

<style scoped>
.scene-render-page {
  max-width: 860px;
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
}

.render-content {
  display: flex;
  flex-direction: column;
  gap: 20px;
}

.preview-section {
  padding: 0 4px 8px;
}

.preview-title {
  font-size: 14px;
  font-weight: 600;
  color: var(--text-primary);
  margin-bottom: 12px;
}

.preview-container {
  display: flex;
  align-items: center;
  justify-content: center;
  border-radius: var(--radius-md);
  border: 1px solid var(--glass-border);
  background: rgba(0, 0, 0, 0.2);
  padding: 8px;
  height: 300px;
}

.selected-name {
  margin-top: 8px;
  font-size: 13px;
  color: var(--text-muted);
  text-align: center;
}

.submit-section {
  padding-bottom: 24px;
}

/* ---- Responsive ---- */
@media (max-width: 768px) {
  .preview-container {
    height: 240px;
  }
}
</style>
