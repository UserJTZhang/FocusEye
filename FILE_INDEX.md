# 📑 FocusEye 项目文件索引

快速查找项目中的任何文件和功能。

---

## 🎯 我想要...

### 🏃‍♂️ 快速开始
- **第一次使用?** → 阅读 [QUICKSTART.md](QUICKSTART.md)
- **想了解项目?** → 阅读 [README.md](README.md)
- **准备部署?** → 阅读 [DEPLOY.md](DEPLOY.md)
- **深入架构?** → 阅读 [PROJECT_STRUCTURE.md](PROJECT_STRUCTURE.md)
- **项目总结?** → 阅读 [PROJECT_COMPLETE.md](PROJECT_COMPLETE.md)

### 🔧 修改配置
- **API 配置** → [.env](.env)
- **Python 依赖** → [requirements.txt](requirements.txt)
- **前端依赖** → [frontend/package.json](frontend/package.json)
- **Vercel 配置** → [vercel.json](vercel.json)

### 🐛 调试问题
- **测试后端** → 运行 `python3 test_backend.py`
- **查看 API 入口** → [api/index.py](api/index.py)
- **查看服务逻辑** → [backend/service/monitor.py](backend/service/monitor.py)
- **查看前端逻辑** → [frontend/src/App.vue](frontend/src/App.vue)

### ✏️ 修改功能

#### 修改 AI Prompt
- **位置**: [backend/Agent/prompts.py](backend/Agent/prompts.py)
- **变量**: `SYSTEM_PROMPT`
- **说明**: 定义监工角色、反馈风格、输出规则

#### 修改监督间隔
- **位置**: [.env](.env)
- **变量**: `MONITOR_INTERVAL=20`
- **说明**: 修改数字即可（单位：秒）

#### 修改图片质量
- **位置**: [.env](.env)
- **变量**: 
  - `MAX_IMAGE_SIZE=800` (最大边长)
  - `IMAGE_QUALITY=0.5` (压缩质量 0-1)

#### 修改 UI 样式
- **位置**: [frontend/src/App.vue](frontend/src/App.vue)
- **区域**: `<style scoped>` 部分
- **说明**: 修改颜色、布局、字体等

#### 修改语音反馈
- **位置**: [frontend/src/utils/tts.js](frontend/src/utils/tts.js)
- **函数**: `speakMessage()`
- **说明**: 可调整语速、音调、音量

---

## 📂 文件功能索引

### 后端文件

| 文件 | 功能 | 何时修改 |
|------|------|----------|
| [api/index.py](api/index.py) | HTTP 请求入口 | 需要添加新的 API 端点 |
| [backend/config/settings.py](backend/config/settings.py) | 配置加载 | 需要添加新的配置项 |
| [backend/client/llm_client.py](backend/client/llm_client.py) | LLM 客户端 | 需要更换模型或调整参数 |
| [backend/Agent/prompts.py](backend/Agent/prompts.py) | Prompt 模板 | 需要修改 AI 行为 |
| [backend/Agent/supervisor.py](backend/Agent/supervisor.py) | Agent 逻辑 | 需要修改分析逻辑 |
| [backend/utils/image_tool.py](backend/utils/image_tool.py) | 图片处理 | 需要修改图片验证规则 |
| [backend/service/monitor.py](backend/service/monitor.py) | 业务逻辑 | 需要修改业务流程 |

### 前端文件

| 文件 | 功能 | 何时修改 |
|------|------|----------|
| [frontend/src/App.vue](frontend/src/App.vue) | 主应用界面 | 需要修改 UI 或交互 |
| [frontend/src/utils/camera.js](frontend/src/utils/camera.js) | 摄像头处理 | 需要修改截图逻辑 |
| [frontend/src/utils/api.js](frontend/src/utils/api.js) | API 调用 | 需要修改接口调用 |
| [frontend/src/utils/tts.js](frontend/src/utils/tts.js) | 语音合成 | 需要修改语音播放 |
| [frontend/src/utils/format.js](frontend/src/utils/format.js) | 格式化工具 | 需要添加格式化函数 |

### 配置文件

