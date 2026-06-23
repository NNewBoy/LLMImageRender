<template>
  <div class="gallery-page">
    <div class="page-header">
      <h2>柜子图库</h2>
    </div>

    <div class="gallery-filter">
      <el-radio-group v-model="category" @change="loadGallery">
        <el-radio-button value="">全部</el-radio-button>
        <el-radio-button v-for="c in categories" :key="c.value" :value="c.value">
          {{ c.label }}
        </el-radio-button>
      </el-radio-group>
    </div>

    <div v-loading="loading" class="gallery-grid">
      <div v-for="img in images" :key="img.image_id" class="gallery-card glass-card">
        <div class="gallery-image">
          <ImageViewer :src="img.thumbnail_url" :alt="img.name" />
        </div>
        <div class="gallery-info">
          <div class="gallery-name">{{ img.name }}</div>
          <div class="gallery-meta">
            <span class="meta-tag">{{ img.category }}</span>
            <span v-if="img.width" class="meta-size">{{ img.width }}x{{ img.height }}</span>
          </div>
        </div>
      </div>
    </div>

    <div v-if="!loading && images.length === 0" class="empty-state glass-card">
      <el-icon :size="48"><PictureFilled /></el-icon>
      <p>暂无图片</p>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { getGallery } from '@/api/gallery'
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
]

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

.page-header {
  margin-bottom: 20px;
}

.page-header h2 {
  font-size: 22px;
  font-weight: 700;
  color: var(--text-primary);
}

.gallery-filter {
  margin-bottom: 24px;
  overflow-x: auto;
}

.gallery-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(220px, 1fr));
  gap: 20px;
}

.gallery-card {
  overflow: hidden;
  cursor: pointer;
}

.gallery-image {
  height: 200px;
  overflow: hidden;
  background: rgba(0, 0, 0, 0.2);
}

.gallery-image :deep(img) {
  width: 100%;
  height: 100%;
  object-fit: cover;
  transition: transform 0.3s ease;
}

.gallery-card:hover .gallery-image :deep(img) {
  transform: scale(1.05);
}

.gallery-info {
  padding: 12px 14px;
}

.gallery-name {
  font-size: 14px;
  font-weight: 600;
  color: var(--text-primary);
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

.gallery-meta {
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin-top: 6px;
  font-size: 12px;
}

.meta-tag {
  color: var(--accent-primary-light);
  background: rgba(99, 102, 241, 0.1);
  padding: 2px 8px;
  border-radius: 6px;
}

.meta-size {
  color: var(--text-faint);
  font-family: 'Inter', monospace;
}

.empty-state {
  text-align: center;
  padding: 60px;
  color: var(--text-muted);
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 12px;
}

.empty-state p {
  font-size: 14px;
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
</style>
