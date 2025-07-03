// 全局变量
let devices = {};

// 页面加载完成后初始化
document.addEventListener('DOMContentLoaded', function() {
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
                        <button class="btn btn-sm btn-info me-2" onclick="manageDeviceTemplates('${id}')">
                            <i class="fas fa-cog"></i> 模板设置
                        </button>
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
function updateDeviceCount() {
    document.getElementById('deviceCount').textContent = Object.keys(devices).length;
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
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(data)
        });
        
        const result = await response.json();
        showToast(result.message, result.success ? 'success' : 'error');
        
        if (result.success) {
            bootstrap.Modal.getInstance(document.getElementById('addDeviceModal')).hide();
            form.reset();
            loadDevices();
        }
    } catch (error) {
        showToast('保存失败', 'error');
    }
}

// 测试推送
async function testPush() {
    const btn = document.getElementById('testBtn');
    btn.disabled = true;
    btn.innerHTML = '<i class="fas fa-paper-plane"></i> 推送中...';
    
    try {
        const response = await fetch('/api/test', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
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

// 设备操作函数
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

// 设备模板管理函数
async function manageDeviceTemplates(deviceId) {
    try {
        const response = await fetch(`/api/devices/${deviceId}/templates`);
        const result = await response.json();
        
        if (result.success) {
            const device = devices[deviceId];
            document.getElementById('deviceTemplateDeviceName').textContent = device.name;
            document.getElementById('addTemplateDeviceId').value = deviceId;
            
            const container = document.getElementById('deviceTemplatesList');
            container.innerHTML = '';
            
            Object.entries(result.data).forEach(([templateId, template]) => {
                const card = document.createElement('div');
                card.className = 'card mb-3';
                card.innerHTML = `
                    <div class="card-body">
                        <div class="d-flex justify-content-between align-items-start mb-2">
                            <h6 class="card-title mb-0">${template.name}</h6>
                            <span class="badge ${template.enabled ? 'bg-success' : 'bg-secondary'}">
                                ${template.enabled ? '启用' : '禁用'}
                            </span>
                        </div>
                        <p class="card-text text-muted small">ID: ${templateId}</p>
                        <p class="card-text"><strong>时间:</strong> ${template.time}</p>
                        <p class="card-text"><strong>标题:</strong> ${template.title}</p>
                        <p class="card-text"><strong>内容:</strong> ${template.content.substring(0, 100)}${template.content.length > 100 ? '...' : ''}</p>
                        <div class="mt-3">
                            <button class="btn btn-sm btn-primary me-2" onclick="editDeviceTemplate('${deviceId}', '${templateId}')">
                                <i class="fas fa-edit"></i> 编辑
                            </button>
                            <button class="btn btn-sm btn-warning me-2" onclick="testDeviceTemplate('${deviceId}', '${templateId}')">
                                <i class="fas fa-paper-plane"></i> 测试
                            </button>
                            <button class="btn btn-sm btn-danger" onclick="deleteDeviceTemplate('${deviceId}', '${templateId}')">
                                <i class="fas fa-trash"></i> 删除
                            </button>
                        </div>
                    </div>
                `;
                container.appendChild(card);
            });
            
            // 显示模态框
            var modal = new bootstrap.Modal(document.getElementById('deviceTemplateModal'));
            modal.show();
        } else {
            showToast(result.message, 'error');
        }
    } catch (error) {
        showToast('加载设备模板失败', 'error');
    }
}

// 新增模板到设备
function addTemplateToDevice() {
    // 隐藏设备模板管理模态框
    bootstrap.Modal.getInstance(document.getElementById('deviceTemplateModal')).hide();
    
    // 显示新增模板模态框
    var modal = new bootstrap.Modal(document.getElementById('addDeviceTemplateModal'));
    modal.show();
}

// 编辑设备模板
async function editDeviceTemplate(deviceId, templateId) {
    try {
        const response = await fetch(`/api/devices/${deviceId}/templates/${templateId}`);
        const result = await response.json();
        
        if (result.success) {
            const template = result.data;
            document.getElementById('editDeviceId').value = deviceId;
            document.getElementById('editTemplateId').value = templateId;
            document.getElementById('editTemplateName').value = template.name;
            document.getElementById('editTemplateTime').value = template.time;
            document.getElementById('editDeviceTemplateTitle').value = template.title;
            document.getElementById('editDeviceTemplateContent').value = template.content;
            document.getElementById('editTemplateEnabled').checked = template.enabled;
            
            // 隐藏设备模板管理模态框
            bootstrap.Modal.getInstance(document.getElementById('deviceTemplateModal')).hide();
            
            // 显示编辑模态框
            var modal = new bootstrap.Modal(document.getElementById('editDeviceTemplateModal'));
            modal.show();
        } else {
            showToast(result.message, 'error');
        }
    } catch (error) {
        showToast('加载模板详情失败', 'error');
    }
}

// 测试设备模板
async function testDeviceTemplate(deviceId, templateId) {
    try {
        const response = await fetch('/api/test', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ template_id: templateId, device_id: deviceId })
        });
        
        const result = await response.json();
        showToast(result.message, result.success ? 'success' : 'error');
    } catch (error) {
        showToast('测试失败', 'error');
    }
}

