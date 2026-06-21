import asyncio
import json
import logging
from typing import Optional
from app.database import SessionLocal
from app.models.task import RenderTask

logger = logging.getLogger(__name__)


class RenderService:
    def __init__(self):
        self._running_tasks: dict[str, asyncio.Task] = {}

    def submit_task(self, task_id: str):
        task = asyncio.create_task(self._execute_render(task_id))
        self._running_tasks[task_id] = task

    async def _execute_render(self, task_id: str):
        db = SessionLocal()
        try:
            task = db.query(RenderTask).filter(RenderTask.task_id == task_id).first()
            if not task:
                return

            task.status = "processing"
            task.progress = 10
            db.commit()

            from app.agent.graph import run_render_agent

            task.progress = 30
            db.commit()

            result = await run_render_agent(
                task_id=task_id,
                mode=task.mode,
                original_image_path=task.original_image,
                params=json.loads(task.params_json) if task.params_json else {},
            )

            task.progress = 80
            db.commit()

            if result.get("success"):
                task.status = "completed"
                task.result_image = result.get("result_image_url", "")
                task.progress = 100
                from datetime import datetime
                task.completed_at = datetime.utcnow()
            else:
                task.status = "failed"
                task.error_message = result.get("error", "未知错误")
                task.progress = 0

            db.commit()

        except Exception as e:
            logger.error(f"渲染任务 {task_id} 失败: {e}")
            task = db.query(RenderTask).filter(RenderTask.task_id == task_id).first()
            if task:
                task.status = "failed"
                task.error_message = str(e)
                task.progress = 0
                db.commit()
        finally:
            db.close()
            self._running_tasks.pop(task_id, None)

    def cancel_task(self, task_id: str):
        if task_id in self._running_tasks:
            self._running_tasks[task_id].cancel()
            self._running_tasks.pop(task_id, None)


render_service = RenderService()