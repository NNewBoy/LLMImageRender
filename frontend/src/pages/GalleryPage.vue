<template>
  <div class="gallery-page">
    <div class="page-header">
      <h2>柜子图库</h2>
      <span class="header-count" v-if="images.length">{{ images.length }} 张图片</span>
    </div>

    <div class="gallery-filter glass-card">
      <el-radio-group v-model="category" @change="loadGallery">
        <el-radio-button value="">全部</el-radio-button>
        <el-radio-button v-for="c in categories" :key="c.value" :value="c.value">
          {{ c.label }}
        </el-radio-button>
      </el-radio-group>
    </div>

    <div v-loading="loading" class="gallery-grid">
      <div
        v-for="(img, index) in images"
        :key="img.image_id"
        class="gallery-card glass-card"
        :style="{ animationDelay: `${index * 40}ms` }"
      >
        <div class="gallery-image">
          <ImageViewer :src="img.thumbnail_url" :alt="img.name" :preview="false" />
          <div class="image-overlay">
            <span class="overlay-tag">{{ categoryLabel(img.category) }}</span>
          </div>
        </div>
        <div class="gallery-info">
          <div class="gallery-name">{{ img.name }}</div>
          <div class="gallery-meta">
            <span v-if="img.width" class="meta-size">{{ img.width }}x{{ img.height }}</span>
          </div>
        </div>
        <div class="card-actions">
          <el-button text size="small" @click="openEditDialog(img)">
            <el-icon><Edit /></el-icon> 编辑
          </el-button>
          <el-button text size="small" type="danger" @click="handleDelete(img)">
            <el-icon><Delete /></el-icon> 删除
          </el-button>
        </div>
      </div>
    </div>

    <div v-if="!loading && images.length === 0" class="empty-state glass-card">
      <el-icon :size="48"><PictureFilled /></el-icon>
      <p>暂无图片</p>
    </div>

    <!-- 编辑对话框 -->
    <el-dialog v-model="editDialogVisible" title="编辑图片" width="400px" append-to-body>
      <el-form :model="editForm" label-width="80px">
        <el-form-item label="图片名称">
          <el-input v-model="editForm.name" placeholder="请输入图片名称" />
        </el-form-item>
        <el-form-item label="所属分类">
          <el-select v-model="editForm.category" placeholder="请选择分类" style="width: 100%">
            <el-option v-for="c in categories" :key="c.value" :label="c.label" :value="c.value" />
          </el-select>
        </el-form-item>
      </el-form>
      <template #footer>
        <el-button @click="editDialogVisible = false">取消</el-button>
        <el-button type="primary" :loading="editLoading" @click="handleEditSubmit">保存</el-button>
      </template>
    </el-dialog>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { ElMessage, ElMessageBox } from 'element-plus'
import { getGallery, deleteImage, updateImage } from '@/api/gallery'
import ImageViewer from '@/components/ImageViewer.vue'
import type { GalleryImage, PresetOption } from '@/types'

const images = ref<GalleryImage[]>([])
const loading = ref(false)
const category = ref('')

const categories: PresetOption[] = [
  { value: 'wardrobe', label: '衣柜' },
  { value: 'kitchen', label: '橱柜' },
  { value: 'bookcase', label: '书柜' },
  { value: 'entryway', label: '玄关柜' },
  { value: 'tv_stand', label: '电视柜' },
  { value: 'other', label: '其他' },
]

const categoryLabel = (value: string) => {
  return categories.find((c) => c.value === value)?.label || value
}

// 编辑对话框
const editDialogVisible = ref(false)
const editLoading = ref(false)
const editForm = ref({ image_id: '', name: '', category: '' })

const openEditDialog = (img: GalleryImage) => {
  editForm.value = {
    image_id: img.image_id,
    name: img.name,
    category: img.category,
  }
  editDialogVisible.value = true
}

const handleEditSubmit = async () => {
  editLoading.value = true
  try {
    const res: any = await updateImage(editForm.value.image_id, {
      name: editForm.value.name,
      category: editForm.value.category,
    })
    if (res.code === 200) {
      ElMessage.success('更新成功')
      editDialogVisible.value = false
      loadGallery()
    }
  } catch (e: any) {
    ElMessage.error(e.message || '更新失败')
  } finally {
    editLoading.value = false
  }
}

const handleDelete = async (img: GalleryImage) => {
  try {
    await ElMessageBox.confirm(`确定删除图片「${img.name}」？删除后不可恢复。`, '删除确认', {
      confirmButtonText: '删除',
      cancelButtonText: '取消',
      type: 'warning',
    })
  } catch {
    return
  }

  try {
    const res: any = await deleteImage(img.image_id)
    if (res.code === 200) {
      ElMessage.success('删除成功')
      loadGallery()
    }
  } catch (e: any) {
    ElMessage.error(e.message || '删除失败')
  }
}

const loadGallery = async () => {
  loading.value = true
  try {
    const res: any = await getGallery(category.value || undefined)
    if (res.code === 200) {
      images.value = res.data
    }
  } catch (e) {
    console.error('加载图库失败', e)
  } finally {
    loading.value = false
  }
}

