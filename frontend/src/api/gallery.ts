import api from './index'

export async function uploadImage(file: File) {
  const formData = new FormData()
  formData.append('file', file)
  return api.post('/images/upload', formData, {
    headers: { 'Content-Type': 'multipart/form-data' },
  })
}

export async function getGallery(category?: string, order: 'desc' | 'asc' = 'asc') {
  return api.get('/images/gallery', { params: { category, order } })
}

export async function getGalleryDetail(imageId: string) {
  return api.get(`/images/gallery/${imageId}`)
}

export async function updateImage(imageId: string, data: { name?: string; category?: string }) {
  return api.put(`/images/gallery/${imageId}`, data)
}

export async function deleteImage(imageId: string) {
  return api.delete(`/images/gallery/${imageId}`)
}