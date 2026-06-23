import uuid
from datetime import datetime
from sqlalchemy import Column, Integer, String, DateTime
from app.database import Base


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
    created_at = Column(DateTime, default=datetime.utcnow)