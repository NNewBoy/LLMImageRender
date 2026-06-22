# LLMImageRender - 柜子家具3D模型图片真实渲染平台

基于 Vue3 + FastAPI + LangGraph + Qwen-Image 的在线柜子家具3D渲染平台。

## 功能特性

- **单品渲染**：上传柜子图片，AI 智能生成真实感3D渲染效果图
- **场景渲染**：将柜子布置在客厅、卧室、厨房、书房、玄关等典型户型中进行渲染
- **图库管理**：预设柜子图库，支持分类浏览和选择
- **渲染历史**：查看和管理所有渲染任务记录

## 技术栈

| 层级 | 技术 |
|------|------|
| 前端 | Vue 3 + Vite + TypeScript + Element Plus + Pinia |
| 后端 | Python + FastAPI + SQLite + SQLAlchemy |
| AI引擎 | LangGraph + Qwen-Image-2.0-Pro (DashScope MultiModalConversation API) |

## 项目结构

```
LLMImageRender/
├── frontend/                    # 前端项目
│   ├── src/
│   │   ├── components/          # 通用组件
│   │   │   ├── AppHeader.vue    # 顶部导航
│   │   │   ├── ImageUploader.vue # 图片上传组件
│   │   │   ├── GalleryPicker.vue # 图库选择器
│   │   │   ├── ParamPanel.vue   # 参数配置面板
│   │   │   ├── ImageCompare.vue # 前后对比组件
│   │   │   ├── SubmitBar.vue    # 提交按钮栏
│   │   │   ├── TaskCard.vue     # 任务卡片
│   │   │   ├── TaskStatus.vue   # 任务状态
│   │   │   └── RoomTypeSelector.vue # 户型选择器
│   │   ├── pages/               # 页面组件
│   │   │   ├── HomePage.vue
│   │   │   ├── SingleRenderPage.vue
│   │   │   ├── SceneRenderPage.vue
│   │   │   ├── RenderDetailPage.vue
│   │   │   ├── HistoryPage.vue
│   │   │   └── GalleryPage.vue
│   │   ├── stores/              # Pinia状态管理
│   │   ├── api/                 # API请求封装
│   │   ├── router/              # 路由配置
│   │   └── types/               # TypeScript类型
│   ├── package.json
│   └── vite.config.ts
│
├── backend/                     # 后端项目
│   ├── app/
│   │   ├── main.py              # FastAPI入口（日志配置）
│   │   ├── config.py            # 配置管理
│   │   ├── database.py          # 数据库连接
│   │   ├── models/              # 数据模型
│   │   │   ├── task.py          # 渲染任务
│   │   │   └── gallery.py       # 图库图片
│   │   ├── routers/             # API路由
│   │   │   ├── images.py        # 图片上传/图库
│   │   │   ├── render.py        # 渲染任务
│   │   │   └── params.py        # 预设参数
│   │   ├── services/            # 业务逻辑
│   │   │   ├── render_service.py
│   │   │   └── file_service.py
│   │   ├── agent/               # LangGraph Agent
│   │   │   ├── graph.py         # 工作流图定义
│   │   │   ├── state.py         # 状态定义
│   │   │   ├── nodes.py         # 节点实现
│   │   │   ├── llm_client.py    # LLM API客户端
│   │   │   └── skills/          # 技能模块
│   │   │       ├── image_preprocess.py
│   │   │       ├── room_template.py
│   │   │       ├── param_optimizer.py
│   │   │       ├── prompt_builder.py
│   │   │       └── result_postprocess.py
│   │   └── utils/               # 工具函数
│   ├── static/                  # 静态文件
│   ├── seed.py                  # 种子数据脚本
│   └── requirements.txt
│
├── SPEC.md                      # 软件规格说明书
└── README.md                    # 本文件
```

## 快速开始

### 环境要求

- Python >= 3.11
- Node.js >= 18
- DashScope API Key (用于调用 qwen-image-2.0-pro)

