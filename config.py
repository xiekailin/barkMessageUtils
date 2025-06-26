import os
from dotenv import load_dotenv

# 加载环境变量
load_dotenv()

class Config:
    """配置类"""
    
    # Bark配置
    BARK_URL = os.getenv('BARK_URL', 'https://api.day.app/Znodd8yskndqUUbMVnmzBn')
    
    # 默认提醒时间配置
    REMINDER_TIME = "08:45"  # 每天早上8点45分
    
    # 默认推送消息配置
    TITLE = "微信红包提醒"
    CONTENT = "早上好！记得发红包哦~ 🧧"
    
    # 日志配置
    LOG_LEVEL = "INFO"
    LOG_FILE = "red_pocket_reminder.log"
    
    @classmethod
    def get_effective_config(cls, config_manager=None):
        """获取有效配置（自定义配置优先，否则使用默认配置）"""
        if config_manager:
            custom_config = config_manager.get_effective_config()
            return {
                'reminder_time': custom_config['reminder_time'],
                'title': custom_config['title'],
                'content': custom_config['content']
            }
        else:
            return {
                'reminder_time': cls.REMINDER_TIME,
                'title': cls.TITLE,
                'content': cls.CONTENT
            } 