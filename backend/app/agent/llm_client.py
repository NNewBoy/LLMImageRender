import os
import base64
import logging
import asyncio
from typing import Optional

from app.config import settings

logger = logging.getLogger(__name__)


class LLMClient:
    def __init__(self):
        self.api_key = settings.DASHSCOPE_API_KEY
        self.model_name = settings.DASHSCOPE_MODEL
        logger.info(f"[LLM客户端] 初始化完成, model={self.model_name}, api_key={'已配置' if self.api_key else '未配置'}")

    async def generate_image(
        self,
        prompt: str,
        reference_image_path: Optional[str] = None,
        negative_prompt: str = "",
        size: str = "1024*1024",
    ) -> dict:
        logger.info(f"[LLM图片生成] 开始调用, model={self.model_name}, size={size}")
        logger.info(f"[LLM图片生成] prompt长度={len(prompt)}, reference_image={'有' if reference_image_path else '无'}")

        try:
            import dashscope
            from dashscope import MultiModalConversation

            dashscope.api_key = self.api_key

            content = []
            if reference_image_path:
                full_path = reference_image_path.lstrip("/")
                if os.path.exists(full_path):
                    with open(full_path, "rb") as f:
                        image_data = base64.b64encode(f.read()).decode("utf-8")
                        content.append({"image": f"data:image/png;base64,{image_data}"})
                    logger.info(f"[LLM图片生成] 参考图片已加载: {full_path}, base64长度={len(image_data)}")
                else:
                    logger.warning(f"[LLM图片生成] 参考图片不存在: {full_path}")

            full_prompt = prompt
            if negative_prompt:
                full_prompt = f"{prompt}. Avoid: {negative_prompt}"
            content.append({"text": full_prompt})

            messages = [{"role": "user", "content": content}]

            logger.info(f"[LLM图片生成] 调用 MultiModalConversation.call, content项数={len(content)}")

            response = await asyncio.to_thread(
                MultiModalConversation.call,
                model=self.model_name,
                messages=messages,
                n=1,
                size=size,
                watermark=False,
            )

            logger.info(f"[LLM图片生成] API响应: status_code={response.status_code}")

            if response.status_code == 200 and response.output:
                choices = response.output.get("choices", [])
                logger.info(f"[LLM图片生成] 返回choices数={len(choices)}")
                if choices:
                    msg_content = choices[0].get("message", {}).get("content", [])
                    for item in msg_content:
                        if "image" in item:
                            logger.info(f"[LLM图片生成] 图片URL生成成功")
                            return {
                                "success": True,
                                "image_url": item["image"],
                                "image_base64": None,
                            }
                logger.warning(f"[LLM图片生成] API返回结果为空")
                return {"success": False, "error": "API 返回结果为空"}
            else:
                error_msg = response.message if hasattr(response, "message") else str(response)
                logger.error(f"[LLM图片生成] API调用失败: {error_msg}")
                return {"success": False, "error": error_msg}

        except ImportError:
            logger.warning("[LLM图片生成] dashscope 未安装，使用模拟模式")
            return self._mock_generate(prompt, reference_image_path)
        except Exception as e:
            logger.error(f"[LLM图片生成] 调用异常: {e}", exc_info=True)
            return {"success": False, "error": str(e)}

    def _mock_generate(self, prompt: str, reference_image_path: Optional[str] = None) -> dict:
        logger.info(f"[LLM图片生成] 模拟模式生成")
        return {
            "success": True,
            "image_url": reference_image_path or "",
            "image_base64": None,
            "note": "模拟渲染结果（dashscope 未安装）",
        }


llm_client = LLMClient()
