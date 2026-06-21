# 柜子家具3D模型图片真实渲染在线网站 - 软件规格说明书 (SPEC)

## 1. 项目概述

### 1.1 项目名称
**LLMImageRender** - 柜子家具3D模型图片真实渲染平台

### 1.2 项目目标
构建一个在线网站，实现柜子家具3D模型图片的真实感渲染。支持两种渲染模式：
- **单品渲染**：对单个柜子家具模型进行真实渲染
- **场景渲染**：将柜子布置在多个典型户型（如客厅、卧室、厨房等）中进行场景化渲染

### 1.3 核心价值
- 用户无需安装专业3D渲染软件，通过浏览器即可获得高质量渲染结果
- 利用AI Agent（qwen-image-2.0-pro）实现智能渲染，降低使用门槛
- 支持连续对话式交互，用户可通过自然语言调整渲染参数

---

## 2. 软件架构

### 2.1 整体架构图

```
┌──────────────────────────────────────────────────────────────────┐
│                        用户浏览器 (Browser)                        │
│  ┌────────────────────────────────────────────────────────────┐  │
│  │              前端 SPA (Vue3 + Vite)                         │  │
│  │  - 图片上传/选择组件                                         │  │
│  │  - 渲染参数配置面板                                          │  │
│  │  - 渲染前后对比展示                                          │  │
│  │  - 对话交互面板                                              │  │
│  └──────────────────────┬─────────────────────────────────────┘  │
└─────────────────────────┼────────────────────────────────────────┘
                          │ HTTP / WebSocket
                          ▼
┌──────────────────────────────────────────────────────────────────┐
│                    后端服务 (Python + FastAPI)                     │
│  ┌──────────────┐  ┌──────────────────┐  ┌──────────────────┐  │
│  │  API 路由层   │  │  业务逻辑层       │  │  数据访问层       │  │
│  │  - 图片上传   │  │  - 渲染任务管理   │  │  - SQLite CRUD   │  │
│  │  - 渲染提交   │  │  - 对话会话管理   │  │  - 任务状态持久化 │  │
│  │  - 任务查询   │  │  - 文件存储管理   │  │                  │  │
│  └──────────────┘  └────────┬─────────┘  └──────────────────┘  │
│                             │                                    │
│                             ▼                                    │
│  ┌──────────────────────────────────────────────────────────┐   │
│  │              LangGraph Agent 渲染引擎                      │   │
│  │  ┌─────────────────────────────────────────────────────┐ │   │
│  │  │  StateGraph (渲染工作流)                             │ │   │
│  │  │  ┌──────────┐  ┌──────────┐  ┌──────────┐          │ │   │
│  │  │  │ 输入解析  │→│ 提示词构建│→│ LLM渲染  │→ 结果   │ │   │
│  │  │  │ 节点     │  │ 节点     │  │ 节点     │          │ │   │
│  │  │  └──────────┘  └──────────┘  └──────────┘          │ │   │
│  │  └─────────────────────────────────────────────────────┘ │   │
│  │  Skills: 图片预处理 / 户型匹配 / 参数优化 / 结果后处理   │   │
│  └──────────────────────────────────────────────────────────┘   │
│                             │                                    │
│                             ▼                                    │
│  ┌──────────────────────────────────────────────────────────┐   │
│  │          外部 LLM API (qwen-image-2.0-pro)                │   │
│  │          API Key: DASHSCOPE_API_KEY (环境变量)             │   │
│  └──────────────────────────────────────────────────────────┘   │
└──────────────────────────────────────────────────────────────────┘
```

### 2.2 架构分层说明

| 层级 | 职责 | 技术栈 |
|------|------|--------|
| 前端展示层 | 图片上传/选择、渲染参数配置、结果展示、对话交互 | Vue3 + Vite |
| API路由层 | HTTP接口暴露、请求验证、文件上传处理 | FastAPI |
| 业务逻辑层 | 渲染任务调度、对话会话管理、状态机控制 | Python |
| Agent渲染引擎 | LLM调用编排、工作流管理、技能调度 | LangGraph |
| 数据持久层 | 任务记录、对话历史、文件元数据存储 | SQLite |
| 外部服务层 | 图片生成API调用 | DashScope API |

---

## 3. 技术栈

### 3.1 前端

| 技术 | 版本 | 用途 |
|------|------|------|
| Vue 3 | ^3.4 | 响应式UI框架 |
| Vite | ^5.0 | 构建工具与开发服务器 |
| Vue Router | ^4.0 | 前端路由管理 |
| Pinia | ^2.0 | 状态管理 |
| Axios | ^1.6 | HTTP请求客户端 |
| Element Plus | ^2.5 | UI组件库 |
| Pinia Plugin Persist | - | 状态持久化 |

### 3.2 后端

