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
        logger.info("[渲染服务] 初始化完成")

    def submit_task(self, task_id: str):
        logger.info(f"[渲染服务] 提交任务: task_id={task_id}, 当前运行中任务数={len(self._running_tasks)}")
        task = asyncio.create_task(self._execute_render(task_id))
        self._running_tasks[task_id] = task
        logger.info(f"[渲染服务] 任务已创建异步执行: task_id={task_id}")

    async def _execute_render(self, task_id: str):
        logger.info(f"[渲染执行] 开始执行渲染: task_id={task_id}")
        db = SessionLocal()
        try:
            task = db.query(RenderTask).filter(RenderTask.task_id == task_id).first()
            if not task:
                logger.error(f"[渲染执行] 任务不存在: task_id={task_id}")
                return

            logger.info(f"[渲染执行] 任务详情: task_id={task_id}, mode={task.mode}, image={task.original_image}")

            task.status = "processing"
            task.progress = 10
            db.commit()
            logger.info(f"[渲染执行] 任务状态更新为 processing: task_id={task_id}")

            from app.agent.graph import run_render_agent

            task.progress = 30
            db.commit()
            logger.info(f"[渲染执行] 开始调用渲染 Agent: task_id={task_id}")

            result = await run_render_agent(
                task_id=task_id,
                mode=task.mode,
                original_image_path=task.original_image,
                params=json.loads(task.params_json) if task.params_json else {},
            )

            logger.info(f"[渲染执行] 渲染 Agent 返回: task_id={task_id}, success={result.get('success')}")

            task.progress = 80
            db.commit()

            if result.get("success"):
                task.status = "completed"
                task.result_image = result.get("result_image_url", "")
                task.progress = 100
                from datetime import datetime
                task.completed_at = datetime.utcnow()
                logger.info(f"[渲染执行] 渲染任务完成: task_id={task_id}, result={task.result_image}")
            else:
                task.status = "failed"
                task.error_message = result.get("error", "未知错误")
                task.progress = 0
                logger.error(f"[渲染执行] 渲染任务失败: task_id={task_id}, error={task.error_message}")

            db.commit()

        except Exception as e:
            logger.error(f"[渲染执行] 渲染任务 {task_id} 异常: {e}", exc_info=True)
            task = db.query(RenderTask).filter(RenderTask.task_id == task_id).first()
            if task:
                task.status = "failed"
                task.error_message = str(e)
                task.progress = 0
                db.commit()
        finally:
            db.close()
            self._running_tasks.pop(task_id, None)
            logger.info(f"[渲染执行] 任务执行结束: task_id={task_id}, 剩余运行中任务数={len(self._running_tasks)}")

    def cancel_task(self, task_id: str):
        logger.info(f"[渲染服务] 取消任务: task_id={task_id}")
        if task_id in self._running_tasks:
            self._running_tasks[task_id].cancel()
            self._running_tasks.pop(task_id, None)
            logger.info(f"[渲染服务] 任务已取消: task_id={task_id}")
        else:
            logger.warning(f"[渲染服务] 任务不存在或已完成: task_id={task_id}")


render_service = RenderService()