// 删除设备模板
async function deleteDeviceTemplate(deviceId, templateId) {
    if (confirm('确定要删除这个模板吗？')) {
        try {
            const response = await fetch(`/api/devices/${deviceId}/templates/${templateId}`, {
                method: 'DELETE'
            });
            
            const result = await response.json();
            showToast(result.message, result.success ? 'success' : 'error');
            
            if (result.success) {
                // 重新加载设备模板管理页面
                manageDeviceTemplates(deviceId);
            }
        } catch (error) {
            showToast('删除失败', 'error');
        }
    }
}

// 绑定设备模板编辑事件
document.addEventListener('DOMContentLoaded', function() {
    // 保存新增设备模板
    document.getElementById('saveDeviceTemplateBtn').addEventListener('click', async function() {
        const form = document.getElementById('addDeviceTemplateForm');
        const formData = new FormData(form);
        const data = {};
        
        for (let [key, value] of formData.entries()) {
            if (key === 'enabled') {
                data[key] = document.getElementById('addTemplateEnabled').checked;
            } else {
                data[key] = value;
            }
        }
        
        const deviceId = data.device_id;
        delete data.device_id;
        
        this.disabled = true;
        this.innerHTML = '保存中...';
        
        try {
            const response = await fetch(`/api/devices/${deviceId}/templates`, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify(data)
            });
            
            const result = await response.json();
            showToast(result.message, result.success ? 'success' : 'error');
            
            if (result.success) {
                bootstrap.Modal.getInstance(document.getElementById('addDeviceTemplateModal')).hide();
                form.reset();
                // 重新加载设备模板管理页面
                manageDeviceTemplates(deviceId);
            }
        } catch (error) {
            showToast('保存失败', 'error');
        } finally {
            this.disabled = false;
            this.innerHTML = '保存模板';
        }
    });
    
    // 更新设备模板
    document.getElementById('updateDeviceTemplateBtn').addEventListener('click', async function() {
        const form = document.getElementById('editDeviceTemplateForm');
        const formData = new FormData(form);
        const data = {};
        
        for (let [key, value] of formData.entries()) {
            if (key === 'enabled') {
                data[key] = document.getElementById('editTemplateEnabled').checked;
            } else {
                data[key] = value;
            }
        }
        
        const deviceId = data.device_id;
        const templateId = data.template_id;
        delete data.device_id;
        delete data.template_id;
        
        this.disabled = true;
        this.innerHTML = '保存中...';
        
        try {
            const response = await fetch(`/api/devices/${deviceId}/templates/${templateId}`, {
                method: 'PUT',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify(data)
            });
            
            const result = await response.json();
            showToast(result.message, result.success ? 'success' : 'error');
            
            if (result.success) {
                bootstrap.Modal.getInstance(document.getElementById('editDeviceTemplateModal')).hide();
                // 重新加载设备模板管理页面
                manageDeviceTemplates(deviceId);
            }
        } catch (error) {
            showToast('保存失败', 'error');
        } finally {
            this.disabled = false;
            this.innerHTML = '保存';
        }
    });
    
    // 删除设备模板
    document.getElementById('deleteDeviceTemplateBtn').addEventListener('click', async function() {
        const deviceId = document.getElementById('editDeviceId').value;
        const templateId = document.getElementById('editTemplateId').value;
        
        if (confirm('确定要删除这个模板吗？')) {
            this.disabled = true;
            this.innerHTML = '删除中...';
            
            try {
                const response = await fetch(`/api/devices/${deviceId}/templates/${templateId}`, {
                    method: 'DELETE'
                });
                
                const result = await response.json();
                showToast(result.message, result.success ? 'success' : 'error');
                
                if (result.success) {
                    bootstrap.Modal.getInstance(document.getElementById('editDeviceTemplateModal')).hide();
                    // 重新加载设备模板管理页面
                    manageDeviceTemplates(deviceId);
                }
            } catch (error) {
                showToast('删除失败', 'error');
            } finally {
                this.disabled = false;
                this.innerHTML = '删除模板';
            }
        }
    });
}); 