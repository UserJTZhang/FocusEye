# ⚡ FocusEye 快速开始指南

## 🎯 5 分钟快速上手

### 步骤 1: 克隆并配置项目

```bash
# 进入项目目录（你已经在这里了）
cd /Users/zhangjintai/Desktop/project/Code/AIaccompany

# 复制环境变量文件（已经创建好了）
# .env 文件已配置完成，内容如下：
# API_KEY=apikey
# API_BASE=https://igw.livzon.cn/ai/qwenvl/v1
# MODEL_NAME=qwen3-vl:32b
```

### 步骤 2: 安装依赖

```bash
# 安装 Python 依赖
pip3 install -r requirements.txt

# 安装前端依赖
cd frontend
npm install
cd ..
```

### 步骤 3: 测试后端

```bash
# 运行测试脚本，验证配置是否正确
python3 test_backend.py
```

期望输出：
```
==================================================
FocusEye 后端功能测试
==================================================

🔍 测试健康检查...
   状态: healthy
   成功: True
   模型: qwen3-vl:32b
   API: https://igw.livzon.cn/ai/qwen...

✅ 测试完成
```

### 步骤 4: 启动开发服务器

#### 方式一：使用 Vercel Dev（推荐）

```bash
# 安装 Vercel CLI（如果还没安装）
npm i -g vercel

# 启动开发服务器
vercel dev
```

访问 http://localhost:3000

#### 方式二：分别启动前后端

**终端 1 - 后端**:
```bash
# 使用 Python 的简单 HTTP 服务器
cd api
python3 -m http.server 5000
```

**终端 2 - 前端**:
```bash
cd frontend
npm run dev
```

访问 http://localhost:3000

### 步骤 5: 使用应用

1. **打开浏览器**: 访问 http://localhost:3000
2. **授权摄像头**: 点击"开启摄像头"，允许浏览器访问
3. **开始监督**: 点击"开始监督"，系统每 20 秒分析一次
4. **查看反馈**: 在页面上查看状态指示灯和语音反馈

## 📱 移动端测试

### 方法一：使用 ngrok（推荐）

```bash
# 安装 ngrok
brew install ngrok  # macOS
# 或访问 https://ngrok.com 下载

# 启动服务后，创建公网隧道
ngrok http 3000
```

使用 ngrok 提供的 HTTPS URL 在手机浏览器中访问。

### 方法二：局域网访问

```bash
# 1. 获取本机 IP
ifconfig | grep "inet " | grep -v 127.0.0.1

# 2. 在手机浏览器访问
# http://YOUR_IP:3000
```

**注意**: 摄像头需要 HTTPS 或 localhost，局域网 HTTP 可能无法访问摄像头。

## 🚀 部署到生产环境

### 部署到 Vercel

```bash
# 1. 登录 Vercel
vercel login

# 2. 部署到生产环境
vercel --prod

# 3. 在 Vercel Dashboard 配置环境变量
# - API_KEY: apikey
# - API_BASE: https://igw.livzon.cn/ai/qwenvl/v1
# - MODEL_NAME: qwen3-vl:32b
```

部署完成后，Vercel 会提供一个 HTTPS URL，可在任何设备访问。

## 🔧 常见问题

### Q1: 安装依赖时出错？

```bash
# 确保 Python 版本 >= 3.12
python3 --version

# 确保 pip 是最新版
pip3 install --upgrade pip

# 使用虚拟环境（推荐）
python3 -m venv venv
source venv/bin/activate  # macOS/Linux
pip install -r requirements.txt
```

### Q2: 摄像头无法访问？

- ✅ 使用 HTTPS 或 localhost
- ✅ 检查浏览器权限设置
- ✅ 确认摄像头未被其他应用占用
- ✅ 尝试其他浏览器（Chrome/Safari）

### Q3: API 调用失败？

```bash
# 检查环境变量
cat .env

# 检查网络连接
curl https://igw.livzon.cn/ai/qwenvl/v1/chat/completions

# 查看日志
vercel dev --debug
```

### Q4: 前端无法连接后端？

检查 `frontend/vite.config.js` 中的 proxy 配置：
```js
proxy: {
  '/api': {
    target: 'http://localhost:5000',
    changeOrigin: true
  }
}
```

### Q5: 语音无法播放？

- ✅ 某些浏览器需要用户交互后才能播放
- ✅ 检查浏览器是否支持 Web Speech API
- ✅ 确认音量未静音

## 📊 监督效果优化

### 调整监督间隔

编辑 `.env` 文件：
```bash
MONITOR_INTERVAL=15  # 改为 15 秒
```

### 调整图片质量

编辑 `.env` 文件：
```bash
MAX_IMAGE_SIZE=1024  # 提高分辨率
IMAGE_QUALITY=0.7    # 提高质量
```

### 调整摄像头位置

- **移动端**: 将手机架在正对面，距离 30-50cm
- **PC 端**: 调整摄像头角度，确保能拍到上半身
- **光线**: 保证充足的光线，避免逆光

## 🎨 自定义配置

### 修改 Prompt

编辑 `backend/Agent/prompts.py` 中的 `SYSTEM_PROMPT`：
```python
SYSTEM_PROMPT = """你是 FocusEye，一个友善但严格的学习监督助手。

[在这里自定义你的 Prompt]
"""
```

### 修改 UI 主题

编辑 `frontend/src/App.vue` 中的 `<style>` 部分：
```css
.app-container {
  background: #000;  /* 修改背景色 */
}

.status-focused .dot {
  background: #4caf50;  /* 修改状态指示灯颜色 */
}
```

## 📚 进一步学习

- [LangChain 文档](https://docs.langchain.com)
- [Vue 3 文档](https://vuejs.org)
- [Vercel 文档](https://vercel.com/docs)
- [Web Speech API](https://developer.mozilla.org/en-US/docs/Web/API/Web_Speech_API)

## 💬 获取帮助

遇到问题？查看：
- 📄 [项目结构说明](PROJECT_STRUCTURE.md)
- 📄 [部署指南](DEPLOY.md)
- 📄 [README](README.md)

---

🎉 **现在开始使用 FocusEye，保持专注，高效学习！**
