import schedule
import time
import logging
from datetime import datetime
from multi_bark_sender import MultiBarkSender
from template_manager import TemplateManager

class MultiTemplateScheduler:
    """多模板定时任务调度器"""
    
    def __init__(self):
        self.template_manager = TemplateManager()
        self.sender = MultiBarkSender(self.template_manager)
        self.setup_logging()
    
    def setup_logging(self):
        """设置日志"""
        self.logger = logging.getLogger(__name__)
    
    def send_template_reminder(self, template_id):
        """发送指定模板的提醒，支持设备特定的自定义内容"""
        # 获取所有有该模板的设备
        all_templates = self.template_manager.get_all_templates()
        if template_id not in all_templates:
            self.logger.error(f"模板 {template_id} 不存在")
            return
        
        device_ids = all_templates[template_id]["devices"]
        if not device_ids:
            self.logger.error(f"模板 {template_id} 没有关联的设备")
            return
        
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.logger.info(f"执行定时任务 - 发送模板 {template_id} [{current_time}]")
        
        # 使用新的发送方法，支持设备特定的内容
        success = self.sender.send_template_to_devices(
            template_id=template_id,
            device_ids=device_ids,
            sound="alarm",  # 使用闹钟提示音
            icon="https://api.day.app/icon/red-packet.png"  # 红包图标
        )
        
        if success:
            self.logger.info(f"模板 {template_id} 发送成功")
        else:
            self.logger.error(f"模板 {template_id} 发送失败")
    
    def setup_schedules(self):
        """设置所有模板的定时任务"""
        enabled_templates = self.template_manager.get_enabled_templates()
        
        # 清除所有现有任务
        schedule.clear()
        
        for template_id, template in enabled_templates.items():
            time_str = template["time"]
            schedule.every().day.at(time_str).do(self.send_template_reminder, template_id)
            self.logger.info(f"已设置模板 {template_id}，每天 {time_str} 发送")
    
    def run(self):
        """运行调度器"""
        self.setup_schedules()
        
        enabled_templates = self.template_manager.get_enabled_templates()
        if not enabled_templates:
            self.logger.warning("没有启用的模板，调度器将不会发送任何消息")
        else:
            self.logger.info(f"调度器已启动，共 {len(enabled_templates)} 个模板")
        
        self.logger.info("按 Ctrl+C 停止程序")
        
        try:
            while True:
                schedule.run_pending()
                time.sleep(60)  # 每分钟检查一次
        except KeyboardInterrupt:
            self.logger.info("收到停止信号，正在关闭调度器...")
        except Exception as e:
            self.logger.error(f"调度器运行出错: {e}")
    
    def test_template(self, template_id):
        """测试指定模板"""
        all_templates = self.template_manager.get_all_templates()
        if template_id not in all_templates:
            self.logger.error(f"模板 {template_id} 不存在")
            return False
        
        self.logger.info(f"测试模板: {template_id}")
        return self.send_template_reminder(template_id)
    
    def refresh_templates(self):
        """刷新模板配置"""
        self.logger.info("刷新模板配置...")
        self.setup_schedules()
        self.logger.info("模板配置刷新完成")
    
    def get_schedule_info(self):
        """获取调度信息"""
        enabled_templates = self.template_manager.get_enabled_templates()
        schedule_info = []
        
        for template_id, template in enabled_templates.items():
            schedule_info.append({
                "id": template_id,
                "name": template["name"],
                "time": template["time"],
                "devices": template["devices"]
            })
        
        return schedule_info 