import uuid
from datetime import datetime, timezone, timedelta
from sqlalchemy import Column, Integer, String, DateTime
from app.database import Base

# 东八区时区
_CST = timezone(timedelta(hours=8))
def _now_cst():
    return datetime.now(_CST).replace(tzinfo=None)


def generate_image_id():
    return f"img_{uuid.uuid4().hex[:12]}"


class GalleryImage(Base):
    __tablename__ = "gallery_images"

    id = Column(Integer, primary_key=True, autoincrement=True)
    image_id = Column(String(64), unique=True, nullable=False, default=generate_image_id)
    name = Column(String(128), nullable=False)
    category = Column(String(32), nullable=False)
    file_path = Column(String(512), nullable=False)
    thumbnail_path = Column(String(512), nullable=True)
    file_hash = Column(String(64), nullable=True, index=True)
    width = Column(Integer, nullable=True)
    height = Column(Integer, nullable=True)
    file_size = Column(Integer, nullable=True)
    cabinet_w = Column(Integer, nullable=True)
    cabinet_d = Column(Integer, nullable=True)
    cabinet_h = Column(Integer, nullable=True)
    material = Column(String(64), nullable=True)
    color = Column(String(32), nullable=True)
    created_at = Column(DateTime, default=_now_cst)
