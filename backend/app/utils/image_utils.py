import os
import uuid
from datetime import datetime
from PIL import Image


def generate_unique_filename(original_filename: str) -> str:
    ext = os.path.splitext(original_filename)[1].lower()
    return f"{uuid.uuid4().hex}{ext}"


def get_upload_subdir() -> str:
    now = datetime.now()
    return os.path.join(str(now.year), f"{now.month:02d}", f"{now.day:02d}")


def make_thumbnail(image_path: str, thumb_path: str, size=(200, 200)):
    try:
        img = Image.open(image_path)
        img.thumbnail(size, Image.LANCZOS)
        img.save(thumb_path)
        return True
    except Exception:
        return False


def get_image_size(image_path: str):
    try:
        img = Image.open(image_path)
        return img.width, img.height
    except Exception:
        return None, None


ALLOWED_EXTENSIONS = {".jpg", ".jpeg", ".png", ".webp"}


def is_allowed_image(filename: str) -> bool:
    ext = os.path.splitext(filename)[1].lower()
    return ext in ALLOWED_EXTENSIONS