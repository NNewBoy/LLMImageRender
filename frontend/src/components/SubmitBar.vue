<template>
  <div class="submit-bar glass-card">
    <el-button
      type="primary"
      size="large"
      :loading="loading"
      :disabled="!canSubmit"
      @click="handleSubmit"
    >
      <el-icon v-if="!loading"><Upload /></el-icon>
      提交渲染
    </el-button>
    <span v-if="!canSubmit" class="hint">请先选择或上传图片</span>
  </div>
</template>

<script setup lang="ts">
import { computed, ref } from 'vue'
import { useRouter } from 'vue-router'
import { ElMessage } from 'element-plus'
import { Upload } from '@element-plus/icons-vue'
import { submitRender } from '@/api/render'
import { useRenderStore } from '@/stores/render'

const router = useRouter()
const renderStore = useRenderStore()
const loading = ref(false)

const canSubmit = computed(() => {
  return !!renderStore.selectedImageId
})

const handleSubmit = async () => {
  if (!canSubmit.value) return
  loading.value = true
  try {
    const res: any = await submitRender({
      mode: renderStore.mode,
      image_source: {
        type: renderStore.uploadImageId ? 'upload' : 'gallery',
        image_id: renderStore.selectedImageId!,
      },
      params: renderStore.params,
    })
    if (res.code === 200) {
      renderStore.currentTaskId = res.data.task_id
      ElMessage.success('渲染任务已提交')
      router.push(`/render/${res.data.task_id}`)
    }
  } catch (e: any) {
    ElMessage.error(e.message || '提交失败')
  } finally {
    loading.value = false
  }
}
</script>

<style scoped>
.submit-bar {
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 16px 20px;
  border-radius: var(--radius-lg);
}

.hint {
  font-size: 13px;
  color: var(--text-faint);
}
</style>