onMounted(loadGallery)
</script>

<style scoped>
.gallery-page {
  max-width: 1100px;
  margin: 0 auto;
}

/* ---- Page Header ---- */
.page-header {
  display: flex;
  align-items: baseline;
  gap: 12px;
  margin-bottom: 24px;
}

.page-header h2 {
  font-size: 24px;
  font-weight: 700;
  color: var(--text-primary);
  letter-spacing: -0.02em;
}

.header-count {
  font-size: 13px;
  color: var(--text-faint);
  font-weight: 500;
}

/* ---- Filter Bar ---- */
.gallery-filter {
  margin-bottom: 24px;
  padding: 10px 16px;
  overflow-x: auto;
  display: flex;
  align-items: center;
}

.gallery-filter :deep(.el-radio-group) {
  flex-wrap: nowrap;
}

/* ---- Gallery Grid ---- */
.gallery-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(240px, 1fr));
  gap: 20px;
}

/* ---- Gallery Card ---- */
.gallery-card {
  overflow: hidden;
  cursor: default;
  animation: card-enter 0.4s ease-out backwards;
}

@keyframes card-enter {
  from {
    opacity: 0;
    transform: translateY(12px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

.gallery-card:hover {
  transform: translateY(-4px);
  border-color: rgba(99, 102, 241, 0.3);
  box-shadow: var(--shadow-glass-lg), 0 0 24px rgba(99, 102, 241, 0.12);
}

/* ---- Card Image ---- */
.gallery-image {
  position: relative;
  height: 200px;
  overflow: hidden;
  background: var(--media-bg);
}

.gallery-image :deep(img) {
  width: 100%;
  height: 100%;
  object-fit: cover;
  transition: transform 0.35s cubic-bezier(0.22, 1, 0.36, 1);
}

.gallery-card:hover .gallery-image :deep(img) {
  transform: scale(1.06);
}

/* Image overlay with category tag */
.image-overlay {
  position: absolute;
  inset: 0;
  background: linear-gradient(
    to bottom,
    rgba(0, 0, 0, 0) 50%,
    rgba(0, 0, 0, 0.5) 100%
  );
  display: flex;
  align-items: flex-end;
  padding: 10px 12px;
  opacity: 0;
  transition: opacity 0.25s ease;
}

.gallery-card:hover .image-overlay {
  opacity: 1;
}

.overlay-tag {
  font-size: 11px;
  font-weight: 600;
  color: #fff;
  background: rgba(99, 102, 241, 0.85);
  backdrop-filter: blur(8px);
  padding: 3px 10px;
  border-radius: 6px;
  letter-spacing: 0.02em;
}

/* ---- Card Info ---- */
.gallery-info {
  padding: 14px 16px 10px;
}

.gallery-name {
  font-size: 14px;
  font-weight: 600;
  color: var(--text-primary);
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
  line-height: 1.4;
}

.gallery-meta {
  display: flex;
  align-items: center;
  margin-top: 6px;
  font-size: 12px;
}

.meta-size {
  color: var(--text-faint);
  font-family: 'Inter', monospace;
  font-variant-numeric: tabular-nums;
}

/* ---- Card Actions ---- */
.card-actions {
  display: flex;
  justify-content: flex-end;
  gap: 2px;
  padding: 8px 10px 12px;
  border-top: 1px solid rgba(255, 255, 255, 0.06);
}

.card-actions :deep(.el-button) {
  --el-button-text-color: var(--text-muted);
  transition: all 0.2s ease;
}

.card-actions :deep(.el-button:hover) {
  --el-button-text-color: var(--text-primary);
  background: rgba(255, 255, 255, 0.06);
}

.card-actions :deep(.el-button.el-button--danger:hover) {
  --el-button-text-color: var(--accent-danger);
  background: rgba(239, 68, 68, 0.1);
}

/* ---- Empty State ---- */
.empty-state {
  text-align: center;
  padding: 80px 40px;
  color: var(--text-muted);
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 16px;
}

.empty-state .el-icon {
  color: var(--text-faint);
  opacity: 0.5;
}

.empty-state p {
  font-size: 15px;
  font-weight: 500;
}

/* ---- Responsive ---- */
@media (max-width: 768px) {
  .gallery-grid {
    grid-template-columns: repeat(auto-fill, minmax(160px, 1fr));
    gap: 14px;
  }

  .gallery-image {
    height: 150px;
  }

  .page-header h2 {
    font-size: 20px;
  }
}

@media (max-width: 375px) {
  .gallery-grid {
    grid-template-columns: 1fr 1fr;
    gap: 12px;
  }

  .gallery-image {
    height: 130px;
  }
}

/* ---- Reduced Motion ---- */
@media (prefers-reduced-motion: reduce) {
  .gallery-card {
    animation: none;
  }

  .gallery-card:hover {
    transform: none;
  }

  .gallery-image :deep(img) {
    transition: none;
  }
}
</style>
