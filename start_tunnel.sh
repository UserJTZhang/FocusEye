#!/bin/bash

echo "🌐 启动 HTTPS 隧道（使用 localhost.run）"
echo "================================================"
echo ""
echo "⏳ 正在创建公网 HTTPS 隧道..."
echo ""
echo "📝 注意: 启动后会显示一个 HTTPS URL，用该 URL 在手机上访问"
echo ""

# 使用 SSH 隧道（localhost.run）
ssh -R 80:localhost:3000 nokey@localhost.run

echo ""
echo "================================================"
echo "✅ 隧道已关闭"
