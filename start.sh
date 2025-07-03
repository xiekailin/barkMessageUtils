#!/bin/bash

# 微信红包提醒系统启动脚本

echo "🧧 微信红包提醒系统"
echo "=================="

# 检查Python是否安装
if ! command -v python &> /dev/null; then
    echo "❌ 错误：未找到Python，请先安装Python"
    exit 1
fi

# 检查依赖是否安装
if ! python -c "import requests, schedule, dotenv" 2>/dev/null; then
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

# 显示菜单
show_menu() {
    echo ""
    echo "🔧 请选择操作："
    echo "1. 启动定时任务"
    echo "2. 测试推送功能"
    echo "3. 查看当前配置"
    echo "4. 配置设置"
    echo "5. 退出"
    echo ""
}

# 主循环
while true; do
    show_menu
    read -p "请输入选择 (1-5): " choice
    
    case $choice in
        1)
            echo "🚀 启动红包提醒调度器..."
            python main.py --run
            break
            ;;
        2)
            echo "🧪 测试推送功能..."
            python main.py --test
            echo ""
            read -p "按回车键继续..."
            ;;
        3)
            echo "📋 当前配置信息："
            python main.py --config
            echo ""
            read -p "按回车键继续..."
            ;;
        4)
            echo "🔧 进入配置设置..."
            python main.py --setup
            ;;
        5)
            echo "👋 再见！"
            exit 0
            ;;
        *)
            echo "❌ 无效选择，请重新输入"
            ;;
    esac
done 