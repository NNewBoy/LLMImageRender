<template>
  <div class="chat-panel">
    <div class="chat-header">
      <span class="chat-title">AI 对话助手</span>
      <div class="chat-actions">
        <el-button
          v-if="isActive"
          size="small"
          type="warning"
          @click="handleStop"
        >
          停止对话
        </el-button>
        <el-button
          v-else
          size="small"
          type="success"
          @click="handleContinue"
        >
          继续对话
        </el-button>
      </div>
    </div>

    <div class="chat-messages" ref="messagesContainer">
      <div v-if="messages.length === 0" class="chat-empty">
        <el-icon :size="32"><ChatDotRound /></el-icon>
        <p>通过对话调整渲染参数</p>
        <p class="hint">例如：把柜子颜色改成深棕色</p>
      </div>
      <div
        v-for="(msg, idx) in messages"
        :key="idx"
        class="chat-message"
        :class="msg.role"
      >
        <div class="message-avatar">
          <el-icon v-if="msg.role === 'user'" :size="18"><User /></el-icon>
          <el-icon v-else :size="18"><Cpu /></el-icon>
        </div>
        <div class="message-content">
          <div class="message-text">{{ msg.content }}</div>
          <div v-if="msg.params_update && Object.keys(msg.params_update).length" class="params-tag">
            <el-tag
              v-for="(val, key) in msg.params_update"
              :key="key"
              size="small"
              type="info"
            >
              {{ key }}: {{ val }}
            </el-tag>
          </div>
        </div>
      </div>
    </div>

    <div class="chat-input">
      <el-input
        v-model="inputText"
        placeholder="输入消息调整渲染参数..."
        :disabled="!isActive"
        @keyup.enter="sendMessage"
      >
        <template #append>
          <el-button
            :disabled="!isActive || !inputText.trim()"
            @click="sendMessage"
          >
            发送
          </el-button>
        </template>
      </el-input>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, nextTick, onMounted } from 'vue'
import { ElMessage } from 'element-plus'
import { startChat, sendMessage as sendChatMessage, stopChat, continueChat } from '@/api/chat'
import { useRenderStore } from '@/stores/render'
import type { ChatMessage } from '@/types'

const props = defineProps<{ taskId: string }>()
const renderStore = useRenderStore()

const messages = ref<ChatMessage[]>([])
const inputText = ref('')
const isActive = ref(false)
const sessionId = ref('')
const messagesContainer = ref<HTMLElement>()

const initChat = async () => {
  try {
    const res: any = await startChat(props.taskId)
    if (res.code === 200) {
      sessionId.value = res.data.session_id
      isActive.value = true
      renderStore.isChatActive = true
    }
  } catch (e: any) {
    ElMessage.error(e.message || '开启对话失败')
  }
}

const sendMessage = async () => {
  const text = inputText.value.trim()
  if (!text || !isActive.value) return

  messages.value.push({ role: 'user', content: text })
  inputText.value = ''
  await scrollToBottom()

  try {
    const res: any = await sendChatMessage(sessionId.value, props.taskId, text)
    if (res.code === 200) {
      messages.value.push({
        role: 'assistant',
        content: res.data.content,
        params_update: res.data.params_update,
      })
      if (res.data.params_update) {
        renderStore.updateParams(res.data.params_update)
      }
    }
  } catch (e: any) {
    ElMessage.error(e.message || '发送失败')
  }
  await scrollToBottom()
}

const handleStop = async () => {
  try {
    await stopChat(props.taskId)
    isActive.value = false
    renderStore.isChatActive = false
    ElMessage.info('对话已停止')
  } catch (e: any) {
    ElMessage.error(e.message || '停止失败')
  }
}

const handleContinue = async () => {
  try {
    await continueChat(props.taskId)
    isActive.value = true
    renderStore.isChatActive = true
    ElMessage.success('对话已继续')
  } catch (e: any) {
    ElMessage.error(e.message || '继续失败')
  }
}

const scrollToBottom = async () => {
  await nextTick()
  if (messagesContainer.value) {
    messagesContainer.value.scrollTop = messagesContainer.value.scrollHeight
  }
}

onMounted(initChat)
</script>

<style scoped>
.chat-panel {
  display: flex;
  flex-direction: column;
  height: 400px;
  background: #fff;
  border-radius: 8px;
  border: 1px solid #e4e7ed;
  overflow: hidden;
}

.chat-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 12px 16px;
  border-bottom: 1px solid #e4e7ed;
  background: #fafafa;
}

.chat-title {
  font-size: 14px;
  font-weight: 600;
  color: #303133;
}

.chat-messages {
  flex: 1;
  overflow-y: auto;
  padding: 12px;
}

.chat-empty {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  height: 100%;
  color: #c0c4cc;
}

.chat-empty p {
  margin-top: 8px;
  font-size: 13px;
}

.chat-empty .hint {
  font-size: 12px;
  color: #e4e7ed;
}

.chat-message {
  display: flex;
  gap: 8px;
  margin-bottom: 12px;
}

.chat-message.user {
  flex-direction: row-reverse;
}

.message-avatar {
  width: 32px;
  height: 32px;
  border-radius: 50%;
  background: #ecf5ff;
  display: flex;
  align-items: center;
  justify-content: center;
  flex-shrink: 0;
}

.chat-message.user .message-avatar {
  background: #e6f7e6;
}

.message-content {
  max-width: 75%;
}

.message-text {
  padding: 8px 12px;
  border-radius: 8px;
  font-size: 13px;
  line-height: 1.6;
  background: #f5f7fa;
  color: #303133;
}

.chat-message.user .message-text {
  background: #409eff;
  color: #fff;
}

.params-tag {
  margin-top: 4px;
  display: flex;
  flex-wrap: wrap;
  gap: 4px;
}

.chat-input {
  padding: 12px;
  border-top: 1px solid #e4e7ed;
}
</style>