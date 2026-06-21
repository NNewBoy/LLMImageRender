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
      <div v-for="img in images" :key="img.image_id" class="gallery-card">
        <div class="gallery-image">
          <img :src="img.thumbnail_url" :alt="img.name" />
        </div>
        <div class="gallery-info">
          <div class="gallery-name">{{ img.name }}</div>
          <div class="gallery-meta">
            <span>{{ img.category }}</span>
            <span v-if="img.width">{{ img.width }}x{{ img.height }}</span>
          </div>
        </div>
      </div>
    </div>

    <div v-if="!loading && images.length === 0" class="empty-state">
      <el-icon :size="48"><PictureFilled /></el-icon>
      <p>暂无图片</p>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { getGallery } from '@/api/gallery'
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
  max-width: 1000px;
  margin: 0 auto;
}

.page-header {
  margin-bottom: 20px;
}

.page-header h2 {
  font-size: 20px;
  font-weight: 600;
  color: #303133;
}

.gallery-filter {
  margin-bottom: 20px;
}

.gallery-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(200px, 1fr));
  gap: 16px;
}

.gallery-card {
  border-radius: 8px;
  overflow: hidden;
  border: 1px solid #e4e7ed;
  background: #fff;
  transition: box-shadow 0.3s;
}

.gallery-card:hover {
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
}

.gallery-image {
  height: 180px;
  overflow: hidden;
  background: #f5f7fa;
}

.gallery-image img {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.gallery-info {
  padding: 10px 12px;
}

.gallery-name {
  font-size: 13px;
  font-weight: 600;
  color: #303133;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

.gallery-meta {
  display: flex;
  justify-content: space-between;
  margin-top: 4px;
  font-size: 12px;
  color: #c0c4cc;
}

.empty-state {
  text-align: center;
  padding: 60px;
  color: #c0c4cc;
}

.empty-state p {
  margin-top: 12px;
  font-size: 14px;
}
</style>