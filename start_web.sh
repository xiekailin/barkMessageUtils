#!/bin/bash

# 微信红包提醒系统 - Web界面启动脚本

echo "🧧 微信红包提醒系统 - Web界面"
echo "================================"

# 检查Python是否安装
if ! command -v python &> /dev/null; then
    echo "❌ 错误：未找到Python，请先安装Python"
    exit 1
fi

# 检查依赖是否安装
if ! python -c "import flask, requests, schedule, dotenv" 2>/dev/null; then
    echo "📦 正在安装依赖包..."
    pip install -r requirements.txt
fi

# 检查.env文件是否存在
if [ ! -f ".env" ]; then
    echo "❌ 错误：未找到.env配置文件"
    echo "请复制 env.example 为 .env 并配置你的Bark推送URL"
    echo "命令：cp env.example .env"
    exit 1
fi

# 启动Web服务
echo "🌐 启动Web配置界面..."
echo "📱 请在浏览器中访问: http://localhost:9918"
echo "按 Ctrl+C 停止服务"
echo "================================"

python web_server.py 