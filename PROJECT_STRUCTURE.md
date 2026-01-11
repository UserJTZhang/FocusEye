# 📂 FocusEye 项目结构说明

## 📁 完整目录树

```
AIaccompany/
├── 📄 README.md                 # 项目说明文档
├── 📄 DEPLOY.md                 # 部署指南
├── 📄 .gitignore                # Git 忽略配置
├── 📄 .env                      # 环境变量（本地）
├── 📄 .env.example              # 环境变量模板
├── 📄 requirements.txt          # Python 依赖
├── 📄 vercel.json               # Vercel 部署配置
├── 📄 deploy.sh                 # 快速部署脚本
├── 📄 test_backend.py           # 后端测试脚本
│
├── 📁 api/                      # Vercel Serverless API
│   └── 📄 index.py              # API 入口（HTTP Handler）
│
├── 📁 backend/                  # Python 后端核心逻辑
│   ├── 📄 __init__.py
│   │
│   ├── 📁 config/               # 配置管理层
│   │   ├── 📄 __init__.py
│   │   └── 📄 settings.py       # 环境变量加载与配置
│   │
│   ├── 📁 client/               # LLM 客户端层
│   │   ├── 📄 __init__.py
│   │   └── 📄 llm_client.py     # LangChain ChatOpenAI 封装
│   │
│   ├── 📁 Agent/                # AI Agent 逻辑层
│   │   ├── 📄 __init__.py
│   │   ├── 📄 prompts.py        # Prompt 模板与数据模型
│   │   └── 📄 supervisor.py     # 监督 Agent 实现
│   │
│   ├── 📁 utils/                # 工具函数层
│   │   ├── 📄 __init__.py
│   │   └── 📄 image_tool.py     # Base64 图片处理工具
│   │
│   └── 📁 service/              # 业务服务层
│       ├── 📄 __init__.py
│       └── 📄 monitor.py        # 监督服务核心逻辑
│
└── 📁 frontend/                 # Vue 3 前端
    ├── 📄 package.json          # 前端依赖配置
    ├── 📄 vite.config.js        # Vite 构建配置
    ├── 📄 index.html            # HTML 入口
    │
    └── 📁 src/
        ├── 📄 main.js           # Vue 应用入口
        ├── 📄 App.vue           # 主组件（完整 UI）
        │
        └── 📁 utils/            # 前端工具函数
            ├── 📄 camera.js     # 摄像头与图片处理
            ├── 📄 api.js        # API 通信
            ├── 📄 tts.js        # 语音合成（TTS）
            └── 📄 format.js     # 格式化工具
```

## 🔧 各模块职责说明

### 后端 (Backend)

#### 1. **config 层** - 配置管理
- `settings.py`: 加载 `.env` 环境变量，提供全局配置常量
- 导出: `API_KEY`, `API_BASE`, `MODEL_NAME` 等

#### 2. **client 层** - LLM 客户端
- `llm_client.py`: 封装 LangChain 的 `ChatOpenAI` 客户端
- 配置 Qwen-VL API 的 base_url、api_key、model 等
- 提供单例模式获取客户端

#### 3. **Agent 层** - AI 逻辑核心
- `prompts.py`: 
  - 定义 `SupervisorResponse` Pydantic 模型
  - 定义 System Prompt（监工角色）
  - 创建 User Message（包含图片）
- `supervisor.py`:
  - 实现 `SupervisorAgent` 类
  - 组装 Chain: System Prompt + User Message + Image
  - 调用 LLM 分析图片
  - 解析结构化输出

#### 4. **utils 层** - 工具函数
- `image_tool.py`:
  - Base64 图片格式验证
  - 图片大小检查
  - Data URI 规范化处理

#### 5. **service 层** - 业务服务
- `monitor.py`:
  - `MonitorService` 类：核心业务逻辑
  - `analyze_user_status()`: 图片验证 → Agent 分析 → 格式化结果
  - `health_check()`: 服务健康检查

#### 6. **api 层** - HTTP 入口
- `api/index.py`:
  - Vercel Serverless Function 入口
  - 路由处理：`/api/analyze`, `/api/health`
  - CORS 配置
  - 错误处理

### 前端 (Frontend)

#### 1. **App.vue** - 主应用组件
- 摄像头视频流管理
- UI 状态管理（待机/专注/分心/离开）
- 定时器控制（20秒一次检查）
- 统计信息展示（运行时长、检查次数、专注时长）

#### 2. **utils/camera.js** - 摄像头工具
- `captureImage()`: 从视频流截图并压缩
- `requestCamera()`: 请求摄像头权限
- `stopMediaStream()`: 停止媒体流

#### 3. **utils/api.js** - API 通信
- `analyzeImage()`: 调用后端分析接口
- `checkHealth()`: 健康检查接口
- 统一错误处理

#### 4. **utils/tts.js** - 语音合成
- `SpeechQueue` 类：语音播放队列
- `speakMessage()`: 播放语音反馈
- 使用 Web Speech API

#### 5. **utils/format.js** - 格式化工具
- `formatTime()`: 毫秒转 HH:MM:SS
- `formatDate()`: 日期格式化
- `formatFileSize()`: 文件大小格式化

## 🔄 核心数据流

```
用户画面
  ↓
[前端] 摄像头捕获
  ↓
[前端] Canvas 压缩（800px, 0.5 质量）
  ↓
[前端] Base64 编码
  ↓
[前端] POST /api/analyze
  ↓
[后端 API] 接收请求
  ↓
[后端 Service] 验证图片格式
  ↓
[后端 Agent] 调用 Qwen-VL 分析
  ↓
[后端 Agent] 解析 JSON 响应
  ↓
[后端 Service] 格式化结果
  ↓
[后端 API] 返回 JSON
  ↓
[前端] 更新 UI 状态
  ↓
[前端 TTS] 播放语音反馈
```

## 🚀 快速启动

### 开发环境
```bash
# 1. 安装依赖
pip install -r requirements.txt
cd frontend && npm install

# 2. 配置环境变量
cp .env.example .env
# 编辑 .env 填入配置

# 3. 测试后端
python test_backend.py

# 4. 启动服务
vercel dev
```

### 生产部署
```bash
# 使用快速部署脚本
chmod +x deploy.sh
./deploy.sh

# 或直接部署到 Vercel
vercel --prod
```

## 📝 关键技术点

1. **LangChain 1.2+**:
   - 使用 `ChatOpenAI` 适配 Qwen-VL
   - 使用 `PydanticOutputParser` 结构化输出
   - 使用 `HumanMessage` + `SystemMessage` 构建对话

2. **多模态输入**:
   - 使用 OpenAI 格式的 `image_url` 传参
   - Base64 Data URI 编码

3. **前端优化**:
   - Canvas 图片压缩（减少传输）
   - Page Visibility API（防后台运行）
   - Web Speech API（语音反馈）

4. **Vercel 部署**:
   - Serverless Functions（Python）
   - 静态站点托管（Vue）
   - 环境变量管理

## 🔒 安全与隐私

- ✅ 图片不存储，仅实时分析
- ✅ HTTPS 加密传输
- ✅ 环境变量管理敏感信息
- ✅ CORS 配置保护 API
