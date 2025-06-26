// 全局变量
let templates = {};
let devices = {};

// 页面加载完成后初始化
document.addEventListener('DOMContentLoaded', function() {
    loadTemplates();
    loadDevices();
    loadSchedulerStatus();
    loadLogs();
    
    // 设置定时刷新
    setInterval(loadSchedulerStatus, 5000);
    setInterval(loadLogs, 10000);
    
    // 绑定事件监听器
    bindEventListeners();
});

// 绑定事件监听器
function bindEventListeners() {
    // 测试推送
    document.getElementById('testBtn').addEventListener('click', function() {
        // 动态填充设备列表
        const select = document.getElementById('testDeviceSelect');
        select.innerHTML = '<option value="all">全部设备</option>';
        Object.entries(devices).forEach(([id, device]) => {
            select.innerHTML += `<option value="${id}">${device.name}</option>`;
        });
        // 显示模态框
        var modal = new bootstrap.Modal(document.getElementById('testDeviceModal'));
        modal.show();
    });
    
    // 启动定时任务
    document.getElementById('startBtn').addEventListener('click', startScheduler);
    
    // 停止定时任务
    document.getElementById('stopBtn').addEventListener('click', stopScheduler);
    
    // 刷新配置
    document.getElementById('refreshBtn').addEventListener('click', refreshScheduler);
    
    // 刷新日志
    document.getElementById('refreshLogsBtn').addEventListener('click', loadLogs);
    
    // 保存模板
    document.getElementById('saveTemplateBtn').addEventListener('click', saveTemplate);
    
    // 保存设备
    document.getElementById('saveDeviceBtn').addEventListener('click', saveDevice);

    // 确认推送
    document.getElementById('confirmTestDeviceBtn').addEventListener('click', async function() {
        const select = document.getElementById('testDeviceSelect');
        const device_id = select.value;
        const template_id = document.getElementById('testTemplateId').value;
        
        this.disabled = true;
        this.innerHTML = '推送中...';
        
        try {
            const requestBody = { device_id };
            if (template_id) {
                requestBody.template_id = template_id;
            }
            
            const response = await fetch('/api/test', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify(requestBody)
            });
            const result = await response.json();
            showToast(result.message, result.success ? 'success' : 'error');
            bootstrap.Modal.getInstance(document.getElementById('testDeviceModal')).hide();
            
            // 清除模板ID
            document.getElementById('testTemplateId').value = '';
        } catch (error) {
            showToast('测试失败', 'error');
        } finally {
            this.disabled = false;
            this.innerHTML = '推送';
        }
    });
}

// 加载模板
async function loadTemplates() {
    try {
        const response = await fetch('/api/templates');
        const result = await response.json();
        
        if (result.success) {
            templates = result.data;
            renderTemplates();
            updateTemplateCount();
        }
    } catch (error) {
        showToast('加载模板失败', 'error');
    }
}

// 加载设备
async function loadDevices() {
    try {
        const response = await fetch('/api/devices');
        const result = await response.json();
        
        if (result.success) {
            devices = result.data;
            renderDevices();
            updateDeviceCount();
        }
    } catch (error) {
        showToast('加载设备失败', 'error');
    }
}

// 渲染模板列表
function renderTemplates() {
    const container = document.getElementById('templatesList');
    container.innerHTML = '';
    
    Object.entries(templates).forEach(([id, template]) => {
        const card = document.createElement('div');
        card.className = 'col-md-6 col-lg-4 mb-3';
        card.innerHTML = `
            <div class="card template-card">
                <div class="card-body">
                    <div class="d-flex justify-content-between align-items-start mb-2">
                        <h6 class="card-title mb-0">${template.name}</h6>
                        <span class="${template.enabled ? 'enabled-badge' : 'disabled-badge'}">
                            ${template.enabled ? '启用' : '禁用'}
                        </span>
                    </div>
                    <p class="card-text text-muted small">ID: ${id}</p>
                    <p class="card-text"><strong>时间:</strong> ${template.time}</p>
                    <p class="card-text"><strong>标题:</strong> ${template.title}</p>
                    <p class="card-text"><strong>内容:</strong> ${template.content.substring(0, 50)}${template.content.length > 50 ? '...' : ''}</p>
                    <div class="mt-3">
                        <button class="btn btn-sm btn-primary me-2" onclick="testTemplate('${id}')">
                            <i class="fas fa-paper-plane"></i> 测试
                        </button>
                        <button class="btn btn-sm btn-danger" onclick="deleteTemplate('${id}')">
                            <i class="fas fa-trash"></i> 删除
                        </button>
                    </div>
                </div>
            </div>
        `;
        container.appendChild(card);
    });
}

