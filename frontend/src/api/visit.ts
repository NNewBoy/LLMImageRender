import axios from 'axios'

const visitApi = axios.create({
  baseURL: '/api/v1',
  timeout: 10000,
  headers: {
    'Content-Type': 'application/json',
  },
})

export function recordVisit(title: string) {
  return visitApi.post('/visit/record', { title })
}
