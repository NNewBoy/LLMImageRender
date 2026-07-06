import os
import shutil
import io
from datetime import datetime
from PIL import Image
from app.config import settings


def save_upload_file(file_content: bytes, filename: str, subdir: str) -> str:
    save_dir = os.path.join(settings.UPLOAD_DIR, subdir)
    os.makedirs(save_dir, exist_ok=True)
    file_path = os.path.join(save_dir, filename)
    with open(file_path, "wb") as f:
        f.write(file_content)
    return os.path.join(subdir, filename).replace("\\", "/")


def save_result_image(file_content: bytes, task_id: str) -> str:
    now = datetime.now()
    subdir = os.path.join(str(now.year), f"{now.month:02d}", f"{now.day:02d}")
    save_dir = os.path.join(settings.RESULT_DIR, subdir)
    os.makedirs(save_dir, exist_ok=True)
    filename = f"{task_id}.png"
    file_path = os.path.join(save_dir, filename)
    with open(file_path, "wb") as f:
        f.write(file_content)
    return f"/render_static/results/{subdir.replace(chr(92), '/')}/{filename}"


def save_thumbnail(file_content: bytes, task_id: str, size=(400, 400)) -> str:
    """从图片二进制内容生成缩略图并保存，返回可访问的URL。"""
    now = datetime.now()
    subdir = os.path.join(str(now.year), f"{now.month:02d}", f"{now.day:02d}")
    save_dir = os.path.join(settings.RESULT_DIR, subdir)
    os.makedirs(save_dir, exist_ok=True)
    filename = f"thumb_{task_id}.png"
    file_path = os.path.join(save_dir, filename)

    img = Image.open(io.BytesIO(file_content))
    if img.mode == "RGBA":
        background = Image.new("RGB", img.size, (255, 255, 255))
        background.paste(img, mask=img.split()[3])
        img = background
    img.thumbnail(size, Image.LANCZOS)
    img.save(file_path, "PNG")

    return f"/render_static/results/{subdir.replace(chr(92), '/')}/{filename}"


def delete_file(file_path: str):
    full_path = file_path.lstrip("/")
    if os.path.exists(full_path):
        os.remove(full_path)
