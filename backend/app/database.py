from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker, DeclarativeBase

from app.config import settings

engine = create_engine(
    settings.DATABASE_URL,
    connect_args={"check_same_thread": False},
    echo=False,
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


class Base(DeclarativeBase):
    pass


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def init_db():
    import logging
    logger = logging.getLogger(__name__)
    Base.metadata.create_all(bind=engine)

    # 自动添加缺失列（SQLite ALTER TABLE）
    # conn = engine.connect()
    # try:
    #     result = conn.execute(text("PRAGMA table_info(gallery_images)"))
    #     columns = [row[1] for row in result.fetchall()]
    #     if 'file_hash' not in columns:
    #         conn.execute(text("ALTER TABLE gallery_images ADD COLUMN file_hash VARCHAR(64)"))
    #         conn.commit()
    #         logger.info("[数据库迁移] 已添加 gallery_images.file_hash 列")
    #     for col, col_type in [
    #         ("cabinet_w", "INTEGER"),
    #         ("cabinet_d", "INTEGER"),
    #         ("cabinet_h", "INTEGER"),
    #         ("material", "VARCHAR(64)"),
    #         ("color", "VARCHAR(32)"),
    #     ]:
    #         if col not in columns:
    #             conn.execute(text(f"ALTER TABLE gallery_images ADD COLUMN {col} {col_type}"))
    #             conn.commit()
    #             logger.info(f"[数据库迁移] 已添加 gallery_images.{col} 列")
    # except Exception:
    #     pass

    # try:
    #     result = conn.execute(text("PRAGMA table_info(render_tasks)"))
    #     columns = [row[1] for row in result.fetchall()]
    #     if 'image_id' not in columns:
    #         conn.execute(text("ALTER TABLE render_tasks ADD COLUMN image_id VARCHAR(64)"))
    #         conn.commit()
    #         logger.info("[数据库迁移] 已添加 render_tasks.image_id 列")
    # except Exception:
    #     pass
    # finally:
    #     conn.close()