| 文件 | 功能 | 何时修改 |
|------|------|----------|
| [.env](.env) | 环境变量 | 修改 API Key、模型等 |
| [requirements.txt](requirements.txt) | Python 依赖 | 添加新的 Python 包 |
| [frontend/package.json](frontend/package.json) | 前端依赖 | 添加新的 npm 包 |
| [vercel.json](vercel.json) | Vercel 配置 | 修改部署设置 |
| [frontend/vite.config.js](frontend/vite.config.js) | Vite 配置 | 修改构建设置 |

---

## 🔍 常见任务快速查找

### 任务 1: 更换 AI 模型
1. 修改 [.env](.env) 中的 `MODEL_NAME`
2. 修改 [.env](.env) 中的 `API_BASE`（如果需要）
3. 重启服务

### 任务 2: 修改反馈语气
1. 编辑 [backend/Agent/prompts.py](backend/Agent/prompts.py)
2. 修改 `SYSTEM_PROMPT` 中的反馈风格说明
3. 重启服务

### 任务 3: 调整监督频率
1. 编辑 [.env](.env)
2. 修改 `MONITOR_INTERVAL=20` 为其他数值
3. 重启服务（或前端会自动读取）

### 任务 4: 修改 UI 主题
1. 编辑 [frontend/src/App.vue](frontend/src/App.vue)
2. 在 `<style scoped>` 部分修改颜色变量
3. 保存即可（Vite 热更新）

### 任务 5: 添加新的 API 端点
1. 在 [api/index.py](api/index.py) 添加路由
2. 在 [backend/service/](backend/service/) 添加业务逻辑
3. 在 [frontend/src/utils/api.js](frontend/src/utils/api.js) 添加调用函数

### 任务 6: 部署到生产
1. 确保 [.env](.env) 配置正确
2. 运行 `vercel --prod`
3. 在 Vercel Dashboard 添加环境变量

---

## 🎨 UI 组件位置

| 组件 | 位置 (App.vue 中) | 功能 |
|------|-------------------|------|
| 视频预览 | `.video-container` | 显示摄像头画面 |
| 状态指示灯 | `.status-indicator` | 显示当前状态 |
| 反馈消息 | `.feedback-message` | 显示 AI 反馈文字 |
| 控制按钮 | `.button-group` | 开始/停止按钮 |
| 统计信息 | `.stats` | 运行时长等数据 |
| 加载动画 | `.loading-overlay` | 分析中提示 |

---

## 🔄 数据流追踪

**用户触发 → 分析完成的完整路径**:

1. **前端**: 用户点击"开始监督" → `startMonitoring()`
2. **前端**: 定时器触发 → `performCheck()`
3. **前端**: 截图 → `captureImage()` (utils/camera.js)
4. **前端**: 调用 API → `analyzeImage()` (utils/api.js)
5. **后端**: 接收请求 → `handler()` (api/index.py)
6. **后端**: 路由到服务 → `analyze_user_status()` (service/monitor.py)
7. **后端**: 验证图片 → `validate_base64_image()` (utils/image_tool.py)
8. **后端**: AI 分析 → `analyze_focus()` (Agent/supervisor.py)
9. **后端**: 调用模型 → `llm.invoke()` (client/llm_client.py)
10. **后端**: 返回结果 → JSON 响应
11. **前端**: 更新 UI → 状态指示灯变化
12. **前端**: 播放语音 → `speakMessage()` (utils/tts.js)

---

## 📞 技术支持

- **后端问题**: 查看 [backend/](backend/) 目录下的代码
- **前端问题**: 查看 [frontend/src/](frontend/src/) 目录下的代码
- **部署问题**: 查看 [DEPLOY.md](DEPLOY.md)
- **配置问题**: 查看 [.env](.env) 和各配置文件

---

## 🎓 学习资源

- **LangChain**: [backend/Agent/supervisor.py](backend/Agent/supervisor.py) - 查看实际使用示例
- **Vue 3**: [frontend/src/App.vue](frontend/src/App.vue) - 查看完整组件
- **Vercel**: [vercel.json](vercel.json) - 查看部署配置
- **Web APIs**: [frontend/src/utils/](frontend/src/utils/) - 查看浏览器 API 使用

---

**💡 提示**: 使用 Cmd+P (VS Code) 快速搜索文件名！
