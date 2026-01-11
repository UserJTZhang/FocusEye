# 🚀 FocusEye 部署指南

## 📋 部署前准备

### 1. 环境变量配置

复制 `.env.example` 为 `.env`，填入你的配置：

```bash
cp .env.example .env
```

编辑 `.env` 文件：

```bash
API_KEY=apikey
API_BASE=https://igw.livzon.cn/ai/qwenvl/v1
MODEL_NAME=qwen3-vl:32b
MONITOR_INTERVAL=20
MAX_IMAGE_SIZE=800
IMAGE_QUALITY=0.5
```

### 2. 安装依赖

#### 后端依赖
```bash
pip install -r requirements.txt
```

#### 前端依赖
```bash
cd frontend
npm install
```

## 🌐 部署到 Vercel

### 方法一：使用 Vercel CLI（推荐）

1. **安装 Vercel CLI**
```bash
npm i -g vercel
```

2. **登录 Vercel**
```bash
vercel login
```

3. **部署项目**
```bash
# 首次部署
vercel

# 生产环境部署
vercel --prod
```

4. **配置环境变量**

在部署过程中，Vercel 会提示你设置环境变量，或者在 Vercel Dashboard 中手动添加：

- `API_KEY`: apikey
- `API_BASE`: https://igw.livzon.cn/ai/qwenvl/v1
- `MODEL_NAME`: qwen3-vl:32b

### 方法二：通过 GitHub 自动部署

1. **推送代码到 GitHub**
```bash
git init
git add .
git commit -m "Initial commit"
git remote add origin <your-repo-url>
git push -u origin main
```

2. **在 Vercel 中导入项目**
   - 访问 https://vercel.com
   - 点击 "Import Project"
   - 选择你的 GitHub 仓库
   - 配置环境变量
   - 点击 "Deploy"

## 🧪 本地测试

### 启动后端（Vercel Dev 模式）
```bash
vercel dev
```

### 启动前端
```bash
cd frontend
npm run dev
```

访问 http://localhost:3000

## 📱 使用说明

### 移动端使用
1. 在手机浏览器中打开部署的 URL
2. 授权摄像头权限
3. 将手机架设在合适的位置
4. 点击"开始监督"

### PC 端使用
1. 在电脑浏览器中打开 URL
2. 授权摄像头权限
3. 调整摄像头角度
4. 点击"开始监督"

## 🔧 故障排除

### 问题 1: 摄像头无法访问
- 检查浏览器权限设置
- 确保使用 HTTPS 连接
- 尝试在其他浏览器中打开

### 问题 2: API 调用失败
- 检查 Vercel 环境变量是否正确配置
- 查看 Vercel Functions 日志
- 确认 API_BASE 和 API_KEY 是否有效

### 问题 3: 语音无法播放
- 某些浏览器需要用户交互后才能播放语音
- 检查浏览器是否支持 Web Speech API
- 尝试在设置中启用语音合成

## 📊 性能优化建议

1. **图片压缩**：已默认压缩至 800px，质量 0.5
2. **监督间隔**：默认 20 秒，可在 `.env` 中调整
3. **后台运行**：已实现 Page Visibility API 防止后台运行

## 🔒 隐私保护

- ✅ 所有图片仅用于实时分析，不存储
- ✅ 数据传输使用 HTTPS 加密
- ✅ 支持本地部署，完全掌控数据

## 📝 更新日志

### v1.0.0 (2026-01-10)
- ✨ 初始版本发布
- 🎥 支持摄像头实时监控
- 🤖 集成 Qwen-VL 多模态分析
- 🔊 智能语音反馈
- 📱 移动端/PC 端适配
