import requests
import logging
import urllib.parse
from config import Config

class MultiBarkSender:
    """多设备Bark推送发送器"""
    
    def __init__(self, template_manager=None):
        self.template_manager = template_manager
        self.logger = logging.getLogger(__name__)
    
    def send_message(self, bark_url, title=None, content=None, sound=None, icon=None, url=None):
        """
        发送Bark推送消息到指定设备
        
        Args:
            bark_url (str): Bark推送URL
            title (str): 消息标题
            content (str): 消息内容
            sound (str): 提示音（可选）
            icon (str): 图标URL（可选）
            url (str): 点击跳转URL（可选）
        """
        if not bark_url:
            self.logger.error("Bark URL未提供")
            return False
        
        # 使用默认值
        title = title or Config.TITLE
        content = content or Config.CONTENT
        
        # 构建URL参数
        params = []
        
        # 可选参数
        if sound:
            params.append(f"sound={sound}")
        if icon:
            params.append(f"icon={urllib.parse.quote(icon)}")
        if url:
            params.append(f"url={urllib.parse.quote(url)}")
        
        # 构建完整URL
        push_url = f"{bark_url}/{urllib.parse.quote(title)}/{urllib.parse.quote(content)}"
        if params:
            push_url += "?" + "&".join(params)
        
        try:
            self.logger.info(f"正在发送Bark推送消息到 {bark_url}: {title}")
            response = requests.get(push_url, timeout=10)
            response.raise_for_status()
            
            result = response.json()
            if result.get("code") == 200:
                self.logger.info("Bark推送消息发送成功")
                return True
            else:
                self.logger.error(f"Bark推送消息发送失败: {result.get('message', '未知错误')}")
                return False
                
        except requests.exceptions.RequestException as e:
            self.logger.error(f"网络请求错误: {e}")
            return False
        except Exception as e:
            self.logger.error(f"发送Bark推送消息时发生错误: {e}")
            return False
    
    def send_to_multiple_devices(self, devices, title=None, content=None, sound=None, icon=None, url=None):
        """
        向多个设备发送消息
        
        Args:
            devices (list): Bark URL列表
            title (str): 消息标题
            content (str): 消息内容
            sound (str): 提示音（可选）
            icon (str): 图标URL（可选）
            url (str): 点击跳转URL（可选）
        """
        if not devices:
            self.logger.error("未提供设备列表")
            return False
        
        success_count = 0
        total_count = len(devices)
        
        for device_url in devices:
            if self.send_message(device_url, title, content, sound, icon, url):
                success_count += 1
        
        self.logger.info(f"批量发送完成: {success_count}/{total_count} 成功")
        return success_count == total_count
    
    def send_template_to_devices(self, template_id, device_ids=None, sound=None, icon=None, url=None):
        """
        向指定设备发送模板消息，支持设备特定的自定义内容
        
        Args:
            template_id (str): 模板ID
            device_ids (list): 设备ID列表，如果为None则使用模板中配置的设备
            sound (str): 提示音（可选）
            icon (str): 图标URL（可选）
            url (str): 点击跳转URL（可选）
        """
        if not self.template_manager:
            self.logger.error("模板管理器未初始化")
            return False
        
        if device_ids is None:
            # 获取所有有该模板的设备
            all_templates = self.template_manager.get_all_templates()
            if template_id not in all_templates:
                self.logger.error(f"模板 {template_id} 不存在")
                return False
            device_ids = all_templates[template_id]["devices"]
        
        if not device_ids:
            self.logger.error("未指定设备")
            return False
        
        success_count = 0
        total_count = 0
        
        for device_id in device_ids:
            if device_id not in self.template_manager.devices:
                self.logger.warning(f"设备 {device_id} 不存在，跳过")
                continue
            
            # 获取设备特定的模板内容
            device_template = self.template_manager.get_template_from_device(device_id, template_id)
            if not device_template:
                self.logger.warning(f"设备 {device_id} 没有模板 {template_id}，跳过")
                continue
            
            device_url = self.template_manager.devices[device_id]["url"]
            device_name = self.template_manager.devices[device_id]["name"]
            
            self.logger.info(f"正在向设备 {device_name} ({device_id}) 发送模板 {template_id}")
            
            if self.send_message(
                device_url, 
                device_template["title"], 
                device_template["content"], 
                sound, 
                icon, 
                url
            ):
                success_count += 1
            
            total_count += 1
        
        self.logger.info(f"模板 {template_id} 发送完成: {success_count}/{total_count} 成功")
        return success_count == total_count
    
    def send_red_pocket_reminder(self, devices=None):
        """发送红包提醒消息"""
        if not devices:
            devices = [Config.BARK_URL]  # 使用默认设备
        
        title = "🧧 微信红包提醒"
        content = "早上好！记得发红包哦~ 🧧\n现在是发红包的最佳时间！"
        
        # 可以添加一些可选参数
        sound = "alarm"  # 使用闹钟提示音
        icon = "https://api.day.app/icon/red-packet.png"  # 红包图标（可选）
        
        return self.send_to_multiple_devices(
            devices=devices,
            title=title, 
            content=content, 
            sound=sound,
            icon=icon
        ) 