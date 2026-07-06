# LLMImageRender - 柜子家具3D模型图片真实渲染平台

基于 Vue3 + FastAPI + LangGraph + Qwen-Image 的在线柜子家具3D渲染平台。

## 功能特性

- **单品渲染**：上传柜子图片，AI 智能生成真实感3D渲染效果图，支持自定义纯色背景
- **场景渲染**：将柜子布置在客厅、卧室、厨房、书房、玄关等典型户型中进行渲染
- **图库管理**：预设柜子图库，每张图片附带柜子属性（宽/深/高/材质/颜色），选择图库图片时自动填充渲染参数；支持分类浏览、正序/倒序排序、图片编辑（改名/改分类/柜子属性）、删除
- **渲染历史**：查看和管理所有渲染任务记录，支持删除记录和再次渲染
- **异步非阻塞渲染**：渲染任务在独立线程池中执行（`asyncio.to_thread`），不阻塞其他 API 请求
- **外部平台对接**：通过 URL 参数传入图片和渲染参数，支持 `image_id`（图库查询）、`image_url`、`image_base64` 三种图片来源

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
│   │   │   ├── render.ts        # 渲染参数状态
│   │   │   ├── task.ts          # 任务列表状态
│   │   │   └── theme.ts         # 主题切换状态（浅色/深色 + URL参数）
│   │   ├── api/                 # API请求封装
│   │   ├── router/              # 路由配置
│   │   ├── styles/              # 全局样式
│   │   │   └── theme.css        # Glassmorphism 主题（Light + Dark Mode）
│   │   ├── utils/               # 工具函数
│   │   │   └── urlParams.ts     # URL 参数解析（外部平台对接）
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
│   ├── render_static/          # 静态文件（图片上传/图库/渲染结果）
│   ├── seed.py                  # 种子数据脚本
│   └── requirements.txt
│
├── SPEC.md                      # 软件规格说明书
├── DEPLOY_UBUNTU.md             # Ubuntu 部署指南
└── README.md                    # 本文件
```

## UI 设计

前端采用 **Glassmorphism + Light/Dark Mode** 风格，支持浅色/深色主题切换、PC / 平板 / 移动端响应式自适应。

### 设计要点

- **双主题模式**：`:root` 为浅色模式（默认），`html.dark` 为深色模式覆盖；顶部导航栏一键切换，刷新后保持上次选择
- **浅色主题**：`#eef2f8` 浅灰蓝背景 + `rgba(248,250,252,0.75)` 玻璃面 + 深色文字（对比度 ≥ 4.5:1）
- **深色主题**：`#0a0a0f` 深色背景 + 动画渐变光球，营造沉浸感
- **玻璃拟态**：`backdrop-filter: blur(16px) saturate(160%~180%)` + 半透明边框 + 悬浮微上浮，卡片浮于背景之上
- **强调色**：靛蓝 `#6366f1` 为主色，紫色 `#8b5cf6` 为辅助
- **字体**：Inter（Google Fonts），配合中文系统字体回退
- **Element Plus 按需加载**：`unplugin-vue-components` 自动导入组件与样式，精简打包体积
- **双模式覆盖**：全组件 CSS 变量覆盖（`html:not(.dark)` / `html.dark`），统一玻璃风格
- **主题持久化**：Pinia store + localStorage 持久化，URL 参数 `?theme=light/dark` 支持外部平台指定主题

### 响应式断点

| 断点 | 适配内容 |
|------|----------|
| PC（1024px+） | 完整布局、双列表单、双列对比图 |
| 平板（768px） | 缩小间距/字体、对比图堆叠、网格调整 |
| 移动端（375-480px） | 汉堡菜单、单列表单、双列网格、三列房间选择器 |

### 无障碍

- `prefers-reduced-motion` 支持，禁用动画
- 所有可交互元素 `cursor-pointer`
- 过渡动画 200-250ms
- 路由链接正确的悬停/激活视觉反馈

### 移动端体验

- 全局 `-webkit-tap-highlight-color: transparent` 去除点击蓝色高亮
- 非文本交互元素（按钮/图片/玻璃卡片/媒体容器）禁用长按选区与系统弹窗，输入框与正文文本选择能力保留
- 修复 Element Plus `el-image` 预览 / 弹窗锁屏导致 body 被收窄左缩的问题（移动端滚动条为 overlay，锁屏的滚动条宽度补偿不正确，已用 `!important` 重置 body 宽度为 100%）

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
uvicorn app.main:app --reload --host 0.0.0.0 --port 8002
```

后端服务启动后：
- API 文档：http://localhost:8002/docs
- 健康检查：http://localhost:8002/render_api/health

### 2. 前端启动

```bash
cd frontend

# 安装依赖
npm install

