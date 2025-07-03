import os
import json
from datetime import datetime
from config import Config

class TemplateManager:
    """设备特定模板管理器"""
    
    def __init__(self):
        self.devices_file = "bark_devices.json"
        self.load_devices()
    
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
    
    def save_devices(self):
        """保存Bark设备列表"""
        with open(self.devices_file, 'w', encoding='utf-8') as f:
            json.dump(self.devices, f, ensure_ascii=False, indent=2)
    
    def get_default_devices(self):
        """获取默认设备列表"""
        return {
            "default": {
                "name": "默认设备",
                "url": Config.BARK_URL,
                "description": "主要推送设备",
                "templates": {
                    "morning_reminder": {
                        "name": "早上红包提醒",
                        "time": "08:45",
                        "title": "🧧 微信红包提醒",
                        "content": "早上好！记得发红包哦~ 🧧\n现在是发红包的最佳时间！",
                        "enabled": True
                    },
                    "afternoon_reminder": {
                        "name": "下午红包提醒",
                        "time": "14:30",
                        "title": "💰 下午红包时间",
                        "content": "下午好！别忘了发红包哦~ 💰\n下午也是发红包的好时机！",
                        "enabled": True
                    }
                }
            }
        }
    
    def add_device(self, device_id, name, url, description=""):
        """添加Bark设备"""
        self.devices[device_id] = {
            "name": name,
            "url": url,
            "description": description,
            "templates": {}
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
    
    def add_template_to_device(self, device_id, template_id, name, time, title, content, enabled=True):
        """为设备添加模板"""
        if device_id not in self.devices:
            return False
        
        if "templates" not in self.devices[device_id]:
            self.devices[device_id]["templates"] = {}
        
        self.devices[device_id]["templates"][template_id] = {
            "name": name,
            "time": time,
            "title": title,
            "content": content,
            "enabled": enabled
        }
        
        self.save_devices()
        return True
    
    def update_template_in_device(self, device_id, template_id, **kwargs):
        """更新设备中的模板"""
        if (device_id in self.devices and 
            "templates" in self.devices[device_id] and
            template_id in self.devices[device_id]["templates"]):
            
            self.devices[device_id]["templates"][template_id].update(kwargs)
            self.save_devices()
            return True
        return False
    
    def delete_template_from_device(self, device_id, template_id):
        """从设备中删除模板"""
        if (device_id in self.devices and 
            "templates" in self.devices[device_id] and
            template_id in self.devices[device_id]["templates"]):
            
            del self.devices[device_id]["templates"][template_id]
            self.save_devices()
            return True
        return False
    
    def get_template_from_device(self, device_id, template_id):
        """获取设备中的指定模板"""
        if (device_id in self.devices and 
            "templates" in self.devices[device_id] and
            template_id in self.devices[device_id]["templates"]):
            return self.devices[device_id]["templates"][template_id]
        return None
    
    def get_all_templates_from_device(self, device_id):
        """获取设备的所有模板"""
        if device_id in self.devices:
            return self.devices[device_id].get("templates", {})
        return {}
    
    def get_all_templates(self):
        """获取所有设备的所有模板（用于统计）"""
        all_templates = {}
        for device_id, device in self.devices.items():
            templates = device.get("templates", {})
            for template_id, template in templates.items():
                if template_id not in all_templates:
                    all_templates[template_id] = {
                        "name": template["name"],
                        "time": template["time"],
                        "devices": []
                    }
                all_templates[template_id]["devices"].append(device_id)
        return all_templates
    
    def get_enabled_templates(self):
        """获取所有启用的模板"""
        enabled_templates = {}
        for device_id, device in self.devices.items():
            templates = device.get("templates", {})
            for template_id, template in templates.items():
                if template.get("enabled", True):
                    if template_id not in enabled_templates:
                        enabled_templates[template_id] = {
                            "name": template["name"],
                            "time": template["time"],
                            "devices": []
                        }
                    enabled_templates[template_id]["devices"].append(device_id)
        return enabled_templates
    
    def get_template_for_device(self, template_id, device_id):
        """获取指定设备应该收到的模板内容"""
        template = self.get_template_from_device(device_id, template_id)
        if not template:
            return None
        
        return {
            "title": template["title"],
            "content": template["content"]
        }
    
    def validate_time(self, time_str):
        """验证时间格式"""
        try:
            datetime.strptime(time_str, "%H:%M")
            return True
        except ValueError:
            return False 