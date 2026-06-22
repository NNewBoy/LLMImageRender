<template>
  <div class="param-panel">
    <h3 class="panel-title">渲染参数配置</h3>

    <el-form label-width="80px" label-position="top" size="default">
      <el-form-item label="渲染风格">
        <el-select v-model="localParams.style" class="full-width">
          <el-option v-for="s in presets.styles" :key="s.value" :label="s.label" :value="s.value" />
        </el-select>
      </el-form-item>

      <el-form-item label="光照条件">
        <el-select v-model="localParams.lighting" class="full-width">
          <el-option v-for="l in presets.lighting" :key="l.value" :label="l.label" :value="l.value" />
        </el-select>
      </el-form-item>

      <el-form-item label="视角">
        <el-select v-model="localParams.view_angle" class="full-width">
          <el-option v-for="v in presets.view_angles" :key="v.value" :label="v.label" :value="v.value" />
        </el-select>
      </el-form-item>

      <el-form-item v-if="showRoomType" label="户型">
        <el-select v-model="localParams.room_type" class="full-width">
          <el-option v-for="r in presets.room_types" :key="r.value" :label="r.label" :value="r.value" />
        </el-select>
      </el-form-item>

      <el-form-item label="材质">
        <el-select v-model="localParams.material" class="full-width">
          <el-option v-for="m in presets.materials" :key="m.value" :label="m.label" :value="m.value" />
        </el-select>
      </el-form-item>

      <el-form-item label="颜色">
        <el-color-picker v-model="localParams.color" />
        <span class="color-value">{{ localParams.color }}</span>
      </el-form-item>

      <el-form-item v-if="showBackground" label="背景颜色">
        <div class="background-picker">
          <el-color-picker v-model="localParams.background_color" />
          <span class="color-value">{{ localParams.background_color }}</span>
          <div class="preset-colors">
            <span class="preset-label">快速选择：</span>
            <el-button
              v-for="c in presetBackgroundColors"
              :key="c.value"
              :style="{ background: c.value }"
              class="preset-color-btn"
              :class="{ active: localParams.background_color === c.value }"
              @click="localParams.background_color = c.value"
              :title="c.label"
            />
          </div>
        </div>
      </el-form-item>

      <el-form-item label="柜子尺寸 (mm)">
        <div class="size-inputs">
          <el-input-number v-model="localParams.cabinet_size!.width" :min="200" :max="5000" placeholder="宽" />
          <span class="size-sep">x</span>
          <el-input-number v-model="localParams.cabinet_size!.height" :min="200" :max="5000" placeholder="高" />
          <span class="size-sep">x</span>
          <el-input-number v-model="localParams.cabinet_size!.depth" :min="100" :max="2000" placeholder="深" />
        </div>
      </el-form-item>

      <el-form-item label="额外描述">
        <el-input
          v-model="localParams.description"
          type="textarea"
          :rows="3"
          placeholder="描述你想要的渲染效果..."
        />
      </el-form-item>
    </el-form>
  </div>
</template>

<script setup lang="ts">
import { reactive, watch, onMounted, ref } from 'vue'
import { useRenderStore } from '@/stores/render'
import type { RenderParams } from '@/types'
import api from '@/api'

const props = defineProps<{ showRoomType?: boolean; showBackground?: boolean }>()
const renderStore = useRenderStore()

const presetBackgroundColors = [
  { value: '#FFFFFF', label: '纯白' },
  { value: '#F5F5F5', label: '浅灰' },
  { value: '#E8E8E8', label: '中性灰' },
  { value: '#000000', label: '纯黑' },
  { value: '#F5E6D3', label: '米色' },
  { value: '#D9E2F3', label: '浅蓝' },
]

const presets = ref({
  styles: [] as any[],
  lighting: [] as any[],
  view_angles: [] as any[],
  room_types: [] as any[],
  materials: [] as any[],
})

const localParams = reactive<RenderParams>({
  style: renderStore.params.style,
  lighting: renderStore.params.lighting,
  view_angle: renderStore.params.view_angle,
  room_type: renderStore.params.room_type,
  material: renderStore.params.material,
  color: renderStore.params.color,
  background_color: renderStore.params.background_color || '#FFFFFF',
  description: renderStore.params.description || '',
  cabinet_size: {
    width: renderStore.params.cabinet_size?.width || 1200,
    height: renderStore.params.cabinet_size?.height || 2200,
    depth: renderStore.params.cabinet_size?.depth || 600,
  },
})

watch(localParams, (val) => {
  renderStore.updateParams({ ...val })
}, { deep: true })

onMounted(async () => {
  try {
    const res: any = await api.get('/params/presets')
    if (res.code === 200) {
      presets.value = res.data
    }
  } catch (e) {
    console.error('加载预设参数失败', e)
  }
})
</script>

<style scoped>
.param-panel {
  padding: 16px;
  background: #fff;
  border-radius: 8px;
  border: 1px solid #e4e7ed;
}

.panel-title {
  font-size: 16px;
  font-weight: 600;
  margin-bottom: 16px;
  color: #303133;
}

.full-width {
  width: 100%;
}

.color-value {
  margin-left: 12px;
  font-size: 13px;
  color: #909399;
  font-family: monospace;
}

.size-inputs {
  display: flex;
  align-items: center;
  gap: 8px;
}

.size-inputs .el-input-number {
  width: 120px;
}

.size-sep {
  color: #c0c4cc;
  font-weight: bold;
}

.background-picker {
  display: flex;
  flex-direction: column;
  gap: 10px;
  width: 100%;
}

.preset-colors {
  display: flex;
  align-items: center;
  gap: 8px;
  flex-wrap: wrap;
}

.preset-label {
  font-size: 13px;
  color: #909399;
}

.preset-color-btn {
  width: 28px;
  height: 28px;
  min-height: 28px;
  padding: 0;
  border: 2px solid #dcdfe6;
  border-radius: 6px;
  cursor: pointer;
}

.preset-color-btn.active {
  border-color: #409eff;
  box-shadow: 0 0 4px rgba(64, 158, 255, 0.5);
}
</style>