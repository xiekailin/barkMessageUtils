#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import logging
from config import Config

logging.basicConfig(
    level=getattr(logging, Config.LOG_LEVEL),
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(Config.LOG_FILE, encoding='utf-8'),
        logging.StreamHandler()
    ]
)

logging.info('测试日志写入')
from flask import Flask, render_template, request, jsonify, redirect, url_for
from flask_cors import CORS
import json
import os
import threading
import time
from datetime import datetime
from config_manager import ConfigManager
from template_manager import TemplateManager
from multi_scheduler import MultiTemplateScheduler
from multi_bark_sender import MultiBarkSender
import logging
app = Flask(__name__)
CORS(app)

# 配置日志
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# 全局变量
scheduler_thread = None
scheduler_running = False
config_manager = ConfigManager()
template_manager = TemplateManager()
scheduler = MultiTemplateScheduler()
sender = MultiBarkSender(template_manager)

@app.route('/')
def index():
    """主页"""
    return render_template('index.html')

@app.route('/static/<path:filename>')
def static_files(filename):
    return app.send_static_file(filename)

# 基础配置API
@app.route('/api/config', methods=['GET', 'POST'])
def config_api():
    if request.method == 'GET':
        try:
            config = config_manager.get_config()
            return jsonify({'success': True, 'data': config})
        except Exception as e:
            logger.error(f"获取配置失败: {e}")
            return jsonify({'success': False, 'message': f'获取配置失败: {e}'})
    
    elif request.method == 'POST':
        try:
            data = request.get_json()
            config_manager.update_config(data)
            return jsonify({'success': True, 'message': '配置更新成功'})
        except Exception as e:
            logger.error(f"更新配置失败: {e}")
            return jsonify({'success': False, 'message': f'更新配置失败: {e}'})

# 设备管理API
@app.route('/api/devices', methods=['GET', 'POST'])
def devices_api():
    if request.method == 'GET':
        try:
            devices = template_manager.get_all_devices()
            return jsonify({'success': True, 'data': devices})
        except Exception as e:
            logger.error(f"获取设备失败: {e}")
            return jsonify({'success': False, 'message': f'获取设备失败: {e}'})
    
    elif request.method == 'POST':
        try:
            data = request.get_json()
            device_id = data.get('device_id')
            url = data.get('url')
            name = data.get('name')
            description = data.get('description', '')
            if not device_id or not url or not name:
                return jsonify({'success': False, 'message': '缺少设备ID、名称或URL'})
            
            template_manager.add_device(device_id, name, url, description)
            return jsonify({'success': True, 'message': '设备添加成功'})
        except Exception as e:
            logger.error(f"添加设备失败: {e}")
            return jsonify({'success': False, 'message': f'添加设备失败: {e}'})

@app.route('/api/devices/<device_id>', methods=['DELETE'])
def delete_device(device_id):
    try:
        template_manager.delete_device(device_id)
        return jsonify({'success': True, 'message': '设备删除成功'})
    except Exception as e:
        logger.error(f"删除设备失败: {e}")
        return jsonify({'success': False, 'message': f'删除设备失败: {e}'})

# 设备模板管理API
@app.route('/api/devices/<device_id>/templates', methods=['GET', 'POST'])
def device_templates_api(device_id):
    if request.method == 'GET':
        try:
            templates = template_manager.get_all_templates_from_device(device_id)
            return jsonify({'success': True, 'data': templates})
        except Exception as e:
            logger.error(f"获取设备模板失败: {e}")
            return jsonify({'success': False, 'message': f'获取设备模板失败: {e}'})
    
    elif request.method == 'POST':
        try:
            data = request.get_json()
            template_id = data.get('template_id')
            name = data.get('name')
            time_str = data.get('time')
            title = data.get('title')
            content = data.get('content')
            enabled = data.get('enabled', True)
            
            if not template_id or not name or not time_str or not title or not content:
                return jsonify({'success': False, 'message': '缺少模板ID、名称、时间、标题或内容'})
            
            success = template_manager.add_template_to_device(device_id, template_id, name, time_str, title, content, enabled)
            if success:
                return jsonify({'success': True, 'message': '模板添加成功'})
            else:
                return jsonify({'success': False, 'message': '设备不存在'})
        except Exception as e:
            logger.error(f"添加设备模板失败: {e}")
            return jsonify({'success': False, 'message': f'添加设备模板失败: {e}'})

@app.route('/api/devices/<device_id>/templates/<template_id>', methods=['GET', 'PUT', 'DELETE'])
def device_template_api(device_id, template_id):
    if request.method == 'GET':
        try:
            template = template_manager.get_template_from_device(device_id, template_id)
            if template:
                return jsonify({'success': True, 'data': template})
            else:
                return jsonify({'success': False, 'message': '模板不存在'})
        except Exception as e:
            logger.error(f"获取设备模板失败: {e}")
            return jsonify({'success': False, 'message': f'获取设备模板失败: {e}'})
    
    elif request.method == 'PUT':
        try:
            data = request.get_json()
            success = template_manager.update_template_in_device(device_id, template_id, **data)
            if success:
                return jsonify({'success': True, 'message': '模板更新成功'})
            else:
                return jsonify({'success': False, 'message': '模板不存在'})
        except Exception as e:
            logger.error(f"更新设备模板失败: {e}")
            return jsonify({'success': False, 'message': f'更新设备模板失败: {e}'})
    
    elif request.method == 'DELETE':
        try:
            success = template_manager.delete_template_from_device(device_id, template_id)
            if success:
                return jsonify({'success': True, 'message': '模板删除成功'})
            else:
                return jsonify({'success': False, 'message': '模板不存在'})
        except Exception as e:
            logger.error(f"删除设备模板失败: {e}")
            return jsonify({'success': False, 'message': f'删除设备模板失败: {e}'})

