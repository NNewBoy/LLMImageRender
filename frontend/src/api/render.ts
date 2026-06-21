import api from './index'
import type { RenderTask, RenderParams } from '@/types'

export interface SubmitRenderParams {
  mode: string
  image_source: {
    type: string
    image_id: string
  }
  params: RenderParams
}

export async function submitRender(data: SubmitRenderParams) {
  return api.post('/render/submit', data)
}

export async function getTaskStatus(taskId: string) {
  return api.get(`/render/task/${taskId}`)
}

export async function getTaskResult(taskId: string) {
  return api.get(`/render/task/${taskId}/result`)
}

export async function getHistory(page = 1, pageSize = 20) {
  return api.get('/render/history', { params: { page, page_size: pageSize } })
}

export async function deleteTask(taskId: string) {
  return api.delete(`/render/task/${taskId}`)
}