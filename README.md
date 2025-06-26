# 微信红包提醒系统

一个基于Bark的微信红包定时提醒系统，每天早上8点45分自动发送提醒消息到你的手机。

## 功能特点

- 🕐 定时提醒：每天早上8点45分自动发送提醒
- 📱 手机推送：通过Bark推送到你的手机
- 🎨 美观界面：现代化的Web管理界面
- 📝 日志记录：完整的运行日志
- ⚙️ 配置灵活：支持自定义时间和消息内容
- 🔧 交互配置：提供友好的配置界面
- 🌐 Web管理：现代化的Web界面管理

## 安装步骤

### 1. 克隆项目
```bash
git clone <项目地址>
cd wechatRedPocketTime
```

### 2. 安装依赖
```bash
pip install -r requirements.txt
```

### 3. 获取Bark推送URL

1. 下载Bark APP（iOS/Android）
2. 注册并登录账号
3. 在设置中获取推送URL，格式如：
   ```
   https://api.day.app/你的设备码/推送标题/推送内容
   ```

### 4. 配置Bark URL

复制环境变量示例文件：
```bash
cp env.example .env
```

编辑 `.env` 文件，填入你的Bark推送URL：
```
BARK_URL=https://api.day.app/Znodd8yskndqUUbMVnmzBn
```

## 使用方法

### 🌐 Web界面管理（推荐）

启动Web服务：
```bash
./start_web.sh
```

然后在浏览器中访问：http://localhost:5000

Web界面功能：
- 📊 实时状态监控
- ⚙️ 可视化配置管理
- 🧪 一键测试推送
- 🚀 启动/停止定时任务
- 📝 实时日志查看
- 🔄 配置重置功能

### 命令行使用

#### 快速启动（传统方式）
```bash
./start.sh
```
启动脚本提供友好的菜单界面，包含所有功能。

#### 查看配置信息
```bash
python main.py --config
```

#### 测试推送功能
```bash
python main.py --test
```

#### 启动定时任务
```bash
python main.py --run
```

#### 交互式配置设置
```bash
python main.py --setup
```

#### 查看帮助
```bash
python main.py --help
```

## 自定义配置

### 通过Web界面配置（推荐）
1. 启动Web服务：`./start_web.sh`
2. 在浏览器中访问：http://localhost:5000
3. 在配置设置页面修改：
   - 提醒时间
   - 消息标题
   - 消息内容（支持换行符 \n）
4. 点击"保存配置"应用更改
5. 使用"测试推送"验证效果

### 通过交互界面配置
运行 `python main.py --setup` 或使用启动脚本选择"配置设置"，可以：
- 修改提醒时间
- 自定义消息标题
- 编辑消息内容（支持换行符）
- 测试当前配置
- 重置为默认配置

### 手动编辑配置文件
自定义配置保存在 `custom_config.json` 文件中，格式如下：
```json
{
  "reminder_time": "08:45",
  "title": "自定义标题",
  "content": "自定义内容"
}
```

### 配置优先级
1. 自定义配置（custom_config.json）
2. 默认配置（config.py）

## Bark推送特性

- **简洁高效**：无需复杂的token配置
- **即时推送**：消息秒级到达
- **支持换行**：使用 \n 分隔多行内容
- **自定义声音**：可设置不同的提示音
- **图标支持**：可设置自定义图标
- **点击跳转**：支持点击跳转到指定URL

### 消息示例
```
标题：🧧 微信红包提醒
内容：早上好！记得发红包哦~ 🧧\n现在是发红包的最佳时间！
```

## 部署建议

### 本地运行
适合个人使用，需要保持电脑开机。

### 服务器部署
推荐部署到云服务器，确保24小时运行：

1. 上传代码到服务器
2. 安装Python环境
3. 配置Bark URL
4. 使用nohup或systemd后台运行

### Docker部署
```bash
# 构建镜像
docker build -t red-pocket-reminder .

# 运行容器
docker run -d --name red-pocket-reminder -p 5000:5000 red-pocket-reminder
```

## 文件结构

```
wechatRedPocketTime/
├── main.py              # 主程序入口
├── web_server.py        # Web服务器
├── config.py            # 配置文件
├── config_manager.py    # 配置管理器
├── bark_sender.py       # Bark推送发送器
├── scheduler.py         # 定时任务调度器
├── requirements.txt     # 项目依赖
├── env.example          # 环境变量示例
├── start.sh            # 命令行启动脚本
├── start_web.sh        # Web界面启动脚本
├── templates/          # Web模板目录
│   └── index.html      # Web界面模板
├── README.md           # 项目说明
├── .env                # 环境变量文件（需要创建）
├── custom_config.json  # 自定义配置文件（自动生成）
└── .gitignore          # Git忽略文件
```

## 日志文件

程序运行日志保存在 `red_pocket_reminder.log` 文件中，包含：
- 定时任务执行记录
- 推送消息发送状态
- 错误信息

## 故障排除

### 推送失败
1. 检查Bark URL是否正确
2. 确认网络连接正常
3. 查看日志文件中的错误信息

### 定时任务不执行
1. 确认系统时间正确
2. 检查程序是否正常运行
3. 查看日志文件

### 配置不生效
1. 确认自定义配置文件格式正确
2. 重启程序使配置生效
3. 使用 `--config` 查看当前有效配置

### Web界面无法访问
1. 确认端口5000未被占用
2. 检查防火墙设置
3. 尝试访问 http://127.0.0.1:5000

## 许可证

MIT License

## 贡献

欢迎提交Issue和Pull Request！ 