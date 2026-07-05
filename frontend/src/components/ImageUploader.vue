<template>
  <div class="image-uploader">
    <el-upload
      class="upload-area"
      drag
      :auto-upload="false"
      :show-file-list="false"
      :on-change="handleFileChange"
      accept=".jpg,.jpeg,.png,.webp"
    >
      <div v-if="!previewUrl" class="upload-placeholder">
        <el-icon :size="48"><Plus /></el-icon>
        <div class="upload-text">点击上传或拖拽图片到此处</div>
        <div class="upload-hint">支持 JPG / PNG / WebP，最大 10MB</div>
      </div>
      <div v-else class="upload-preview">
        <el-image :src="previewUrl" alt="预览" fit="contain" />
        <div class="preview-mask">
          <span>点击更换图片</span>
        </div>
      </div>
    </el-upload>
    <div v-if="fileName" class="file-info">
      <el-icon><Document /></el-icon>
      <span>{{ fileName }}</span>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue'
import { ElMessage } from 'element-plus'
import { Plus, Document } from '@element-plus/icons-vue'
import { uploadImage } from '@/api/gallery'
import { useRenderStore } from '@/stores/render'

const emit = defineEmits(['uploaded'])
const renderStore = useRenderStore()

const previewUrl = ref('')
const fileName = ref('')

const handleFileChange = async (file: any) => {
  const raw = file.raw
  if (!raw) return

  const maxSize = 10 * 1024 * 1024
  if (raw.size > maxSize) {
    ElMessage.error('文件大小不能超过 10MB')
    return
  }

  previewUrl.value = URL.createObjectURL(raw)
  fileName.value = raw.name

  try {
    const res: any = await uploadImage(raw)
    if (res.code === 200) {
      renderStore.setUploadImage(res.data.image_id, res.data.url, res.data.name)
      emit('uploaded', res.data)
      ElMessage.success('图片上传成功')
    }
  } catch (e: any) {
    ElMessage.error(e.message || '上传失败')
  }
}
</script>

<style scoped>
.image-uploader {
  width: 100%;
}

.upload-area {
  width: 100%;
}

.upload-placeholder {
  padding: 40px;
  text-align: center;
  color: var(--text-muted);
}

.upload-text {
  margin-top: 12px;
  font-size: 15px;
  color: var(--text-secondary);
  font-weight: 500;
}

.upload-hint {
  margin-top: 8px;
  font-size: 12px;
  color: var(--text-faint);
}

.upload-preview {
  position: relative;
  height: 300px;
  overflow: hidden;
  border-radius: var(--radius-md);
}

.upload-preview .el-image {
  width: 100%;
  height: 100%;
}

.preview-mask {
  position: absolute;
  inset: 0;
  background: rgba(0, 0, 0, 0.5);
  backdrop-filter: blur(4px);
  display: flex;
  align-items: center;
  justify-content: center;
  color: #fff;
  font-size: 14px;
  opacity: 0;
  transition: opacity 0.25s ease;
}

.upload-preview:hover .preview-mask {
  opacity: 1;
}

.file-info {
  margin-top: 8px;
  display: flex;
  align-items: center;
  gap: 6px;
  font-size: 13px;
  color: var(--text-muted);
}
</style>
