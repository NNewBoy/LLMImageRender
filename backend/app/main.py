import os
import logging
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

from app.config import settings
from app.database import init_db
from app.routers import images, render, params

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)
logger = logging.getLogger(__name__)

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

app.mount("/render_static", StaticFiles(directory="render_static"), name="render_static")

app.include_router(images.router, prefix="/render_api/images", tags=["images"])
app.include_router(render.router, prefix="/render_api/render", tags=["render"])
app.include_router(params.router, prefix="/render_api/params", tags=["params"])

logger.info("=" * 50)
logger.info("[应用启动] LLMImageRender API 初始化中...")
logger.info(f"[应用配置] UPLOAD_DIR={settings.UPLOAD_DIR}")
logger.info(f"[应用配置] GALLERY_DIR={settings.GALLERY_DIR}")
logger.info(f"[应用配置] RESULT_DIR={settings.RESULT_DIR}")
logger.info(f"[应用配置] CORS_ORIGINS={settings.CORS_ORIGINS}")
logger.info(f"[应用配置] MAX_UPLOAD_SIZE_MB={settings.MAX_UPLOAD_SIZE_MB}")


@app.on_event("startup")
def on_startup():
    logger.info("[应用启动] 初始化数据库...")
    init_db()
    logger.info("[应用启动] 数据库初始化完成")
    logger.info("[应用启动] LLMImageRender API 启动成功!")
    logger.info("=" * 50)


@app.get("/render_api/health")
def health_check():
    logger.debug("[健康检查] 收到健康检查请求")
    return {"status": "ok", "service": "LLMImageRender"}
