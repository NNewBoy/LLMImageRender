<template>
  <div class="param-panel">
    <h3 class="panel-title">渲染参数配置</h3>

    <el-form label-width="80px" label-position="top" size="default">
      <div class="form-grid">
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
          <div class="bg-current">
            <el-color-picker v-model="localParams.color" />
            <span class="color-value">{{ localParams.color }}</span>
          </div>
        </el-form-item>

        <el-form-item v-if="showBackground" label="背景颜色" class="full-span">
          <div class="background-picker">
            <div class="bg-current">
              <el-color-picker v-model="localParams.background_color" />
              <span class="color-value">{{ localParams.background_color }}</span>
            </div>
            <div class="preset-colors">
              <button v-for="c in presetBackgroundColors" :key="c.value" type="button" :style="{ background: c.value }"
                class="preset-color-btn" :class="{ active: localParams.background_color === c.value }"
                @click="localParams.background_color = c.value" :title="c.label" :aria-label="c.label">
                <span class="preset-color-name">{{ c.label }}</span>
              </button>
            </div>
          </div>
        </el-form-item>

        <el-form-item label="柜子尺寸(宽×高×深 mm)" class="full-span">
          <div class="size-inputs">
            <el-input-number v-model="localParams.cabinet_size!.width" :min="200" :max="5000" />
            <span class="size-sep">×</span>
            <el-input-number v-model="localParams.cabinet_size!.height" :min="200" :max="5000" />
            <span class="size-sep">×</span>
            <el-input-number v-model="localParams.cabinet_size!.depth" :min="100" :max="2000" />
          </div>
        </el-form-item>

        <el-form-item label="额外描述" class="full-span">
          <el-input v-model="localParams.description" type="textarea" :rows="3" placeholder="描述你想要的渲染效果..." />
        </el-form-item>
      </div>
    </el-form>
  </div>
</template>

<script setup lang="ts">
import { reactive, watch, onMounted, ref, nextTick } from 'vue'
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

// 用户修改参数 → 同步到 store
let syncing = false
watch(localParams, (val) => {
  if (syncing) return
  renderStore.updateParams({ ...val })
}, { deep: true })

// 监听 store 变化（图库选择等外部操作修改了 store）→ 同步到 localParams
watch(() => renderStore.params, () => {
  syncing = true
  syncFromStore()
  nextTick(() => { syncing = false })
}, { deep: true })

// 从 store 同步赋值到 localParams
function syncFromStore() {
  const s = renderStore.params
  localParams.style = s.style
  localParams.lighting = s.lighting
  localParams.view_angle = s.view_angle
  localParams.room_type = s.room_type || ''
  localParams.material = s.material || ''
  localParams.color = s.color || ''
  localParams.background_color = s.background_color || '#FFFFFF'
  localParams.description = s.description || ''
  if (localParams.cabinet_size && s.cabinet_size) {
    localParams.cabinet_size.width = s.cabinet_size.width || 1200
    localParams.cabinet_size.height = s.cabinet_size.height || 2200
    localParams.cabinet_size.depth = s.cabinet_size.depth || 600
  }
}

onMounted(async () => {
  // 加载预设选项
  try {
    const res: any = await api.get('/params/presets')
    if (res.code === 200) {
      presets.value = res.data
    }
  } catch (e) {
    console.error('加载预设参数失败', e)
  }
  // nextTick 确保父组件的 onMounted（URL 参数写入 store）已执行完毕
  await nextTick()
  syncFromStore()
})
</script>

<style scoped>
.panel-title {
  font-size: 16px;
  font-weight: 600;
  margin-bottom: 20px;
  color: var(--text-primary);
}

.form-grid {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 0 20px;
}

.full-width {
  width: 100%;
}

.full-span {
  grid-column: 1 / -1;
}

.color-value {
  margin-left: 12px;
  font-size: 13px;
  color: var(--text-muted);
  font-family: 'Inter', monospace;
}

.size-inputs {
  display: flex;
  align-items: center;
  gap: 8px;
  flex-wrap: wrap;
}

.size-inputs .el-input-number {
  width: 120px;
}

.size-sep {
  color: var(--text-faint);
  font-weight: bold;
}

.background-picker {
  display: flex;
  flex-direction: column;
  gap: 14px;
  width: 100%;
}

.bg-current {
  display: flex;
  align-items: center;
  gap: 12px;
}

.preset-colors {
  display: flex;
  flex-wrap: wrap;
  gap: 8px;
}

.preset-color-btn {
  position: relative;
  width: 56px;
  height: 32px;
  padding: 0;
  border: 2px solid var(--glass-border);
  border-radius: var(--radius-sm);
  cursor: pointer;
  transition: all 0.2s ease;
  overflow: hidden;
}

.preset-color-btn:hover {
  border-color: var(--glass-border-hover);
  transform: scale(1.05);
}

.preset-color-btn.active {
  border-color: var(--accent-primary);
  box-shadow: 0 0 10px var(--accent-primary-glow);
}

.preset-color-name {
  position: absolute;
  bottom: 0;
  left: 0;
  right: 0;
  font-size: 10px;
  font-weight: 500;
  color: var(--text-primary);
  background: rgba(0, 0, 0, 0.55);
  backdrop-filter: blur(4px);
  padding: 1px 0;
  text-align: center;
  line-height: 1.2;
}

/* ---- Responsive ---- */
@media (max-width: 640px) {
  .form-grid {
    grid-template-columns: 1fr;
  }

  .size-inputs .el-input-number {
    width: 100%;
    flex: 1;
  }
}
</style>
