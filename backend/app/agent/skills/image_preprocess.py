import os
import logging
from PIL import Image

logger = logging.getLogger(__name__)

MAX_IMAGE_SIZE = (2048, 2048)


def preprocess_image(image_path: str) -> str:
    full_path = image_path.lstrip("/")
    if not os.path.exists(full_path):
        logger.warning(f"图片不存在: {full_path}")
        return image_path

    try:
        img = Image.open(full_path)
        original_format = img.format

        if img.mode not in ("RGB", "RGBA"):
            img = img.convert("RGB")

        if img.width > MAX_IMAGE_SIZE[0] or img.height > MAX_IMAGE_SIZE[1]:
            img.thumbnail(MAX_IMAGE_SIZE, Image.LANCZOS)
            logger.info(f"图片已缩放: {img.size}")

        if original_format not in ("PNG", "JPEG"):
            new_path = os.path.splitext(full_path)[0] + ".png"
            img.save(new_path, "PNG")
            logger.info(f"图片已转换: {new_path}")
            return new_path

        img.save(full_path, original_format)
        return image_path

    except Exception as e:
        logger.error(f"图片预处理失败: {e}")
        return image_path