| 技术 | 版本 | 用途 |
|------|------|------|
| Python | ^3.11 | 编程语言 |
| FastAPI | ^0.109 | Web框架 |
| Uvicorn | ^0.27 | ASGI服务器 |
| SQLite | 3 | 嵌入式数据库 |
| SQLAlchemy | ^2.0 | ORM框架 |
| Alembic | ^1.13 | 数据库迁移 |
| LangGraph | ^0.2 | Agent工作流编排 |
| LangChain | ^0.2 | LLM集成组件 |
| DashScope | - | 阿里云模型服务SDK |
| python-multipart | - | 文件上传支持 |
| Pillow | ^10.0 | 图片处理 |

### 3.3 AI模型

| 模型 | 用途 | 调用方式 |
|------|------|----------|
| qwen-image-2.0-pro | 图片真实渲染生成 | DashScope API (环境变量 DASHSCOPE_API_KEY) |

---

## 4. 功能需求

### 4.1 功能模块划分

```
┌───────────────────────────────────────────────────┐
│                 LLMImageRender                    │
├───────────────────────────────────────────────────┤
│ 模块一：图片管理                                   │
│  - 用户上传柜子图片                                │
│  - 从柜子列表中选择已有图片                         │
│  - 图片预览与裁剪                                  │
│  - 图片格式：JPG/PNG/WebP，最大 10MB              │
├───────────────────────────────────────────────────┤
│ 模块二：渲染参数配置                               │
│  - 渲染模式选择（单品渲染 / 场景渲染）               │
│  - 户型选择（客厅、卧室、厨房、书房、玄关）          │
│  - 渲染风格（现代简约、北欧风、日式、工业风、美式）   │
│  - 光照条件（自然光、暖光、冷光、混合光）            │
│  - 视角选择（正面、侧面45°、俯视、自定义角度）      │
│  - 柜子尺寸参数（宽/高/深）                        │
│  - 柜子材质/颜色覆写                              │
│  - 自然语言描述（额外渲染需求）                     │
├───────────────────────────────────────────────────┤
│ 模块三：渲染任务管理                               │
│  - 提交渲染任务                                    │
│  - 任务状态查询（排队中/处理中/已完成/失败）         │
│  - 渲染结果展示（原图 vs 渲染后对比）               │
│  - 渲染历史记录                                    │
│  - 图片下载（渲染结果）                             │
├───────────────────────────────────────────────────┤
│ 模块四：AI对话交互                                 │
│  - 自然语言调整渲染参数                            │
│  - 连续多轮对话                                    │
│  - 停止/继续对话控制                               │
│  - 对话历史展示                                    │
│  - 上下文感知（记住之前的参数选择）                   │
├───────────────────────────────────────────────────┤
│ 模块五：柜子图库管理                               │
│  - 预设柜子图片列表                                │
│  - 柜子分类（衣柜/橱柜/书柜/玄关柜/电视柜）         │
│  - 柜子缩略图展示                                  │
│  - 收藏/常用柜子                                   │
└───────────────────────────────────────────────────┘
```

### 4.2 用户流程

#### 流程A：单品渲染
```
用户进入首页 → 选择"单品渲染"模式
  → 上传柜子图片 或 从图库选择
  → 配置渲染参数（风格/光照/视角/材质）
  → 可选：通过对话微调参数
  → 提交渲染
  → 等待渲染完成（显示进度）
  → 查看渲染前后对比
  → 下载渲染结果
```

#### 流程B：场景渲染
```
用户进入首页 → 选择"场景渲染"模式
  → 上传柜子图片 或 从图库选择
  → 选择目标户型（客厅/卧室/厨房/书房/玄关）
  → 配置渲染参数（风格/光照/视角/材质/尺寸）
  → 可选：通过对话微调参数
  → 提交渲染
  → 等待渲染完成（显示进度）
  → 查看渲染前后对比
  → 下载渲染结果
```

---

## 5. 系统设计

### 5.1 前端路由设计

| 路由 | 页面 | 说明 |
|------|------|------|
| `/` | HomePage | 首页，渲染模式选择入口 |
| `/render/single` | SingleRenderPage | 单品渲染页面 |
| `/render/scene` | SceneRenderPage | 场景渲染页面 |
| `/render/:taskId` | RenderDetailPage | 渲染任务详情与结果 |
| `/history` | HistoryPage | 渲染历史记录 |
| `/gallery` | GalleryPage | 柜子图库浏览 |

### 5.2 前端组件树

