import os
import json
from datetime import datetime
from config import Config

class ConfigManager:
    """配置管理器"""
    
    def __init__(self):
        self.config_file = "custom_config.json"
        self.load_custom_config()
    
    def load_custom_config(self):
        """加载自定义配置"""
        if os.path.exists(self.config_file):
            try:
                with open(self.config_file, 'r', encoding='utf-8') as f:
                    self.custom_config = json.load(f)
            except:
                self.custom_config = {}
        else:
            self.custom_config = {}
    
    def save_custom_config(self):
        """保存自定义配置"""
        with open(self.config_file, 'w', encoding='utf-8') as f:
            json.dump(self.custom_config, f, ensure_ascii=False, indent=2)
    
    def get_config(self, key, default=None):
        """获取配置值"""
        return self.custom_config.get(key, default)
    
    def set_config(self, key, value):
        """设置配置值"""
        self.custom_config[key] = value
        self.save_custom_config()
    
    def interactive_config(self):
        """交互式配置界面"""
        print("🧧 微信红包提醒系统 - 配置管理")
        print("=" * 50)
        
        while True:
            print("\n📋 当前配置：")
            print(f"  提醒时间: {self.get_config('reminder_time', Config.REMINDER_TIME)}")
            print(f"  消息标题: {self.get_config('title', Config.TITLE)}")
            print(f"  消息内容: {self.get_config('content', Config.CONTENT)}")
            
            print("\n🔧 配置选项：")
            print("1. 修改提醒时间")
            print("2. 修改消息标题")
            print("3. 修改消息内容")
            print("4. 重置为默认配置")
            print("5. 测试当前配置")
            print("0. 返回主菜单")
            
            choice = input("\n请选择操作 (0-5): ").strip()
            
            if choice == "0":
                break
            elif choice == "1":
                self.config_reminder_time()
            elif choice == "2":
                self.config_title()
            elif choice == "3":
                self.config_content()
            elif choice == "4":
                self.reset_config()
            elif choice == "5":
                self.test_config()
            else:
                print("❌ 无效选择，请重新输入")
    
    def config_reminder_time(self):
        """配置提醒时间"""
        print(f"\n⏰ 当前提醒时间: {self.get_config('reminder_time', Config.REMINDER_TIME)}")
        print("时间格式: HH:MM (例如: 08:45)")
        
        while True:
            new_time = input("请输入新的提醒时间: ").strip()
            if self.validate_time(new_time):
                self.set_config('reminder_time', new_time)
                print(f"✅ 提醒时间已更新为: {new_time}")
                break
            else:
                print("❌ 时间格式错误，请使用 HH:MM 格式")
    
    def config_title(self):
        """配置消息标题"""
        print(f"\n📝 当前消息标题: {self.get_config('title', Config.TITLE)}")
        new_title = input("请输入新的消息标题: ").strip()
        if new_title:
            self.set_config('title', new_title)
            print(f"✅ 消息标题已更新为: {new_title}")
        else:
            print("❌ 标题不能为空")
    
    def config_content(self):
        """配置消息内容"""
        print(f"\n📄 当前消息内容: {self.get_config('content', Config.CONTENT)}")
        print("请输入新的消息内容:")
        print("提示: Bark支持换行符 \\n 来分隔多行内容")
        
        new_content = input("新消息内容: ").strip()
        if new_content:
            self.set_config('content', new_content)
            print("✅ 消息内容已更新")
        else:
            print("❌ 内容不能为空")
    
    def reset_config(self):
        """重置为默认配置"""
        confirm = input("确定要重置为默认配置吗？(y/N): ").strip().lower()
        if confirm == 'y':
            self.custom_config = {}
            self.save_custom_config()
            print("✅ 配置已重置为默认值")
    
    def test_config(self):
        """测试当前配置"""
        print("\n🧪 测试当前配置...")
        from bark_sender import BarkSender
        
        sender = BarkSender()
        title = self.get_config('title', Config.TITLE)
        content = self.get_config('content', Config.CONTENT)
        
        success = sender.send_message(title=title, content=content)
        if success:
            print("✅ 测试消息发送成功！请检查你的Bark APP")
        else:
            print("❌ 测试消息发送失败，请检查日志文件")
    
    def validate_time(self, time_str):
        """验证时间格式"""
        try:
            datetime.strptime(time_str, "%H:%M")
            return True
        except ValueError:
            return False
    
    def get_effective_config(self):
        """获取有效配置（自定义配置优先，否则使用默认配置）"""
        return {
            'reminder_time': self.get_config('reminder_time', Config.REMINDER_TIME),
            'title': self.get_config('title', Config.TITLE),
            'content': self.get_config('content', Config.CONTENT)
        } 