import os
import hashlib
import logging
import shutil
from fastapi import APIRouter, UploadFile, File, Form, Depends, HTTPException
from pydantic import BaseModel
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
async def upload_image(
    file: UploadFile = File(...),
    cabinet_w: int | None = Form(None),
    cabinet_d: int | None = Form(None),
    cabinet_h: int | None = Form(None),
    material: str | None = Form(None),
    color: str | None = Form(None),
    db: Session = Depends(get_db),
):
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
                "cabinet_w": existing.cabinet_w,
                "cabinet_d": existing.cabinet_d,
                "cabinet_h": existing.cabinet_h,
                "material": existing.material,
                "color": existing.color,
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
        category="other",
        file_path=f"/render_static/uploads/{rel_path}",
        thumbnail_path=f"/render_static/uploads/{subdir.replace(chr(92), '/')}/thumbnails/{filename}",
        file_hash=file_hash,
        width=width,
        height=height,
        file_size=file_size,
        cabinet_w=cabinet_w,
        cabinet_d=cabinet_d,
        cabinet_h=cabinet_h,
        material=material,
        color=color,
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
            "cabinet_w": cabinet_w,
            "cabinet_d": cabinet_d,
            "cabinet_h": cabinet_h,
            "material": material,
            "color": color,
        },
    }


@router.get("/gallery")
def get_gallery(category: str = None, order: str = "desc", db: Session = Depends(get_db)):
    logger.info(f"[获取图片列表] category={category}, order={order}")

    query = db.query(GalleryImage)
    if category:
        query = query.filter(GalleryImage.category == category)
    if order == "asc":
        images = query.order_by(GalleryImage.created_at.asc()).all()
    else:
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
                "cabinet_w": img.cabinet_w,
                "cabinet_d": img.cabinet_d,
                "cabinet_h": img.cabinet_h,
                "material": img.material,
                "color": img.color,
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


class UpdateImageRequest(BaseModel):
    name: str | None = None
    category: str | None = None


@router.put("/gallery/{image_id}")
def update_image(image_id: str, req: UpdateImageRequest, db: Session = Depends(get_db)):
    logger.info(f"[更新图片信息] image_id={image_id}, name={req.name}, category={req.category}")

    img = db.query(GalleryImage).filter(GalleryImage.image_id == image_id).first()
    if not img:
        logger.warning(f"[更新图片信息] 图片不存在: {image_id}")
        raise HTTPException(status_code=404, detail="图片不存在")

    if req.name is not None:
        img.name = req.name
    if req.category is not None:
        img.category = req.category
    if req.cabinet_w is not None:
        img.cabinet_w = req.cabinet_w
    if req.cabinet_d is not None:
        img.cabinet_d = req.cabinet_d
    if req.cabinet_h is not None:
        img.cabinet_h = req.cabinet_h
    if req.material is not None:
        img.material = req.material
    if req.color is not None:
        img.color = req.color

    db.commit()
    db.refresh(img)

    logger.info(f"[更新图片信息] 更新成功: image_id={image_id}")

    return {
        "code": 200,
        "message": "更新成功",
        "data": {
            "image_id": img.image_id,
            "name": img.name,
            "category": img.category,
            "url": img.file_path,
            "thumbnail_url": img.thumbnail_path or img.file_path,
            "width": img.width,
            "height": img.height,
            "cabinet_w": img.cabinet_w,
            "cabinet_d": img.cabinet_d,
            "cabinet_h": img.cabinet_h,
            "material": img.material,
            "color": img.color,
        },
    }


@router.delete("/gallery/{image_id}")
def delete_image(image_id: str, db: Session = Depends(get_db)):
    logger.info(f"[删除图片] image_id={image_id}")

    img = db.query(GalleryImage).filter(GalleryImage.image_id == image_id).first()
    if not img:
        logger.warning(f"[删除图片] 图片不存在: {image_id}")
        raise HTTPException(status_code=404, detail="图片不存在")

    # 删除物理文件
    if img.file_path:
        file_abs = os.path.join(settings.UPLOAD_DIR, img.file_path.replace("/render_static/uploads/", ""))
        if os.path.exists(file_abs):
            os.remove(file_abs)
            logger.info(f"[删除图片] 已删除文件: {file_abs}")
    if img.thumbnail_path:
        thumb_abs = os.path.join(settings.UPLOAD_DIR, img.thumbnail_path.replace("/render_static/uploads/", ""))
        if os.path.exists(thumb_abs):
            os.remove(thumb_abs)
            logger.info(f"[删除图片] 已删除缩略图: {thumb_abs}")

    db.delete(img)
    db.commit()

    logger.info(f"[删除图片] 删除成功: image_id={image_id}")

    return {"code": 200, "message": "删除成功"}
