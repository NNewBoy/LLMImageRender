import os
import hashlib
import logging
import shutil
from fastapi import APIRouter, UploadFile, File, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db
from app.config import settings
from app.models.gallery import GalleryImage
from app.utils.image_utils import (
    generate_unique_filename, get_upload_subdir, make_thumbnail,
    get_image_size, is_allowed_image,
)

logger = logging.getLogger(__name__)
router = APIRouter()


@router.post("/upload")
async def upload_image(file: UploadFile = File(...), db: Session = Depends(get_db)):
    logger.info(f"[图片上传] filename={file.filename}, content_type={file.content_type}")

    if not file.filename or not is_allowed_image(file.filename):
        logger.warning(f"[图片上传] 不支持的文件格式: {file.filename}")
        raise HTTPException(status_code=400, detail="不支持的文件格式，仅支持 JPG/PNG/WebP")

    content = await file.read()
    file_size_mb = len(content) / (1024 * 1024)
    logger.info(f"[图片上传] 文件大小: {file_size_mb:.2f}MB")

    if len(content) > settings.MAX_UPLOAD_SIZE_MB * 1024 * 1024:
        logger.warning(f"[图片上传] 文件大小超过限制: {file_size_mb:.2f}MB > {settings.MAX_UPLOAD_SIZE_MB}MB")
        raise HTTPException(status_code=400, detail=f"文件大小超过 {settings.MAX_UPLOAD_SIZE_MB}MB 限制")

    # 计算文件哈希，检查是否已存在
    file_hash = hashlib.md5(content).hexdigest()
    existing = db.query(GalleryImage).filter(GalleryImage.file_hash == file_hash).first()
    if existing:
        logger.info(f"[图片上传] 图片已存在，跳过保存: image_id={existing.image_id}, hash={file_hash}")
        return {
            "code": 200,
            "message": "图片已存在",
            "data": {
                "image_id": existing.image_id,
                "name": existing.name,
                "url": existing.file_path,
                "thumbnail_url": existing.thumbnail_path,
                "width": existing.width,
                "height": existing.height,
                "file_size": existing.file_size,
            },
        }

    filename = generate_unique_filename(file.filename)
    subdir = get_upload_subdir()
    save_dir = os.path.join(settings.UPLOAD_DIR, subdir)
    os.makedirs(save_dir, exist_ok=True)

    file_path = os.path.join(save_dir, filename)
    with open(file_path, "wb") as f:
        f.write(content)

    logger.info(f"[图片上传] 文件保存成功: {file_path}")

    rel_path = os.path.join(subdir, filename).replace("\\", "/")
    width, height = get_image_size(file_path)
    file_size = os.path.getsize(file_path)

    thumb_dir = os.path.join(save_dir, "thumbnails")
    os.makedirs(thumb_dir, exist_ok=True)
    thumb_path = os.path.join(thumb_dir, filename)
    make_thumbnail(file_path, thumb_path)

    gallery_image = GalleryImage(
        name=file.filename,
        category="uploaded",
        file_path=f"/static/uploads/{rel_path}",
        thumbnail_path=f"/static/uploads/{subdir.replace(chr(92), '/')}/thumbnails/{filename}",
        file_hash=file_hash,
        width=width,
        height=height,
        file_size=file_size,
    )
    db.add(gallery_image)
    db.commit()
    db.refresh(gallery_image)

    logger.info(f"[图片上传] 图片入库成功: image_id={gallery_image.image_id}, size={width}x{height}, hash={file_hash}")

    return {
        "code": 200,
        "message": "上传成功",
        "data": {
            "image_id": gallery_image.image_id,
            "name": gallery_image.name,
            "url": gallery_image.file_path,
            "thumbnail_url": gallery_image.thumbnail_path,
            "width": width,
            "height": height,
            "file_size": file_size,
        },
    }


@router.get("/gallery")
def get_gallery(category: str = None, db: Session = Depends(get_db)):
    logger.info(f"[获取图片列表] category={category}")

    query = db.query(GalleryImage)
    if category:
        query = query.filter(GalleryImage.category == category)
    images = query.order_by(GalleryImage.created_at.desc()).all()

    logger.info(f"[获取图片列表] 返回 {len(images)} 张图片")

    return {
        "code": 200,
        "data": [
            {
                "image_id": img.image_id,
                "name": img.name,
                "category": img.category,
                "url": img.file_path,
                "thumbnail_url": img.thumbnail_path or img.file_path,
                "width": img.width,
                "height": img.height,
            }
            for img in images
        ],
    }


@router.get("/gallery/{image_id}")
def get_gallery_detail(image_id: str, db: Session = Depends(get_db)):
    logger.info(f"[获取图片详情] image_id={image_id}")

    img = db.query(GalleryImage).filter(GalleryImage.image_id == image_id).first()
    if not img:
        logger.warning(f"[获取图片详情] 图片不存在: {image_id}")
        raise HTTPException(status_code=404, detail="图片不存在")

    logger.info(f"[获取图片详情] image_id={image_id}, name={img.name}, size={img.width}x{img.height}")

    return {
        "code": 200,
        "data": {
            "image_id": img.image_id,
            "name": img.name,
            "category": img.category,
            "url": img.file_path,
            "thumbnail_url": img.thumbnail_path or img.file_path,
            "width": img.width,
            "height": img.height,
        },
    }