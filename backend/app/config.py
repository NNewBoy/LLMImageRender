import os
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    DASHSCOPE_API_KEY: str = os.getenv("DASHSCOPE_API_KEY", "")
    DASHSCOPE_MODEL: str = os.getenv("DASHSCOPE_MODEL", "qwen-image-2.0-pro")
    DATABASE_URL: str = "sqlite:///./llm_image_render.db"
    UPLOAD_DIR: str = "render_static/uploads"
    GALLERY_DIR: str = "render_static/gallery"
    RESULT_DIR: str = "render_static/results"
    MAX_UPLOAD_SIZE_MB: int = 10
    CORS_ORIGINS: str = "http://localhost:5175,http://localhost:3000"

    class Config:
        env_file = ".env"


settings = Settings()
