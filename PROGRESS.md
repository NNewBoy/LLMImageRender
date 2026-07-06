# LLMImageRender 项目完成情况记录

> 基于 `SPEC.md` 第8章开发计划实现，最后更新：2026-07-06（Phase 22）

---

## 一、总体状态

| 阶段 | 内容 | 预估工时 | 状态 |
|------|------|----------|------|
| **Phase 1** | 项目初始化与基础框架搭建 | 2天 | ✅ 已完成 |
| **Phase 2** | 核心功能开发 | 3天 | ✅ 已完成 |
| **Phase 3** | LangGraph Agent 集成 | 3天 | ✅ 已完成 |
| **Phase 4** | 前端完善与联调 | 2天 | ✅ 已完成 |
| **Phase 5** | 优化与部署 | 2天 | ✅ 已完成 |
| **Phase 6** | API 修复与日志系统 | - | ✅ 已完成 |
| **Phase 7** | 移除 AI 对话功能 | - | ✅ 已完成 |
| **Phase 8** | 移除底部信息栏组件 | - | ✅ 已完成 |
| **Phase 9** | 单品渲染纯色背景功能 | - | ✅ 已完成 |
| **Phase 10** | UI 重构：Glassmorphism + Dark Mode 响应式布局 | - | ✅ 已完成 |
| **Phase 11** | 外部平台对接：URL 参数传入渲染参数与图片 | - | ✅ 已完成 |
| **Phase 12** | 图片上传去重 + URL 参数 # 修复 + ParamPanel 同步修复 | - | ✅ 已完成 |
| **Phase 13** | 外部平台对接 image_id + 图库"其他"分类 + 上传默认分类 | - | ✅ 已完成 |
| **Phase 14** | 渲染详情页删除/再次渲染 + 后端 image_id 存储 | - | ✅ 已完成 |
| **Phase 15** | 图库图片管理（删除/改名/改分类） | - | ✅ 已完成 |
| **Phase 16** | UI 重构：GalleryPage + RenderDetailPage Glassmorphism 增强 + 弹窗样式 | - | ✅ 已完成 |
| **Phase 17** | RenderDetailPage 移动端响应式布局 | - | ✅ 已完成 |
| **Phase 18** | API 路由重构 `/api`→`/render_api`、`/static`→`/render_static` + 模型环境变量配置 + Ubuntu 部署文档 | - | ✅ 已完成 |
| **Phase 19** | 图库图片柜子属性（宽/深/高/材质/颜色）+ 选择图库自动填充参数 + 新增材质提示词 | - | ✅ 已完成 |
| **Phase 20** | 时区修复（UTC→东八区）+ 渲染任务异步阻塞修复（asyncio.to_thread） | - | ✅ 已完成 |
| **Phase 21** | UI 主题切换：Glassmorphism + Light Mode 新增 + 顶栏切换 + URL 参数控制主题 | - | ✅ 已完成 |
| **Phase 22** | 主题兼容修复 + 移动端 UX 修复 + LLM 图片本地持久化 | - | ✅ 已完成 |
| **Phase 23** | Element Plus 按需加载 + UI 交互优化 + 图库排序 + 毛玻璃样式精调 | - | ✅ 已完成 |

**验证结果**：
- 后端服务启动成功（`http://localhost:8002`）
- API 接口 `/render_api/images/gallery` 返回 200，数据正常
- 前端 TypeScript 类型检查通过（`vue-tsc --noEmit` 无报错）
- 前端生产构建成功（`npm run build` 生成 dist 目录）
- 种子数据初始化成功（3 条图库记录）
- LLM API 调用正常（使用 MultiModalConversation 接口）

---

## 二、Phase 1：项目初始化与基础框架搭建

### 2.1.1 前端 Vue3+Vite 项目初始化

