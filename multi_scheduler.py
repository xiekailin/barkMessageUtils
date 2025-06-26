import schedule
import time
import logging
from datetime import datetime
from multi_bark_sender import MultiBarkSender
from template_manager import TemplateManager

class MultiTemplateScheduler:
    """多模板定时任务调度器"""
    
    def __init__(self):
        self.sender = MultiBarkSender()
        self.template_manager = TemplateManager()
        self.setup_logging()
    
    def setup_logging(self):
        """设置日志"""
        self.logger = logging.getLogger(__name__)
    
    def send_template_reminder(self, template_id):
        """发送指定模板的提醒"""
        template = self.template_manager.get_template(template_id)
        if not template:
            self.logger.error(f"模板 {template_id} 不存在")
            return
        
        if not template.get("enabled", True):
            self.logger.info(f"模板 {template_id} 已禁用，跳过发送")
            return
        
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.logger.info(f"执行定时任务 - 发送模板 {template['name']} [{current_time}]")
        
        # 获取设备URL列表
        device_urls = self.template_manager.get_device_urls(template["devices"])
        
        if not device_urls:
            self.logger.error(f"模板 {template_id} 没有有效的设备")
            return
        
        # 发送消息
        success = self.sender.send_message(
            bark_url=device_urls[0],  # 暂时只发送到第一个设备
            title=template["title"],
            content=template["content"]
        )
        
        if success:
            self.logger.info(f"模板 {template['name']} 发送成功")
        else:
            self.logger.error(f"模板 {template['name']} 发送失败")
    
    def setup_schedules(self):
        """设置所有模板的定时任务"""
        enabled_templates = self.template_manager.get_enabled_templates()
        
        # 清除所有现有任务
        schedule.clear()
        
        for template_id, template in enabled_templates.items():
            time_str = template["time"]
            schedule.every().day.at(time_str).do(self.send_template_reminder, template_id)
            self.logger.info(f"已设置模板 {template['name']}，每天 {time_str} 发送")
    
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
        template = self.template_manager.get_template(template_id)
        if not template:
            self.logger.error(f"模板 {template_id} 不存在")
            return False
        
        self.logger.info(f"测试模板: {template['name']}")
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