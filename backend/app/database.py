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
    conn = engine.connect()
    try:
        result = conn.execute(text("PRAGMA table_info(render_tasks)"))
        columns = [row[1] for row in result.fetchall()]
        if 'thumbnail' not in columns:
            conn.execute(text("ALTER TABLE render_tasks ADD COLUMN thumbnail VARCHAR(512)"))
            conn.commit()
            logger.info("[数据库迁移] 已添加 render_tasks.thumbnail 列")
    except Exception:
        pass
    finally:
        conn.close()
