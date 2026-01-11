# 🎯 FocusEye - AI 学习监督工具

基于 Web 的轻量级 AI 监督工具，通过摄像头实时监控学习/工作状态，提供智能语音反馈。

## 📋 功能特性

- 🎥 实时摄像头监控（移动端/PC端）
- 🤖 AI 多模态分析（Qwen-VL）
- 🔊 智能语音反馈（TTS）
- ⚡ 极低延迟（无存储）
- 📱 移动端适配（前置摄像头）

## 🛠️ 技术栈

### 前端
- Vue 3 + Vite
- TypeScript
- Web APIs (getUserMedia, Canvas, TTS)

### 后端
- Python 3.12
- LangChain 1.2+
- Vercel Serverless Functions

### AI 服务
- Qwen-VL (qwen3-vl:32b)
- OpenAI Compatible API

## 📁 项目结构

```
AIaccompany/
├── api/                  # Vercel Serverless API
│   └── index.py
├── backend/              # Python 后端逻辑
│   ├── config/          # 配置管理
│   ├── client/          # LLM 客户端
│   ├── Agent/           # AI Agent 逻辑
│   ├── utils/           # 工具函数
│   └── service/         # 业务服务
├── frontend/             # Vue 3 前端
│   ├── src/
│   ├── public/
│   └── package.json
├── requirements.txt      # Python 依赖
├── vercel.json          # Vercel 部署配置
└── .env.example         # 环境变量示例
```

## 🚀 快速开始

### 1. 环境配置

```bash
# 复制环境变量模板
cp .env.example .env

# 编辑 .env 文件，填入你的配置
# API_KEY=your_api_key
# API_BASE=https://igw.livzon.cn/ai/qwenvl/v1
# MODEL_NAME=qwen3-vl:32b
```

### 2. 后端开发

```bash
# 安装 Python 依赖
pip install -r requirements.txt

# 本地测试（需要 vercel CLI）
vercel dev
```

### 3. 前端开发

```bash
cd frontend
npm install
npm run dev
```

### 4. 部署到 Vercel

```bash
# 安装 Vercel CLI
npm i -g vercel

# 部署
vercel --prod
```

## 📝 使用说明

1. **移动端使用**：将手机架设在旁边，打开浏览器访问应用
2. **PC端使用**：直接在电脑浏览器打开应用
3. **授权摄像头**：首次使用需要授权摄像头权限
4. **开始监督**：点击开始按钮，AI 将每20秒分析一次状态
5. **语音反馈**：根据检测结果播放相应的语音提示

## 🔒 隐私说明

- ✅ 所有图像仅用于实时分析，不会存储
- ✅ 数据传输使用 HTTPS 加密
- ✅ 支持本地部署，完全掌控数据

## 📄 License

MIT License
# FocusEye
