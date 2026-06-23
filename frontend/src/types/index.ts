export interface RenderParams {
  style: string
  lighting: string
  view_angle: string
  room_type?: string
  cabinet_size?: {
    width: number
    height: number
    depth: number
  }
  material?: string
  color?: string
  background_color?: string
  description?: string
}

export interface RenderTask {
  task_id: string
  mode: string
  status: string
  progress: number
  image_source: string
  image_id: string | null
  original_image_url: string
  result_image_url: string | null
  params: RenderParams
  created_at: string
  completed_at: string | null
  error_message: string | null
}

export interface GalleryImage {
  image_id: string
  name: string
  category: string
  url: string
  thumbnail_url: string
  width: number
  height: number
}

export interface PresetOption {
  value: string
  label: string
}

export interface Presets {
  styles: PresetOption[]
  lighting: PresetOption[]
  view_angles: PresetOption[]
  room_types: PresetOption[]
  materials: PresetOption[]
  categories: PresetOption[]
}