# 启动开发服务器
npm run dev
```

前端开发服务器启动后：http://localhost:5175/llmimagerender/

### 3. 访问应用

打开浏览器访问 http://localhost:5175/llmimagerender/

## 外部平台对接（URL 参数）

渲染页面支持通过 URL 查询参数（query string）传入所有渲染参数和图片，方便外部平台嵌入跳转。

### 基本用法

```
http://localhost:5175/llmimagerender/render/single?<params>
http://localhost:5175/llmimagerender/render/scene?<params>
```

### 支持的参数

| 参数 | 说明 | 示例 |
|------|------|------|
| `theme` | 主题模式（light / dark），全局生效，便于外部平台指定 | `theme=light` |
| `image_id` | 图库图片 ID（直接查询图库） | `image_id=abc123def456` |
| `image_url` | 图片 URL 地址 | `image_url=https://example.com/cabinet.png` |
| `image_base64` | 图片 Base64（data URI） | `image_base64=data:image/png;base64,iVBOR...` |
| `style` | 渲染风格 | `style=nordic` |
| `lighting` | 光照条件 | `lighting=warm` |
| `view_angle` | 视角 | `view_angle=front_45` |
| `room_type` | 户型（场景渲染） | `room_type=bedroom` |
| `material` | 材质 | `material=oak_wood` |
| `color` | 颜色（支持 # 开头） | `color=#8B7355` |
| `bg_color` | 背景颜色（支持 # 开头） | `bg_color=#FFFFFF` |
| `description` | 额外描述 | `description=modern+style` |
| `width` | 柜子宽度 (mm) | `width=1200` |
| `height` | 柜子高度 (mm) | `height=2200` |
| `depth` | 柜子深度 (mm) | `depth=600` |

> 有传参则使用传入值，无传参则使用默认值。`image_id`、`image_url` 和 `image_base64` 三选一，优先级：`image_id` > `image_url` > `image_base64`。颜色值中的 `#` 无需 URL 编码，代码自动处理。`theme` 参数为全局参数，可附加在任意页面 URL 上。

### 示例

```bash
# 指定浅色主题打开渲染页（外部平台嵌入）
http://localhost:5175/llmimagerender/render/single?theme=light&image_id=abc123def456&style=nordic&lighting=warm

# 单品渲染：通过图库 image_id 传图（查不到则提示）
http://localhost:5175/llmimagerender/render/single?image_id=abc123def456&style=nordic&lighting=warm&material=oak_wood

# 单品渲染：通过 URL 传图 + 自定义风格
http://localhost:5175/llmimagerender/render/single?image_url=https://example.com/cabinet.png&style=nordic&lighting=warm&material=oak_wood
http://localhost:5175/llmimagerender/render/single?image_id=img_e913bf656d45&style=japanese&lighting=warm&view_angle=front_45&material=oak_wood&color=%238B7355&bg_color=%23FFFFFF&description=modern&width=800&height=2000&depth=400

# 场景渲染：通过 base64 传图 + 户型和尺寸
http://localhost:5175/llmimagerender/render/scene?image_base64=data:image/png;base64,...&room_type=bedroom&width=800&height=2000&depth=500
http://localhost:5175/llmimagerender/render/scene?image_url=https://d00.paixin.com/thumbs/1765561/28728719/staff_1024.jpg&style=industrial&lighting=cool&view_angle=top&room_type=study&material=metal&color=%238B7354&description=bright-colored&width=810&height=2010&depth=410
```

## API 端点

| 方法 | 端点 | 说明 |
|------|------|------|
| POST | `/render_api/images/upload` | 上传图片（MD5 去重，支持附带柜子属性） |
| GET | `/render_api/images/gallery` | 获取图库（支持分类筛选、正序/倒序排序 `order=asc\|desc`） |
| GET | `/render_api/images/gallery/:id` | 获取图片详情（含柜子属性） |
| PUT | `/render_api/images/gallery/:id` | 更新图片信息（名称/分类/柜子属性） |
| DELETE | `/render_api/images/gallery/:id` | 删除图片（含物理文件） |
| POST | `/render_api/render/submit` | 提交渲染任务 |
| GET | `/render_api/render/task/:id` | 查询任务状态 |
| DELETE | `/render_api/render/task/:id` | 删除渲染任务 |
| GET | `/render_api/render/history` | 渲染历史 |
| GET | `/render_api/params/presets` | 获取预设参数 |

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
| `DASHSCOPE_MODEL` | DashScope 图片生成模型名称 | `qwen-image-2.0-pro` |
| `DATABASE_URL` | SQLite 数据库路径 | `sqlite:///./llm_image_render.db` |
| `CORS_ORIGINS` | 允许的前端域名 | `http://localhost:5175` |
| `MAX_UPLOAD_SIZE_MB` | 上传文件大小限制 | `10` |
| `UPLOAD_DIR` | 上传图片存储目录 | `render_static/uploads` |
| `GALLERY_DIR` | 图库图片存储目录 | `render_static/gallery` |
| `RESULT_DIR` | 渲染结果存储目录 | `render_static/results` |

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
- `model`: 由 `DASHSCOPE_MODEL` 环境变量配置（默认 "qwen-image-2.0-pro"）
- `size`: 使用星号分隔格式（如 "1024*1024"）
- `messages`: 包含 `image` 和 `text` 对象的数组

## 部署

详见 [Ubuntu 部署指南](DEPLOY_UBUNTU.md)，包含完整的 Nginx 配置、Systemd 服务、SSL 配置等内容。
