# LLMImageRender 项目完成情况记录

> 基于 `SPEC.md` 第8章开发计划实现，最后更新：2026-06-21

---

## 一、总体状态

| 阶段 | 内容 | 预估工时 | 状态 |
|------|------|----------|------|
| **Phase 1** | 项目初始化与基础框架搭建 | 2天 | ✅ 已完成 |
| **Phase 2** | 核心功能开发 | 3天 | ✅ 已完成 |
| **Phase 3** | LangGraph Agent 集成 | 3天 | ✅ 已完成 |
| **Phase 4** | 前端完善与联调 | 2天 | ✅ 已完成 |
| **Phase 5** | 优化与部署 | 2天 | ✅ 已完成 |

**验证结果**：
- 后端服务启动成功（`http://localhost:8000`）
- API 接口 `/api/images/gallery` 返回 200，数据正常
- 前端 TypeScript 类型检查通过（`vue-tsc --noEmit` 无报错）
- 前端生产构建成功（`npm run build` 生成 dist 目录）
- 种子数据初始化成功（3 条图库记录）

---

## 二、Phase 1：项目初始化与基础框架搭建

### 2.1.1 前端 Vue3+Vite 项目初始化

| 文件 | 说明 | 状态 |
|------|------|------|
| [frontend/package.json](file:///e:/AICodeProgram/LLMImageRender/frontend/package.json) | 依赖与脚本（Vue3 + Vite + TS + Element Plus + Pinia） | ✅ |
| [frontend/vite.config.ts](file:///e:/AICodeProgram/LLMImageRender/frontend/vite.config.ts) | Vite 配置（代理 /api → localhost:8000） | ✅ |
| [frontend/tsconfig.json](file:///e:/AICodeProgram/LLMImageRender/frontend/tsconfig.json) | TypeScript 配置 | ✅ |
| [frontend/tsconfig.node.json](file:///e:/AICodeProgram/LLMImageRender/frontend/tsconfig.node.json) | Node 环境 TS 配置 | ✅ |
| [frontend/index.html](file:///e:/AICodeProgram/LLMImageRender/frontend/index.html) | HTML 入口 | ✅ |
| [frontend/src/main.ts](file:///e:/AICodeProgram/LLMImageRender/frontend/src/main.ts) | 应用入口（Pinia + Router + Element Plus） | ✅ |
| [frontend/src/App.vue](file:///e:/AICodeProgram/LLMImageRender/frontend/src/App.vue) | 根组件 | ✅ |
| [frontend/src/env.d.ts](file:///e:/AICodeProgram/LLMImageRender/frontend/src/env.d.ts) | Vue 类型声明 | ✅ |
| [frontend/src/router/index.ts](file:///e:/AICodeProgram/LLMImageRender/frontend/src/router/index.ts) | 路由配置（6条路由） | ✅ |
| [frontend/src/types/index.ts](file:///e:/AICodeProgram/LLMImageRender/frontend/src/types/index.ts) | TypeScript 类型定义 | ✅ |

### 2.1.2 后端 FastAPI 项目初始化

| 文件 | 说明 | 状态 |
|------|------|------|
| [backend/app/main.py](file:///e:/AICodeProgram/LLMImageRender/backend/app/main.py) | FastAPI 入口，CORS、静态文件挂载、路由注册 | ✅ |
| [backend/app/config.py](file:///e:/AICodeProgram/LLMImageRender/backend/app/config.py) | Settings 配置类（环境变量读取） | ✅ |
| [backend/app/database.py](file:///e:/AICodeProgram/LLMImageRender/backend/app/database.py) | SQLAlchemy 引擎、SessionLocal、init_db | ✅ |
| [backend/requirements.txt](file:///e:/AICodeProgram/LLMImageRender/backend/requirements.txt) | Python 依赖清单 | ✅ |
| [backend/.env.example](file:///e:/AICodeProgram/LLMImageRender/backend/.env.example) | 环境变量示例 | ✅ |

### 2.1.3 SQLite 数据库模型定义

| 文件 | 模型 | 说明 | 状态 |
|------|------|------|------|
| [backend/app/models/__init__.py](file:///e:/AICodeProgram/LLMImageRender/backend/app/models/__init__.py) | 模型导出 | ✅ |
| [backend/app/models/task.py](file:///e:/AICodeProgram/LLMImageRender/backend/app/models/task.py) | RenderTask | 渲染任务（task_id、mode、status、progress、图片路径、参数JSON） | ✅ |
| [backend/app/models/chat.py](file:///e:/AICodeProgram/LLMImageRender/backend/app/models/chat.py) | ChatSession / ChatMessage | 对话会话与消息记录 | ✅ |
| [backend/app/models/gallery.py](file:///e:/AICodeProgram/LLMImageRender/backend/app/models/gallery.py) | GalleryImage | 图库图片（分类、路径、缩略图） | ✅ |

### 2.1.4 基础 API 端点实现

| 端点 | 方法 | 说明 | 状态 |
|------|------|------|------|
| `/api/health` | GET | 健康检查 | ✅ |
| `/api/images/gallery` | GET | 获取图库图片列表 | ✅ |
| `/api/render/submit` | POST | 提交渲染任务 | ✅ |
| `/api/render/task/{task_id}` | GET | 查询任务状态 | ✅ |
| `/api/render/history` | GET | 渲染历史记录 | ✅ |

---

## 三、Phase 2：核心功能开发

### 3.2.1 图片上传与管理功能

| 文件 | 说明 | 状态 |
|------|------|------|
| [backend/app/routers/images.py](file:///e:/AICodeProgram/LLMImageRender/backend/app/routers/images.py) | 图片路由：图库列表、图片上传 | ✅ |
| [backend/app/services/file_service.py](file:///e:/AICodeProgram/LLMImageRender/backend/app/services/file_service.py) | 文件存储管理（保存、路径生成） | ✅ |
| [backend/app/utils/image_utils.py](file:///e:/AICodeProgram/LLMImageRender/backend/app/utils/image_utils.py) | 图片工具函数（尺寸获取等） | ✅ |
| [frontend/src/components/ImageUploader.vue](file:///e:/AICodeProgram/LLMImageRender/frontend/src/components/ImageUploader.vue) | 图片上传组件（拖拽+预览） | ✅ |
| [frontend/src/api/gallery.ts](file:///e:/AICodeProgram/LLMImageRender/frontend/src/api/gallery.ts) | 图库 API 封装 | ✅ |

**实现要点**：
- 支持 JPG/PNG/WebP 格式上传
- 拖拽上传与点击上传
- 上传后实时预览
- 图片存储到 `static/uploads/` 目录

### 3.2.2 图库浏览与选择功能

| 文件 | 说明 | 状态 |
|------|------|------|
| [backend/seed.py](file:///e:/AICodeProgram/LLMImageRender/backend/seed.py) | 种子数据脚本（3条图库记录） | ✅ |
| [backend/static/gallery/wardrobe/cabinet-main.png](file:///e:/AICodeProgram/LLMImageRender/backend/static/gallery/wardrobe/cabinet-main.png) | 衣柜图片 | ✅ |
| [backend/static/gallery/kitchen/cabinet-open.png](file:///e:/AICodeProgram/LLMImageRender/backend/static/gallery/kitchen/cabinet-open.png) | 橱柜图片 | ✅ |
| [backend/static/gallery/bookcase/cabinet-side.png](file:///e:/AICodeProgram/LLMImageRender/backend/static/gallery/bookcase/cabinet-side.png) | 书柜图片 | ✅ |
| [frontend/src/pages/GalleryPage.vue](file:///e:/AICodeProgram/LLMImageRender/frontend/src/pages/GalleryPage.vue) | 图库浏览页：分类筛选+网格展示 | ✅ |
| [frontend/src/components/GalleryPicker.vue](file:///e:/AICodeProgram/LLMImageRender/frontend/src/components/GalleryPicker.vue) | 图库选择器组件 | ✅ |

**实现要点**：
- 预设3类柜子图库（衣柜/橱柜/书柜）
- 分类标签筛选
- 缩略图网格布局
- 点击选择柜子图片

### 3.2.3 渲染参数配置面板

| 文件 | 说明 | 状态 |
|------|------|------|
| [backend/app/routers/params.py](file:///e:/AICodeProgram/LLMImageRender/backend/app/routers/params.py) | 参数选项 API（风格/光照/视角/户型） | ✅ |
| [frontend/src/components/ParamPanel.vue](file:///e:/AICodeProgram/LLMImageRender/frontend/src/components/ParamPanel.vue) | 渲染参数配置面板 | ✅ |
| [frontend/src/components/RoomTypeSelector.vue](file:///e:/AICodeProgram/LLMImageRender/frontend/src/components/RoomTypeSelector.vue) | 户型选择器（5种户型） | ✅ |
| [frontend/src/stores/render.ts](file:///e:/AICodeProgram/LLMImageRender/frontend/src/stores/render.ts) | 渲染参数状态管理（Pinia） | ✅ |

**实现要点**：
- 渲染风格：现代简约/北欧/日式/工业风/美式
- 光照条件：自然光/暖光/冷光/混合光
- 视角选择：正面/侧面45°/俯视/自定义
- 柜子材质/颜色覆写
- 自然语言描述输入

### 3.2.4 渲染任务提交与状态查询

| 文件 | 说明 | 状态 |
|------|------|------|
| [backend/app/routers/render.py](file:///e:/AICodeProgram/LLMImageRender/backend/app/routers/render.py) | 渲染路由：提交/查询/结果/历史/删除 | ✅ |
| [backend/app/services/render_service.py](file:///e:/AICodeProgram/LLMImageRender/backend/app/services/render_service.py) | 渲染任务调度与状态管理 | ✅ |
| [frontend/src/components/SubmitBar.vue](file:///e:/AICodeProgram/LLMImageRender/frontend/src/components/SubmitBar.vue) | 提交渲染操作栏 | ✅ |
| [frontend/src/api/render.ts](file:///e:/AICodeProgram/LLMImageRender/frontend/src/api/render.ts) | 渲染 API 封装 | ✅ |
| [frontend/src/stores/task.ts](file:///e:/AICodeProgram/LLMImageRender/frontend/src/stores/task.ts) | 任务列表状态管理 | ✅ |

**API 端点**：

| 端点 | 方法 | 说明 | 状态 |
|------|------|------|------|
| `/api/render/submit` | POST | 提交渲染任务 | ✅ |
| `/api/render/task/{task_id}` | GET | 查询任务状态 | ✅ |
| `/api/render/task/{task_id}/result` | GET | 获取渲染结果 | ✅ |
| `/api/render/history` | GET | 渲染历史记录（分页） | ✅ |
| `/api/render/task/{task_id}` | DELETE | 删除任务 | ✅ |

---

## 四、Phase 3：LangGraph Agent 集成

### 4.3.1 Agent 工作流图构建

| 文件 | 说明 | 状态 |
|------|------|------|
| [backend/app/agent/state.py](file:///e:/AICodeProgram/LLMImageRender/backend/app/agent/state.py) | RenderAgentState 状态定义（TypedDict） | ✅ |
| [backend/app/agent/graph.py](file:///e:/AICodeProgram/LLMImageRender/backend/app/agent/graph.py) | StateGraph 工作流编排（6节点+条件路由+MemorySaver） | ✅ |
| [backend/app/agent/nodes.py](file:///e:/AICodeProgram/LLMImageRender/backend/app/agent/nodes.py) | 6个工作流节点实现 | ✅ |

**工作流节点**：
```
START → parse_input → build_prompt → check_interrupt
                                              │
                            ┌──────────────────┼──────────────────┐
                            ▼                  ▼                  ▼
                     call_llm_render      save_result            END
                            │            （取消时）
                            ▼
                     post_process → save_result → END
```

**条件路由**：
- `check_interrupt` → 取消时走 `save_result`，暂停时走 `END`，正常走 `call_llm_render`
- `call_llm_render` → 出错时走 `save_result`，成功走 `post_process`

### 4.3.2 qwen-image-2.0-pro API 集成

| 文件 | 说明 | 状态 |
|------|------|------|
| [backend/app/agent/llm_client.py](file:///e:/AICodeProgram/LLMImageRender/backend/app/agent/llm_client.py) | DashScope LLM 客户端 | ✅ |

**实现要点**：
- 模型：`qwen-image-2.0-pro`
- API Key：`os.getenv("DASHSCOPE_API_KEY")` 环境变量读取
- 通过 DashScope SDK 调用图片生成接口
- 支持错误处理与重试

### 4.3.3 Skills 模块实现

| 文件 | 技能 | 说明 | 状态 |
|------|------|------|------|
| [skills/image_preprocess.py](file:///e:/AICodeProgram/LLMImageRender/backend/app/agent/skills/image_preprocess.py) | 图片预处理 | 格式转换、尺寸校验 | ✅ |
| [skills/param_optimizer.py](file:///e:/AICodeProgram/LLMImageRender/backend/app/agent/skills/param_optimizer.py) | 参数优化 | 渲染参数校验与补全 | ✅ |
| [skills/prompt_builder.py](file:///e:/AICodeProgram/LLMImageRender/backend/app/agent/skills/prompt_builder.py) | 提示词构建 | 单品渲染提示词、系统提示词 | ✅ |
| [skills/room_template.py](file:///e:/AICodeProgram/LLMImageRender/backend/app/agent/skills/room_template.py) | 户型模板 | 场景渲染提示词（客厅/卧室/厨房/书房/玄关） | ✅ |
| [skills/result_postprocess.py](file:///e:/AICodeProgram/LLMImageRender/backend/app/agent/skills/result_postprocess.py) | 结果后处理 | 图片下载、格式处理 | ✅ |

### 4.3.4 对话管理（停止/继续）

| 文件 | 说明 | 状态 |
|------|------|------|
| [backend/app/routers/chat.py](file:///e:/AICodeProgram/LLMImageRender/backend/app/routers/chat.py) | 对话路由：开启/消息/停止/继续/历史 | ✅ |
| [backend/app/services/chat_service.py](file:///e:/AICodeProgram/LLMImageRender/backend/app/services/chat_service.py) | 对话会话管理、停止/继续控制 | ✅ |
| [frontend/src/api/chat.ts](file:///e:/AICodeProgram/LLMImageRender/frontend/src/api/chat.ts) | 对话 API 封装 | ✅ |

**API 端点**：

| 端点 | 方法 | 说明 | 状态 |
|------|------|------|------|
| `/api/chat/start` | POST | 开启对话会话 | ✅ |
| `/api/chat/message` | POST | 发送对话消息 | ✅ |
| `/api/chat/{session_id}/stop` | POST | 停止对话 | ✅ |
| `/api/chat/{session_id}/continue` | POST | 继续对话 | ✅ |
| `/api/chat/{session_id}/history` | GET | 对话历史 | ✅ |

**实现要点**：
- LangGraph `MemorySaver` 检查点实现上下文持久化
- 支持连续多轮对话
- 停止/继续对话控制
- 对话历史记录持久化到 SQLite

---

## 五、Phase 4：前端完善与联调

### 5.4.1 渲染结果展示（前后对比）

| 文件 | 说明 | 状态 |
|------|------|------|
| [frontend/src/pages/RenderDetailPage.vue](file:///e:/AICodeProgram/LLMImageRender/frontend/src/pages/RenderDetailPage.vue) | 渲染详情页：状态轮询+前后对比+下载 | ✅ |
| [frontend/src/components/ImageCompare.vue](file:///e:/AICodeProgram/LLMImageRender/frontend/src/components/ImageCompare.vue) | 渲染前后对比展示组件 | ✅ |

**实现要点**：
- 轮询任务状态（queued → processing → completed/failed）
- 渲染前后图片并排对比
- 渲染结果下载功能
- 进度条展示

### 5.4.2 对话交互面板

| 文件 | 说明 | 状态 |
|------|------|------|
| [frontend/src/components/ChatPanel.vue](file:///e:/AICodeProgram/LLMImageRender/frontend/src/components/ChatPanel.vue) | AI对话交互面板 | ✅ |

**实现要点**：
- 自然语言调整渲染参数
- 对话消息气泡展示
- 停止/继续对话按钮
- 对话历史加载

### 5.4.3 历史记录页面

| 文件 | 说明 | 状态 |
|------|------|------|
| [frontend/src/pages/HistoryPage.vue](file:///e:/AICodeProgram/LLMImageRender/frontend/src/pages/HistoryPage.vue) | 历史记录页：分页列表 | ✅ |
| [frontend/src/components/TaskCard.vue](file:///e:/AICodeProgram/LLMImageRender/frontend/src/components/TaskCard.vue) | 任务卡片组件 | ✅ |
| [frontend/src/components/TaskStatus.vue](file:///e:/AICodeProgram/LLMImageRender/frontend/src/components/TaskStatus.vue) | 任务状态标签组件 | ✅ |

**实现要点**：
- 分页加载历史任务
- 任务状态标签（排队中/处理中/已完成/失败）
- 点击跳转任务详情
- 任务删除功能

### 5.4.4 前后端联调测试

| 测试项 | 结果 | 状态 |
|--------|------|------|
| 后端服务启动 | `uvicorn` 正常运行在 :8000 | ✅ |
| API `/api/images/gallery` | 返回 200，3条图库数据 | ✅ |
| API `/api/health` | 返回 `{"status":"ok"}` | ✅ |
| 前端 TS 类型检查 | `vue-tsc --noEmit` 无报错 | ✅ |
| 前端生产构建 | `npm run build` 成功，生成 dist | ✅ |
| 种子数据初始化 | `python seed.py` 成功导入3条 | ✅ |
| Vite 开发代理 | `/api` 代理到 localhost:8000 | ✅ |

---

## 六、Phase 5：优化与部署

### 6.5.1 性能优化

| 优化项 | 说明 | 状态 |
|--------|------|------|
| 前端路由懒加载 | 所有页面使用 `() => import()` 动态导入 | ✅ |
| Vite 开发代理 | 配置 `/api` 代理避免跨域 | ✅ |
| 静态文件挂载 | FastAPI StaticFiles 提供 `/static` 访问 | ✅ |
| 构建产物压缩 | Vite 生产构建 gzip 压缩 | ✅ |

### 6.5.2 错误处理完善

| 文件 | 说明 | 状态 |
|------|------|------|
| [backend/app/routers/render.py](file:///e:/AICodeProgram/LLMImageRender/backend/app/routers/render.py) | HTTP 异常处理（400/404） | ✅ |
| [backend/app/routers/chat.py](file:///e:/AICodeProgram/LLMImageRender/backend/app/routers/chat.py) | 会话状态校验（active/paused） | ✅ |
| [backend/app/agent/nodes.py](file:///e:/AICodeProgram/LLMImageRender/backend/app/agent/nodes.py) | LLM 调用错误捕获与状态标记 | ✅ |
| [backend/app/agent/graph.py](file:///e:/AICodeProgram/LLMImageRender/backend/app/agent/graph.py) | 条件路由处理取消/暂停/错误 | ✅ |

### 6.5.3 UI/UX 打磨

| 文件 | 说明 | 状态 |
|------|------|------|
| [frontend/src/pages/HomePage.vue](file:///e:/AICodeProgram/LLMImageRender/frontend/src/pages/HomePage.vue) | 首页：模式选择卡片+近期任务 | ✅ |
| [frontend/src/pages/SingleRenderPage.vue](file:///e:/AICodeProgram/LLMImageRender/frontend/src/pages/SingleRenderPage.vue) | 单品渲染页：上传+参数+提交 | ✅ |
| [frontend/src/pages/SceneRenderPage.vue](file:///e:/AICodeProgram/LLMImageRender/frontend/src/pages/SceneRenderPage.vue) | 场景渲染页：户型选择+参数 | ✅ |
| [frontend/src/components/AppHeader.vue](file:///e:/AICodeProgram/LLMImageRender/frontend/src/components/AppHeader.vue) | 顶部导航栏 | ✅ |
| [frontend/src/components/AppFooter.vue](file:///e:/AICodeProgram/LLMImageRender/frontend/src/components/AppFooter.vue) | 底部信息栏 | ✅ |

**实现要点**：
- Element Plus 组件库统一视觉风格
- 响应式布局适配
- 加载状态与空状态处理
- 操作反馈（消息提示）

### 6.5.4 部署文档

| 文件 | 说明 | 状态 |
|------|------|------|
| [README.md](file:///e:/AICodeProgram/LLMImageRender/README.md) | 项目说明文档（功能/技术栈/结构/启动） | ✅ |
| [backend/.env.example](file:///e:/AICodeProgram/LLMImageRender/backend/.env.example) | 环境变量配置示例 | ✅ |

---

## 七、功能实现对照（SPEC 需求）

### 7.1 模块一：图片管理

| 需求 | 实现情况 | 状态 |
|------|----------|------|
| 用户上传柜子图片 | ImageUploader 组件支持拖拽上传+预览 | ✅ |
| 从柜子列表中选择已有图片 | GalleryPicker 组件，从图库选择 | ✅ |
| 图片格式：JPG/PNG/WebP | 后端 file_service 支持 | ✅ |
| 图库分类浏览 | GalleryPage 支持分类筛选 | ✅ |

### 7.2 模块二：渲染参数配置

| 需求 | 实现情况 | 状态 |
|------|----------|------|
| 渲染模式选择（单品/场景） | 首页模式选择 + 路由分流 | ✅ |
| 户型选择 | RoomTypeSelector 组件（5种户型） | ✅ |
| 渲染风格 | ParamPanel（现代简约/北欧/日式/工业风/美式） | ✅ |
| 光照条件 | ParamPanel（自然光/暖光/冷光/混合光） | ✅ |
| 视角选择 | ParamPanel（正面/侧面45°/俯视/自定义） | ✅ |
| 柜子材质/颜色覆写 | ParamPanel 支持 | ✅ |
| 自然语言描述 | ParamPanel 文本输入框 | ✅ |

### 7.3 模块三：渲染任务管理

| 需求 | 实现情况 | 状态 |
|------|----------|------|
| 提交渲染任务 | POST /api/render/submit | ✅ |
| 任务状态查询 | GET /api/render/task/{id} + 前端轮询 | ✅ |
| 渲染结果展示 | RenderDetailPage + ImageCompare 前后对比 | ✅ |
| 渲染历史记录 | HistoryPage 分页列表 | ✅ |
| 图片下载 | RenderDetailPage 下载按钮 | ✅ |
| 任务状态（排队/处理中/完成/失败） | 后端 status 字段 + TaskStatus 组件 | ✅ |

### 7.4 模块四：AI对话交互

| 需求 | 实现情况 | 状态 |
|------|----------|------|
| 自然语言调整渲染参数 | ChatPanel + /api/chat/message | ✅ |
| 连续多轮对话 | ChatSession + MemorySaver 检查点 | ✅ |
| 停止/继续对话控制 | /api/chat/{id}/stop + /continue | ✅ |
| 对话历史展示 | /api/chat/{id}/history + ChatPanel | ✅ |
| 上下文感知 | LangGraph MemorySaver 持久化 | ✅ |

### 7.5 模块五：柜子图库管理

| 需求 | 实现情况 | 状态 |
|------|----------|------|
| 预设柜子图片列表 | GalleryImage 模型 + 种子数据 | ✅ |
| 柜子分类 | wardrobe / kitchen / bookcase | ✅ |
| 柜子缩略图展示 | GalleryPage 网格布局 | ✅ |

---

## 八、技术栈实现确认

| 层级 | SPEC 要求 | 实际使用 | 状态 |
|------|-----------|----------|------|
| 前端框架 | Vue 3 + Vite | Vue 3.4 + Vite 5.4 | ✅ |
| 前端路由 | Vue Router 4 | Vue Router 4 | ✅ |
| 状态管理 | Pinia | Pinia 2 | ✅ |
| UI 组件库 | Element Plus | Element Plus 2 | ✅ |
| 后端框架 | FastAPI | FastAPI 0.109 | ✅ |
| ASGI 服务器 | Uvicorn | Uvicorn 0.27 | ✅ |
| 数据库 | SQLite | SQLite 3 | ✅ |
| ORM | SQLAlchemy 2 | SQLAlchemy 2.0.25 | ✅ |
| Agent 编排 | LangGraph | LangGraph 0.2+ | ✅ |
| LLM 集成 | LangChain | LangChain 0.2+ | ✅ |
| LLM 模型 | qwen-image-2.0-pro | DashScope SDK 调用 | ✅ |
| API Key | os.getenv("DASHSCOPE_API_KEY") | 环境变量读取 | ✅ |
| 图片处理 | Pillow | Pillow 10.2 | ✅ |

---

## 九、已知问题与后续优化

### 9.1 已知问题

| 编号 | 问题 | 影响 | 优先级 |
|------|------|------|--------|
| 1 | 前端构建产物主 chunk 较大（1.18MB） | 首屏加载稍慢 | 低 |
| 2 | 种子数据仅 3 条，图库内容较少 | 演示效果有限 | 中 |
| 3 | 未配置 DASHSCOPE_API_KEY 时渲染会失败 | 需用户配置环境变量 | 高 |

### 9.2 后续优化建议

- [ ] 配置 `DASHSCOPE_API_KEY` 环境变量后进行端到端渲染测试
- [ ] 增加图库种子数据（更多柜子类型：玄关柜、电视柜）
- [ ] 前端代码分割优化（manualChunks）减小主 chunk 体积
- [ ] 增加 WebSocket 实时推送渲染进度（替代轮询）
- [ ] 增加用户认证与多用户隔离
- [ ] 增加渲染结果图片 CDN 存储支持

---

## 十、启动方式

### 后端

```bash
cd backend
.\venv\Scripts\Activate.ps1
# 配置环境变量
set DASHSCOPE_API_KEY=your_api_key_here
python -m uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
```

### 前端

```bash
cd frontend
npm run dev      # 开发模式
npm run build    # 生产构建
```

### 种子数据初始化

```bash
cd backend
.\venv\Scripts\Activate.ps1
python seed.py
```