```
App.vue
├── AppLayout.vue
│   ├── AppHeader.vue              # 顶部导航栏
│   ├── RouterView
│   │   ├── HomePage.vue
│   │   │   ├── ModeSelector.vue   # 渲染模式选择卡片
│   │   │   └── RecentTasks.vue    # 近期渲染任务
│   │   │
│   │   ├── SingleRenderPage.vue
│   │   │   ├── ImageUploader.vue  # 图片上传/拖拽
│   │   │   ├── GalleryPicker.vue  # 图库选择器
│   │   │   ├── ParamPanel.vue     # 参数配置面板
│   │   │   ├── ChatPanel.vue      # AI对话面板
│   │   │   └── SubmitBar.vue      # 提交按钮栏
│   │   │
│   │   ├── SceneRenderPage.vue
│   │   │   ├── ImageUploader.vue
│   │   │   ├── GalleryPicker.vue
│   │   │   ├── RoomTypeSelector.vue # 户型选择器
│   │   │   ├── ParamPanel.vue
│   │   │   ├── ChatPanel.vue
│   │   │   └── SubmitBar.vue
│   │   │
│   │   ├── RenderDetailPage.vue
│   │   │   ├── TaskStatus.vue     # 任务状态指示
│   │   │   ├── ImageCompare.vue   # 前后对比滑块
│   │   │   └── DownloadButton.vue # 下载按钮
│   │   │
│   │   ├── HistoryPage.vue
│   │   │   ├── TaskFilter.vue     # 筛选条件
│   │   │   └── TaskCardList.vue   # 任务卡片列表
│   │   │
│   │   └── GalleryPage.vue
│   │       ├── CategoryTabs.vue   # 分类标签
│   │       └── ImageGrid.vue      # 图片网格
│   │
│   └── AppFooter.vue              # 底部信息栏
```

### 5.3 前端状态管理 (Pinia)

```typescript
// stores/render.ts - 渲染状态
interface RenderState {
  mode: 'single' | 'scene';           // 渲染模式
  uploadImage: File | null;           // 上传的图片
  selectedImageId: string | null;     // 从图库选择的图片ID
  params: RenderParams;               // 渲染参数
  chatHistory: ChatMessage[];         // 对话历史
  currentTaskId: string | null;       // 当前任务ID
  isChatActive: boolean;              // 对话是否活跃
}

// stores/task.ts - 任务状态
interface TaskState {
  tasks: RenderTask[];                // 任务列表
  currentTask: RenderTask | null;     // 当前查看的任务
}
```

### 5.4 后端API设计

#### 5.4.1 API端点列表

| 方法 | 端点 | 说明 |
|------|------|------|
| `POST` | `/api/images/upload` | 上传柜子图片 |
| `GET` | `/api/images/gallery` | 获取图库列表 |
| `GET` | `/api/images/gallery/:id` | 获取图库图片详情 |
| `POST` | `/api/render/submit` | 提交渲染任务 |
| `GET` | `/api/render/task/:taskId` | 查询任务状态 |
| `GET` | `/api/render/task/:taskId/result` | 获取渲染结果图片 |
| `GET` | `/api/render/history` | 获取渲染历史 |
| `DELETE` | `/api/render/task/:taskId` | 删除渲染任务 |
| `POST` | `/api/chat/start` | 开启对话会话 |
| `POST` | `/api/chat/message` | 发送对话消息 |
| `POST` | `/api/chat/stop` | 停止对话 |
| `POST` | `/api/chat/continue` | 继续对话 |
| `GET` | `/api/chat/:sessionId/history` | 获取对话历史 |
| `GET` | `/api/params/presets` | 获取预设参数模板 |

#### 5.4.2 核心API详情

**POST /api/render/submit**
```json
// Request
{
  "mode": "single",                    // "single" | "scene"
  "image_source": {
    "type": "upload",                  // "upload" | "gallery"
    "image_id": "img_xxx"             // 上传返回的ID 或 图库图片ID
  },
  "params": {
    "style": "modern_minimalist",      // 渲染风格
    "lighting": "natural",             // 光照条件
    "view_angle": "front_45",          // 视角
    "room_type": "living_room",        // 户型（场景模式必填）
    "cabinet_size": {                  // 柜子尺寸（可选）
      "width": 1200,
      "height": 2200,
      "depth": 600
    },
    "material": "oak_wood",            // 材质覆写（可选）
    "color": "#8B7355",               // 颜色覆写（可选）
    "description": "暖色调，柔和光线"    // 自然语言描述（可选）
  }
}

// Response
{
  "code": 200,
  "message": "渲染任务已提交",
  "data": {
    "task_id": "task_20240621_001",
    "status": "queued",
    "created_at": "2024-06-21T10:30:00Z"
  }
}
```

**GET /api/render/task/:taskId**
```json
// Response
{
  "code": 200,
  "data": {
    "task_id": "task_20240621_001",
    "status": "completed",             // "queued" | "processing" | "completed" | "failed"
    "progress": 100,
    "original_image_url": "/static/uploads/img_xxx.png",
    "result_image_url": "/static/results/task_xxx.png",
    "params": { ... },
    "created_at": "2024-06-21T10:30:00Z",
    "completed_at": "2024-06-21T10:31:30Z",
    "error_message": null
  }
}
```

