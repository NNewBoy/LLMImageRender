import logging

logger = logging.getLogger(__name__)

STYLE_MAP = {
    "modern_minimalist": "现代简约风格，线条简洁，色彩纯净，空间通透",
    "nordic": "北欧风格，自然温馨，大量使用木材和浅色系，光线柔和",
    "japanese": "日式风格，禅意简约，深色木材，自然质感，宁静氛围",
    "industrial": "工业风格，粗犷质感，金属元素，深灰色调，Loft感觉",
    "american": "美式风格，经典大气，深色实木，复古元素，温暖色调",
}

LIGHTING_MAP = {
    "natural": "自然光线，明亮均匀，来自窗户的自然日光",
    "warm": "暖色灯光，色温约3000K，营造温馨舒适氛围",
    "cool": "冷色灯光，色温约5000K，明亮清晰，现代感强",
    "mixed": "混合光线，自然光与人工光结合，层次丰富",
}

VIEW_ANGLE_MAP = {
    "front": "正面视角，直接面对柜子正面",
    "front_45": "45度角侧面视角，展示柜子正面和侧面",
    "top": "俯视视角，从上方俯瞰柜子",
    "custom": "自定义角度",
}

MATERIAL_MAP = {
    "oak_wood": "橡木材质，纹理清晰，温暖色调",
    "walnut_wood": "胡桃木材质，深色高贵，纹理优雅",
    "cherry_wood": "樱桃木材质，红棕色，细腻光泽",
    "white_lacquer": "白色烤漆，光滑亮面，现代感强",
    "metal": "金属材质，拉丝不锈钢，冷峻现代",
    "glass": "玻璃材质，通透感，轻盈现代",
}


def build_system_prompt() -> str:
    return """你是一个专业的家具3D渲染助手。你的任务是根据用户提供的柜子图片和参数，生成高质量的3D真实感渲染图。
你需要：
1. 理解用户的渲染需求
2. 根据参数构建精确的渲染提示词
3. 确保渲染风格、光照、材质等参数正确应用
4. 对于场景渲染，确保柜子与户型环境自然融合"""


def build_render_prompt(params: dict, mode: str) -> str:
    style = STYLE_MAP.get(params.get("style", ""), "")
    lighting = LIGHTING_MAP.get(params.get("lighting", ""), "")
    view_angle = VIEW_ANGLE_MAP.get(params.get("view_angle", ""), "")
    material = MATERIAL_MAP.get(params.get("material", ""), "")
    color = params.get("color", "")
    background_color = params.get("background_color", "")
    description = params.get("description", "")

    size = params.get("cabinet_size", {})
    size_desc = ""
    if size:
        size_desc = f"柜子尺寸：宽{size.get('width', '')}mm x 高{size.get('height', '')}mm x 深{size.get('depth', '')}mm"

    prompt_parts = ["请对图中的柜子进行3D真实感渲染，要求如下："]

    if style:
        prompt_parts.append(f"风格：{style}")
    if lighting:
        prompt_parts.append(f"光照：{lighting}")
    if view_angle:
        prompt_parts.append(f"视角：{view_angle}")
    if material:
        prompt_parts.append(f"材质：{material}")
    if color:
        prompt_parts.append(f"颜色：{color}")
    if mode == "single" and background_color:
        prompt_parts.append(f"背景：纯色背景，背景颜色为{background_color}，背景干净简洁无杂物无纹理")
    if size_desc:
        prompt_parts.append(size_desc)
    if description:
        prompt_parts.append(f"额外要求：{description}")

    prompt_parts.append("请生成高质量、真实感强的3D渲染图，细节清晰，材质质感逼真。")

    prompt = "，".join(prompt_parts)
    logger.info(f"渲染提示词构建完成: {prompt[:200]}...")
    return prompt