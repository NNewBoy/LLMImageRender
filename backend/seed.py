import os
import hashlib
import sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app.database import SessionLocal, init_db
from app.models.gallery import GalleryImage
from app.utils.image_utils import get_image_size


SEED_IMAGES = [
    {
        "name": "简约衣柜",
        "category": "wardrobe",
        "file_path": "/render_static/gallery/wardrobe/wardrobe1.png",
        "thumbnail_path": "/render_static/gallery/wardrobe/wardrobe1.png",
        "cabinet_w": 1350,
        "cabinet_d": 550,
        "cabinet_h": 2180,
        "material": "white_lacquer",
        "color": "#ffffed",
    },
    {
        "name": "简约橱柜",
        "category": "kitchen",
        "file_path": "/render_static/gallery/kitchen/kitchen1.png",
        "thumbnail_path": "/render_static/gallery/kitchen/kitchen1.png",
        "cabinet_w": 900,
        "cabinet_d": 550,
        "cabinet_h": 660,
        "material": "plywood",
        "color": "#d1bfb6",
    },
    {
        "name": "简约书柜",
        "category": "bookcase",
        "file_path": "/render_static/gallery/bookcase/bookcase1.png",
        "thumbnail_path": "/render_static/gallery/bookcase/bookcase1.png",
        "cabinet_w": 900,
        "cabinet_d": 400,
        "cabinet_h": 2180,
        "material": "walnut_wood",
        "color": "#ebe4df",
    },
    {
        "name": "简约玄关柜",
        "category":"entryway",
        "file_path": "/render_static/gallery/entryway/entryway1.png",
        "thumbnail_path": "/render_static/gallery/entryway/entryway1.png",
        "cabinet_w": 900,
        "cabinet_d": 350,
        "cabinet_h": 2180,
        "material": "white_lacquer",
        "color": "#ffffed",
    },
    {
        "name": "简约电视柜",
        "category": "tv_stand",
        "file_path": "/render_static/gallery/tv_stand/tv_stand1.png",
        "thumbnail_path": "/render_static/gallery/tv_stand/tv_stand1.png",
        "cabinet_w": 1350,
        "cabinet_d": 350,
        "cabinet_h": 205,
        "material": "white_lacquer",
        "color": "#ffffed",
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
            file_hash = None
            if os.path.exists(full_path):
                width, height = get_image_size(full_path)
                file_size = os.path.getsize(full_path)
                with open(full_path, "rb") as f:
                    file_hash = hashlib.md5(f.read()).hexdigest()

            image = GalleryImage(
                name=img_data["name"],
                category=img_data["category"],
                file_path=img_data["file_path"],
                thumbnail_path=img_data["thumbnail_path"],
                file_hash=file_hash,
                width=width,
                height=height,
                file_size=file_size,
                cabinet_w=img_data.get("cabinet_w"),
                cabinet_d=img_data.get("cabinet_d"),
                cabinet_h=img_data.get("cabinet_h"),
                material=img_data.get("material"),
                color=img_data.get("color"),
            )
            db.add(image)
            print(f"添加图库图片: {img_data['name']} ({img_data['category']})")

        db.commit()
        print(f"种子数据导入完成，共 {len(SEED_IMAGES)} 条")

    finally:
        db.close()


if __name__ == "__main__":
    seed()