| 文件 | 说明 | 状态 |
|------|------|------|
| [frontend/package.json](file:///e:/AICodeProgram/LLMImageRender/frontend/package.json) | 依赖与脚本（Vue3 + Vite + TS + Element Plus + Pinia） | ✅ |
| [frontend/vite.config.ts](file:///e:/AICodeProgram/LLMImageRender/frontend/vite.config.ts) | Vite 配置（代理 /api → localhost:8002，base /llmimagerender/） | ✅ |
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
| [backend/app/models/gallery.py](file:///e:/AICodeProgram/LLMImageRender/backend/app/models/gallery.py) | GalleryImage | 图库图片（分类、路径、缩略图、柜子属性：宽/深/高/材质/颜色） | ✅ |

### 2.1.4 基础 API 端点实现

| 端点 | 方法 | 说明 | 状态 |
|------|------|------|------|
| `/render_api/health` | GET | 健康检查 | ✅ |
| `/render_api/images/gallery` | GET | 获取图库图片列表 | ✅ |
| `/render_api/render/submit` | POST | 提交渲染任务 | ✅ |
| `/render_api/render/task/{task_id}` | GET | 查询任务状态 | ✅ |
| `/render_api/render/history` | GET | 渲染历史记录 | ✅ |

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
| [backend/render_static/gallery/wardrobe/cabinet-main.png](file:///e:/AICodeProgram/LLMImageRender/backend/render_static/gallery/wardrobe/cabinet-main.png) | 衣柜图片 | ✅ |
| [backend/render_static/gallery/kitchen/cabinet-open.png](file:///e:/AICodeProgram/LLMImageRender/backend/render_static/gallery/kitchen/cabinet-open.png) | 橱柜图片 | ✅ |
| [backend/render_static/gallery/bookcase/cabinet-side.png](file:///e:/AICodeProgram/LLMImageRender/backend/render_static/gallery/bookcase/cabinet-side.png) | 书柜图片 | ✅ |
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
| `/render_api/render/submit` | POST | 提交渲染任务 | ✅ |
| `/render_api/render/task/{task_id}` | GET | 查询任务状态 | ✅ |
| `/render_api/render/task/{task_id}/result` | GET | 获取渲染结果 | ✅ |
| `/render_api/render/history` | GET | 渲染历史记录（分页） | ✅ |
| `/render_api/render/task/{task_id}` | DELETE | 删除任务 | ✅ |

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
- 使用 `MultiModalConversation` API（支持 Base64 数据 URI 格式参考图片）
- 请求格式：`messages` + `content` 数组（包含 `image` 和 `text` 对象）
- 响应解析：`output.choices[0].message.content` 中提取 `image` URL
- 支持错误处理与重试

### 4.3.3 Skills 模块实现

| 文件 | 技能 | 说明 | 状态 |
|------|------|------|------|
| [skills/image_preprocess.py](file:///e:/AICodeProgram/LLMImageRender/backend/app/agent/skills/image_preprocess.py) | 图片预处理 | 格式转换、尺寸校验 | ✅ |
| [skills/param_optimizer.py](file:///e:/AICodeProgram/LLMImageRender/backend/app/agent/skills/param_optimizer.py) | 参数优化 | 渲染参数校验与补全 | ✅ |
| [skills/prompt_builder.py](file:///e:/AICodeProgram/LLMImageRender/backend/app/agent/skills/prompt_builder.py) | 提示词构建 | 单品渲染提示词、系统提示词 | ✅ |
| [skills/room_template.py](file:///e:/AICodeProgram/LLMImageRender/backend/app/agent/skills/room_template.py) | 户型模板 | 场景渲染提示词（客厅/卧室/厨房/书房/玄关） | ✅ |
| [skills/result_postprocess.py](file:///e:/AICodeProgram/LLMImageRender/backend/app/agent/skills/result_postprocess.py) | 结果后处理 | 图片下载、格式处理 | ✅ |

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

### 5.4.2 历史记录页面

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

### 5.4.3 前后端联调测试

| 测试项 | 结果 | 状态 |
|--------|------|------|
| 后端服务启动 | `uvicorn` 正常运行在 :8002 | ✅ |
| API `/render_api/images/gallery` | 返回 200，3条图库数据 | ✅ |
| API `/render_api/health` | 返回 `{"status":"ok"}` | ✅ |
| 前端 TS 类型检查 | `vue-tsc --noEmit` 无报错 | ✅ |
| 前端生产构建 | `npm run build` 成功，生成 dist | ✅ |
| 种子数据初始化 | `python seed.py` 成功导入3条 | ✅ |
| Vite 开发代理 | `/render_api` 和 `/render_static` 代理到 localhost:8002 | ✅ |

---

## 六、Phase 5：优化与部署

### 6.5.1 性能优化

| 优化项 | 说明 | 状态 |
|--------|------|------|
| 前端路由懒加载 | 所有页面使用 `() => import()` 动态导入 | ✅ |
| Vite 开发代理 | 配置 `/render_api` 和 `/render_static` 代理避免跨域 | ✅ |
| 静态文件挂载 | FastAPI StaticFiles 提供 `/render_static` 访问 | ✅ |
| 构建产物压缩 | Vite 生产构建 gzip 压缩 | ✅ |

### 6.5.2 错误处理完善

| 文件 | 说明 | 状态 |
|------|------|------|
| [backend/app/routers/render.py](file:///e:/AICodeProgram/LLMImageRender/backend/app/routers/render.py) | HTTP 异常处理（400/404） | ✅ |
| [backend/app/agent/nodes.py](file:///e:/AICodeProgram/LLMImageRender/backend/app/agent/nodes.py) | LLM 调用错误捕获与状态标记 | ✅ |
| [backend/app/agent/graph.py](file:///e:/AICodeProgram/LLMImageRender/backend/app/agent/graph.py) | 条件路由处理取消/暂停/错误 | ✅ |

### 6.5.3 UI/UX 打磨

| 文件 | 说明 | 状态 |
|------|------|------|
| [frontend/src/pages/HomePage.vue](file:///e:/AICodeProgram/LLMImageRender/frontend/src/pages/HomePage.vue) | 首页：模式选择卡片+近期任务 | ✅ |
| [frontend/src/pages/SingleRenderPage.vue](file:///e:/AICodeProgram/LLMImageRender/frontend/src/pages/SingleRenderPage.vue) | 单品渲染页：上传+参数+提交 | ✅ |
| [frontend/src/pages/SceneRenderPage.vue](file:///e:/AICodeProgram/LLMImageRender/frontend/src/pages/SceneRenderPage.vue) | 场景渲染页：户型选择+参数 | ✅ |
| [frontend/src/components/AppHeader.vue](file:///e:/AICodeProgram/LLMImageRender/frontend/src/components/AppHeader.vue) | 顶部导航栏 | ✅ |

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

## 七、Phase 6：API 修复与日志系统（2026-06-22 新增）

### 7.6.1 LLM API 问题修复

**问题描述**：
- 原代码使用 `ImageSynthesis.call()`（旧版万相文生图 API）
- `ref_images` 参数只接受公网 URL，不接受 Base64 数据 URI
- 导致报错：`url error, please check url!`

**修复方案**：
- 改用 `MultiModalConversation.call()` API
- 使用 `messages` + `content` 数组格式
- 图片使用 `{"image": "data:image/png;base64,..."}` 格式
- 文本使用 `{"text": prompt}` 格式
- 响应解析改为 `output.choices[0].message.content` 结构

**修改文件**：
- [backend/app/agent/llm_client.py](file:///e:/AICodeProgram/LLMImageRender/backend/app/agent/llm_client.py) - LLM 客户端核心逻辑

### 7.6.2 后端日志系统集成

**日志配置**：
- 统一日志格式：`%(asctime)s - %(name)s - %(levelname)s - %(message)s`
- 日志级别：INFO / WARNING / ERROR
- 在 main.py 中配置 `logging.basicConfig`

**日志覆盖模块**：

| 模块 | 日志标签 | 说明 |
|------|----------|------|
| [main.py](file:///e:/AICodeProgram/LLMImageRender/backend/app/main.py) | `[应用启动]` | 应用初始化、配置信息、数据库初始化 |
| [render.py](file:///e:/AICodeProgram/LLMImageRender/backend/app/routers/render.py) | `[渲染任务提交]` / `[查询任务状态]` / `[获取任务结果]` / `[获取渲染历史]` / `[删除任务]` | 渲染任务全流程 |
| [images.py](file:///e:/AICodeProgram/LLMImageRender/backend/app/routers/images.py) | `[图片上传]` / `[获取图片列表]` / `[获取图片详情]` | 图片管理操作 |
| [render_service.py](file:///e:/AICodeProgram/LLMImageRender/backend/app/services/render_service.py) | `[渲染服务]` / `[渲染执行]` | 渲染任务调度与执行 |
| [llm_client.py](file:///e:/AICodeProgram/LLMImageRender/backend/app/agent/llm_client.py) | `[LLM客户端]` / `[LLM图片生成]` | LLM API 调用详情 |

**日志输出示例**：
```
2026-06-22 14:30:00 - app.routers.render - INFO - [渲染任务提交] mode=single, image_source={'type': 'gallery', 'image_id': 'img_xxx'}, params={'style': 'modern_minimalist'}
2026-06-22 14:30:01 - app.services.render_service - INFO - [渲染执行] 开始执行渲染: task_id=task_xxx
2026-06-22 14:30:02 - app.agent.llm_client - INFO - [LLM图片生成] 开始调用, model=qwen-image-2.0-pro, size=1024*1024
```

---

## 八、Phase 7：移除 AI 对话功能（2026-06-22 新增）

### 8.7.1 功能移除原因

AI 对话调整功能已从项目中移除，简化系统架构，专注于核心渲染功能。

### 8.7.2 删除的文件

**后端**：
- `backend/app/routers/chat.py` - 对话路由
- `backend/app/services/chat_service.py` - 对话服务
- `backend/app/models/chat.py` - 对话数据模型（ChatSession、ChatMessage）

**前端**：
- `frontend/src/api/chat.ts` - 对话 API 封装
- `frontend/src/components/ChatPanel.vue` - 对话面板组件

### 8.7.3 修改的文件

| 文件 | 修改内容 |
|------|----------|
| [frontend/src/pages/RenderDetailPage.vue](file:///e:/AICodeProgram/LLMImageRender/frontend/src/pages/RenderDetailPage.vue) | 删除 ChatPanel 组件引用和使用 |
| [backend/app/main.py](file:///e:/AICodeProgram/LLMImageRender/backend/app/main.py) | 删除 chat 路由注册 |
| [backend/app/models/__init__.py](file:///e:/AICodeProgram/LLMImageRender/backend/app/models/__init__.py) | 删除 ChatSession、ChatMessage 导出 |
| [backend/app/agent/graph.py](file:///e:/AICodeProgram/LLMImageRender/backend/app/agent/graph.py) | 删除 run_chat_agent 函数 |
| [backend/app/agent/llm_client.py](file:///e:/AICodeProgram/LLMImageRender/backend/app/agent/llm_client.py) | 删除 chat 方法 |
| [backend/app/agent/nodes.py](file:///e:/AICodeProgram/LLMImageRender/backend/app/agent/nodes.py) | 删除 build_chat_response 导入 |
| [backend/app/agent/skills/prompt_builder.py](file:///e:/AICodeProgram/LLMImageRender/backend/app/agent/skills/prompt_builder.py) | 删除 build_chat_response 函数 |
| [frontend/src/stores/render.ts](file:///e:/AICodeProgram/LLMImageRender/frontend/src/stores/render.ts) | 删除 currentSessionId、isChatActive 状态 |
| [frontend/src/types/index.ts](file:///e:/AICodeProgram/LLMImageRender/frontend/src/types/index.ts) | 删除 ChatMessage 接口 |

### 8.7.4 移除后的系统架构

系统现在专注于核心渲染功能：
- 图片上传与图库管理
- 渲染参数配置
- 渲染任务提交与状态查询
- 渲染结果展示与下载

---

## 九、Phase 8：移除底部信息栏组件（2026-06-22 新增）

### 9.8.1 功能移除原因

移除底部信息栏（AppFooter）组件，简化页面布局。

### 9.8.2 删除的文件

**前端**：
- `frontend/src/components/AppFooter.vue` - 底部信息栏组件

### 9.8.3 修改的文件

| 文件 | 修改内容 |
|------|----------|
| [frontend/src/App.vue](file:///e:/AICodeProgram/LLMImageRender/frontend/src/App.vue) | 删除 AppFooter 组件引用和使用 |

---

## 十一、Phase 9：单品渲染纯色背景功能（2026-06-23 新增）

### 11.9.1 功能说明

为单品渲染模式增加可选的纯色背景功能。用户在单品渲染页可通过颜色选择器或预设色块选择背景颜色，AI 生成渲染图时会按所选纯色背景渲染，背景干净简洁无杂物。场景渲染模式不受影响。

### 11.9.2 修改的文件

**前端**：

| 文件 | 修改内容 |
|------|----------|
| [frontend/src/types/index.ts](file:///e:/AICodeProgram/LLMImageRender/frontend/src/types/index.ts) | RenderParams 新增 `background_color` 字段 |
| [frontend/src/stores/render.ts](file:///e:/AICodeProgram/LLMImageRender/frontend/src/stores/render.ts) | params 默认值与 resetParams 增加 `background_color: '#FFFFFF'` |
| [frontend/src/components/ParamPanel.vue](file:///e:/AICodeProgram/LLMImageRender/frontend/src/components/ParamPanel.vue) | 新增 `showBackground` prop，含颜色选择器 + 6 个预设色块 |
| [frontend/src/pages/SingleRenderPage.vue](file:///e:/AICodeProgram/LLMImageRender/frontend/src/pages/SingleRenderPage.vue) | 传入 `:show-background="true"`，仅在单品渲染页显示背景色配置 |
| [frontend/src/pages/RenderDetailPage.vue](file:///e:/AICodeProgram/LLMImageRender/frontend/src/pages/RenderDetailPage.vue) | 渲染参数详情中单品渲染时展示背景颜色 |

**后端**：

| 文件 | 修改内容 |
|------|----------|
| [backend/app/agent/state.py](file:///e:/AICodeProgram/LLMImageRender/backend/app/agent/state.py) | RenderAgentState 新增 `background_color` 字段 |
| [backend/app/agent/graph.py](file:///e:/AICodeProgram/LLMImageRender/backend/app/agent/graph.py) | 初始 state 透传 `background_color` |
| [backend/app/agent/nodes.py](file:///e:/AICodeProgram/LLMImageRender/backend/app/agent/nodes.py) | parse_input、build_prompt 携带 `background_color` |
| [backend/app/agent/skills/prompt_builder.py](file:///e:/AICodeProgram/LLMImageRender/backend/app/agent/skills/prompt_builder.py) | 单品模式下注入纯色背景提示词 |

### 11.9.3 实现要点

- 背景色仅对单品渲染生效，场景渲染页不显示该选项，提示词也不注入纯色背景要求
- UI 提供 `el-color-picker` 任意选色 + 6 个常用预设色块（纯白/浅灰/中性灰/纯黑/米色/浅蓝）
- 提示词模板：`背景：纯色背景，背景颜色为{color}，背景干净简洁无杂物无纹理`
- 渲染详情页仅在 `task.mode === 'single'` 且存在 `background_color` 时展示

---

## 十二、功能实现对照（SPEC 需求）

### 10.1 模块一：图片管理

| 需求 | 实现情况 | 状态 |
|------|----------|------|
| 用户上传柜子图片 | ImageUploader 组件支持拖拽上传+预览 | ✅ |
| 从柜子列表中选择已有图片 | GalleryPicker 组件，从图库选择 | ✅ |
| 图片格式：JPG/PNG/WebP | 后端 file_service 支持 | ✅ |
| 图库分类浏览 | GalleryPage 支持分类筛选 | ✅ |

### 12.2 模块二：渲染参数配置

| 需求 | 实现情况 | 状态 |
|------|----------|------|
| 渲染模式选择（单品/场景） | 首页模式选择 + 路由分流 | ✅ |
| 户型选择 | RoomTypeSelector 组件（5种户型） | ✅ |
| 渲染风格 | ParamPanel（现代简约/北欧/日式/工业风/美式） | ✅ |
| 光照条件 | ParamPanel（自然光/暖光/冷光/混合光） | ✅ |
| 视角选择 | ParamPanel（正面/侧面45°/俯视/自定义） | ✅ |
| 柜子材质/颜色覆写 | ParamPanel 支持 | ✅ |
| 单品渲染纯色背景 | ParamPanel 颜色选择器+预设色块（仅单品模式） | ✅ |
| 自然语言描述 | ParamPanel 文本输入框 | ✅ |

### 12.3 模块三：渲染任务管理

| 需求 | 实现情况 | 状态 |
|------|----------|------|
| 提交渲染任务 | POST /render_api/render/submit | ✅ |
| 任务状态查询 | GET /render_api/render/task/{id} + 前端轮询 | ✅ |
| 渲染结果展示 | RenderDetailPage + ImageCompare 前后对比 | ✅ |
| 渲染历史记录 | HistoryPage 分页列表 | ✅ |
| 图片下载 | RenderDetailPage 下载按钮 | ✅ |
| 任务状态（排队/处理中/完成/失败） | 后端 status 字段 + TaskStatus 组件 | ✅ |

### 10.4 模块四：柜子图库管理

| 需求 | 实现情况 | 状态 |
|------|----------|------|
| 预设柜子图片列表 | GalleryImage 模型 + 种子数据 | ✅ |
| 柜子分类 | wardrobe / kitchen / bookcase | ✅ |
| 柜子缩略图展示 | GalleryPage 网格布局 | ✅ |

---

## 十一、技术栈实现确认

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
| LLM 模型 | qwen-image-2.0-pro | DashScope MultiModalConversation API | ✅ |

---

## 十五、Phase 10：UI 重构 - Glassmorphism + Dark Mode 响应式布局（2026-06-23 新增）

### 15.10.1 全局设计系统搭建

| 文件 | 说明 | 状态 |
|------|------|------|
| [frontend/index.html](file:///d:/AIProjects/LLMImageRender/frontend/index.html) | 添加 Inter 字体、dark 模式 class、theme-color 元数据 | ✅ |
| [frontend/src/main.ts](file:///d:/AIProjects/LLMImageRender/frontend/src/main.ts) | 引入 Element Plus 暗色模式 CSS 变量、自定义主题 | ✅ |
| [frontend/src/styles/theme.css](file:///d:/AIProjects/LLMImageRender/frontend/src/styles/theme.css) | **新增**：Glassmorphism 设计系统，CSS 变量 + Element Plus 暗色模式全覆盖 | ✅ |

**设计系统要点**：
- 暗色背景：`#0a0a0f`（主背景）/ `#12121a`（高亮层）
- 玻璃效果：`backdrop-filter: blur(20px)` + `rgba(255,255,255,0.06)` 半透明
- 强调色：`#6366f1`（靛蓝主色）/ `#8b5cf6`（紫色辅助）
- 文字层级：`#f8fafc`（主文字）/ `#cbd5e1`（次要）/ `#94a3b8`（静音）
- Element Plus 全组件暗色覆盖：Card、Menu、Button、Tabs、Input、Select、Upload、Pagination、Descriptions 等

### 15.10.2 布局与导航重构

| 文件 | 说明 | 状态 |
|------|------|------|
| [frontend/src/App.vue](file:///d:/AIProjects/LLMImageRender/frontend/src/App.vue) | 动画渐变背景球（靛蓝/紫色/蓝色）、页面切换过渡、响应式布局容器 | ✅ |
| [frontend/src/components/AppHeader.vue](file:///d:/AIProjects/LLMImageRender/frontend/src/components/AppHeader.vue) | 浮动玻璃导航栏、移动端汉堡菜单、路由切换自动关闭 | ✅ |

### 15.10.3 页面重构

| 文件 | 说明 | 状态 |
|------|------|------|
| [frontend/src/pages/HomePage.vue](file:///d:/AIProjects/LLMImageRender/frontend/src/pages/HomePage.vue) | 玻璃 Hero 区 + 徽章、双模式卡片带图标强调与 CTA 动画 | ✅ |
| [frontend/src/pages/SingleRenderPage.vue](file:///d:/AIProjects/LLMImageRender/frontend/src/pages/SingleRenderPage.vue) | 玻璃卡片布局、样式化返回按钮 | ✅ |
| [frontend/src/pages/SceneRenderPage.vue](file:///d:/AIProjects/LLMImageRender/frontend/src/pages/SceneRenderPage.vue) | 玻璃卡片布局、户型选择玻璃卡片 | ✅ |
| [frontend/src/pages/GalleryPage.vue](file:///d:/AIProjects/LLMImageRender/frontend/src/pages/GalleryPage.vue) | 玻璃图库卡片、悬停缩放、meta 标签 | ✅ |
| [frontend/src/pages/HistoryPage.vue](file:///d:/AIProjects/LLMImageRender/frontend/src/pages/HistoryPage.vue) | 玻璃任务网格、居中 CTA 空状态 | ✅ |
| [frontend/src/pages/RenderDetailPage.vue](file:///d:/AIProjects/LLMImageRender/frontend/src/pages/RenderDetailPage.vue) | 玻璃状态卡片、对比卡片、3 列描述列表移动端堆叠 | ✅ |

### 15.10.4 组件重构

| 文件 | 说明 | 状态 |
|------|------|------|
| [frontend/src/components/TaskCard.vue](file:///d:/AIProjects/LLMImageRender/frontend/src/components/TaskCard.vue) | 玻璃卡片、圆角状态徽章带模糊、图片悬停缩放 | ✅ |
| [frontend/src/components/ParamPanel.vue](file:///d:/AIProjects/LLMImageRender/frontend/src/components/ParamPanel.vue) | 响应式 2 列表单网格（移动端 1 列）、预设色块 flex 布局带名称标签、柜子尺寸标签 | ✅ |
| [frontend/src/components/SubmitBar.vue](file:///d:/AIProjects/LLMImageRender/frontend/src/components/SubmitBar.vue) | 玻璃提交栏 | ✅ |
| [frontend/src/components/ImageUploader.vue](file:///d:/AIProjects/LLMImageRender/frontend/src/components/ImageUploader.vue) | 玻璃拖拽区、模糊遮罩悬停 | ✅ |
| [frontend/src/components/GalleryPicker.vue](file:///d:/AIProjects/LLMImageRender/frontend/src/components/GalleryPicker.vue) | 玻璃项目、发光选中态 | ✅ |
| [frontend/src/components/ImageViewer.vue](file:///d:/AIProjects/LLMImageRender/frontend/src/components/ImageViewer.vue) | 主题色加载/错误状态 | ✅ |
| [frontend/src/components/ImageCompare.vue](file:///d:/AIProjects/LLMImageRender/frontend/src/components/ImageCompare.vue) | 双列对比移动端堆叠 | ✅ |
| [frontend/src/components/TaskStatus.vue](file:///d:/AIProjects/LLMImageRender/frontend/src/components/TaskStatus.vue) | 主题状态色 | ✅ |
| [frontend/src/components/RoomTypeSelector.vue](file:///d:/AIProjects/LLMImageRender/frontend/src/components/RoomTypeSelector.vue) | 玻璃房间卡片、发光选中态、移动端 3 列 | ✅ |

### 15.10.5 响应式断点

| 断点 | 适配内容 |
|------|----------|
| PC（1024px+） | 完整布局、2 列表单、双列对比 |
| 平板（768px） | 缩小间距/字体、对比图堆叠、网格调整 |
| 移动端（375-480px） | 汉堡菜单、1 列表单、2 列网格、3 列房间选择器 |

### 15.10.6 无障碍设计

- 所有可交互元素 `cursor-pointer`
- 过渡动画 200-250ms（微交互标准）
- `prefers-reduced-motion` 支持 — 禁用背景球动画
- 路由链接正确的悬停/激活视觉反馈
- 表单内 button 添加 `type="button"` 防止误提交

### 15.10.7 验证结果

- 前端 TypeScript 类型检查通过（`vue-tsc` 无报错）
- 前端生产构建成功（`npm run build` 生成 dist 目录）
- 三端响应式适配验证（375px / 768px / 1024px / 1440px）

---

## 十六、Phase 11：外部平台对接 - URL 参数传入渲染参数与图片（2026-06-23 新增）

### 16.11.1 功能需求

渲染页面（单品渲染、场景渲染）支持通过 URL 查询参数（query string）传入所有渲染参数和图片，方便外部平台嵌入跳转，无需二次配置即可发起渲染。

### 16.11.2 实现文件

| 文件 | 说明 | 状态 |
|------|------|------|
| [frontend/src/utils/urlParams.ts](file:///d:/AIProjects/LLMImageRender/frontend/src/utils/urlParams.ts) | **新增**：URL 参数解析工具函数，支持图片 URL/base64 处理 | ✅ |
| [frontend/src/pages/SingleRenderPage.vue](file:///d:/AIProjects/LLMImageRender/frontend/src/pages/SingleRenderPage.vue) | onMounted 解析 URL 参数并应用到 render store | ✅ |
| [frontend/src/pages/SceneRenderPage.vue](file:///d:/AIProjects/LLMImageRender/frontend/src/pages/SceneRenderPage.vue) | onMounted 解析 URL 参数并应用到 render store | ✅ |
| [frontend/src/components/ParamPanel.vue](file:///d:/AIProjects/LLMImageRender/frontend/src/components/ParamPanel.vue) | `syncFromStore` + `nextTick` 确保 URL 参数同步到表单 | ✅ |

### 16.11.3 支持的 URL 参数

| 参数 | 类型 | 说明 |
|------|------|------|
| `image_url` | string | 图片 URL 地址（外部平台直接提供图片链接） |
| `image_base64` | string | 图片 Base64 数据 URI |
| `style` | string | 渲染风格 |
| `lighting` | string | 光照条件 |
| `view_angle` | string | 视角 |
| `room_type` | string | 户型（场景渲染用） |
| `material` | string | 材质 |
| `color` | string | 颜色（支持 # 开头，如 #8B7355） |
| `bg_color` | string | 背景颜色（支持 # 开头） |
| `description` | string | 额外描述 |
| `width` | number | 柜子宽度 (mm) |
| `height` | number | 柜子高度 (mm) |
| `depth` | number | 柜子深度 (mm) |

### 16.11.4 设计要点

- **有传参则使用传入值，无传参则使用默认值** — 渐进式参数覆盖，不破坏页面正常使用
- **图片支持两种方式**：`image_url`（下载后上传到后端）和 `image_base64`（转 Blob 后上传到后端）
- **URL 参数解析**：通过 Vue Router 的 `useRoute().query` + `route.hash` 读取
- **`#` 字符处理**：`color=#8B7355` 中的 `#` 被浏览器当作 fragment 分隔符，代码从 `route.hash` 中恢复丢失的参数
- **颜色值自动补前缀**：无论传 `color=8B7355` 还是 `color=#8B7355` 都能正确解析
- **外部图片上传**：URL 图片通过 `fetch` 下载后上传到后端 `/render_api/images/upload`，获取真实 `image_id`
- **ParamPanel 同步**：`onMounted` 中用 `await nextTick()` 确保 URL 参数写入 store 后再同步到表单

### 16.11.5 验证结果

- 前端 TypeScript 类型检查通过（`vue-tsc` 无报错）
- 前端生产构建成功（`npm run build` 生成 dist 目录）
- 参数解析逻辑独立封装，可复用

---

## 十七、Phase 12：图片上传去重 + URL 参数修复 + ParamPanel 同步修复（2026-06-23 新增）

### 17.12.1 图片上传 MD5 去重

**问题**：外部平台通过 URL/base64 传入图片时，每次都重新保存文件并入库，造成重复
**方案**：基于文件内容 MD5 哈希去重

| 文件 | 说明 | 状态 |
|------|------|------|
| [backend/app/models/gallery.py](file:///d:/AIProjects/LLMImageRender/backend/app/models/gallery.py) | `GalleryImage` 新增 `file_hash` 列（MD5，带索引） | ✅ |
| [backend/app/database.py](file:///d:/AIProjects/LLMImageRender/backend/app/database.py) | `init_db()` 自动迁移：检测并添加缺失的 `file_hash` 列 | ✅ |
| [backend/app/routers/images.py](file:///d:/AIProjects/LLMImageRender/backend/app/routers/images.py) | 上传接口：计算 MD5 → 查询已存在 → 返回已有图片或保存新文件 | ✅ |
| [backend/seed.py](file:///d:/AIProjects/LLMImageRender/backend/seed.py) | 种子数据同步计算文件哈希 | ✅ |

**上传流程**：
1. 读取文件内容 → 计算 MD5 哈希
2. 查询数据库是否已存在相同哈希
3. 已存在 → 直接返回已有 image_id（跳过文件保存、缩略图生成、入库）
4. 不存在 → 保存文件、生成缩略图、入库（含哈希）

### 17.12.2 URL 参数 `#` 字符修复

**问题**：`color=#8B7355` 中的 `#` 被浏览器当作 fragment 分隔符，导致 `color`、`bg_color`、`description`、`width`、`height`、`depth` 全部丢失
**方案**：从 `route.hash` 中恢复被 fragment 吞掉的参数

| 文件 | 说明 | 状态 |
|------|------|------|
| [frontend/src/utils/urlParams.ts](file:///d:/AIProjects/LLMImageRender/frontend/src/utils/urlParams.ts) | 新增 `hash` 参数，解析 hash 中的 key=value 对并合并到 query | ✅ |
| [frontend/src/pages/SingleRenderPage.vue](file:///d:/AIProjects/LLMImageRender/frontend/src/pages/SingleRenderPage.vue) | 传入 `route.hash` | ✅ |
| [frontend/src/pages/SceneRenderPage.vue](file:///d:/AIProjects/LLMImageRender/frontend/src/pages/SceneRenderPage.vue) | 传入 `route.hash` | ✅ |

**额外处理**：颜色值自动补 `#` 前缀（无论传 `8B7355` 还是 `#8B7355`）

### 17.12.3 ParamPanel 表单同步修复

**问题**：URL 参数写入 store 后，ParamPanel 的表单控件未同步更新
**方案**：`onMounted` 中用 `await nextTick()` 确保父组件写入 store 后再执行 `syncFromStore()`

### 17.12.4 验证结果

- 图片重复上传时返回已有记录，不产生重复文件
- URL 中 `color=#8B7355` 不编码也能正确解析所有参数
- ParamPanel 表单正确显示 URL 传入的参数值

---

## 十三、Phase 13：外部平台 image_id + 图库"其他"分类（2026-06-24）

### 13.1 外部平台对接新增 image_id 参数

**功能**：URL 参数新增 `image_id`，直接查询图库数据中的图片，查得到则添加，查不到则提示

**修改文件**：

| 文件 | 修改内容 |
|------|----------|
| [frontend/src/utils/urlParams.ts](file:///e:/AICodeProgram/LLMImageRender/frontend/src/utils/urlParams.ts) | `UrlParamsResult` 新增 `imageId` 字段；`parseUrlParams` 解析 `image_id`；`applyExternalImage` 新增 `imageId` 参数，优先查询图库 |
| [frontend/src/pages/SingleRenderPage.vue](file:///e:/AICodeProgram/LLMImageRender/frontend/src/pages/SingleRenderPage.vue) | 传入 `imageId`，查询失败时提示 `图库中未找到该图片` |
| [frontend/src/pages/SceneRenderPage.vue](file:///e:/AICodeProgram/LLMImageRender/frontend/src/pages/SceneRenderPage.vue) | 同上 |
| [README.md](file:///e:/AICodeProgram/LLMImageRender/README.md) | 参数表新增 `image_id` 行，示例新增用法 |

**优先级**：`image_id` > `image_url` > `image_base64`

### 13.2 图库"其他"分类

**功能**：图库目录分类增加"其他"分类

**修改文件**：

| 文件 | 修改内容 |
|------|----------|
| [backend/app/routers/params.py](file:///e:/AICodeProgram/LLMImageRender/backend/app/routers/params.py) | `categories` 新增 `{"value": "other", "label": "其他"}` |
| [frontend/src/pages/GalleryPage.vue](file:///e:/AICodeProgram/LLMImageRender/frontend/src/pages/GalleryPage.vue) | `categories` 数组新增"其他" |
| [frontend/src/components/GalleryPicker.vue](file:///e:/AICodeProgram/LLMImageRender/frontend/src/components/GalleryPicker.vue) | 同上 |

### 13.3 上传图片默认分类

**修改文件**：

| 文件 | 修改内容 |
|------|----------|
| [backend/app/routers/images.py](file:///e:/AICodeProgram/LLMImageRender/backend/app/routers/images.py) | 上传图片 `category` 从 `"uploaded"` 改为 `"other"`，使上传图片归入"其他"分类，可在图库中筛选到 |

### 13.4 ImageUploader 组件优化

| 文件 | 修改内容 |
|------|----------|
| [frontend/src/components/ImageUploader.vue](file:///e:/AICodeProgram/LLMImageRender/frontend/src/components/ImageUploader.vue) | `<img>` 替换为 `<el-image fit="contain">`，CSS 选择器从 `img` 改为 `.el-image`，`max-height` 改为固定 `height: 300px` |

---

## 十四、Phase 14：渲染详情页删除/再次渲染（2026-06-24）

### 14.1 后端 RenderTask 模型新增 image_id 列

**功能**：存储任务使用的图库图片 ID，支持再次渲染时复用

**修改文件**：

| 文件 | 修改内容 |
|------|----------|
| [backend/app/models/task.py](file:///e:/AICodeProgram/LLMImageRender/backend/app/models/task.py) | 新增 `image_id = Column(String(64), nullable=True)` |
| [backend/app/database.py](file:///e:/AICodeProgram/LLMImageRender/backend/app/database.py) | `init_db()` 新增 `render_tasks.image_id` 列自动迁移（SQLite ALTER TABLE） |
| [backend/app/routers/render.py](file:///e:/AICodeProgram/LLMImageRender/backend/app/routers/render.py) | 提交接口存储 `image_id`；状态接口返回 `image_source` 和 `image_id` |

### 14.2 前端类型与页面

| 文件 | 修改内容 |
|------|----------|
| [frontend/src/types/index.ts](file:///e:/AICodeProgram/LLMImageRender/frontend/src/types/index.ts) | `RenderTask` 新增 `image_source` 和 `image_id` 字段 |
| [frontend/src/pages/RenderDetailPage.vue](file:///e:/AICodeProgram/LLMImageRender/frontend/src/pages/RenderDetailPage.vue) | 新增删除按钮（确认对话框 → deleteTask → 跳转首页）；新增再次渲染按钮（复用 mode/image_source/image_id/params 提交新任务）；`watch` 路由参数变化支持同组件跳转 |

---

## 十五、Phase 15：图库图片管理（2026-06-24）

### 15.1 后端接口

| 端点 | 方法 | 说明 |
|------|------|------|
| `/render_api/images/gallery/:id` | PUT | 更新图片名称和分类（支持部分更新） |
| `/render_api/images/gallery/:id` | DELETE | 删除图片记录 + 物理文件 + 缩略图 |

**修改文件**：[backend/app/routers/images.py](file:///e:/AICodeProgram/LLMImageRender/backend/app/routers/images.py)

### 15.2 前端 API 与页面

| 文件 | 修改内容 |
|------|----------|
| [frontend/src/api/gallery.ts](file:///e:/AICodeProgram/LLMImageRender/frontend/src/api/gallery.ts) | 新增 `updateImage()` 和 `deleteImage()` |
| [frontend/src/pages/GalleryPage.vue](file:///e:/AICodeProgram/LLMImageRender/frontend/src/pages/GalleryPage.vue) | 每张卡片新增编辑/删除按钮；编辑对话框（改名+改分类）；删除确认；分类标签显示中文（`categoryLabel` 函数） |

---

## 十六、Phase 16：UI 重构 Glassmorphism 增强（2026-06-24）

### 16.1 GalleryPage 重构

| 优化项 | 说明 |
|--------|------|
| 页头 | 标题字间距优化 + 图片数量计数标签 |
| 筛选栏 | 包裹在 glass-card 玻璃容器中 |
| 卡片交错动画 | 40ms 间隔依次淡入上滑 |
| 悬停效果 | 卡片上浮 4px + 紫色光晕边框 + 图片 1.06x 缩放 |
| 图片悬浮叠层 | 渐变遮罩 + 毛玻璃分类标签 |
| 操作按钮 | `:deep()` 控制悬停色，删除按钮红色高亮 |
| 无障碍 | `prefers-reduced-motion` 支持 |

### 16.2 RenderDetailPage 重构

| 优化项 | 说明 |
|--------|------|
| 状态标签光晕 | 根据 processing/completed/failed 显示不同颜色 box-shadow |
| 状态卡片 | 边框颜色随状态变化，处理中状态紫色外发光 |
| 返回按钮 | 毛玻璃 + 悬停左移微动效 |
| 参数网格标题 | 左侧紫色竖条指示器 + 发光效果 |
| 参数项 | 悬停背景渐变、标签大写+字间距、细腻边框分隔 |

### 16.3 弹窗样式修复

**问题**：Dialog 和 MessageBox 背景透明度过高，透出底层内容

**修改文件**：[frontend/src/styles/theme.css](file:///e:/AICodeProgram/LLMImageRender/frontend/src/styles/theme.css)

| 元素 | 样式 |
|------|------|
| 遮罩层 | `rgba(0, 0, 0, 0.75)` + 8px 毛玻璃模糊 |
| Dialog 内容 | `rgba(18, 18, 26, 0.96)` 近乎不透明 + 玻璃边框 + 大阴影 |
| MessageBox 内容 | 同上，统一视觉风格 |
| header/footer | 分隔线，按钮主色/危险色统一 |

---

## 十七、Phase 17：RenderDetailPage 移动端响应式布局（2026-06-24）

### 17.1 模板结构调整

将 header 拆分为 `header-left`（返回按钮 + 标题 + 状态标签）和 `header-actions`（操作按钮）两个逻辑组，按钮文字包裹 `.btn-label` 以便移动端控制显隐。

### 17.2 响应式策略

| 屏幕宽度 | 布局表现 |
|---------|---------|
| 桌面端 | `header-left` 左对齐，`header-actions` 右对齐，同一行 |
| ≤768px | `header-actions` 换行到下一行，宽度 100%，两个按钮等分宽度 |
| ≤480px | 返回按钮和操作按钮仅显示图标（隐藏文字），最小高度 40px 保证触控区域 |

**关键 CSS**：
- `justify-content: space-between` + `flex-wrap: wrap` 实现两端对齐自动换行
- `header-left` 设置 `min-width: 0` 让标题可正确截断
- `flex-shrink: 0` 防止按钮和标签被压缩

---

## 十八、Phase 18：API 路由重构 + 模型环境变量配置 + Ubuntu 部署文档（2026-06-24）

### 18.1 API 路由前缀重构

将后端 API 路由从 `/api` 改为 `/render_api`，静态资源从 `/static` 改为 `/render_static`，避免与其他服务的 `/api` 和 `/static` 路径冲突。

| 文件 | 修改内容 |
|------|----------|
| [backend/app/main.py](file:///e:/AICodeProgram/LLMImageRender/backend/app/main.py) | `app.mount("/render_static", ...)`，路由前缀 `/render_api/*`，健康检查 `/render_api/health` |
| [backend/app/routers/images.py](file:///e:/AICodeProgram/LLMImageRender/backend/app/routers/images.py) | 图片路径 `/render_static/uploads/`（上传保存 + 删除替换） |
| [backend/app/services/file_service.py](file:///e:/AICodeProgram/LLMImageRender/backend/app/services/file_service.py) | 结果图路径 `/render_static/results/` |
| [backend/seed.py](file:///e:/AICodeProgram/LLMImageRender/backend/seed.py) | 种子数据路径 `/render_static/gallery/` |
| [frontend/vite.config.ts](file:///e:/AICodeProgram/LLMImageRender/frontend/vite.config.ts) | 代理路径 `/render_api` 和 `/render_static` |
| [frontend/src/api/index.ts](file:///e:/AICodeProgram/LLMImageRender/frontend/src/api/index.ts) | axios baseURL `/render_api` |

### 18.2 LLM 模型环境变量配置

将硬编码的模型名称改为通过环境变量配置。

| 文件 | 修改内容 |
|------|----------|
| [backend/app/config.py](file:///e:/AICodeProgram/LLMImageRender/backend/app/config.py) | 新增 `DASHSCOPE_MODEL` 配置项，默认 `qwen-image-2.0-pro` |
| [backend/app/agent/llm_client.py](file:///e:/AICodeProgram/LLMImageRender/backend/app/agent/llm_client.py) | `model_name` 从 `settings.DASHSCOPE_MODEL` 读取，`api_key` 统一从 `settings` 读取 |
| [backend/.env.example](file:///e:/AICodeProgram/LLMImageRender/backend/.env.example) | 新增 `DASHSCOPE_MODEL=qwen-image-2.0-pro` |

### 18.3 Ubuntu 部署文档

| 文件 | 说明 |
|------|------|
| [DEPLOY_UBUNTU.md](file:///e:/AICodeProgram/LLMImageRender/DEPLOY_UBUNTU.md) | 完整的 Ubuntu 部署指南，包含 Python/Node.js 环境安装、Nginx 配置、Systemd 服务、SSL 配置、故障排查等 |

---

## 十九、Phase 19：图库图片柜子属性 + 选择图库自动填充参数 + 新增材质提示词（2026-06-24）

### 19.1 数据库模型扩展

为图库图片新增 5 个柜子属性字段，支持上传时附带、图库选择时自动填充渲染参数。

| 文件 | 修改内容 |
|------|----------|
| [backend/app/models/gallery.py](file:///e:/AICodeProgram/LLMImageRender/backend/app/models/gallery.py) | 新增 `cabinet_w`、`cabinet_d`、`cabinet_h`、`material`、`color` 5 列 |
| [backend/app/database.py](file:///e:/AICodeProgram/LLMImageRender/backend/app/database.py) | 自动迁移：循环检查 5 个新列，缺失则 `ALTER TABLE` 添加 |
| [backend/seed.py](file:///e:/AICodeProgram/LLMImageRender/backend/seed.py) | 种子数据 `SEED_IMAGES` 包含 5 个属性，`GalleryImage` 构造函数传参 |

### 19.2 后端 API 接口更新

| 文件 | 修改内容 |
|------|----------|
| [backend/app/routers/images.py](file:///e:/AICodeProgram/LLMImageRender/backend/app/routers/images.py) | 上传接口入参新增 5 个可选 `Form` 参数；去重返回、上传成功返回、图库列表、详情、更新接口均返回 5 个字段；`UpdateImageRequest` 支持更新 5 个字段 |

### 19.3 前端图库选择自动填充

| 文件 | 修改内容 |
|------|----------|
| [frontend/src/types/index.ts](file:///e:/AICodeProgram/LLMImageRender/frontend/src/types/index.ts) | `GalleryImage` 接口新增 5 个可选字段 |
| [frontend/src/stores/render.ts](file:///e:/AICodeProgram/LLMImageRender/frontend/src/stores/render.ts) | `setGalleryImage` 接收 `extra` 参数，写入 `material`、`color`、`cabinet_size` |
| [frontend/src/components/GalleryPicker.vue](file:///e:/AICodeProgram/LLMImageRender/frontend/src/components/GalleryPicker.vue) | 选中图片时将 5 个属性传给 `setGalleryImage` |
| [frontend/src/components/ParamPanel.vue](file:///e:/AICodeProgram/LLMImageRender/frontend/src/components/ParamPanel.vue) | 新增 `watch(renderStore.params)` 监听 store 变化，图库选择后自动同步材质/颜色/尺寸到表单，用 `syncing` flag 防止递归 |

### 19.4 新增材质提示词

| 文件 | 修改内容 |
|------|----------|
| [backend/app/routers/params.py](file:///e:/AICodeProgram/LLMImageRender/backend/app/routers/params.py) | 材质选项已有"多层板"和"中密度板" |
| [backend/app/agent/skills/prompt_builder.py](file:///e:/AICodeProgram/LLMImageRender/backend/app/agent/skills/prompt_builder.py) | `MATERIAL_MAP` 新增 `plywood`（多层板）和 `mdf`（中密度板）提示词 |

---

## 二十、Phase 20：时区修复 + 渲染任务异步阻塞修复（2026-06-24）

### 20.1 时区修复（UTC → 东八区）

**问题**：`datetime.utcnow()` 返回 UTC 时间，比中国时区慢 8 小时，且该函数在 Python 3.12+ 已弃用。

**修复**：统一使用 `datetime.now(timezone(timedelta(hours=8)))` 获取东八区时间。

| 文件 | 修改内容 |
|------|----------|
| [backend/app/models/task.py](file:///e:/AICodeProgram/LLMImageRender/backend/app/models/task.py) | 新增 `_now_cst()` 函数，`created_at`、`updated_at` 的 `default`/`onupdate` 改为 `_now_cst` |
| [backend/app/models/gallery.py](file:///e:/AICodeProgram/LLMImageRender/backend/app/models/gallery.py) | 新增 `_now_cst()` 函数，`created_at` 的 `default` 改为 `_now_cst` |
| [backend/app/services/render_service.py](file:///e:/AICodeProgram/LLMImageRender/backend/app/services/render_service.py) | `completed_at` 赋值改为 `datetime.now(_CST)` |

### 20.2 渲染任务异步阻塞修复

**问题**：渲染任务虽然用 `asyncio.create_task` 创建，但内部 `MultiModalConversation.call()`、`preprocess_image()`、`postprocess_result()` 均为同步阻塞调用，会卡住整个事件循环，导致渲染期间其他 API 请求无响应。

**修复**：用 `asyncio.to_thread()` 将同步阻塞调用包装到线程池中执行。

| 文件 | 修改内容 |
|------|----------|
| [backend/app/agent/llm_client.py](file:///e:/AICodeProgram/LLMImageRender/backend/app/agent/llm_client.py) | `MultiModalConversation.call()` 用 `await asyncio.to_thread()` 包装 |
| [backend/app/agent/nodes.py](file:///e:/AICodeProgram/LLMImageRender/backend/app/agent/nodes.py) | `preprocess_image()` 和 `postprocess_result()` 均用 `await asyncio.to_thread()` 包装 |

---

## 二十一、Phase 21：UI 主题切换 - Glassmorphism + Light Mode（2026-06-30 新增）

### 21.1 功能说明

在原有 Glassmorphism + Dark Mode 基础上新增浅色主题（Light Mode），支持顶栏一键切换、URL 参数控制主题、localStorage 持久化，切换后直接刷新 CSS 变量无需重启页面。

### 21.2 修改的文件

| 文件 | 修改内容 |
|------|----------|
| [frontend/src/styles/theme.css](file:///d:/AIProjects/LLMImageRender/frontend/src/styles/theme.css) | 重构：`:root` 改为浅色模式默认值，`html.dark` 为深色覆盖；新增 `html:not(.dark)` 浅色模式 Element Plus 全组件覆盖（Card/Menu/Button/Tabs/Input/Select/Dialog/MessageBox/Popper 等） |
| [frontend/src/stores/theme.ts](file:///d:/AIProjects/LLMImageRender/frontend/src/stores/theme.ts) | **新增**：主题 Pinia store，含 `setMode`/`toggle`/`applyToDOM`/`initFromUrl`，localStorage 持久化（key=theme） |
| [frontend/index.html](file:///d:/AIProjects/LLMImageRender/frontend/index.html) | 移除硬编码 `class="dark"`，新增内联脚本防 FOUC（优先级：URL ?theme > localStorage > 默认 dark） |
| [frontend/src/main.ts](file:///d:/AIProjects/LLMImageRender/frontend/src/main.ts) | app 挂载前调用 `themeStore.initFromUrl()` 同步 URL 参数/持久化到 store |
| [frontend/src/components/AppHeader.vue](file:///d:/AIProjects/LLMImageRender/frontend/src/components/AppHeader.vue) | 新增主题切换按钮（太阳/月亮图标），桌面端导航栏 + 移动端操作区各一个，悬停图标旋转微交互 |

### 21.3 设计要点

- **主题架构**：`:root` = Light Mode（默认），`html.dark` = Dark Mode 覆盖，参考 LLMChatRAG 双主题方案
- **浅色配色**：`#eef2f8` 浅灰蓝底色 + `rgba(248,250,252,0.75)` 玻璃面 + 深色文字（`#0f172a`/`#334155`/`#475569`，对比度 ≥ 4.5:1）
- **切换机制**：通过 `document.documentElement.classList` 切换 `.dark` 类，CSS 变量即时生效，**无需重启页面**
- **防闪烁（FOUC）**：index.html 内联脚本在 Vue 加载前根据优先级设置 `.dark` 类，避免页面加载时主题闪烁
- **URL 参数控制**：`?theme=light` 或 `?theme=dark`，便于外部平台跳转特定主题系统（优先级高于 localStorage）
- **持久化**：Pinia + `pinia-plugin-persistedstate`，刷新后保持上次主题选择
- **移动端适配**：`meta[name="theme-color"]` 随主题同步（深色 `#0a0a0f` / 浅色 `#eef2f8`），适配移动端浏览器顶栏
- **平滑过渡**：`body` 添加 `transition: background-color 0.3s ease, color 0.3s ease`，主题切换时背景/文字平滑过渡

### 21.4 验证结果

- 前端 TypeScript 类型检查通过（`vue-tsc` 无报错）
- 前端生产构建成功（`npm run build` 生成 dist 目录）
- 顶栏切换按钮在浅色/深色间即时切换，刷新后保持选择
- URL 参数 `?theme=light` / `?theme=dark` 正确生效

---

## 二十二、Phase 22：主题兼容修复 + 移动端 UX 修复 + LLM 图片本地持久化（2026-06-30 新增）

### 22.1 浅色主题媒体背景兼容（--media-bg）

**问题**：5 处图片/媒体展示区域硬编码 `background: rgba(0, 0, 0, 0.2)`（深色专用），浅色主题下背景过深、与整体风格不协调。

**方案**：在 theme.css 新增主题感知变量 `--media-bg`（浅色 `rgba(15, 23, 42, 0.05)` / 深色 `rgba(0, 0, 0, 0.2)`），5 处引用统一替换。

| 文件 | 修改内容 |
|------|----------|
| [frontend/src/styles/theme.css](file:///e:/AICodeProgram/LLMImageRender/frontend/src/styles/theme.css) | `:root` 与 `html.dark` 各新增 `--media-bg` 变量 |
| [frontend/src/pages/SceneRenderPage.vue](file:///e:/AICodeProgram/LLMImageRender/frontend/src/pages/SceneRenderPage.vue) | `.preview-container` 背景改用 `var(--media-bg)` |
| [frontend/src/pages/SingleRenderPage.vue](file:///e:/AICodeProgram/LLMImageRender/frontend/src/pages/SingleRenderPage.vue) | `.preview-container` 背景改用 `var(--media-bg)` |
| [frontend/src/components/GalleryPicker.vue](file:///e:/AICodeProgram/LLMImageRender/frontend/src/components/GalleryPicker.vue) | `.gallery-item` 背景改用 `var(--media-bg)` |
| [frontend/src/components/ImageCompare.vue](file:///e:/AICodeProgram/LLMImageRender/frontend/src/components/ImageCompare.vue) | `.compare-image` 背景改用 `var(--media-bg)` |
| [frontend/src/components/TaskCard.vue](file:///e:/AICodeProgram/LLMImageRender/frontend/src/components/TaskCard.vue) | `.task-thumbnail` 背景改用 `var(--media-bg)` |

### 22.2 RenderDetailPage 参数网格主题兼容

**问题**：`.params-grid-body` / `.param-item` 硬编码 `rgba(255, 255, 255, ...)`（深色专用），浅色主题下边框/底色几乎不可见。

**方案**：替换为主题感知变量（边框 → `var(--glass-border)`、底色 → `var(--el-fill-color-lighter)`、hover → `var(--el-fill-color-light)`），响应式断点边框同步替换。

| 文件 | 修改内容 |
|------|----------|
| [frontend/src/pages/RenderDetailPage.vue](file:///e:/AICodeProgram/LLMImageRender/frontend/src/pages/RenderDetailPage.vue) | 参数网格边框/底色/hover 及移动端断点边框全部改用主题变量 |

### 22.3 移动端长按选区 / 点击高亮修复

**问题**：移动端长按可点击 UI 区域时，WebKit 触发蓝色透明选区闪烁与系统弹窗。

**方案**：全局去除 tap-highlight，对非文本交互元素禁用 `touch-callout` 与 `user-select`，保留输入框/正文文本正常选择。

| 文件 | 修改内容 |
|------|----------|
| [frontend/src/styles/theme.css](file:///e:/AICodeProgram/LLMImageRender/frontend/src/styles/theme.css) | `body` 新增 `-webkit-tap-highlight-color: transparent`；新增 `button/img/.glass/.glass-card/.task-card/.gallery-item/.preview-container/.compare-image/.task-thumbnail` 的 `-webkit-touch-callout: none` + `user-select: none` 规则 |

### 22.4 移动端 el-image 预览窗口左缩修复

**问题**：移动端点击 el-image 展开预览时，Element Plus `useLockscreen` hook 给 body 写入内联 `width: calc(100% - 滚动条宽度)` 补偿滚动条消失；移动端滚动条为 overlay 不占宽度，该补偿导致整个窗口向左缩小。

**方案**：移动端媒体查询中用 `!important` 覆盖内联宽度，重置 body 为 100%，同时覆盖 `el-image-viewer-parent--hidden` 与 `el-popup-parent--hidden` 两类锁屏类。

| 文件 | 修改内容 |
|------|----------|
| [frontend/src/styles/theme.css](file:///e:/AICodeProgram/LLMImageRender/frontend/src/styles/theme.css) | 新增 `@media (max-width: 768px) { body[class*="parent--hidden"] { width: 100% !important; } }` |

### 22.5 LLM 临时图片 URL 本地持久化

**问题**：`llm_client.generate_image` 返回 DashScope 临时图片 URL（会过期），原代码直接存入 state，后续访问 404；且 `postprocess_result` 对 http URL 直接跳过处理。

**方案**：`call_llm_render` 节点拿到临时 URL 后，异步下载图片字节，调用现有 `save_result_image` 落盘到 `render_static/results/YYYY/MM/DD/{task_id}.png`，将本地 URL 存入 state；下载失败回退原 URL。改用本地路径后 `postprocess_result` 也能正确执行 RGBA→RGB 转换与 PNG 压缩。

| 文件 | 修改内容 |
|------|----------|
| [backend/app/agent/nodes.py](file:///e:/AICodeProgram/LLMImageRender/backend/app/agent/nodes.py) | 新增 `_download_remote_image`（标准库 `urllib.request` + `asyncio.to_thread`，带 User-Agent 头）；`call_llm_render` 对 http URL 下载落盘后存本地 URL，失败回退原 URL |

### 22.6 验证结果

- 前端浅色/深色主题切换，5 处媒体区域与参数网格背景正确随主题变化
- 移动端长按 UI 无蓝色选区闪烁，输入框/正文文本仍可选择
- 移动端点击 el-image 展开预览，窗口不再左缩
- 后端 `python -m py_compile app/agent/nodes.py` 编译通过
- LLM 渲染结果落盘到 `render_static/results/`，任务详情返回本地持久化 URL

---

## 二十三、Phase 23：Element Plus 按需加载 + UI 交互优化 + 图库排序 + 毛玻璃样式精调（2026-07-06 新增）

### 23.1 Element Plus 按需加载（commit abb19e2）

**问题**：原方案全局引入 `ElementPlus` 及全部图标，打包体积大，首屏加载慢。

**方案**：引入 `unplugin-vue-components`，自动按需导入模板中使用的 `el-*` 组件与 `v-loading` 指令及其样式，移除全局 `ElementPlus` 与图标注册。

| 文件 | 修改内容 |
|------|----------|
| [frontend/package.json](file:///d:/AIProjects/LLMImageRender/frontend/package.json) | 新增 `unplugin-vue-components` 依赖，按字母排序 dependencies/devDependencies |
| [frontend/vite.config.ts](file:///d:/AIProjects/LLMImageRender/frontend/vite.config.ts) | plugins 新增 `Components({ resolvers: [ElementPlusResolver()], dts: 'src/components.d.ts' })` |
| [frontend/src/main.ts](file:///d:/AIProjects/LLMImageRender/frontend/src/main.ts) | 移除 `import ElementPlus` / `import * as IconsVue` / 全局图标注册；仅保留 `dark/css-vars.css` + `base.css` + `el-message.css` + `el-message-box.css` |
| [frontend/src/components.d.ts](file:///d:/AIProjects/LLMImageRender/frontend/src/components.d.ts) | **新增**：自动生成的组件类型声明文件 |
| [frontend/index.html](file:///d:/AIProjects/LLMImageRender/frontend/index.html) | 移除 Inter 字重 300（不再使用） |

### 23.2 UI 交互优化（commit 7172e5e）

#### 23.2.1 ElScrollbar 接管全局滚动

| 文件 | 修改内容 |
|------|----------|
| [frontend/src/App.vue](file:///d:/AIProjects/LLMImageRender/frontend/src/App.vue) | 最外层 `div#app-layout` 改为 `height: 100vh; overflow: hidden`；用 `el-scrollbar` 包裹 `AppHeader + main` 实现统一滚动容器，不再使用系统滚动条 |

#### 23.2.2 图片选择 Tab 顺序调整

| 文件 | 修改内容 |
|------|----------|
| [frontend/src/pages/SingleRenderPage.vue](file:///d:/AIProjects/LLMImageRender/frontend/src/pages/SingleRenderPage.vue) | Tab 顺序改为"从图库选择"在前、"上传图片"在后；`activeTab` 默认 `'gallery'`；`.image-card :deep(.el-tabs)` 添加 `overflow: hidden` |
| [frontend/src/pages/SceneRenderPage.vue](file:///d:/AIProjects/LLMImageRender/frontend/src/pages/SceneRenderPage.vue) | 同上 |

#### 23.2.3 GalleryPage 筛选改为自定义标签

| 文件 | 修改内容 |
|------|----------|
| [frontend/src/pages/GalleryPage.vue](file:///d:/AIProjects/LLMImageRender/frontend/src/pages/GalleryPage.vue) | `el-radio-group` / `el-radio-button` 替换为自定义 `<button.filter-tag>` 胶囊按钮，`flex-wrap` 自动换行；激活态靛蓝填充+发光阴影；`focus-visible` 键盘焦点环 |

#### 23.2.4 GalleryPicker 标题样式优化

| 文件 | 修改内容 |
|------|----------|
| [frontend/src/components/GalleryPicker.vue](file:///d:/AIProjects/LLMImageRender/frontend/src/components/GalleryPicker.vue) | `.gallery-title` 从固定 `width: 100px` 改为 `flex-shrink: 0` + `white-space: nowrap`，内容不换行 |

### 23.3 图库查询排序（commit 9a90ee4 / 69d318e）

**功能**：图库列表 API 新增 `order` 参数（`asc` 正序 / `desc` 倒序），前端默认正序（旧→新）；渲染详情页移除状态标签（精简 header），处理中任务禁用"再次渲染"和"删除"按钮。

| 文件 | 修改内容 |
|------|----------|
| [backend/app/routers/images.py](file:///d:/AIProjects/LLMImageRender/backend/app/routers/images.py) | `get_gallery` 新增 `order: str = "desc"` 参数，`asc` 时 `order_by(created_at.asc())` |
| [frontend/src/api/gallery.ts](file:///d:/AIProjects/LLMImageRender/frontend/src/api/gallery.ts) | `getGallery()` 新增 `order` 参数，默认 `'asc'` |
| [frontend/src/pages/RenderDetailPage.vue](file:///d:/AIProjects/LLMImageRender/frontend/src/pages/RenderDetailPage.vue) | 移除 header 中的 `el-tag` 状态标签及 `statusLabel`/`tagType` 计算属性；再次渲染按钮 `:disabled` 增加 `task.status === 'processing'`；删除按钮同样禁用；清理对应的 `.status-tag` 发光样式 |
| [frontend/src/components/TaskStatus.vue](file:///d:/AIProjects/LLMImageRender/frontend/src/components/TaskStatus.vue) | `processing` 状态图标添加 `is-loading` class，触发旋转动画 |

### 23.4 毛玻璃样式精调（commit b3e28be）

| 文件 | 修改内容 |
|------|----------|
| [frontend/src/styles/theme.css](file:///d:/AIProjects/LLMImageRender/frontend/src/styles/theme.css) | `--glass-blur` 从 20px → 16px；新增 `--saturate`（浅色 180% / 深色 160%）；`.glass` / `.glass-card` 的 `backdrop-filter` 增加 `saturate()` 滤镜，视觉效果更通透；`.glass` 新增 `border-radius: var(--radius-lg)`；`.glass-card:hover` 移除边框色变化、新增 `transform: translateY(-2px)` 微上浮效果；过渡曲线改为 `cubic-bezier(0.16, 1, 0.3, 1)` 更流畅的缓出 |

### 23.5 验证结果

- 前端 TypeScript 类型检查通过（`vue-tsc` 无报错）
- 前端生产构建成功（`npm run build` 生成 dist 目录）
- Element Plus 按需加载，打包体积显著减少
- 全局 ElScrollbar 统一滚动体验
- 图库列表按创建时间正序展示
- 毛玻璃卡片悬停微上浮，视觉层次增强

---

## 2026-07-07 渲染缩略图 + 路由进度条

### 一、渲染结果缩略图生成

**背景**：渲染历史列表加载全尺寸渲染结果图，带宽消耗大、加载缓慢。

**方案**：渲染结果保存到本地时同步生成 400x400 缩略图，历史列表优先加载缩略图。

#### 后端改动

| 文件 | 改动 |
|------|------|
| `backend/app/agent/state.py` | `RenderAgentState` 新增 `thumbnail_url` 字段 |
| `backend/app/models/task.py` | `RenderTask` 模型新增 `thumbnail` 列（`VARCHAR(512)`，nullable） |
| `backend/app/database.py` | 启用 SQLite 自动迁移，`ALTER TABLE render_tasks ADD COLUMN thumbnail` |
| `backend/app/services/file_service.py` | 新增 `save_thumbnail()` 函数：PIL 从 bytes 生成 400x400 缩略图，处理 RGBA→RGB，保存为 `thumb_{task_id}.png` |
| `backend/app/agent/nodes.py` | `call_llm_render` 节点：下载远程图片保存后立即调用 `save_thumbnail` 生成缩略图，存入 `state["thumbnail_url"]`；失败时优雅降级为 `None` |
| `backend/app/agent/graph.py` | `run_render_agent` 返回值新增 `thumbnail_url`；初始 state 新增 `thumbnail_url: None` |
| `backend/app/services/render_service.py` | 渲染完成时将 `thumbnail_url` 写入 `task.thumbnail` |
| `backend/app/routers/render.py` | `/history` 接口返回项新增 `thumbnail_url` 字段 |

#### 前端改动

| 文件 | 改动 |
|------|------|
| `frontend/src/types/index.ts` | `RenderTask` 接口新增 `thumbnail_url: string \| null` |
| `frontend/src/components/TaskCard.vue` | 缩略图源优先级：`thumbnail_url` → `result_image_url` → `original_image_url` |

#### 数据流

```
LLM 返回临时图片 URL
  → _download_remote_image 下载二进制
  → save_result_image 保存全尺寸到 render_static/results/YYYY/MM/DD/{task_id}.png
  → save_thumbnail 生成缩略图到 render_static/results/YYYY/MM/DD/thumb_{task_id}.png
  → state["thumbnail_url"] → graph 返回 → render_service 写入 DB → /history API 返回
  → 前端 TaskCard 优先加载缩略图
```

---

### 二、路由跳转加载进度条

**背景**：前端使用 `unplugin-vue-components` 按需加载 + Vue Router 懒加载（`() => import()`），首次跳转路由需下载 chunk，等待过久无视觉反馈。

**方案**：路由导航守卫触发顶部进度条，纯 CSS 动画无新增依赖。

#### 新增文件

| 文件 | 说明 |
|------|------|
| `frontend/src/composables/useRouteProgress.ts` | 模块级单例 composable，提供 `progress`（响应式进度值）、`visible`（是否显示）、`startProgress`（快速推进到 80% 后放缓）、`finishProgress`（到 100% 后淡出） |
| `frontend/src/components/RouteProgress.vue` | 顶部 3px 进度条组件，`scaleX` 变换动画，靛蓝→紫色渐变 + glow 阴影，`z-index: 9999`，`pointer-events: none` |

#### 改动文件

| 文件 | 改动 |
|------|------|
| `frontend/src/router/index.ts` | 新增 `beforeEach`（启动进度条）、`afterEach`（完成进度条）、`onError`（异常时完成进度条）导航守卫 |
| `frontend/src/App.vue` | 布局顶部挂载 `<RouteProgress />` 组件 |

#### 进度条动画逻辑

```
beforeEach → startProgress()
  progress: 0 → 80%（每 200ms 按剩余距离 15% 递增，越接近 80% 越慢）

afterEach → finishProgress()
  progress: → 100%（立即）
  350ms 后 visible: false（淡出隐藏）
```

---

## 二十四、已知问题与解决方案

### 24.1 API 调用问题（已解决）

**问题**：`ImageSynthesis.call()` 不支持 Base64 数据 URI 格式
**解决**：改用 `MultiModalConversation.call()` API
**状态**：✅ 已修复

### 24.2 日志缺失问题（已解决）

**问题**：后端关键节点缺少日志输出，难以排查问题
**解决**：集成完整日志系统，覆盖所有 API 和服务模块
**状态**：✅ 已修复

---

> 本文档将随项目演进持续更新。