**POST /api/chat/message**
```json
// Request
{
  "session_id": "session_xxx",
  "task_id": "task_xxx",               // 关联的渲染任务
  "message": "把柜子颜色改成深棕色，光照调暗一些"
}

// Response
{
  "code": 200,
  "data": {
    "session_id": "session_xxx",
    "role": "assistant",
    "content": "好的，我将柜子颜色调整为深棕色，并降低光照强度。正在重新渲染...",
    "params_update": {
      "color": "#4A3728",
      "lighting": "warm_dim"
    }
  }
}
```

### 5.5 数据库设计 (SQLite)

```sql
-- 渲染任务表
CREATE TABLE render_tasks (
    id              INTEGER PRIMARY KEY AUTOINCREMENT,
    task_id         VARCHAR(64) NOT NULL UNIQUE,
    mode            VARCHAR(16) NOT NULL,          -- 'single' | 'scene'
    status          VARCHAR(16) NOT NULL DEFAULT 'queued',  -- queued/processing/completed/failed
    progress        INTEGER DEFAULT 0,             -- 0-100
    image_source    VARCHAR(16) NOT NULL,           -- 'upload' | 'gallery'
    original_image  VARCHAR(512) NOT NULL,          -- 原始图片路径
    result_image    VARCHAR(512),                   -- 渲染结果路径
    params_json     TEXT NOT NULL,                  -- 渲染参数JSON
    error_message   TEXT,                           -- 错误信息
    created_at      DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at      DATETIME DEFAULT CURRENT_TIMESTAMP,
    completed_at    DATETIME
);

-- 图库图片表
CREATE TABLE gallery_images (
    id              INTEGER PRIMARY KEY AUTOINCREMENT,
    image_id        VARCHAR(64) NOT NULL UNIQUE,
    name            VARCHAR(128) NOT NULL,
    category        VARCHAR(32) NOT NULL,           -- wardrobe/kitchen/bookcase/entryway/tv_stand
    file_path       VARCHAR(512) NOT NULL,
    thumbnail_path  VARCHAR(512),
    width           INTEGER,
    height          INTEGER,
    file_size       INTEGER,
    created_at      DATETIME DEFAULT CURRENT_TIMESTAMP
);

-- 对话会话表
CREATE TABLE chat_sessions (
    id              INTEGER PRIMARY KEY AUTOINCREMENT,
    session_id      VARCHAR(64) NOT NULL UNIQUE,
    task_id         VARCHAR(64),                    -- 关联的渲染任务
    status          VARCHAR(16) NOT NULL DEFAULT 'active', -- active/paused/closed
    created_at      DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at      DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (task_id) REFERENCES render_tasks(task_id)
);

-- 对话消息表
CREATE TABLE chat_messages (
    id              INTEGER PRIMARY KEY AUTOINCREMENT,
    session_id      VARCHAR(64) NOT NULL,
    role            VARCHAR(16) NOT NULL,           -- 'user' | 'assistant' | 'system'
    content         TEXT NOT NULL,
    params_update   TEXT,                           -- 参数更新JSON
    created_at      DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (session_id) REFERENCES chat_sessions(session_id)
);

-- 渲染参数预设表
CREATE TABLE param_presets (
    id              INTEGER PRIMARY KEY AUTOINCREMENT,
    preset_id       VARCHAR(64) NOT NULL UNIQUE,
    name            VARCHAR(64) NOT NULL,
    mode            VARCHAR(16) NOT NULL,
    params_json     TEXT NOT NULL,
    is_default      INTEGER DEFAULT 0,
    created_at      DATETIME DEFAULT CURRENT_TIMESTAMP
);
```

### 5.6 文件存储结构

```
backend/
├── static/
│   ├── uploads/           # 用户上传的原始图片
│   │   └── YYYY/MM/DD/
│   │       └── {uuid}.png
│   ├── gallery/           # 图库预设图片
│   │   ├── wardrobe/
│   │   ├── kitchen/
│   │   ├── bookcase/
│   │   ├── entryway/
│   │   └── tv_stand/
│   └── results/           # 渲染结果图片
│       └── YYYY/MM/DD/
│           └── {task_id}.png
```

---

## 6. Agent 设计（LangGraph）

### 6.1 LangGraph 工作流图