# 获取所有模板统计信息
@app.route('/api/templates', methods=['GET'])
def templates_api():
    try:
        templates = template_manager.get_all_templates()
        return jsonify({'success': True, 'data': templates})
    except Exception as e:
        logger.error(f"获取模板统计失败: {e}")
        return jsonify({'success': False, 'message': f'获取模板统计失败: {e}'})

# 测试API
@app.route('/api/test', methods=['POST'])
def test_push():
    try:
        data = request.get_json()
        template_id = data.get('template_id')
        device_id = data.get('device_id')

        if template_id:
            # 测试特定模板
            if device_id == 'all':
                # 推送到所有有该模板的设备
                all_templates = template_manager.get_all_templates()
                if template_id in all_templates:
                    device_ids = all_templates[template_id]["devices"]
                    result = sender.send_template_to_devices(
                        template_id=template_id,
                        device_ids=device_ids,
                        sound="alarm",
                        icon="https://api.day.app/icon/red-packet.png"
                    )
                else:
                    return jsonify({'success': False, 'message': '模板不存在'})
            else:
                # 推送到用户选择的特定设备
                if not device_id:
                    device_id = 'default'
                
                # 检查设备是否有该模板
                template = template_manager.get_template_from_device(device_id, template_id)
                if not template:
                    return jsonify({'success': False, 'message': f'设备 {device_id} 没有模板 {template_id}'})
                
                result = sender.send_template_to_devices(
                    template_id=template_id,
                    device_ids=[device_id],
                    sound="alarm",
                    icon="https://api.day.app/icon/red-packet.png"
                )
            
            if result:
                return jsonify({'success': True, 'message': f'模板 {template_id} 推送成功'})
            else:
                return jsonify({'success': False, 'message': f'模板 {template_id} 推送失败'})
        else:
            # 测试推送到指定设备或全部设备
            if device_id == 'all':
                device_urls = [d['url'] for d in template_manager.get_all_devices().values()]
            else:
                if not device_id:
                    device_id = 'default'
                device_urls = template_manager.get_device_urls([device_id])
            config = config_manager.get_effective_config()
            result = sender.send_to_multiple_devices(
                devices=device_urls,
                title=config.get('title', '测试消息'),
                content=config.get('content', '这是一条测试消息')
            )
            if result:
                return jsonify({'success': True, 'message': '测试推送成功'})
            else:
                return jsonify({'success': False, 'message': '测试推送失败'})
    except Exception as e:
        logger.error(f"测试推送失败: {e}")
        return jsonify({'success': False, 'message': f'测试推送失败: {e}'})

# 调度器API
@app.route('/api/scheduler/start', methods=['POST'])
def start_scheduler():
    global scheduler_thread, scheduler_running
    if scheduler_running:
        return jsonify({'success': False, 'message': '定时任务已在运行中'})
    try:
        scheduler_thread = threading.Thread(target=scheduler.run, daemon=True)
        scheduler_thread.start()
        scheduler_running = True
        return jsonify({'success': True, 'message': '定时任务启动成功'})
    except Exception as e:
        logger.error(f"启动定时任务失败: {e}")
        scheduler_running = False
        return jsonify({'success': False, 'message': f'启动定时任务失败: {e}'})

@app.route('/api/scheduler/stop', methods=['POST'])
def stop_scheduler():
    global scheduler_running
    if not scheduler_running:
        return jsonify({'success': False, 'message': '定时任务未在运行'})
    try:
        # 通过清除所有定时任务实现停止
        import schedule
        schedule.clear()
        scheduler_running = False
        return jsonify({'success': True, 'message': '定时任务停止成功'})
    except Exception as e:
        logger.error(f"停止定时任务失败: {e}")
        return jsonify({'success': False, 'message': f'停止定时任务失败: {e}'})

@app.route('/api/scheduler/status', methods=['GET'])
def scheduler_status():
    global scheduler_running
    try:
        return jsonify({'success': True, 'data': {'running': scheduler_running}})
    except Exception as e:
        logger.error(f"获取定时任务状态失败: {e}")
        return jsonify({'success': False, 'message': f'获取定时任务状态失败: {e}'})

@app.route('/api/scheduler/refresh', methods=['POST'])
def refresh_scheduler():
    try:
        scheduler.refresh_templates()
        return jsonify({'success': True, 'message': '定时任务配置刷新成功'})
    except Exception as e:
        logger.error(f"刷新定时任务配置失败: {e}")
        return jsonify({'success': False, 'message': f'刷新定时任务配置失败: {e}'})

# 其他API
@app.route('/api/reset', methods=['POST'])
def reset_config():
    try:
        config_manager.reset_config()
        return jsonify({'success': True, 'message': '配置重置成功'})
    except Exception as e:
        logger.error(f"重置配置失败: {e}")
        return jsonify({'success': False, 'message': f'重置配置失败: {e}'})

@app.route('/api/logs', methods=['GET'])
def get_logs():
    try:
        log_file = 'red_pocket_reminder.log'
        if os.path.exists(log_file):
            with open(log_file, 'r', encoding='utf-8') as f:
                lines = f.readlines()
                return jsonify({'success': True, 'data': lines[-50:]})
        else:
            return jsonify({'success': True, 'data': []})
    except Exception as e:
        logger.error(f"获取日志失败: {e}")
        return jsonify({'success': False, 'message': f'获取日志失败: {e}'})

if __name__ == '__main__':
    print("🌐 启动Web配置界面...")
    print("📱 请在浏览器中访问: http://localhost:9918")
    print("按 Ctrl+C 停止服务")
    app.run(host='0.0.0.0', port=9918, debug=False) 