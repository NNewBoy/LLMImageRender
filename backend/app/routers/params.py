from fastapi import APIRouter

router = APIRouter()

PRESET_PARAMS = {
    "styles": [
        {"value": "modern_minimalist", "label": "现代简约"},
        {"value": "nordic", "label": "北欧风"},
        {"value": "japanese", "label": "日式"},
        {"value": "industrial", "label": "工业风"},
        {"value": "american", "label": "美式"},
    ],
    "lighting": [
        {"value": "natural", "label": "自然光"},
        {"value": "warm", "label": "暖光"},
        {"value": "cool", "label": "冷光"},
        {"value": "mixed", "label": "混合光"},
    ],
    "view_angles": [
        {"value": "front", "label": "正面"},
        {"value": "front_45", "label": "侧面45°"},
        {"value": "top", "label": "俯视"},
        {"value": "custom", "label": "自定义角度"},
    ],
    "room_types": [
        {"value": "living_room", "label": "客厅"},
        {"value": "bedroom", "label": "卧室"},
        {"value": "kitchen", "label": "厨房"},
        {"value": "study", "label": "书房"},
        {"value": "entryway", "label": "玄关"},
    ],
    "materials": [
        {"value": "oak_wood", "label": "橡木"},
        {"value": "walnut_wood", "label": "胡桃木"},
        {"value": "cherry_wood", "label": "樱桃木"},
        {"value": "white_lacquer", "label": "白色烤漆"},
        {"value": "metal", "label": "金属"},
        {"value": "glass", "label": "玻璃"},
    ],
    "categories": [
        {"value": "wardrobe", "label": "衣柜"},
        {"value": "kitchen", "label": "橱柜"},
        {"value": "bookcase", "label": "书柜"},
        {"value": "entryway", "label": "玄关柜"},
        {"value": "tv_stand", "label": "电视柜"},
    ],
}


@router.get("/presets")
def get_presets():
    return {"code": 200, "data": PRESET_PARAMS}