```
┌──────────────────────────────────────────────────────────────────┐
│                    RenderAgent (StateGraph)                       │
│                                                                  │
│  ┌─────────┐     ┌──────────────┐     ┌───────────────────┐     │
│  │  START   │────▶│ parse_input  │────▶│ build_prompt      │     │
│  └─────────┘     │ 输入解析节点  │     │ 提示词构建节点     │     │
│                  └──────┬───────┘     └────────┬──────────┘     │
│                         │                      │                 │
│                         │              ┌───────▼──────────┐     │
│                         │              │ check_interrupt   │     │
│                         │              │ 中断检查节点       │     │
│                         │              └───────┬──────────┘     │
│                         │                      │                 │
│                         │              ┌───────▼──────────┐     │
│                         │              │ call_llm_render   │     │
│                         │              │ LLM渲染调用节点    │     │
│                         │              └───────┬──────────┘     │
│                         │                      │                 │
│                         │              ┌───────▼──────────┐     │
│                         │              │ post_process      │     │
│                         │              │ 结果后处理节点     │     │
│                         │              └───────┬──────────┘     │
│                         │                      │                 │
│                         │              ┌───────▼──────────┐     │
│                         └──────────────│ save_result       │     │
│                                        │ 结果保存节点       │     │
│                                        └───────┬──────────┘     │
│                                                │                 │
│                                         ┌──────▼──────┐         │
│                                         │    END       │         │
│                                         └─────────────┘         │
│                                                                  │
│  ┌─────────────────────────────────────────────────────────────┐ │
│  │  中断路由 (check_interrupt)                                  │ │
│  │  - 检查 is_paused 状态 → 路由到 END（暂停）                   │ │
│  │  - 检查 is_cancelled 状态 → 路由到 END（取消）                │ │
│  │  - 正常 → 路由到 call_llm_render                             │ │
│  └─────────────────────────────────────────────────────────────┘ │
└──────────────────────────────────────────────────────────────────┘
```

### 6.2 Agent 状态定义

```python
from typing import TypedDict, Optional, Literal
from langgraph.graph import StateGraph, MessagesState

class RenderAgentState(TypedDict):
    # 任务标识
    task_id: str
    session_id: str

    # 输入数据
    mode: Literal["single", "scene"]
    image_source_type: Literal["upload", "gallery"]
    original_image_path: str
    original_image_url: str

    # 渲染参数
    style: str                          # 渲染风格
    lighting: str                       # 光照条件
    view_angle: str                     # 视角
    room_type: Optional[str]            # 户型（场景模式）
    cabinet_size: Optional[dict]        # 柜子尺寸
    material: Optional[str]             # 材质
    color: Optional[str]                # 颜色
    description: Optional[str]          # 自然语言描述

    # 对话消息
    messages: list[dict]                # 对话历史

    # 提示词
    system_prompt: str
    user_prompt: str

    # 渲染结果
    result_image_base64: Optional[str]
    result_image_url: Optional[str]

    # 控制状态
    status: Literal["queued", "processing", "completed", "failed", "paused", "cancelled"]
    is_paused: bool
    is_cancelled: bool
    error_message: Optional[str]
    progress: int                       # 0-100
```

### 6.3 Agent 节点定义

```python
# 节点1：输入解析
def parse_input(state: RenderAgentState) -> RenderAgentState:
    """解析输入图片和参数，进行预处理"""
    # 1. 加载图片，验证格式
    # 2. 图片预处理（缩放、格式转换）
    # 3. 参数验证与默认值填充
    # 4. 从对话消息中提取参数更新
    return state

# 节点2：提示词构建
def build_prompt(state: RenderAgentState) -> RenderAgentState:
    """根据渲染模式和参数构建LLM提示词"""
    # 1. 构建系统提示词（角色设定、渲染规则）
    # 2. 构建用户提示词（包含图片、参数、风格等）
    # 3. 模式特定提示词（单品 vs 场景）
    return state

# 节点3：中断检查
def check_interrupt(state: RenderAgentState) -> RenderAgentState:
    """检查是否需要中断/暂停"""
    # 返回路由条件
    return state

# 节点4：LLM渲染调用
def call_llm_render(state: RenderAgentState) -> RenderAgentState:
    """调用 qwen-image-2.0-pro 进行图片渲染"""
    # 1. 构建API请求
    # 2. 调用 DashScope API
    # 3. 解析响应，获取渲染结果
    return state

# 节点5：结果后处理
def post_process(state: RenderAgentState) -> RenderAgentState:
    """对渲染结果进行后处理"""
    # 1. 图片格式转换
    # 2. 添加水印（可选）
    # 3. 生成缩略图
    return state

# 节点6：结果保存
def save_result(state: RenderAgentState) -> RenderAgentState:
    """保存渲染结果到文件系统和数据库"""
    # 1. 保存图片到 static/results/
    # 2. 更新数据库任务状态
    return state
```

### 6.4 条件路由与中断控制

```python
from langgraph.graph import StateGraph, START, END
from langgraph.checkpoint.memory import MemorySaver

def route_after_check(state: RenderAgentState) -> str:
    """中断检查后的路由"""
    if state.get("is_cancelled"):
        return "save_result"  # 取消后保存当前状态
    if state.get("is_paused"):
        return END            # 暂停，等待恢复
    return "call_llm_render"  # 正常执行

def route_after_llm(state: RenderAgentState) -> str:
    """LLM调用后的路由"""
    if state.get("error_message"):
        return "save_result"  # 错误时保存错误状态
    return "post_process"

# 构建图
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
builder.add_conditional_edges("check_interrupt", route_after_check)
builder.add_conditional_edges("call_llm_render", route_after_llm)
builder.add_edge("post_process", "save_result")
builder.add_edge("save_result", END)

# 编译图（带内存检查点，支持中断恢复）
memory = MemorySaver()
graph = builder.compile(checkpointer=memory)
```

