import type { RenderParams } from '@/types'
import { uploadImage, getGalleryDetail } from '@/api/gallery'

/**
 * 从 URL 查询参数中解析渲染参数
 * 支持的参数：
 *   - image_id: 图库中的图片 ID（直接查询图库获取）
 *   - image_url: 图片 URL（网络地址）
 *   - image_base64: 图片 base64（data:image/xxx;base64,...）
 *   - style: 渲染风格
 *   - lighting: 光照条件
 *   - view_angle: 视角
 *   - room_type: 户型（场景渲染）
 *   - material: 材质
 *   - color: 颜色（如 #8B7355）
 *   - bg_color: 背景颜色
 *   - description: 额外描述
 *   - width / height / depth: 柜子尺寸 (mm)
 *
 * 示例：
 *   /render/single?image_id=abc123&style=nordic&lighting=warm
 *   /render/single?image_url=https://example.com/img.png&style=nordic&lighting=warm
 *   /render/scene?image_base64=data:image/png;base64,...&room_type=bedroom
 */
export interface UrlParamsResult {
  /** 解析到的渲染参数（部分，仅包含 URL 中有传的） */
  params: Partial<RenderParams>
  /** 图片 URL（外部地址） */
  imageUrl: string | null
  /** 图片 base64 */
  imageBase64: string | null
  /** 图库图片 ID */
  imageId: string | null
  /** 是否有外部图片参数 */
  hasExternalImage: boolean
}

export function parseUrlParams(query: Record<string, any>, hash?: string): UrlParamsResult {
  const result: UrlParamsResult = {
    params: {},
    imageUrl: null,
    imageBase64: null,
    imageId: null,
    hasExternalImage: false,
  }

  // 修复 color=#8B7355 中 # 被浏览器当作片段分隔符的问题
  // 如果 hash 以颜色值开头（8B7355&...），将其合并到 query 参数中
  const mergedQuery = { ...query }
  if (hash && !hash.startsWith('/') && hash.includes('=')) {
    const hashParams = new URLSearchParams(hash.replace(/^#/, ''))
    for (const [key, value] of hashParams.entries()) {
      if (!mergedQuery[key]) {
        mergedQuery[key] = value
      }
    }
  }

  const q = mergedQuery

  // 图片参数
  if (q.image_id && typeof q.image_id === 'string') {
    result.imageId = q.image_id
    result.hasExternalImage = true
  }
  if (q.image_url && typeof q.image_url === 'string') {
    result.imageUrl = q.image_url
    result.hasExternalImage = true
  }
  if (q.image_base64 && typeof q.image_base64 === 'string') {
    result.imageBase64 = q.image_base64
    result.hasExternalImage = true
  }

  // 渲染参数（有传才设置）
  if (q.style && typeof q.style === 'string') {
    result.params.style = q.style
  }
  if (q.lighting && typeof q.lighting === 'string') {
    result.params.lighting = q.lighting
  }
  if (q.view_angle && typeof q.view_angle === 'string') {
    result.params.view_angle = q.view_angle
  }
  if (q.room_type && typeof q.room_type === 'string') {
    result.params.room_type = q.room_type
  }
  if (q.material && typeof q.material === 'string') {
    result.params.material = q.material
  }
  if (q.color && typeof q.color === 'string') {
    result.params.color = q.color.startsWith('#') ? q.color : `#${q.color}`
  }
  if (q.bg_color && typeof q.bg_color === 'string') {
    result.params.background_color = q.bg_color.startsWith('#') ? q.bg_color : `#${q.bg_color}`
  }
  if (q.description && typeof q.description === 'string') {
    result.params.description = q.description
  }

  // 柜子尺寸
  const hasSize = q.width || q.height || q.depth
  if (hasSize) {
    result.params.cabinet_size = {
      width: q.width ? Number(q.width) : 1200,
      height: q.height ? Number(q.height) : 2200,
      depth: q.depth ? Number(q.depth) : 600,
    }
  }

  return result
}

/**
 * 处理外部图片（图库 ID、URL 或 base64），设置到 render store
 * 优先级：image_id > image_url > image_base64
 * @returns 上传成功返回 true，失败返回 false
 */
export async function applyExternalImage(
  store: any,
  imageUrl: string | null,
  imageBase64: string | null,
  imageId: string | null = null,
): Promise<boolean> {
  try {
    // 优先通过 image_id 查询图库
    if (imageId) {
      const res: any = await getGalleryDetail(imageId)
      if (res.code === 200 && res.data) {
        store.setGalleryImage(res.data.image_id, res.data.url, res.data.name)
        return true
      }
      // 查不到图库图片
      console.error('图库中未找到该图片', imageId)
      return false
    }

    let file: File | null = null

    if (imageUrl) {
      // 通过 URL 下载图片，转为 File 对象
      file = await urlToFile(imageUrl)
    } else if (imageBase64) {
      // base64 转 File 对象
      const blob = base64ToBlob(imageBase64)
      const ext = imageBase64.startsWith('data:image/png') ? 'png' :
        imageBase64.startsWith('data:image/webp') ? 'webp' : 'jpg'
      file = new File([blob], `external.${ext}`, { type: blob.type })
    }

    if (!file) return false

    // 上传到后端，获取真实的 image_id
    const res: any = await uploadImage(file)
    if (res.code === 200) {
      store.setUploadImage(res.data.image_id, res.data.url, res.data.name)
      return true
    }

    return false
  } catch (e) {
    console.error('应用外部图片失败', e)
    return false
  }
}

/**
 * 通过 URL 下载图片并转为 File 对象
 */
async function urlToFile(url: string): Promise<File> {
  const resp = await fetch(url)
  if (!resp.ok) throw new Error(`下载图片失败: ${resp.status}`)
  const blob = await resp.blob()
  // 从 URL 或 Content-Type 推断文件名
  const urlName = url.split('?')[0].split('/').pop() || 'external.png'
  const ext = urlName.includes('.') ? urlName.split('.').pop() || 'png' : 'png'
  return new File([blob], `external.${ext}`, { type: blob.type || 'image/png' })
}

function base64ToBlob(base64: string): Blob {
  // 从 data URI 中提取 MIME 和 base64 数据
  const parts = base64.split(',')
  const mime = parts[0].match(/:(.*?);/)?.[1] || 'image/png'
  // 修复经 URL 解码后损坏的 base64 字符
  const rawBase64 = fixBase64(parts[1] || parts[0])
  const raw = atob(rawBase64)
  const arr = new Uint8Array(raw.length)
  for (let i = 0; i < raw.length; i++) {
    arr[i] = raw.charCodeAt(i)
  }
  return new Blob([arr], { type: mime })
}

/**
 * 修复经 URL query string 解码后损坏的 base64 字符
 * - 空格还原为 +
 * - 补齐 = 填充
 */
function fixBase64(str: string): string {
  // URL 解码会把 + 变成空格，还原回来
  let s = str.replace(/ /g, '+')
  // 补齐 base64 填充 =
  const padding = s.length % 4
  if (padding === 2) s += '=='
  else if (padding === 3) s += '='
  return s
}