// 渲染设备列表
function renderDevices() {
    const container = document.getElementById('devicesList');
    container.innerHTML = '';
    
    Object.entries(devices).forEach(([id, device]) => {
        const card = document.createElement('div');
        card.className = 'col-md-6 col-lg-4 mb-3';
        card.innerHTML = `
            <div class="card device-card">
                <div class="card-body">
                    <h6 class="card-title">${device.name}</h6>
                    <p class="card-text text-muted small">ID: ${id}</p>
                    <p class="card-text"><strong>URL:</strong> ${device.url}</p>
                    ${device.description ? `<p class="card-text"><strong>描述:</strong> ${device.description}</p>` : ''}
                    <div class="mt-3">
                        <button class="btn btn-sm btn-danger" onclick="deleteDevice('${id}')">
                            <i class="fas fa-trash"></i> 删除
                        </button>
                    </div>
                </div>
            </div>
        `;
        container.appendChild(card);
    });
}

// 更新统计信息
function updateTemplateCount() {
    document.getElementById('templateCount').textContent = Object.keys(templates).length;
}

function updateDeviceCount() {
    document.getElementById('deviceCount').textContent = Object.keys(devices).length;
}

// 保存模板
async function saveTemplate() {
    const form = document.getElementById('addTemplateForm');
    const formData = new FormData(form);
    const data = {};
    
    for (let [key, value] of formData.entries()) {
        data[key] = value;
    }
    
    // 添加默认设备
    data.devices = ['default'];
    data.enabled = true;
    
    try {
        const response = await fetch('/api/templates', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(data)
        });
        
        const result = await response.json();
        
        if (result.success) {
            showToast(result.message, 'success');
            loadTemplates();
            bootstrap.Modal.getInstance(document.getElementById('addTemplateModal')).hide();
            form.reset();
        } else {
            showToast(result.message, 'error');
        }
    } catch (error) {
        showToast('保存模板失败', 'error');
    }
}

// 保存设备
async function saveDevice() {
    const form = document.getElementById('addDeviceForm');
    const formData = new FormData(form);
    const data = {};
    
    for (let [key, value] of formData.entries()) {
        data[key] = value;
    }
    
    try {
        const response = await fetch('/api/devices', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(data)
        });
        
        const result = await response.json();
        
        if (result.success) {
            showToast(result.message, 'success');
            loadDevices();
            bootstrap.Modal.getInstance(document.getElementById('addDeviceModal')).hide();
            form.reset();
        } else {
            showToast(result.message, 'error');
        }
    } catch (error) {
        showToast('保存设备失败', 'error');
    }
}

// 测试推送
async function testPush() {
    const btn = document.getElementById('testBtn');
    btn.disabled = true;
    btn.innerHTML = '<i class="fas fa-spinner fa-spin"></i> 发送中...';
    
    try {
        const response = await fetch('/api/test', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({})
        });
        
        const result = await response.json();
        showToast(result.message, result.success ? 'success' : 'error');
    } catch (error) {
        showToast('测试失败', 'error');
    } finally {
        btn.disabled = false;
        btn.innerHTML = '<i class="fas fa-paper-plane"></i> 测试推送';
    }
}

// 启动定时任务
async function startScheduler() {
    try {
        const response = await fetch('/api/scheduler/start', {
            method: 'POST'
        });
        
        const result = await response.json();
        showToast(result.message, result.success ? 'success' : 'error');
        
        if (result.success) {
            loadSchedulerStatus();
        }
    } catch (error) {
        showToast('启动失败', 'error');
    }
}