### 6.5 Skills 设计

```
┌─────────────────────────────────────────────────────────┐
│                      Skills 模块                         │
├─────────────────────────────────────────────────────────┤
│                                                         │
│  Skill 1: image_preprocess  - 图片预处理                 │
│    - 图片格式验证与转换（JPG/PNG/WebP → PNG）            │
│    - 图片尺寸调整（最大 2048px）                         │
│    - 图片质量优化                                        │
│    - 生成缩略图                                          │
│                                                         │
│  Skill 2: room_template_match - 户型模板匹配             │
│    - 加载户型参考图（客厅/卧室/厨房/书房/玄关）           │
│    - 计算柜子在户型中的最佳摆放位置                       │
│    - 生成场景合成提示词                                  │
│                                                         │
│  Skill 3: param_optimizer - 参数优化                     │
│    - 根据图片内容自动推荐渲染风格                         │
│    - 根据柜子类型推荐最佳视角                             │
│    - 光照参数智能推荐                                    │
│    - 尺寸比例校验                                        │
│                                                         │
│  Skill 4: prompt_builder - 提示词构建                    │
│    - 单品渲染提示词模板                                   │
│    - 场景渲染提示词模板                                   │
│    - 风格/光照/材质参数映射到自然语言描述                  │
│    - 多轮对话上下文整合                                   │
│                                                         │
│  Skill 5: result_postprocess - 结果后处理                │
│    - 渲染结果质量检查                                    │
│    - 图片对比度/亮度微调                                 │
│    - 生成前后对比图                                      │
│    - 图片格式标准化                                       │
│                                                         │
└─────────────────────────────────────────────────────────┘
```

### 6.6 对话管理

```python
class ConversationManager:
    """对话管理器 - 支持连续对话、停止、继续"""

    def __init__(self):
        self.sessions: dict[str, ConversationSession] = {}
        self.checkpointer = MemorySaver()

    async def start_session(self, task_id: str) -> str:
        """开启新对话会话"""
        session_id = generate_session_id()
        session = ConversationSession(
            session_id=session_id,
            task_id=task_id,
            graph=self._build_graph(),
            status="active"
        )
        self.sessions[session_id] = session
        return session_id

    async def send_message(self, session_id: str, message: str):
        """发送消息，触发Agent处理"""
        session = self.sessions[session_id]
        # 更新状态，注入用户消息
        config = {"configurable": {"thread_id": session_id}}
        result = await session.graph.ainvoke(
            {"messages": [{"role": "user", "content": message}]},
            config
        )
        return result

    async def stop_session(self, session_id: str):
        """停止对话（暂停Agent执行）"""
        session = self.sessions[session_id]
        session.status = "paused"
        # 更新图状态中的 is_paused 标志
        config = {"configurable": {"thread_id": session_id}}
        await session.graph.aupdate_state(
            config,
            {"is_paused": True}
        )

    async def continue_session(self, session_id: str):
        """继续对话（恢复Agent执行）"""
        session = self.sessions[session_id]
        session.status = "active"
        config = {"configurable": {"thread_id": session_id}}
        await session.graph.aupdate_state(
            config,
            {"is_paused": False}
        )
        # 恢复执行
        result = await session.graph.ainvoke(None, config)
        return result
```

---

## 7. 前端页面设计

### 7.1 首页布局

```
┌──────────────────────────────────────────────────────────┐
│  [Logo] LLMImageRender     [图库] [历史]        [设置]   │
├──────────────────────────────────────────────────────────┤
│                                                          │
│         欢迎使用柜子家具3D渲染平台                          │
│         选择渲染模式开始体验                                │
│                                                          │
│  ┌──────────────────┐    ┌──────────────────┐            │
│  │                  │    │                  │            │
│  │   🪑 单品渲染     │    │   🏠 场景渲染     │            │
│  │                  │    │                  │            │
│  │  对单个柜子进行   │    │  将柜子布置在     │            │
│  │  真实感渲染       │    │  典型户型中渲染   │            │
│  │                  │    │                  │            │
│  │   [开始渲染]      │    │   [开始渲染]      │            │
│  └──────────────────┘    └──────────────────┘            │
│                                                          │
│  📋 近期渲染任务                                          │
│  ┌──────────────────────────────────────────────────┐    │
│  │ 衣柜-现代简约  ✅ 已完成  2分钟前                   │    │
│  │ 橱柜-北欧风    🔄 处理中  刚刚                     │    │
│  │ 书柜-日式      ✅ 已完成  1小时前                  │    │
│  └──────────────────────────────────────────────────┘    │
└──────────────────────────────────────────────────────────┘
```

