import logging
from langgraph.graph import StateGraph, START, END
from langgraph.checkpoint.memory import MemorySaver

from app.agent.state import RenderAgentState
from app.agent.nodes import (
    parse_input, build_prompt, check_interrupt,
    call_llm_render, post_process, save_result,
)

logger = logging.getLogger(__name__)


def route_after_check(state: RenderAgentState) -> str:
    if state.get("is_cancelled"):
        logger.info("路由: 任务已取消 -> save_result")
        return "save_result"
    if state.get("is_paused"):
        logger.info("路由: 任务已暂停 -> END")
        return END
    return "call_llm_render"


def route_after_llm(state: RenderAgentState) -> str:
    if state.get("error_message"):
        logger.info("路由: LLM出错 -> save_result")
        return "save_result"
    return "post_process"


def build_render_graph():
    builder = StateGraph(RenderAgentState)

    builder.add_node("parse_input", parse_input)
    builder.add_node("build_prompt", build_prompt)
    builder.add_node("check_interrupt", check_interrupt)
    builder.add_node("call_llm_render", call_llm_render)
    builder.add_node("post_process", post_process)
    builder.add_node("save_result", save_result)

    builder.add_edge(START, "parse_input")
    builder.add_edge("parse_input", "build_prompt")
    builder.add_edge("build_prompt", "check_interrupt")
    builder.add_conditional_edges("check_interrupt", route_after_check, {
        "call_llm_render": "call_llm_render",
        "save_result": "save_result",
        END: END,
    })
    builder.add_conditional_edges("call_llm_render", route_after_llm, {
        "post_process": "post_process",
        "save_result": "save_result",
    })
    builder.add_edge("post_process", "save_result")
    builder.add_edge("save_result", END)

    memory = MemorySaver()
    graph = builder.compile(checkpointer=memory)
    logger.info("LangGraph 渲染工作流已编译")
    return graph


_render_graph = None


def get_render_graph():
    global _render_graph
    if _render_graph is None:
        _render_graph = build_render_graph()
    return _render_graph


async def run_render_agent(
    task_id: str,
    mode: str,
    original_image_path: str,
    params: dict,
) -> dict:
    graph = get_render_graph()

    initial_state: RenderAgentState = {
        "task_id": task_id,
        "session_id": task_id,
        "mode": mode,
        "original_image_path": original_image_path,
        "original_image_url": original_image_path,
        "style": params.get("style", "modern_minimalist"),
        "lighting": params.get("lighting", "natural"),
        "view_angle": params.get("view_angle", "front_45"),
        "room_type": params.get("room_type"),
        "cabinet_size": params.get("cabinet_size"),
        "material": params.get("material"),
        "color": params.get("color"),
        "description": params.get("description", ""),
        "messages": [],
        "system_prompt": "",
        "user_prompt": "",
        "result_image_base64": None,
        "result_image_url": None,
        "status": "queued",
        "is_paused": False,
        "is_cancelled": False,
        "error_message": None,
        "progress": 0,
    }

    config = {"configurable": {"thread_id": task_id}}

    try:
        final_state = await graph.ainvoke(initial_state, config)
        return {
            "success": final_state.get("status") == "completed",
            "result_image_url": final_state.get("result_image_url", ""),
            "error": final_state.get("error_message"),
            "status": final_state.get("status", "failed"),
        }
    except Exception as e:
        logger.error(f"渲染 Agent 执行失败: {e}")
        return {
            "success": False,
            "error": str(e),
            "status": "failed",
        }


async def run_chat_agent(
    session_id: str,
    task_id: str,
    messages: list[dict],
    user_message: str,
) -> dict:
    from app.agent.skills.prompt_builder import build_chat_response

    from app.database import SessionLocal
    from app.models.task import RenderTask
    import json

    db = SessionLocal()
    try:
        task = db.query(RenderTask).filter(RenderTask.task_id == task_id).first()
        params = {}
        if task and task.params_json:
            params = json.loads(task.params_json)
    finally:
        db.close()

    content, params_update = build_chat_response(user_message, params)

    try:
        llm_result = await llm_client.chat(
            messages=messages,
            system_prompt="你是家具渲染助手，帮助用户调整渲染参数。",
        )
        if llm_result.get("success") and llm_result.get("content"):
            content = llm_result["content"]
    except Exception:
        pass

    return {
        "content": content,
        "params_update": params_update,
    }


from app.agent.llm_client import llm_client