import { defineStore } from 'pinia'
import { ref } from 'vue'
import type { RenderParams } from '@/types'

export const useRenderStore = defineStore('render', () => {
  const mode = ref<'single' | 'scene'>('single')
  const uploadImageId = ref<string | null>(null)
  const selectedImageId = ref<string | null>(null)
  const selectedImageUrl = ref<string>('')
  const selectedImageName = ref<string>('')
  const params = ref<RenderParams>({
    style: 'modern_minimalist',
    lighting: 'natural',
    view_angle: 'front_45',
    room_type: 'living_room',
    material: 'oak_wood',
    color: '#8B7355',
    background_color: '#FFFFFF',
    description: '',
    cabinet_size: { width: 1200, height: 2200, depth: 600 },
  })
  const currentTaskId = ref<string | null>(null)

  function setMode(m: 'single' | 'scene') {
    mode.value = m
  }

  function setUploadImage(id: string, url: string, name: string) {
    uploadImageId.value = id
    selectedImageId.value = id
    selectedImageUrl.value = url
    selectedImageName.value = name
  }

  function setGalleryImage(id: string, url: string, name: string, extra?: {
    cabinet_w?: number
    cabinet_d?: number
    cabinet_h?: number
    material?: string
    color?: string
  }) {
    selectedImageId.value = id
    selectedImageUrl.value = url
    selectedImageName.value = name
    if (extra) {
      if (extra.material) params.value.material = extra.material
      if (extra.color) params.value.color = extra.color
      if (extra.cabinet_w || extra.cabinet_h || extra.cabinet_d) {
        params.value.cabinet_size = {
          width: extra.cabinet_w || params.value.cabinet_size?.width || 1200,
          height: extra.cabinet_h || params.value.cabinet_size?.height || 2200,
          depth: extra.cabinet_d || params.value.cabinet_size?.depth || 600,
        }
      }
    }
  }

  function updateParams(p: Partial<RenderParams>) {
    Object.assign(params.value, p)
  }

  function resetParams() {
    params.value = {
      style: 'modern_minimalist',
      lighting: 'natural',
      view_angle: 'front_45',
      room_type: 'living_room',
      material: 'oak_wood',
      color: '#8B7355',
      background_color: '#FFFFFF',
      description: '',
      cabinet_size: { width: 1200, height: 2200, depth: 600 },
    }
  }

  return {
    mode, uploadImageId, selectedImageId, selectedImageUrl, selectedImageName,
    params, currentTaskId,
    setMode, setUploadImage, setGalleryImage, updateParams, resetParams,
  }
}, {
  persist: true,
})