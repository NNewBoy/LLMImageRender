import json
import logging
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from pydantic import BaseModel

from app.database import get_db
from app.models.chat import ChatSession, ChatMessage
from app.services.chat_service import chat_service

logger = logging.getLogger(__name__)
router = APIRouter()


class ChatStartRequest(BaseModel):
    task_id: str


class ChatMessageRequest(BaseModel):
    session_id: str
    task_id: str
    message: str


@router.post("/start")
def start_chat(req: ChatStartRequest, db: Session = Depends(get_db)):
    logger.info(f"[开启对话] task_id={req.task_id}")

    session = ChatSession(
        task_id=req.task_id,
        status="active",
    )
    db.add(session)
    db.commit()
    db.refresh(session)

    chat_service.start_session(session.session_id, req.task_id)

    logger.info(f"[开启对话] 会话创建成功: session_id={session.session_id}, task_id={req.task_id}")

    return {
        "code": 200,
        "message": "对话已开启",
        "data": {
            "session_id": session.session_id,
            "task_id": session.task_id,
            "status": session.status,
        },
    }


@router.post("/message")
async def send_message(req: ChatMessageRequest, db: Session = Depends(get_db)):
    logger.info(f"[发送消息] session_id={req.session_id}, task_id={req.task_id}, message={req.message[:50]}...")

    session = db.query(ChatSession).filter(ChatSession.session_id == req.session_id).first()
    if not session:
        logger.warning(f"[发送消息] 会话不存在: {req.session_id}")
        raise HTTPException(status_code=404, detail="会话不存在")
    if session.status != "active":
        logger.warning(f"[发送消息] 会话已暂停或关闭: {req.session_id}, status={session.status}")
        raise HTTPException(status_code=400, detail="会话已暂停或关闭")

    user_msg = ChatMessage(
        session_id=req.session_id,
        role="user",
        content=req.message,
    )
    db.add(user_msg)
    db.commit()

    logger.info(f"[发送消息] 用户消息已保存, 开始调用对话服务")

    result = await chat_service.send_message(req.session_id, req.message)

    assistant_msg = ChatMessage(
        session_id=req.session_id,
        role="assistant",
        content=result.get("content", ""),
        params_update=json.dumps(result.get("params_update", {}), ensure_ascii=False),
    )
    db.add(assistant_msg)
    db.commit()

    logger.info(f"[发送消息] 对话响应完成: session_id={req.session_id}, params_update={result.get('params_update')}")

    return {
        "code": 200,
        "data": {
            "session_id": req.session_id,
            "role": "assistant",
            "content": result.get("content", ""),
            "params_update": result.get("params_update", {}),
        },
    }


@router.post("/stop")
def stop_chat(req: ChatStartRequest, db: Session = Depends(get_db)):
    logger.info(f"[停止对话] task_id={req.task_id}")

    session = db.query(ChatSession).filter(ChatSession.session_id == req.task_id).first()
    if not session:
        sessions = db.query(ChatSession).filter(ChatSession.task_id == req.task_id).all()
        if not sessions:
            logger.warning(f"[停止对话] 会话不存在: task_id={req.task_id}")
            raise HTTPException(status_code=404, detail="会话不存在")
        session = sessions[-1]

    session.status = "paused"
    db.commit()
    chat_service.stop_session(session.session_id)

    logger.info(f"[停止对话] 对话已停止: session_id={session.session_id}")

    return {"code": 200, "message": "对话已停止"}


@router.post("/continue")
def continue_chat(req: ChatStartRequest, db: Session = Depends(get_db)):
    logger.info(f"[继续对话] task_id={req.task_id}")

    session = db.query(ChatSession).filter(ChatSession.session_id == req.task_id).first()
    if not session:
        sessions = db.query(ChatSession).filter(ChatSession.task_id == req.task_id).all()
        if not sessions:
            logger.warning(f"[继续对话] 会话不存在: task_id={req.task_id}")
            raise HTTPException(status_code=404, detail="会话不存在")
        session = sessions[-1]

    session.status = "active"
    db.commit()
    result = chat_service.continue_session(session.session_id)

    logger.info(f"[继续对话] 对话已继续: session_id={session.session_id}")

    return {
        "code": 200,
        "message": "对话已继续",
        "data": result,
    }


@router.get("/{session_id}/history")
def get_chat_history(session_id: str, db: Session = Depends(get_db)):
    logger.info(f"[获取对话历史] session_id={session_id}")

    messages = (
        db.query(ChatMessage)
        .filter(ChatMessage.session_id == session_id)
        .order_by(ChatMessage.created_at.asc())
        .all()
    )

    logger.info(f"[获取对话历史] session_id={session_id}, 返回 {len(messages)} 条消息")

    return {
        "code": 200,
        "data": [
            {
                "role": m.role,
                "content": m.content,
                "params_update": json.loads(m.params_update) if m.params_update else None,
                "created_at": m.created_at.isoformat() if m.created_at else None,
            }
            for m in messages
        ],
    }