import os
import json
from datetime import datetime
from config import Config

class TemplateManager:
    """提醒模板管理器"""
    
    def __init__(self):
        self.templates_file = "reminder_templates.json"
        self.devices_file = "bark_devices.json"
        self.load_templates()
        self.load_devices()
    
    def load_templates(self):
        """加载提醒模板"""
        if os.path.exists(self.templates_file):
            try:
                with open(self.templates_file, 'r', encoding='utf-8') as f:
                    self.templates = json.load(f)
            except:
                self.templates = self.get_default_templates()
        else:
            self.templates = self.get_default_templates()
    
    def load_devices(self):
        """加载Bark设备列表"""
        if os.path.exists(self.devices_file):
            try:
                with open(self.devices_file, 'r', encoding='utf-8') as f:
                    self.devices = json.load(f)
            except:
                self.devices = self.get_default_devices()
        else:
            self.devices = self.get_default_devices()
    
    def save_templates(self):
        """保存提醒模板"""
        with open(self.templates_file, 'w', encoding='utf-8') as f:
            json.dump(self.templates, f, ensure_ascii=False, indent=2)
    
    def save_devices(self):
        """保存Bark设备列表"""
        with open(self.devices_file, 'w', encoding='utf-8') as f:
            json.dump(self.devices, f, ensure_ascii=False, indent=2)
    
    def get_default_templates(self):
        """获取默认模板"""
        return {
            "morning_reminder": {
                "name": "早上红包提醒",
                "time": "08:45",
                "title": "🧧 微信红包提醒",
                "content": "早上好！记得发红包哦~ 🧧\n现在是发红包的最佳时间！",
                "devices": ["default"],
                "enabled": True
            },
            "afternoon_reminder": {
                "name": "下午红包提醒",
                "time": "14:30",
                "title": "💰 下午红包时间",
                "content": "下午好！别忘了发红包哦~ 💰\n下午也是发红包的好时机！",
                "devices": ["default"],
                "enabled": True
            }
        }
    
    def get_default_devices(self):
        """获取默认设备列表"""
        return {
            "default": {
                "name": "默认设备",
                "url": Config.BARK_URL,
                "description": "主要推送设备"
            }
        }
    
    def add_template(self, template_id, name, time, title, content, devices=None, enabled=True):
        """添加提醒模板"""
        if devices is None:
            devices = ["default"]
        
        self.templates[template_id] = {
            "name": name,
            "time": time,
            "title": title,
            "content": content,
            "devices": devices,
            "enabled": enabled
        }
        self.save_templates()
    
    def update_template(self, template_id, **kwargs):
        """更新提醒模板"""
        if template_id in self.templates:
            self.templates[template_id].update(kwargs)
            self.save_templates()
            return True
        return False
    
    def delete_template(self, template_id):
        """删除提醒模板"""
        if template_id in self.templates:
            del self.templates[template_id]
            self.save_templates()
            return True
        return False
    
    def get_template(self, template_id):
        """获取指定模板"""
        return self.templates.get(template_id)
    
    def get_all_templates(self):
        """获取所有模板"""
        return self.templates
    
    def add_device(self, device_id, name, url, description=""):
        """添加Bark设备"""
        self.devices[device_id] = {
            "name": name,
            "url": url,
            "description": description
        }
        self.save_devices()
    
    def update_device(self, device_id, **kwargs):
        """更新Bark设备"""
        if device_id in self.devices:
            self.devices[device_id].update(kwargs)
            self.save_devices()
            return True
        return False
    
    def delete_device(self, device_id):
        """删除Bark设备"""
        if device_id in self.devices:
            del self.devices[device_id]
            self.save_devices()
            return True
        return False
    
    def get_device(self, device_id):
        """获取指定设备"""
        return self.devices.get(device_id)
    
    def get_all_devices(self):
        """获取所有设备"""
        return self.devices
    
    def get_device_urls(self, device_ids):
        """根据设备ID列表获取URL列表"""
        urls = []
        for device_id in device_ids:
            if device_id in self.devices:
                urls.append(self.devices[device_id]["url"])
        return urls
    
    def validate_time(self, time_str):
        """验证时间格式"""
        try:
            datetime.strptime(time_str, "%H:%M")
            return True
        except ValueError:
            return False
    
    def get_enabled_templates(self):
        """获取所有启用的模板"""
        return {k: v for k, v in self.templates.items() if v.get("enabled", True)} 