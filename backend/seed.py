import os
import sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app.database import SessionLocal, init_db
from app.models.gallery import GalleryImage
from app.utils.image_utils import get_image_size


SEED_IMAGES = [
    {
        "name": "现代简约衣柜",
        "category": "wardrobe",
        "file_path": "/static/gallery/wardrobe/cabinet-main.png",
        "thumbnail_path": "/static/gallery/wardrobe/cabinet-main.png",
    },
    {
        "name": "欧式橱柜",
        "category": "kitchen",
        "file_path": "/static/gallery/kitchen/cabinet-open.png",
        "thumbnail_path": "/static/gallery/kitchen/cabinet-open.png",
    },
    {
        "name": "日式书柜",
        "category": "bookcase",
        "file_path": "/static/gallery/bookcase/cabinet-side.png",
        "thumbnail_path": "/static/gallery/bookcase/cabinet-side.png",
    },
]


def seed():
    init_db()
    db = SessionLocal()

    try:
        existing = db.query(GalleryImage).count()
        if existing > 0:
            print(f"图库已有 {existing} 条数据，跳过种子数据")
            return

        for img_data in SEED_IMAGES:
            full_path = img_data["file_path"].lstrip("/")
            width, height = None, None
            file_size = None
            if os.path.exists(full_path):
                width, height = get_image_size(full_path)
                file_size = os.path.getsize(full_path)

            image = GalleryImage(
                name=img_data["name"],
                category=img_data["category"],
                file_path=img_data["file_path"],
                thumbnail_path=img_data["thumbnail_path"],
                width=width,
                height=height,
                file_size=file_size,
            )
            db.add(image)
            print(f"添加图库图片: {img_data['name']} ({img_data['category']})")

        db.commit()
        print(f"种子数据导入完成，共 {len(SEED_IMAGES)} 条")

    finally:
        db.close()


if __name__ == "__main__":
    seed()