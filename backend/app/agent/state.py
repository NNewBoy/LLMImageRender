from typing import TypedDict, Optional, Literal, Any


class RenderAgentState(TypedDict, total=False):
    task_id: str
    session_id: str

    mode: Literal["single", "scene"]
    original_image_path: str
    original_image_url: str

    style: str
    lighting: str
    view_angle: str
    room_type: Optional[str]
    cabinet_size: Optional[dict]
    material: Optional[str]
    color: Optional[str]
    background_color: Optional[str]
    description: Optional[str]

    messages: list[dict]

    system_prompt: str
    user_prompt: str

    result_image_base64: Optional[str]
    result_image_url: Optional[str]
    thumbnail_url: Optional[str]

    status: str
    is_paused: bool
    is_cancelled: bool
    error_message: Optional[str]
    progress: int