### 1. 后端启动

```bash
cd backend

# 创建虚拟环境
python -m venv venv

# 激活虚拟环境
# Windows:
venv\Scripts\activate
# Linux/Mac:
source venv/bin/activate

# 安装依赖
pip install -r requirements.txt

# 配置环境变量
cp .env.example .env
# 编辑 .env 文件，填入你的 DASHSCOPE_API_KEY

# 初始化种子数据
python seed.py

# 启动服务
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

后端服务启动后：
- API 文档：http://localhost:8000/docs
- 健康检查：http://localhost:8000/api/health

### 2. 前端启动

```bash
cd frontend

# 安装依赖
npm install

# 启动开发服务器
npm run dev
```

前端开发服务器启动后：http://localhost:5173

### 3. 访问应用

打开浏览器访问 http://localhost:5173

## API 端点

| 方法 | 端点 | 说明 |
|------|------|------|
| POST | `/api/images/upload` | 上传图片 |
| GET | `/api/images/gallery` | 获取图库 |
| POST | `/api/render/submit` | 提交渲染任务 |
| GET | `/api/render/task/:id` | 查询任务状态 |
| GET | `/api/render/history` | 渲染历史 |
| GET | `/api/params/presets` | 获取预设参数 |

## LangGraph Agent 工作流

```
START → parse_input → build_prompt → check_interrupt
                                           ↓
                          ┌─────────────────┴──────────────────┐
                          ↓ (正常)          ↓ (暂停)      ↓ (取消)
                     call_llm_render        END        save_result
                          ↓
                     post_process → save_result → END
```

- **中断/恢复**：通过 `MemorySaver` 检查点机制实现
- **停止任务**：设置 `is_cancelled=True`，路由到 save_result
- **暂停任务**：设置 `is_paused=True`，路由到 END

## 环境变量

| 变量 | 说明 | 默认值 |
|------|------|--------|
| `DASHSCOPE_API_KEY` | 阿里云 DashScope API Key | - |
| `DATABASE_URL` | SQLite 数据库路径 | `sqlite:///./llm_image_render.db` |
| `CORS_ORIGINS` | 允许的前端域名 | `http://localhost:5173` |
| `MAX_UPLOAD_SIZE_MB` | 上传文件大小限制 | `10` |

## 日志系统

后端已集成完整的日志系统，覆盖所有关键节点：

### 日志格式
```
2026-06-22 14:30:00 - app.routers.render - INFO - [渲染任务提交] mode=single, image_source={...}
```

### 日志覆盖范围

| 模块 | 日志标签 | 说明 |
|------|----------|------|
| main.py | `[应用启动]` | 应用初始化、配置信息、数据库初始化 |
| render.py | `[渲染任务提交]` / `[查询任务状态]` / `[获取任务结果]` | 渲染任务全流程 |
| images.py | `[图片上传]` / `[获取图片列表]` / `[获取图片详情]` | 图片管理操作 |
| render_service.py | `[渲染服务]` / `[渲染执行]` | 渲染任务调度与执行 |
| llm_client.py | `[LLM客户端]` / `[LLM图片生成]` | LLM API 调用详情 |

### 日志级别

- **INFO**：正常业务流程
- **WARNING**：非关键异常（如图片不存在）
- **ERROR**：关键错误（如 API 调用失败、任务执行异常）

## LLM API 集成说明

### qwen-image-2.0-pro 图片生成

使用 DashScope `MultiModalConversation` API（而非旧版 `ImageSynthesis`），支持：
- Base64 数据 URI 格式的参考图片
- 多模态消息内容（图片 + 文本）
- 标准 `content` 数组格式

**关键参数**：
- `model`: "qwen-image-2.0-pro"
- `size`: 使用星号分隔格式（如 "1024*1024"）
- `messages`: 包含 `image` 和 `text` 对象的数组