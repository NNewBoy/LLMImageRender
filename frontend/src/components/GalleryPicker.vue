<template>
  <div class="gallery-picker">
    <div class="gallery-header">
      <span class="gallery-title">从图库选择</span>
      <el-select v-model="category" placeholder="全部分类" clearable @change="loadGallery">
        <el-option v-for="c in categories" :key="c.value" :label="c.label" :value="c.value" />
      </el-select>
    </div>
    <div v-loading="loading" class="gallery-grid">
      <div
        v-for="img in images"
        :key="img.image_id"
        class="gallery-item"
        :class="{ selected: selectedId === img.image_id }"
        @click="selectImage(img)"
      >
        <img :src="img.thumbnail_url" :alt="img.name" />
        <div class="item-name">{{ img.name }}</div>
        <div v-if="selectedId === img.image_id" class="selected-badge">
          <el-icon><Check /></el-icon>
        </div>
      </div>
      <div v-if="!loading && images.length === 0" class="empty-hint">
        暂无图片
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { getGallery } from '@/api/gallery'
import { useRenderStore } from '@/stores/render'
import type { GalleryImage, PresetOption } from '@/types'

const emit = defineEmits(['selected'])
const renderStore = useRenderStore()

const images = ref<GalleryImage[]>([])
const loading = ref(false)
const selectedId = ref<string | null>(null)
const category = ref('')

const categories: PresetOption[] = [
  { value: 'wardrobe', label: '衣柜' },
  { value: 'kitchen', label: '橱柜' },
  { value: 'bookcase', label: '书柜' },
  { value: 'entryway', label: '玄关柜' },
  { value: 'tv_stand', label: '电视柜' },
  { value: 'other', label: '其他' },
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

const selectImage = (img: GalleryImage) => {
  selectedId.value = img.image_id
  renderStore.setGalleryImage(img.image_id, img.url, img.name)
  emit('selected', img)
}

onMounted(loadGallery)
</script>

<style scoped>
.gallery-picker {
  margin-top: 16px;
}

.gallery-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin-bottom: 12px;
}

.gallery-title {
  width: 100px;
  margin-right: 12px;
  font-size: 14px;
  font-weight: 600;
  color: var(--text-primary);
}

.gallery-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(140px, 1fr));
  gap: 12px;
  max-height: 300px;
  overflow-y: auto;
  padding: 4px;
}

.gallery-item {
  position: relative;
  border: 2px solid var(--glass-border);
  border-radius: var(--radius-md);
  overflow: hidden;
  cursor: pointer;
  transition: all 0.2s ease;
  background: rgba(0, 0, 0, 0.2);
}

.gallery-item:hover {
  border-color: var(--accent-primary-light);
  background: rgba(99, 102, 241, 0.05);
}

.gallery-item.selected {
  border-color: var(--accent-primary);
  box-shadow: 0 0 12px var(--accent-primary-glow);
}

.gallery-item img {
  width: 100%;
  height: 120px;
  object-fit: contain;
}

.item-name {
  padding: 6px 8px;
  font-size: 12px;
  color: var(--text-muted);
  text-align: center;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

.selected-badge {
  position: absolute;
  top: 6px;
  right: 6px;
  background: var(--accent-primary);
  color: #fff;
  border-radius: 50%;
  width: 22px;
  height: 22px;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 12px;
  box-shadow: 0 0 8px var(--accent-primary-glow);
}

.empty-hint {
  grid-column: 1 / -1;
  text-align: center;
  padding: 20px;
  color: var(--text-faint);
  font-size: 13px;
}

/* ---- Responsive ---- */
@media (max-width: 480px) {
  .gallery-grid {
    grid-template-columns: repeat(auto-fill, minmax(110px, 1fr));
    gap: 10px;
  }
}
</style>
