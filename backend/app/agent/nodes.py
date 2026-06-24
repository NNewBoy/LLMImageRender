import logging
import asyncio
from app.agent.state import RenderAgentState
from app.agent.skills.image_preprocess import preprocess_image
from app.agent.skills.param_optimizer import optimize_params
from app.agent.skills.prompt_builder import build_system_prompt, build_render_prompt
from app.agent.skills.room_template import build_scene_prompt
from app.agent.llm_client import llm_client

logger = logging.getLogger(__name__)


async def parse_input(state: RenderAgentState) -> RenderAgentState:
    logger.info(f"[parse_input] 开始解析输入, task_id={state.get('task_id')}")

    original_path = state.get("original_image_path", "")
    processed_path = await asyncio.to_thread(preprocess_image, original_path)
    state["original_image_path"] = processed_path

    params = {
        "style": state.get("style", "modern_minimalist"),
        "lighting": state.get("lighting", "natural"),
        "view_angle": state.get("view_angle", "front_45"),
        "room_type": state.get("room_type"),
        "cabinet_size": state.get("cabinet_size"),
        "material": state.get("material"),
        "color": state.get("color"),
        "background_color": state.get("background_color"),
        "description": state.get("description", ""),
    }

    optimized_params = optimize_params(params)
    for key, value in optimized_params.items():
        state[key] = value

    state["progress"] = 20
    state["status"] = "processing"
    logger.info(f"[parse_input] 输入解析完成")
    return state


async def build_prompt(state: RenderAgentState) -> RenderAgentState:
    logger.info(f"[build_prompt] 开始构建提示词")

    mode = state.get("mode", "single")
    params = {
        "style": state.get("style"),
        "lighting": state.get("lighting"),
        "view_angle": state.get("view_angle"),
        "room_type": state.get("room_type"),
        "cabinet_size": state.get("cabinet_size"),
        "material": state.get("material"),
        "color": state.get("color"),
        "background_color": state.get("background_color"),
        "description": state.get("description"),
    }

    system_prompt = build_system_prompt()
    render_prompt = build_render_prompt(params, mode)

    if mode == "scene" and state.get("room_type"):
        cabinet_desc = f"柜子风格：{params.get('style', '')}, 材质：{params.get('material', '')}"
        scene_prompt = build_scene_prompt(state["room_type"], cabinet_desc)
        render_prompt = f"{render_prompt}\n\n场景要求：{scene_prompt}"

    state["system_prompt"] = system_prompt
    state["user_prompt"] = render_prompt
    state["progress"] = 40
    logger.info(f"[build_prompt] 提示词构建完成")
    return state


async def check_interrupt(state: RenderAgentState) -> RenderAgentState:
    logger.info(f"[check_interrupt] 检查中断状态: paused={state.get('is_paused')}, cancelled={state.get('is_cancelled')}")
    return state


async def call_llm_render(state: RenderAgentState) -> RenderAgentState:
    logger.info(f"[call_llm_render] 开始调用 LLM 渲染")

    try:
        result = await llm_client.generate_image(
            prompt=state.get("user_prompt", ""),
            reference_image_path=state.get("original_image_path"),
        )

        if result.get("success"):
            state["result_image_url"] = result.get("image_url", "")
            state["result_image_base64"] = result.get("image_base64")
            state["progress"] = 70
            state["status"] = "processing"
            logger.info(f"[call_llm_render] LLM 渲染成功")
        else:
            state["error_message"] = result.get("error", "渲染失败")
            state["status"] = "failed"
            logger.error(f"[call_llm_render] LLM 渲染失败: {state['error_message']}")

    except Exception as e:
        state["error_message"] = str(e)
        state["status"] = "failed"
        logger.error(f"[call_llm_render] LLM 渲染异常: {e}")

    return state


async def post_process(state: RenderAgentState) -> RenderAgentState:
    logger.info(f"[post_process] 开始结果后处理")

    from app.agent.skills.result_postprocess import postprocess_result

    result_url = state.get("result_image_url", "")
    original_path = state.get("original_image_path", "")

    processed_url = postprocess_result(result_url, original_path)
    state["result_image_url"] = processed_url
    state["progress"] = 90
    logger.info(f"[post_process] 结果后处理完成")
    return state


async def save_result(state: RenderAgentState) -> RenderAgentState:
    logger.info(f"[save_result] 保存结果")

    if state.get("error_message"):
        state["status"] = "failed"
        state["progress"] = 0
    elif state.get("result_image_url"):
        state["status"] = "completed"
        state["progress"] = 100
    else:
        state["status"] = "completed"
        state["progress"] = 100

    logger.info(f"[save_result] 结果保存完成, status={state['status']}")
    return state