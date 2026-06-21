<template>
  <div class="scene-render-page">
    <div class="page-header">
      <el-button text @click="$router.push('/')">
        <el-icon><ArrowLeft /></el-icon> 返回
      </el-button>
      <h2>场景渲染</h2>
    </div>

    <div class="render-layout">
      <div class="render-left">
        <el-card header="上传图片">
          <ImageUploader @uploaded="onImageUploaded" />
        </el-card>
        <el-card header="从图库选择" class="gallery-card">
          <GalleryPicker @selected="onGallerySelected" />
        </el-card>
        <el-card header="选择户型" class="room-card">
          <RoomTypeSelector
            :model-value="renderStore.params.room_type || 'living_room'"
            @update:model-value="onRoomChange"
          />
        </el-card>
        <div v-if="renderStore.selectedImageUrl" class="preview-card">
          <el-card header="已选图片">
            <img :src="renderStore.selectedImageUrl" alt="已选图片" class="selected-preview" />
            <div class="selected-name">{{ renderStore.selectedImageName }}</div>
          </el-card>
        </div>
      </div>

      <div class="render-right">
        <el-card>
          <ParamPanel :show-room-type="true" />
        </el-card>
        <SubmitBar />
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { onMounted } from 'vue'
import { useRenderStore } from '@/stores/render'
import ImageUploader from '@/components/ImageUploader.vue'
import GalleryPicker from '@/components/GalleryPicker.vue'
import RoomTypeSelector from '@/components/RoomTypeSelector.vue'
import ParamPanel from '@/components/ParamPanel.vue'
import SubmitBar from '@/components/SubmitBar.vue'

const renderStore = useRenderStore()

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
  max-width: 1200px;
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

.render-layout {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 20px;
  align-items: start;
}

.gallery-card, .room-card {
  margin-top: 16px;
}

.preview-card {
  margin-top: 16px;
}

.selected-preview {
  width: 100%;
  max-height: 200px;
  object-fit: contain;
  border-radius: 6px;
}

.selected-name {
  margin-top: 8px;
  font-size: 13px;
  color: #909399;
  text-align: center;
}
</style>