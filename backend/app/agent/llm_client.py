import os
import base64
import logging
from typing import Optional

logger = logging.getLogger(__name__)


class LLMClient:
    def __init__(self):
        self.api_key = os.getenv("DASHSCOPE_API_KEY", "")
        self.model_name = "qwen-image-2.0-pro"

    async def generate_image(
        self,
        prompt: str,
        reference_image_path: Optional[str] = None,
        negative_prompt: str = "",
        size: str = "1024*1024",
    ) -> dict:
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

            full_prompt = prompt
            if negative_prompt:
                full_prompt = f"{prompt}. Avoid: {negative_prompt}"
            content.append({"text": full_prompt})

            messages = [{"role": "user", "content": content}]

            logger.info(f"调用 LLM 渲染: prompt={full_prompt[:200]}...")

            response = MultiModalConversation.call(
                model=self.model_name,
                messages=messages,
                n=1,
                size=size,
                watermark=False,
            )

            if response.status_code == 200 and response.output:
                choices = response.output.get("choices", [])
                if choices:
                    msg_content = choices[0].get("message", {}).get("content", [])
                    for item in msg_content:
                        if "image" in item:
                            return {
                                "success": True,
                                "image_url": item["image"],
                                "image_base64": None,
                            }
                return {"success": False, "error": "API 返回结果为空"}
            else:
                error_msg = response.message if hasattr(response, "message") else str(response)
                logger.error(f"LLM API 调用失败: {error_msg}")
                return {"success": False, "error": error_msg}

        except ImportError:
            logger.warning("dashscope 未安装，使用模拟模式")
            return self._mock_generate(prompt, reference_image_path)
        except Exception as e:
            logger.error(f"LLM API 调用异常: {e}")
            return {"success": False, "error": str(e)}

    def _mock_generate(self, prompt: str, reference_image_path: Optional[str] = None) -> dict:
        return {
            "success": True,
            "image_url": reference_image_path or "",
            "image_base64": None,
            "note": "模拟渲染结果（dashscope 未安装）",
        }

    async def chat(
        self,
        messages: list[dict],
        system_prompt: str = "",
    ) -> dict:
        try:
            import dashscope
            from dashscope import Generation

            dashscope.api_key = self.api_key

            formatted_messages = []
            if system_prompt:
                formatted_messages.append({"role": "system", "content": system_prompt})
            for msg in messages:
                formatted_messages.append({
                    "role": msg.get("role", "user"),
                    "content": msg.get("content", ""),
                })

            response = Generation.call(
                model="qwen-plus",
                messages=formatted_messages,
                result_format="message",
            )

            if response.status_code == 200 and response.output:
                content = response.output.get("choices", [{}])[0].get("message", {}).get("content", "")
                return {"success": True, "content": content}
            else:
                error_msg = response.message if hasattr(response, "message") else str(response)
                return {"success": False, "content": "", "error": error_msg}

        except ImportError:
            logger.warning("dashscope 未安装，使用模拟模式")
            return self._mock_chat(messages)
        except Exception as e:
            logger.error(f"LLM 对话调用异常: {e}")
            return {"success": False, "content": "", "error": str(e)}

    def _mock_chat(self, messages: list[dict]) -> dict:
        last_msg = messages[-1]["content"] if messages else ""
        return {
            "success": True,
            "content": f"已收到您的需求：'{last_msg}'。正在根据您的要求调整渲染参数...",
            "params_update": {},
        }


llm_client = LLMClient()