import api from './index'

export async function startChat(taskId: string) {
  return api.post('/chat/start', { task_id: taskId })
}

export async function sendMessage(sessionId: string, taskId: string, message: string) {
  return api.post('/chat/message', {
    session_id: sessionId,
    task_id: taskId,
    message,
  })
}

export async function stopChat(taskId: string) {
  return api.post('/chat/stop', { task_id: taskId })
}

export async function continueChat(taskId: string) {
  return api.post('/chat/continue', { task_id: taskId })
}

export async function getChatHistory(sessionId: string) {
  return api.get(`/chat/${sessionId}/history`)
}