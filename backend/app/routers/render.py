import json
from datetime import datetime
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from pydantic import BaseModel

from app.database import get_db
from app.models.task import RenderTask
from app.services.render_service import render_service

router = APIRouter()


class RenderSubmitRequest(BaseModel):
    mode: str
    image_source: dict
    params: dict


@router.post("/submit")
async def submit_render(req: RenderSubmitRequest, db: Session = Depends(get_db)):
    if req.mode not in ("single", "scene"):
        raise HTTPException(status_code=400, detail="渲染模式必须为 single 或 scene")

    image_id = req.image_source.get("image_id")
    if not image_id:
        raise HTTPException(status_code=400, detail="缺少图片ID")

    from app.models.gallery import GalleryImage
    gallery_img = db.query(GalleryImage).filter(GalleryImage.image_id == image_id).first()
    if not gallery_img:
        raise HTTPException(status_code=400, detail="图片不存在")

    task = RenderTask(
        mode=req.mode,
        status="queued",
        image_source=req.image_source.get("type", "gallery"),
        original_image=gallery_img.file_path,
        params_json=json.dumps(req.params, ensure_ascii=False),
    )
    db.add(task)
    db.commit()
    db.refresh(task)

    render_service.submit_task(task.task_id)

    return {
        "code": 200,
        "message": "渲染任务已提交",
        "data": {
            "task_id": task.task_id,
            "status": task.status,
            "created_at": task.created_at.isoformat() if task.created_at else None,
        },
    }


@router.get("/task/{task_id}")
def get_task_status(task_id: str, db: Session = Depends(get_db)):
    task = db.query(RenderTask).filter(RenderTask.task_id == task_id).first()
    if not task:
        raise HTTPException(status_code=404, detail="任务不存在")

    return {
        "code": 200,
        "data": {
            "task_id": task.task_id,
            "status": task.status,
            "progress": task.progress,
            "mode": task.mode,
            "original_image_url": task.original_image,
            "result_image_url": task.result_image,
            "params": json.loads(task.params_json) if task.params_json else {},
            "created_at": task.created_at.isoformat() if task.created_at else None,
            "completed_at": task.completed_at.isoformat() if task.completed_at else None,
            "error_message": task.error_message,
        },
    }


@router.get("/task/{task_id}/result")
def get_task_result(task_id: str, db: Session = Depends(get_db)):
    task = db.query(RenderTask).filter(RenderTask.task_id == task_id).first()
    if not task:
        raise HTTPException(status_code=404, detail="任务不存在")
    if task.status != "completed":
        raise HTTPException(status_code=400, detail="任务尚未完成")
    if not task.result_image:
        raise HTTPException(status_code=404, detail="结果图片不存在")

    return {
        "code": 200,
        "data": {
            "task_id": task.task_id,
            "result_image_url": task.result_image,
            "original_image_url": task.original_image,
        },
    }


@router.get("/history")
def get_history(page: int = 1, page_size: int = 20, db: Session = Depends(get_db)):
    total = db.query(RenderTask).count()
    tasks = (
        db.query(RenderTask)
        .order_by(RenderTask.created_at.desc())
        .offset((page - 1) * page_size)
        .limit(page_size)
        .all()
    )

    return {
        "code": 200,
        "data": {
            "total": total,
            "page": page,
            "page_size": page_size,
            "items": [
                {
                    "task_id": t.task_id,
                    "mode": t.mode,
                    "status": t.status,
                    "original_image_url": t.original_image,
                    "result_image_url": t.result_image,
                    "params": json.loads(t.params_json) if t.params_json else {},
                    "created_at": t.created_at.isoformat() if t.created_at else None,
                    "completed_at": t.completed_at.isoformat() if t.completed_at else None,
                    "error_message": t.error_message,
                }
                for t in tasks
            ],
        },
    }


@router.delete("/task/{task_id}")
def delete_task(task_id: str, db: Session = Depends(get_db)):
    task = db.query(RenderTask).filter(RenderTask.task_id == task_id).first()
    if not task:
        raise HTTPException(status_code=404, detail="任务不存在")

    render_service.cancel_task(task_id)
    db.delete(task)
    db.commit()

    return {"code": 200, "message": "任务已删除"}