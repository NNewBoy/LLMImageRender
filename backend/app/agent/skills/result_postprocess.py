import os
import logging
from PIL import Image

logger = logging.getLogger(__name__)


def postprocess_result(result_image_url: str, original_image_path: str) -> str:
    if not result_image_url:
        return result_image_url

    if result_image_url.startswith("http"):
        return result_image_url

    full_path = result_image_url.lstrip("/")
    if not os.path.exists(full_path):
        return result_image_url

    try:
        img = Image.open(full_path)

        if img.mode == "RGBA":
            background = Image.new("RGB", img.size, (255, 255, 255))
            background.paste(img, mask=img.split()[3])
            img = background

        img.save(full_path, "PNG", optimize=True)
        logger.info(f"渲染结果后处理完成: {full_path}")
        return result_image_url

    except Exception as e:
        logger.error(f"结果后处理失败: {e}")
        return result_image_url


def generate_comparison_image(original_path: str, result_path: str, output_path: str) -> bool:
    try:
        orig_full = original_path.lstrip("/")
        result_full = result_path.lstrip("/")

        if not os.path.exists(orig_full) or not os.path.exists(result_full):
            return False

        orig_img = Image.open(orig_full)
        result_img = Image.open(result_full)

        max_height = max(orig_img.height, result_img.height)
        total_width = orig_img.width + result_img.width

        comparison = Image.new("RGB", (total_width, max_height), (255, 255, 255))
        comparison.paste(orig_img, (0, 0))
        comparison.paste(result_img, (orig_img.width, 0))

        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        comparison.save(output_path, "PNG")
        return True

    except Exception as e:
        logger.error(f"对比图生成失败: {e}")
        return False