import logging

logger = logging.getLogger(__name__)

ROOM_TEMPLATES = {
    "living_room": {
        "name": "客厅",
        "description": "宽敞明亮的客厅，配有沙发、茶几、电视墙，地板为浅色木地板，墙面为米白色",
        "cabinet_placement": "靠墙放置，与电视墙协调",
    },
    "bedroom": {
        "name": "卧室",
        "description": "温馨舒适的卧室，配有双人床、床头柜、梳妆台，暖色调墙面",
        "cabinet_placement": "靠墙放置，与床和梳妆台协调",
    },
    "kitchen": {
        "name": "厨房",
        "description": "现代开放式厨房，配有大理石台面、不锈钢电器，白色橱柜",
        "cabinet_placement": "与厨房中岛或墙面平行放置",
    },
    "study": {
        "name": "书房",
        "description": "安静的书房，配有书桌、书架、阅读椅，深色木地板",
        "cabinet_placement": "靠墙放置，与书桌和书架协调",
    },
    "entryway": {
        "name": "玄关",
        "description": "简洁的玄关入口，配有鞋柜、穿衣镜、挂钩，明亮灯光",
        "cabinet_placement": "靠墙放置，作为玄关储物柜",
    },
}


def get_room_template(room_type: str) -> dict:
    template = ROOM_TEMPLATES.get(room_type, ROOM_TEMPLATES["living_room"])
    logger.info(f"户型匹配: {room_type} -> {template['name']}")
    return template


def build_scene_prompt(room_type: str, cabinet_desc: str) -> str:
    template = get_room_template(room_type)
    return f"""
将柜子放置在{template['name']}场景中。
场景描述：{template['description']}
柜子摆放：{template['cabinet_placement']}
柜子描述：{cabinet_desc}
要求：真实感渲染，光线自然，材质质感清晰，柜子与场景融为一体。
"""