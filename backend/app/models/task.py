import uuid
from datetime import datetime
from sqlalchemy import Column, Integer, String, Text, DateTime
from app.database import Base


def generate_task_id():
    return f"task_{datetime.now().strftime('%Y%m%d%H%M%S')}_{uuid.uuid4().hex[:6]}"


class RenderTask(Base):
    __tablename__ = "render_tasks"

    id = Column(Integer, primary_key=True, autoincrement=True)
    task_id = Column(String(64), unique=True, nullable=False, default=generate_task_id)
    mode = Column(String(16), nullable=False)
    status = Column(String(16), nullable=False, default="queued")
    progress = Column(Integer, default=0)
    image_source = Column(String(16), nullable=False)
    original_image = Column(String(512), nullable=False)
    result_image = Column(String(512), nullable=True)
    params_json = Column(Text, nullable=False)
    error_message = Column(Text, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    completed_at = Column(DateTime, nullable=True)