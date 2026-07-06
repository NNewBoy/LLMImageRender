import { ref } from 'vue'

// 路由跳转进度条的共享状态（模块级单例）
const progress = ref(0)
const visible = ref(false)

let timer: ReturnType<typeof setInterval> | null = null

function clearTimer() {
  if (timer) {
    clearInterval(timer)
    timer = null
  }
}

/** 开始进度条：快速推进到 80% 后放缓，模拟异步加载 */
function startProgress() {
  clearTimer()
  visible.value = true
  progress.value = 0
  timer = setInterval(() => {
    // 越接近 80% 增幅越小，模拟真实加载感
    const remain = 80 - progress.value
    if (remain > 0) {
      progress.value += Math.max(1, remain * 0.15)
    }
  }, 200)
}

/** 完成进度条：直接到 100% 然后淡出 */
function finishProgress() {
  clearTimer()
  progress.value = 100
  // 等待 CSS 过渡到 100% 后隐藏
  setTimeout(() => {
    visible.value = false
    progress.value = 0
  }, 350)
}

export function useRouteProgress() {
  return { progress, visible, startProgress, finishProgress }
}
