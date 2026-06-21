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
  description?: string
}

export interface RenderTask {
  task_id: string
  mode: string
  status: string
  progress: number
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

export interface ChatMessage {
  role: 'user' | 'assistant' | 'system'
  content: string
  params_update?: Record<string, any>
  created_at?: string
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