import os
import shutil
from app.config import settings


def save_upload_file(file_content: bytes, filename: str, subdir: str) -> str:
    save_dir = os.path.join(settings.UPLOAD_DIR, subdir)
    os.makedirs(save_dir, exist_ok=True)
    file_path = os.path.join(save_dir, filename)
    with open(file_path, "wb") as f:
        f.write(file_content)
    return os.path.join(subdir, filename).replace("\\", "/")


def save_result_image(file_content: bytes, task_id: str) -> str:
    from datetime import datetime
    now = datetime.now()
    subdir = os.path.join(str(now.year), f"{now.month:02d}", f"{now.day:02d}")
    save_dir = os.path.join(settings.RESULT_DIR, subdir)
    os.makedirs(save_dir, exist_ok=True)
    filename = f"{task_id}.png"
    file_path = os.path.join(save_dir, filename)
    with open(file_path, "wb") as f:
        f.write(file_content)
    return f"/render_static/results/{subdir.replace(chr(92), '/')}/{filename}"


def delete_file(file_path: str):
    full_path = file_path.lstrip("/")
    if os.path.exists(full_path):
        os.remove(full_path)
