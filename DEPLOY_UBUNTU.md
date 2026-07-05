# LLMImageRender Ubuntu 部署指南

本文档介绍如何将 LLMImageRender 部署到 Ubuntu 服务器上。

## 目录

- [环境要求](#环境要求)
- [1. 系统准备](#1-系统准备)
- [2. 安装 Python 环境](#2-安装-python-环境)
- [3. 安装 Node.js 环境](#3-安装-nodejs-环境)
- [4. 部署后端服务](#4-部署后端服务)
- [5. 构建前端](#5-构建前端)
- [6. 配置 Nginx](#6-配置-nginx)
- [7. 配置 Systemd 服务](#7-配置-systemd-服务)
- [8. 防火墙配置](#8-防火墙配置)
- [9. SSL/HTTPS 配置（可选）](#9-sslhttps-配置可选)
- [10. 常用运维命令](#10-常用运维命令)
- [故障排查](#故障排查)

---

## 环境要求

| 组件 | 版本要求 |
|------|---------|
| Ubuntu | 20.04 LTS 或更高版本 |
| Python | 3.11+ |
| Node.js | 18+ |
| Nginx | 1.18+ |
| DashScope API Key | 阿里云百炼平台 |

---

## 1. 系统准备

### 更新系统

```bash
sudo apt update && sudo apt upgrade -y
```

### 安装基础依赖

```bash
sudo apt install -y curl wget git build-essential
```

### 创建项目目录

```bash
sudo mkdir -p /var/LLMImageRender
sudo chown $USER:$USER /var/LLMImageRender
```

### 克隆项目

```bash
cd /var/LLMImageRender
git clone <你的仓库地址> .
# 或者使用 scp/rsync 从本地上传
# scp -r ./LLMImageRender user@server:/var/LLMImageRender/
```

---

## 2. 安装 Python 环境

### 安装 Python 3.11

```bash
# 添加 Python 3.11 PPA
sudo add-apt-repository ppa:deadsnakes/ppa -y
sudo apt update

# 安装 Python 3.11 及相关工具
sudo apt install -y python3.11 python3.11-venv python3.11-dev python3-pip
```

### 验证安装

```bash
python3.11 --version
# 应输出: Python 3.11.x
```

### 创建虚拟环境

```bash
cd /var/LLMImageRender/backend

# 创建虚拟环境
python -m venv venv

# 激活虚拟环境
source venv/bin/activate

# 升级 pip
pip install --upgrade pip
```

### 安装后端依赖

```bash
pip install -r requirements.txt
```

---

## 3. 安装 Node.js 环境

### 使用 NodeSource 安装 Node.js 18

```bash
# 添加 NodeSource 仓库
curl -fsSL https://deb.nodesource.com/setup_18.x | sudo -E bash -

# 安装 Node.js
sudo apt install -y nodejs

# 验证安装
node --version  # 应输出: v18.x.x
npm --version   # 应输出: 9.x.x 或更高
```

### 安装前端依赖

```bash
cd /var/LLMImageRender/frontend

# 安装依赖
npm install
```

---

## 4. 部署后端服务

### 配置环境变量

```bash
cd /var/LLMImageRender/backend

# 从模板创建 .env 文件
cp .env.example .env

# 编辑 .env 文件，填入你的 DashScope API Key
nano .env
```

> **必填项**: `DASHSCOPE_API_KEY` 必须配置为实际值，否则 AI 渲染功能无法使用。
> 其他配置项可使用默认值。

### .env 主要配置项

| 变量 | 说明 | 示例值 |
|------|------|--------|
| `DASHSCOPE_API_KEY` | 阿里云 DashScope API 密钥 | `sk-xxxx` |
| `DATABASE_URL` | 数据库连接串 | `sqlite:///./llm_image_render.db` |
| `UPLOAD_DIR` | 上传图片存储目录 | `render_static/uploads` |
| `GALLERY_DIR` | 图库图片存储目录 | `render_static/gallery` |
| `RESULT_DIR` | 渲染结果存储目录 | `render_static/results` |
| `MAX_UPLOAD_SIZE_MB` | 最大上传大小（MB） | `10` |
| `CORS_ORIGINS` | 跨域允许来源（逗号分隔） | `http://localhost:5175` |

### 创建静态资源目录

```bash
# 后端启动时会自动创建以下目录，也可手动创建
mkdir -p /var/LLMImageRender/backend/render_static/uploads
mkdir -p /var/LLMImageRender/backend/render_static/gallery
mkdir -p /var/LLMImageRender/backend/render_static/results
```

### 导入种子数据（可选）

```bash
cd /var/LLMImageRender/backend
source venv/bin/activate

# 导入示例图库数据
python seed.py
```

### 测试后端启动

```bash
cd /var/LLMImageRender/backend
source venv/bin/activate

# 测试运行
uvicorn app.main:app --host 127.0.0.1 --port 8002

# 如果看到类似以下输出表示成功:
# INFO:     Started server process [xxxxx]
# INFO:     Waiting for application startup.
# INFO:     [应用启动] 初始化数据库...
# INFO:     [应用启动] 数据库初始化完成
# INFO:     [应用启动] LLMImageRender API 启动成功!
# INFO:     Uvicorn running on http://127.0.0.1:8002

# 按 Ctrl+C 停止测试
```

### 验证健康检查

```bash
curl http://127.0.0.1:8002/render_api/health
# 应返回: {"status":"ok","service":"LLMImageRender"}
```

---

## 5. 构建前端

### 前端路径配置说明

前端已配置为部署到 `/llmimagerender/` 子路径：

- `vite.config.ts` 中 `base: '/llmimagerender/'`
- `src/router/index.ts` 中 `createWebHistory('/llmimagerender/')`
- 开发环境通过 Vite 代理 `/render_api` 和 `/render_static` 到后端

### 构建生产版本

```bash
cd /var/LLMImageRender/frontend
npm run build
```

构建完成后，静态文件将生成在 `frontend/dist/` 目录。

### 复制静态文件到 Nginx 目录

```bash
sudo mkdir -p /var/www/llmimagerender
sudo rm -rf /var/www/llmimagerender/*
sudo cp -r /var/LLMImageRender/frontend/dist/* /var/www/llmimagerender/
sudo chown -R www-data:www-data /var/www/llmimagerender
```

---

## 6. 配置 Nginx

### 安装 Nginx

```bash
sudo apt install -y nginx
```

### 创建站点配置

```bash
sudo nano /etc/nginx/sites-available/LLMImageRender
```

### Nginx 配置内容

```nginx
# 静态文件目录结构:
# /var/www/llmimagerender/
# ├── index.html
# └── assets/
#     ├── index-xxx.js
#     └── index-xxx.css

# LLMImageRender 前端 - 路径: /llmimagerender
location /llmimagerender {
    root /var/www;
    index index.html;
    try_files $uri $uri/ /llmimagerender/index.html;
}

# API 代理
location /render_api/ {
    proxy_pass http://127.0.0.1:8002/render_api/;
    proxy_set_header Host $host;
    proxy_set_header X-Real-IP $remote_addr;
    proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
    proxy_set_header X-Forwarded-Proto $scheme;
}

# 静态资源代理（图片、上传文件、渲染结果）
location ^~ /render_static/ {
    proxy_pass http://127.0.0.1:8002/render_static/;
    proxy_set_header Host $host;
    proxy_set_header X-Real-IP $remote_addr;
    proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
    proxy_set_header X-Forwarded-Proto $scheme;
}

# 静态资源缓存
location ~* /llmimagerender/.*\.(js|css|png|jpg|jpeg|gif|ico|svg|woff|woff2|ttf|eot)$ {
    root /var/www;
    expires 1y;
    add_header Cache-Control "public, immutable";
}
```

> **注意**: 以上 location 配置应添加到 Nginx 的 `server {}` 块中。如果服务器上只有一个站点，可以直接替换默认配置；如果已有其他站点，将 location 块添加到现有 server 配置中。

### 完整 Nginx 配置示例（独立站点）

```nginx
server {
    listen 80;
    server_name your-domain.com;  # 替换为你的域名或 IP

    # LLMImageRender 前端
    location /llmimagerender {
        root /var/www;
        index index.html;
        try_files $uri $uri/ /llmimagerender/index.html;
    }

    # API 代理
    location /render_api/ {
        proxy_pass http://127.0.0.1:8002/render_api/;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }

    # 静态资源代理
    location ^~ /render_static/ {
        proxy_pass http://127.0.0.1:8002/render_static/;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }

    # 前端静态资源缓存
    location ~* /llmimagerender/.*\.(js|css|png|jpg|jpeg|gif|ico|svg|woff|woff2|ttf|eot)$ {
        root /var/www;
        expires 1y;
        add_header Cache-Control "public, immutable";
    }
}
```

### 部署静态文件

```bash
# 创建目录
sudo mkdir -p /var/www/llmimagerender

# 复制构建产物
sudo cp -r /var/LLMImageRender/frontend/dist/* /var/www/llmimagerender/

# 设置权限
sudo chown -R www-data:www-data /var/www/llmimagerender

# 验证文件结构
ls -la /var/www/llmimagerender/
# 应该看到: index.html  assets/
```

### 启用站点

```bash
# 创建符号链接
sudo ln -s /etc/nginx/sites-available/LLMImageRender /etc/nginx/sites-enabled/

# 删除默认站点（可选）
sudo rm /etc/nginx/sites-enabled/default

# 测试配置
sudo nginx -t

# 重载 Nginx
sudo systemctl reload nginx
```

---

## 7. 配置 Systemd 服务

### 创建后端服务文件

```bash
sudo nano /etc/systemd/system/LLMImageRender.service
```

### 服务配置内容

```ini
[Unit]
Description=LLMImageRender Backend
After=network.target

[Service]
Type=simple
User=root
Group=root
WorkingDirectory=/var/LLMImageRender/backend
Environment="PATH=/var/LLMImageRender/backend/venv/bin"
EnvironmentFile=/var/LLMImageRender/backend/.env
ExecStart=/var/LLMImageRender/backend/venv/bin/uvicorn app.main:app --host 127.0.0.1 --port 8002 --workers 1
Restart=always
RestartSec=5

[Install]
WantedBy=multi-user.target
```

> **注意**: 使用 root 用户运行可以避免文件权限问题。如果需要更安全的配置，请创建专用用户并设置相应目录权限。

### 设置目录权限

```bash
# 确保项目目录可访问
sudo chmod -R 755 /var/LLMImageRender

# 确保静态资源目录可写（上传图片、渲染结果）
sudo chmod -R 777 /var/LLMImageRender/backend/render_static
```

### 启动服务

```bash
# 重载 systemd 配置
sudo systemctl daemon-reload

# 启动服务
sudo systemctl start LLMImageRender

# 设置开机自启
sudo systemctl enable LLMImageRender

# 查看服务状态
sudo systemctl status LLMImageRender
```

---

## 8. 防火墙配置

### 使用 UFW 配置防火墙

```bash
# 启用防火墙
sudo ufw enable

# 允许 SSH
sudo ufw allow ssh

# 允许 HTTP
sudo ufw allow 80/tcp

# 允许 HTTPS（如果需要）
sudo ufw allow 443/tcp

# 查看防火墙状态
sudo ufw status
```

> **注意**: 后端运行在 `127.0.0.1:8002`，仅本机可访问，无需开放 8002 端口。外部请求通过 Nginx 80/443 端口转发。

---

## 9. SSL/HTTPS 配置（可选）

### 使用 Let's Encrypt 免费证书

```bash
# 安装 Certbot
sudo apt install -y certbot python3-certbot-nginx

# 获取证书
sudo certbot --nginx -d your-domain.com

# 自动续期测试
sudo certbot renew --dry-run
```

Certbot 会自动修改 Nginx 配置，添加 HTTPS 支持。

---

## 10. 常用运维命令

### 服务管理

```bash
# 启动后端服务
sudo systemctl start LLMImageRender

# 停止后端服务
sudo systemctl stop LLMImageRender

# 重启后端服务
sudo systemctl restart LLMImageRender

# 查看服务状态
sudo systemctl status LLMImageRender

# 查看服务日志
sudo journalctl -u LLMImageRender -f

# 查看最近 100 行日志
sudo journalctl -u LLMImageRender -n 100
```

### Nginx 管理

```bash
# 测试配置
sudo nginx -t

# 重载配置
sudo systemctl reload nginx

# 重启 Nginx
sudo systemctl restart nginx

# 查看 Nginx 日志
sudo tail -f /var/log/nginx/access.log
sudo tail -f /var/log/nginx/error.log
```

### 更新项目

```bash
cd /var/LLMImageRender

# 拉取最新代码
git pull origin main

# 更新后端依赖
cd backend
source venv/bin/activate
pip install -r requirements.txt

# 重新构建前端
cd ../frontend
npm install
npm run build

# 清空旧文件
sudo rm -rf /var/www/llmimagerender/*

# 复制新的静态文件
sudo cp -r dist/* /var/www/llmimagerender/
sudo chown -R www-data:www-data /var/www/llmimagerender

# 重启后端服务
sudo systemctl restart LLMImageRender
```

### 数据库备份

```bash
# 备份 SQLite 数据库
cp /var/LLMImageRender/backend/llm_image_render.db /var/LLMImageRender/backend/llm_image_render.db.backup.$(date +%Y%m%d)

# 定时备份（添加到 crontab）
# 每天凌晨 3 点备份
0 3 * * * cp /var/LLMImageRender/backend/llm_image_render.db /var/LLMImageRender/backend/llm_image_render.db.backup.$(date +\%Y\%m\%d).db
```

---

## 故障排查

### 1. 后端服务无法启动

```bash
# 查看详细日志
sudo journalctl -u LLMImageRender -n 50 --no-pager

# 手动测试启动
cd /var/LLMImageRender/backend
source venv/bin/activate
uvicorn app.main:app --host 127.0.0.1 --port 8002
```

### 2. 前端显示空白

```bash
# 检查静态文件是否存在
ls -la /var/www/llmimagerender/

# 检查 Nginx 配置
sudo nginx -t

# 检查浏览器控制台是否有错误
# 确认访问路径为 http://your-domain.com/llmimagerender/
```

### 3. API 请求 404

```bash
# 确认后端服务正在运行
curl http://127.0.0.1:8002/render_api/health
# 应返回: {"status":"ok","service":"LLMImageRender"}

# 检查 Nginx 代理配置
sudo nginx -t

# 确认 /render_api/ 代理配置正确
```

### 4. 图片无法显示

```bash
# 检查静态资源目录是否存在且有内容
ls -la /var/LLMImageRender/backend/render_static/uploads/
ls -la /var/LLMImageRender/backend/render_static/gallery/
ls -la /var/LLMImageRender/backend/render_static/results/

# 测试静态资源访问
curl -I http://127.0.0.1:8002/render_static/gallery/wardrobe/cabinet-main.png
# 应返回 200 OK

# 检查 Nginx /render_static/ 代理配置
```

### 5. 图片上传失败

```bash
# 检查上传目录权限
ls -la /var/LLMImageRender/backend/render_static/uploads/

# 确认目录可写
sudo chmod -R 777 /var/LLMImageRender/backend/render_static

# 检查文件大小限制
# 默认限制 10MB，可在 .env 中修改 MAX_UPLOAD_SIZE_MB
```

### 6. 权限问题

```bash
# 修复文件权限
sudo chown -R www-data:www-data /var/LLMImageRender
sudo chown -R www-data:www-data /var/www/llmimagerender
sudo chmod -R 755 /var/LLMImageRender
sudo chmod -R 777 /var/LLMImageRender/backend/render_static
```

---

## 性能优化（可选）

### 1. 增加 Worker 数量

编辑 `/etc/systemd/system/LLMImageRender.service`：

```ini
ExecStart=/var/LLMImageRender/backend/venv/bin/uvicorn app.main:app --host 127.0.0.1 --port 8002 --workers 4
```

> **注意**: Worker 数量建议设置为 CPU 核心数的 1-2 倍。AI 渲染任务较重，不建议设置过多 Worker。

### 2. Nginx 上传大小限制

在 Nginx 配置的 `server` 块中添加：

```nginx
# 允许上传大文件（根据实际需求调整）
client_max_body_size 20M;
```

### 3. Nginx 缓存优化

在 `nginx.conf` 的 `http` 块中添加：

```nginx
# 代理缓存
proxy_cache_path /var/cache/nginx levels=1:2 keys_zone=api_cache:10m max_size=100m inactive=60m;
```

---

## 完整部署检查清单

- [ ] Ubuntu 系统已更新
- [ ] Python 3.11+ 已安装
- [ ] Node.js 18+ 已安装
- [ ] 项目代码已克隆/上传
- [ ] Python 虚拟环境已创建
- [ ] 后端依赖已安装
- [ ] `.env` 文件已配置（包含正确的 `DASHSCOPE_API_KEY`）
- [ ] 种子数据已导入（可选）
- [ ] 后端服务可以手动启动
- [ ] 健康检查接口返回正常
- [ ] 前端已构建（`npm run build`）
- [ ] 静态文件已复制到 `/var/www/llmimagerender/`
- [ ] Nginx 已配置并启用
- [ ] Systemd 服务已创建并启动
- [ ] 防火墙已配置
- [ ] 服务已设置开机自启
- [ ] 浏览器可以正常访问 `http://your-domain.com/llmimagerender/`

---

如有问题，请查看项目日志或提交 Issue。

**日志位置**:
- 后端日志: `sudo journalctl -u LLMImageRender`
- Nginx 访问日志: `/var/log/nginx/access.log`
- Nginx 错误日志: `/var/log/nginx/error.log`
