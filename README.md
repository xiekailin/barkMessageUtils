# 微信红包提醒系统

一个基于Bark的微信红包定时提醒系统，支持多设备、多模板和设备特定推送内容管理。

## 功能特点

- 🕐 定时提醒：支持多个时间点的定时提醒
- 📱 多设备推送：支持多个Bark设备同时推送
- 🎯 设备特定内容：每个设备可以设置独特的推送内容
- 📝 设备模板管理：每个设备独立管理自己的提醒模板
- 🎨 美观界面：现代化的Web管理界面
- 📝 日志记录：完整的运行日志
- ⚙️ 配置灵活：支持自定义时间和消息内容
- 🔧 交互配置：提供友好的配置界面
- 🌐 Web管理：现代化的Web界面管理

## 新功能：设备模板管理

### 功能说明
每个设备可以独立管理自己的提醒模板，包括新增、编辑、删除和测试功能。每个设备都有完全独立的模板配置。

### 使用场景
- **个性化提醒**：不同设备设置不同的提醒内容和时间
- **多语言支持**：不同设备使用不同语言
- **角色区分**：工作设备收到正式提醒，个人设备收到轻松提醒
- **时间差异**：不同时区的设备收到对应时间的提醒

### 管理方式
1. 在Web界面中添加设备
2. 点击设备的"模板设置"按钮进入模板管理
3. 使用"新增模板"按钮添加新的提醒模板
4. 点击"编辑"按钮修改模板内容
5. 点击"测试"按钮测试模板推送
6. 点击"删除"按钮删除不需要的模板

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
- 📱 多设备管理
- 🎯 设备模板管理（新增、编辑、删除、测试）
- 🧪 一键测试推送
- 🚀 启动/停止定时任务
- 📝 实时日志查看
- 🔄 配置重置功能

### 设备模板管理

#### 1. 添加设备
1. 在"设备管理"标签页点击"添加设备"
2. 填写设备ID、名称、Bark URL和描述
3. 点击"保存设备"

#### 2. 管理设备模板
1. 在设备列表中点击"模板设置"按钮
2. 查看该设备的所有模板列表
3. 使用"新增模板"按钮添加新模板
4. 点击"编辑"按钮修改模板内容
5. 点击"测试"按钮测试模板推送
6. 点击"删除"按钮删除模板

#### 3. 模板配置
每个模板包含以下配置：
- **模板ID**：唯一标识符
- **模板名称**：显示名称
- **提醒时间**：每天的执行时间
- **消息标题**：推送消息的标题
- **消息内容**：推送消息的内容
- **启用状态**：是否启用该模板

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
3. 在"设备管理"标签页添加设备
4. 为每个设备设置特定的模板内容
5. 使用"测试推送"验证效果

### 设备管理
- **添加设备**：配置新的Bark设备
- **设备模板管理**：为每个设备独立管理提醒模板
- **删除设备**：移除不需要的设备

### 模板管理
- **新增模板**：为设备添加新的提醒模板
- **编辑模板**：修改模板的所有配置
- **删除模板**：移除不需要的模板
- **测试模板**：立即测试模板推送效果

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
1. 设备特定模板内容
2. 自定义配置（custom_config.json）
3. 默认配置（config.py）

## Bark推送特性

- **简洁高效**：无需复杂的token配置
- **即时推送**：消息秒级到达
- **支持换行**：使用 \n 分隔多行内容
- **自定义声音**：可设置不同的提示音
- **图标支持**：可设置自定义图标
- **点击跳转**：支持点击跳转到指定URL
- **设备特定内容**：每个设备可以收到不同的消息

### 消息示例
```
标题：🧧 微信红包提醒
内容：早上好！记得发红包哦~ 🧧\n现在是发红包的最佳时间！
```

## API接口

### 设备管理

#### 获取所有设备
```
GET /api/devices
```

#### 添加设备
```
POST /api/devices
Content-Type: application/json

{
  "device_id": "my_phone",
  "name": "我的手机",
  "url": "https://api.day.app/设备码",
  "description": "主要设备"
}
```

#### 删除设备
```
DELETE /api/devices/{device_id}
```

### 设备模板管理

#### 获取设备的所有模板
```
GET /api/devices/{device_id}/templates
```

#### 为设备添加模板
```
POST /api/devices/{device_id}/templates
Content-Type: application/json

{
  "template_id": "morning_reminder",
  "name": "早上红包提醒",
  "time": "08:45",
  "title": "🧧 微信红包提醒",
  "content": "早上好！记得发红包哦~ 🧧",
  "enabled": true
}
```

#### 获取设备的特定模板
```
GET /api/devices/{device_id}/templates/{template_id}
```

#### 更新设备的模板
```
PUT /api/devices/{device_id}/templates/{template_id}
Content-Type: application/json

{
  "name": "更新后的名称",
  "time": "09:00",
  "title": "更新后的标题",
  "content": "更新后的内容",
  "enabled": false
}
```

#### 删除设备的模板
```
DELETE /api/devices/{device_id}/templates/{template_id}
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
├── web_server.py        # Web服务器
├── config.py            # 配置文件
├── config_manager.py    # 配置管理器
├── template_manager.py  # 设备模板管理器
├── multi_bark_sender.py # 多设备Bark推送发送器
├── multi_scheduler.py   # 多模板定时任务调度器
├── requirements.txt     # 项目依赖
├── env.example          # 环境变量示例
├── start_web.sh        # Web界面启动脚本
├── templates/          # Web模板目录
│   └── index.html      # Web界面模板
├── static/             # 静态文件目录
│   ├── app.js          # 前端JavaScript
│   └── style.css       # 前端样式
├── bark_devices.json   # Bark设备配置
├── README.md           # 项目说明
├── .env                # 环境变量文件（需要创建）
└── .gitignore          # Git忽略文件
```

## 日志文件

程序运行日志保存在 `red_pocket_reminder.log` 文件中，包含：
- 定时任务执行记录
- 推送消息发送状态
- 设备模板使用情况
- 错误信息 