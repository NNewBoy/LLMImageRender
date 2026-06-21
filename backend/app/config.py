import os
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    DASHSCOPE_API_KEY: str = os.getenv("DASHSCOPE_API_KEY", "")
    DATABASE_URL: str = "sqlite:///./llm_image_render.db"
    UPLOAD_DIR: str = "static/uploads"
    GALLERY_DIR: str = "static/gallery"
    RESULT_DIR: str = "static/results"
    MAX_UPLOAD_SIZE_MB: int = 10
    CORS_ORIGINS: str = "http://localhost:5173,http://localhost:3000"

    class Config:
        env_file = ".env"


settings = Settings()