### 7.2 渲染页面布局

```
┌──────────────────────────────────────────────────────────┐
│  ← 返回    单品渲染 / 场景渲染                  [提交渲染] │
├────────────────────────┬─────────────────────────────────┤
│                        │                                 │
│  ┌──────────────────┐  │  渲染参数配置                    │
│  │                  │  │  ┌─────────────────────────┐    │
│  │   上传图片区域    │  │  │ 风格：[现代简约 ▾]      │    │
│  │                  │  │  │ 光照：[自然光 ▾]        │    │
│  │  [点击上传]       │  │  │ 视角：[正面45° ▾]      │    │
│  │  或拖拽到此处     │  │  │ 材质：[橡木 ▾]         │    │
│  │                  │  │  │ 颜色：[■] #8B7355      │    │
│  │  或从图库选择 →   │  │  │ 尺寸：1200x2200x600   │    │
│  └──────────────────┘  │  │ 户型：[客厅 ▾] (场景)   │    │
│                        │  └─────────────────────────┘    │
│  ┌──────────────────┐  │                                 │
│  │  图库预览         │  │  ┌─────────────────────────┐    │
│  │  [衣柜] [橱柜]    │  │  │  🤖 AI对话助手          │    │
│  │  [书柜] [玄关]    │  │  │                         │    │
│  │  [电视柜]         │  │  │  User: 换成暖色光       │    │
│  │  ┌──┐┌──┐┌──┐   │  │  │  AI: 好的，已调整光照   │    │
│  │  │  ││  ││  │   │  │  │  为暖光，正在重新渲染   │    │
│  │  └──┘└──┘└──┘   │  │  │                         │    │
│  │                  │  │  │  [停止对话] [继续对话]    │    │
│  └──────────────────┘  │  └─────────────────────────┘    │
│                        │                                 │
└────────────────────────┴─────────────────────────────────┘
```

### 7.3 渲染结果页布局

```
┌──────────────────────────────────────────────────────────┐
│  ← 返回    渲染结果 - 衣柜_现代简约_20240621_001          │
├──────────────────────────────────────────────────────────┤
│                                                          │
│  ┌──────────────────────────────────────────────────┐    │
│  │              图片对比（滑块拖动）                   │    │
│  │  ┌─────────────────┐    ┌─────────────────┐       │    │
│  │  │   原始图片        │    │   渲染结果        │       │    │
│  │  │                  │    │                  │       │    │
│  │  │   [原始图]       │    │   [渲染图]        │       │    │
│  │  │                  │    │                  │       │    │
│  │  └─────────────────┘    └─────────────────┘       │    │
│  │              ◀───────滑块───────▶                   │    │
│  └──────────────────────────────────────────────────┘    │
│                                                          │
│  渲染参数：                                               │
│  模式：单品渲染 | 风格：现代简约 | 光照：自然光              │
│  视角：正面45° | 材质：橡木 | 颜色：#8B7355                │
│                                                          │
│  [下载渲染图]  [重新渲染]  [分享]                         │
└──────────────────────────────────────────────────────────┘
```

---

## 8. 开发计划

### 8.1 开发阶段

| 阶段 | 内容 | 预估工时 |
|------|------|----------|
| **Phase 1** | 项目初始化与基础框架搭建 | 2天 |
| | - 前端Vue3+Vite项目初始化 | |
| | - 后端FastAPI项目初始化 | |
| | - SQLite数据库模型定义 | |
| | - 基础API端点实现 | |
| **Phase 2** | 核心功能开发 | 3天 |
| | - 图片上传与管理功能 | |
| | - 图库浏览与选择功能 | |
| | - 渲染参数配置面板 | |
| | - 渲染任务提交与状态查询 | |
| **Phase 3** | LangGraph Agent 集成 | 3天 |
| | - Agent工作流图构建 | |
| | - qwen-image-2.0-pro API集成 | |
| | - Skills模块实现 | |
| | - 对话管理（停止/继续） | |
| **Phase 4** | 前端完善与联调 | 2天 |
| | - 渲染结果展示（前后对比） | |
| | - 对话交互面板 | |
| | - 历史记录页面 | |
| | - 前后端联调测试 | |
| **Phase 5** | 优化与部署 | 2天 |
| | - 性能优化 | |
| | - 错误处理完善 | |
| | - UI/UX打磨 | |
| | - 部署文档 | |

### 8.2 项目目录结构

