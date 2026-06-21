import api from './index'

export async function uploadImage(file: File) {
  const formData = new FormData()
  formData.append('file', file)
  return api.post('/images/upload', formData, {
    headers: { 'Content-Type': 'multipart/form-data' },
  })
}

export async function getGallery(category?: string) {
  return api.get('/images/gallery', { params: { category } })
}

export async function getGalleryDetail(imageId: string) {
  return api.get(`/images/gallery/${imageId}`)
}