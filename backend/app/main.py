import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

from app.config import settings
from app.database import init_db
from app.routers import images, render, chat, params

app = FastAPI(
    title="LLMImageRender API",
    description="柜子家具3D模型图片真实渲染平台",
    version="1.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS.split(","),
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

os.makedirs(settings.UPLOAD_DIR, exist_ok=True)
os.makedirs(settings.GALLERY_DIR, exist_ok=True)
os.makedirs(settings.RESULT_DIR, exist_ok=True)

app.mount("/static", StaticFiles(directory="static"), name="static")

app.include_router(images.router, prefix="/api/images", tags=["images"])
app.include_router(render.router, prefix="/api/render", tags=["render"])
app.include_router(chat.router, prefix="/api/chat", tags=["chat"])
app.include_router(params.router, prefix="/api/params", tags=["params"])


@app.on_event("startup")
def on_startup():
    init_db()


@app.get("/api/health")
def health_check():
    return {"status": "ok", "service": "LLMImageRender"}