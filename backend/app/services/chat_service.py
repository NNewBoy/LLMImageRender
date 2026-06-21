import logging
from typing import Optional

logger = logging.getLogger(__name__)


class ChatService:
    def __init__(self):
        self._sessions: dict[str, dict] = {}

    def start_session(self, session_id: str, task_id: str):
        self._sessions[session_id] = {
            "session_id": session_id,
            "task_id": task_id,
            "status": "active",
            "messages": [],
        }
        logger.info(f"对话会话已开启: {session_id}")

    async def send_message(self, session_id: str, message: str) -> dict:
        session = self._sessions.get(session_id)
        if not session:
            return {"content": "会话不存在", "params_update": {}}

        session["messages"].append({"role": "user", "content": message})

        from app.agent.graph import run_chat_agent

        try:
            result = await run_chat_agent(
                session_id=session_id,
                task_id=session["task_id"],
                messages=session["messages"],
                user_message=message,
            )

            session["messages"].append({
                "role": "assistant",
                "content": result.get("content", ""),
            })

            return {
                "content": result.get("content", "已收到您的需求，正在调整参数..."),
                "params_update": result.get("params_update", {}),
            }
        except Exception as e:
            logger.error(f"对话处理失败: {e}")
            return {
                "content": f"抱歉，处理您的消息时出现错误: {str(e)}",
                "params_update": {},
            }

    def stop_session(self, session_id: str):
        if session_id in self._sessions:
            self._sessions[session_id]["status"] = "paused"
            logger.info(f"对话会话已停止: {session_id}")

    def continue_session(self, session_id: str) -> dict:
        if session_id in self._sessions:
            self._sessions[session_id]["status"] = "active"
            logger.info(f"对话会话已继续: {session_id}")
        return {"session_id": session_id, "status": "active"}


chat_service = ChatService()