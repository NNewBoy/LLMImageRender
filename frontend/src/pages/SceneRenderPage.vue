<template>
  <div class="scene-render-page">
    <div class="page-header">
      <el-button text @click="$router.push('/')">
        <el-icon><ArrowLeft /></el-icon> 返回
      </el-button>
      <h2>场景渲染</h2>
    </div>

    <div class="render-content">
      <el-card class="image-card">
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

      <el-card class="room-card" header="选择户型">
        <RoomTypeSelector
          :model-value="renderStore.params.room_type || 'living_room'"
          @update:model-value="onRoomChange"
        />
      </el-card>

      <el-card class="params-card">
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
import { useRenderStore } from '@/stores/render'
import ImageUploader from '@/components/ImageUploader.vue'
import GalleryPicker from '@/components/GalleryPicker.vue'
import ImageViewer from '@/components/ImageViewer.vue'
import RoomTypeSelector from '@/components/RoomTypeSelector.vue'
import ParamPanel from '@/components/ParamPanel.vue'
import SubmitBar from '@/components/SubmitBar.vue'

const renderStore = useRenderStore()
const activeTab = ref('upload')

onMounted(() => {
  renderStore.setMode('scene')
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
  max-width: 800px;
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
}

.render-content {
  display: flex;
  flex-direction: column;
  gap: 20px;
}

.image-card {
  width: 100%;
}

.preview-section {
  padding: 0 20px 20px;
}

.preview-title {
  font-size: 14px;
  font-weight: 600;
  color: #303133;
  margin-bottom: 12px;
}

.preview-container {
  display: flex;
  align-items: center;
  justify-content: center;
  border-radius: 6px;
  border: 1px solid #e4e7ed;
  background: #fafafa;
  padding: 8px;
  height: 300px;
}

.selected-name {
  margin-top: 8px;
  font-size: 13px;
  color: #909399;
  text-align: center;
}

.room-card {
  width: 100%;
}

.params-card {
  width: 100%;
}

.submit-section {
  width: 100%;
  padding-bottom: 40px;
}
</style>