// 停止定时任务
async function stopScheduler() {
    try {
        const response = await fetch('/api/scheduler/stop', {
            method: 'POST'
        });
        
        const result = await response.json();
        showToast(result.message, result.success ? 'success' : 'error');
        
        if (result.success) {
            loadSchedulerStatus();
        }
    } catch (error) {
        showToast('停止失败', 'error');
    }
}

// 刷新配置
async function refreshScheduler() {
    try {
        const response = await fetch('/api/scheduler/refresh', {
            method: 'POST'
        });
        
        const result = await response.json();
        showToast(result.message, result.success ? 'success' : 'error');
        
        if (result.success) {
            loadSchedulerStatus();
        }
    } catch (error) {
        showToast('刷新失败', 'error');
    }
}

// 模板操作函数
async function testTemplate(templateId) {
    // 动态填充设备列表
    const select = document.getElementById('testDeviceSelect');
    select.innerHTML = '<option value="all">全部设备</option>';
    Object.entries(devices).forEach(([id, device]) => {
        select.innerHTML += `<option value="${id}">${device.name}</option>`;
    });
    
    // 设置模板ID到模态框
    document.getElementById('testTemplateId').value = templateId;
    
    // 显示模态框
    var modal = new bootstrap.Modal(document.getElementById('testDeviceModal'));
    modal.show();
}

async function deleteTemplate(templateId) {
    if (confirm('确定要删除这个模板吗？')) {
        try {
            const response = await fetch(`/api/templates/${templateId}`, {
                method: 'DELETE'
            });
            
            const result = await response.json();
            showToast(result.message, result.success ? 'success' : 'error');
            
            if (result.success) {
                loadTemplates();
            }
        } catch (error) {
            showToast('删除失败', 'error');
        }
    }
}

async function deleteDevice(deviceId) {
    if (confirm('确定要删除这个设备吗？')) {
        try {
            const response = await fetch(`/api/devices/${deviceId}`, {
                method: 'DELETE'
            });
            
            const result = await response.json();
            showToast(result.message, result.success ? 'success' : 'error');
            
            if (result.success) {
                loadDevices();
            }
        } catch (error) {
            showToast('删除失败', 'error');
        }
    }
}

// 加载定时任务状态
async function loadSchedulerStatus() {
    try {
        const response = await fetch('/api/scheduler/status');
        const result = await response.json();
        
        if (result.success) {
            const indicator = document.getElementById('statusIndicator');
            const statusText = document.getElementById('statusText');
            
            if (result.data.running) {
                indicator.className = 'status-indicator status-running';
                statusText.textContent = '运行中';
            } else {
                indicator.className = 'status-indicator status-stopped';
                statusText.textContent = '已停止';
            }
        }
    } catch (error) {
        console.error('加载状态失败:', error);
    }
}

// 加载日志
async function loadLogs() {
    try {
        const response = await fetch('/api/logs');
        const result = await response.json();
        
        if (result.success) {
            const container = document.getElementById('logContainer');
            
            if (result.data.length > 0) {
                container.innerHTML = result.data.map(log => 
                    `<div class="text-muted">${log}</div>`
                ).join('');
                container.scrollTop = container.scrollHeight;
            } else {
                container.innerHTML = '<div class="text-muted">暂无日志...</div>';
            }
        }
    } catch (error) {
        console.error('加载日志失败:', error);
    }
}

// 显示消息提示
function showToast(message, type = 'info') {
    const container = document.getElementById('toastContainer');
    const toastId = 'toast-' + Date.now();
    
    const bgClass = type === 'success' ? 'bg-success' : 
                   type === 'error' ? 'bg-danger' : 'bg-info';
    
    const toast = document.createElement('div');
    toast.className = `toast align-items-center text-white border-0 ${bgClass}`;
    toast.id = toastId;
    toast.setAttribute('role', 'alert');
    
    toast.innerHTML = `
        <div class="d-flex">
            <div class="toast-body">
                ${message}
            </div>
            <button type="button" class="btn-close btn-close-white me-2 m-auto" data-bs-dismiss="toast"></button>
        </div>
    `;
    
    container.appendChild(toast);
    
    const bsToast = new bootstrap.Toast(toast);
    bsToast.show();
    
    // 自动移除
    toast.addEventListener('hidden.bs.toast', function() {
        container.removeChild(toast);
    });
} 