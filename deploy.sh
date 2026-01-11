#!/bin/bash

# FocusEye 快速部署脚本

echo "🚀 FocusEye 快速部署脚本"
echo "========================="

# 检查 Node.js
if ! command -v node &> /dev/null; then
    echo "❌ 未检测到 Node.js，请先安装 Node.js"
    exit 1
fi

# 检查 Python
if ! command -v python3 &> /dev/null; then
    echo "❌ 未检测到 Python 3，请先安装 Python 3"
    exit 1
fi

# 检查环境变量文件
if [ ! -f .env ]; then
    echo "⚠️  未找到 .env 文件，从模板复制..."
    cp .env.example .env
    echo "✅ 已创建 .env 文件，请编辑并填入你的配置"
    echo "📝 编辑 .env 文件："
    echo "   API_KEY=your_api_key"
    echo "   API_BASE=https://igw.livzon.cn/ai/qwenvl/v1"
    echo "   MODEL_NAME=qwen3-vl:32b"
    exit 1
fi

echo "📦 安装后端依赖..."
pip3 install -r requirements.txt

echo "📦 安装前端依赖..."
cd frontend
npm install
cd ..

echo ""
echo "✅ 安装完成！"
echo ""
echo "🌐 部署选项："
echo "   1. 本地开发："
echo "      vercel dev"
echo ""
echo "   2. 部署到 Vercel："
echo "      vercel --prod"
echo ""
echo "   3. 仅启动前端："
echo "      cd frontend && npm run dev"
echo ""
