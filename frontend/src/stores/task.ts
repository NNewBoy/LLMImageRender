import { defineStore } from 'pinia'
import { ref } from 'vue'
import type { RenderTask } from '@/types'

export const useTaskStore = defineStore('task', () => {
  const tasks = ref<RenderTask[]>([])
  const currentTask = ref<RenderTask | null>(null)
  const total = ref(0)

  function setCurrentTask(task: RenderTask | null) {
    currentTask.value = task
  }

  function setTasks(taskList: RenderTask[], t: number) {
    tasks.value = taskList
    total.value = t
  }

  return { tasks, currentTask, total, setCurrentTask, setTasks }
}, {
  persist: true,
})