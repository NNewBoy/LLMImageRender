import uuid
from datetime import datetime
from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey
from app.database import Base


def generate_session_id():
    return f"session_{uuid.uuid4().hex[:12]}"


class ChatSession(Base):
    __tablename__ = "chat_sessions"

    id = Column(Integer, primary_key=True, autoincrement=True)
    session_id = Column(String(64), unique=True, nullable=False, default=generate_session_id)
    task_id = Column(String(64), nullable=True)
    status = Column(String(16), nullable=False, default="active")
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)


class ChatMessage(Base):
    __tablename__ = "chat_messages"

    id = Column(Integer, primary_key=True, autoincrement=True)
    session_id = Column(String(64), nullable=False)
    role = Column(String(16), nullable=False)
    content = Column(Text, nullable=False)
    params_update = Column(Text, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)