```
LLMImageRender/
├── frontend/                        # 前端项目
│   ├── src/
│   │   ├── components/              # 通用组件
│   │   │   ├── AppHeader.vue
│   │   │   ├── AppFooter.vue
│   │   │   ├── ImageUploader.vue
│   │   │   ├── GalleryPicker.vue
│   │   │   ├── ParamPanel.vue
│   │   │   ├── ChatPanel.vue
│   │   │   ├── ImageCompare.vue
│   │   │   └── TaskCard.vue
│   │   ├── pages/                   # 页面组件
│   │   │   ├── HomePage.vue
│   │   │   ├── SingleRenderPage.vue
│   │   │   ├── SceneRenderPage.vue
│   │   │   ├── RenderDetailPage.vue
│   │   │   ├── HistoryPage.vue
│   │   │   └── GalleryPage.vue
│   │   ├── stores/                  # Pinia状态管理
│   │   │   ├── render.ts
│   │   │   └── task.ts
│   │   ├── api/                     # API请求封装
│   │   │   ├── index.ts
│   │   │   ├── render.ts
│   │   │   ├── chat.ts
│   │   │   └── gallery.ts
│   │   ├── router/                  # 路由配置
│   │   │   └── index.ts
│   │   ├── types/                   # TypeScript类型
│   │   │   └── index.ts
│   │   ├── App.vue
│   │   └── main.ts
│   ├── index.html
│   ├── vite.config.ts
│   ├── package.json
│   └── tsconfig.json
│
├── backend/                         # 后端项目
│   ├── app/
│   │   ├── main.py                  # FastAPI入口
│   │   ├── config.py                # 配置管理
│   │   ├── database.py              # 数据库连接
│   │   ├── models/                  # SQLAlchemy模型
│   │   │   ├── __init__.py
│   │   │   ├── task.py
│   │   │   ├── gallery.py
│   │   │   └── chat.py
│   │   ├── routers/                 # API路由
│   │   │   ├── __init__.py
│   │   │   ├── images.py
│   │   │   ├── render.py
│   │   │   ├── chat.py
│   │   │   └── params.py
│   │   ├── services/                # 业务逻辑
│   │   │   ├── __init__.py
│   │   │   ├── render_service.py
│   │   │   ├── chat_service.py
│   │   │   └── file_service.py
│   │   ├── agent/                   # LangGraph Agent
│   │   │   ├── __init__.py
│   │   │   ├── graph.py             # 工作流图定义
│   │   │   ├── state.py             # 状态定义
│   │   │   ├── nodes.py             # 节点实现
│   │   │   ├── skills/              # Skills模块
│   │   │   │   ├── __init__.py
│   │   │   │   ├── image_preprocess.py
│   │   │   │   ├── room_template.py
│   │   │   │   ├── param_optimizer.py
│   │   │   │   ├── prompt_builder.py
│   │   │   │   └── result_postprocess.py
│   │   │   └── llm_client.py        # LLM API客户端
│   │   └── utils/                   # 工具函数
│   │       ├── __init__.py
│   │       └── image_utils.py
│   ├── static/                      # 静态文件
│   │   ├── uploads/
│   │   ├── gallery/
│   │   └── results/
│   ├── requirements.txt
│   └── .env.example
│
├── images/                          # 文档/设计用图片
│   ├── cabinet-main.png
│   ├── cabinet-open.png
│   └── cabinet-side.png
│
├── SPEC.md                          # 本规格说明书
└── README.md                        # 项目说明文档
```

---

## 9. 关键设计决策

### 9.1 为什么使用 LangGraph 而非简单的 API 调用？

| 考量 | 简单API调用 | LangGraph |
|------|-------------|-----------|
| 工作流编排 | 手动编码 | 声明式图定义 |
| 状态管理 | 自行维护 | 内置持久化状态 |
| 中断/恢复 | 难以实现 | 原生支持 Human-in-the-loop |
| 多轮对话 | 需自行管理上下文 | 内置 MemorySaver 检查点 |
| 可观测性 | 需自行埋点 | 集成 LangSmith 追踪 |
| 扩展性 | 代码耦合 | 模块化节点，易扩展 |

### 9.2 为什么使用 SQLite？

- 项目初期数据量小，SQLite 足够应对
- 零配置，无需独立数据库服务
- 方便开发和部署
- 后期可无缝迁移至 PostgreSQL

### 9.3 安全保障

- API Key 通过环境变量 `DASHSCOPE_API_KEY` 读取，不硬编码
- 上传文件类型校验（仅允许图片格式）
- 文件大小限制（最大 10MB）
- 请求频率限制（防止滥用）
- CORS 配置（仅允许前端域名）

---

## 10. 非功能性需求

| 需求 | 指标 |
|------|------|
| 性能 | 页面首屏加载 < 3s，API响应 < 500ms |
| 可用性 | 系统可用性 > 99% |
| 安全性 | 文件上传校验，API Key 保护 |
| 可维护性 | 代码模块化，符合 PEP8/ESLint 规范 |
| 兼容性 | 支持 Chrome/Firefox/Edge 最新版本 |
| 响应式 | 支持桌面端（1920px）和移动端（375px） |

---

*文档版本: v1.0 | 创建日期: 2024-06-21*