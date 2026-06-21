import logging

logger = logging.getLogger(__name__)

STYLE_DEFAULTS = {
    "modern_minimalist": {"lighting": "natural", "color": "#FFFFFF"},
    "nordic": {"lighting": "warm", "color": "#F5F5DC"},
    "japanese": {"lighting": "warm_dim", "color": "#8B7355"},
    "industrial": {"lighting": "cool", "color": "#808080"},
    "american": {"lighting": "mixed", "color": "#D2B48C"},
}


def optimize_params(params: dict) -> dict:
    optimized = params.copy()

    style = optimized.get("style", "")
    if style in STYLE_DEFAULTS:
        defaults = STYLE_DEFAULTS[style]
        if "lighting" not in optimized or not optimized["lighting"]:
            optimized["lighting"] = defaults["lighting"]
        if "color" not in optimized or not optimized["color"]:
            optimized["color"] = defaults["color"]

    if "cabinet_size" not in optimized:
        optimized["cabinet_size"] = {"width": 1200, "height": 2200, "depth": 600}

    if "view_angle" not in optimized:
        optimized["view_angle"] = "front_45"

    logger.info(f"参数优化完成: {optimized}")
    return optimized