<template>
  <div :class="['image-viewer', { 'image-viewer--clickable': preview }]" @click="handleClick">
    <el-image
      :src="src"
      :alt="alt"
      :fit="fit"
      :preview-src-list="preview ? [src] : []"
      :initial-index="0"
      :preview-teleported="true"
      class="image-viewer__img"
    >
      <template #error>
        <div class="image-error">
          <el-icon><PictureFilled /></el-icon>
          <span>加载失败</span>
        </div>
      </template>
      <template #placeholder>
        <div class="image-loading">
          <el-icon class="is-loading"><Loading /></el-icon>
        </div>
      </template>
    </el-image>
  </div>
</template>

<script setup lang="ts">
import { PictureFilled, Loading } from '@element-plus/icons-vue'

interface Props {
  src: string
  alt?: string
  fit?: 'fill' | 'contain' | 'cover' | 'none' | 'scale-down'
  preview?: boolean
}

const props = withDefaults(defineProps<Props>(), {
  alt: '',
  fit: 'contain',
  preview: true,
})

const emit = defineEmits<{
  click: [event: MouseEvent]
}>()

const handleClick = (event: MouseEvent) => {
  emit('click', event)
}
</script>

<style scoped>
.image-viewer {
  width: 100%;
  height: 100%;
}

.image-viewer--clickable {
  cursor: pointer;
}

.image-viewer__img {
  width: 100%;
  height: 100%;
  display: block;
}

.image-error {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  height: 100%;
  min-height: 100px;
  color: var(--text-muted);
  font-size: 13px;
  gap: 8px;
}

.image-error .el-icon {
  font-size: 24px;
}

.image-loading {
  display: flex;
  align-items: center;
  justify-content: center;
  height: 100%;
  min-height: 100px;
}

.image-loading .el-icon {
  font-size: 24px;
  color: var(--accent-primary-light);
}
</style>
