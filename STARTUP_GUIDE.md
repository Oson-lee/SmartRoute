# SmartRoute 启动指南

## 🚀 快速启动

### 选项1：使用 PowerShell 脚本（推荐）
```powershell
./run_app.ps1
```

**优点**：
- ✓ 自动检查虚拟环境
- ✓ 自动检查依赖库
- ✓ 彩色输出，易于阅读
- ✓ 显示访问地址

### 选项2：使用 Batch 脚本
```cmd
run_app.bat
```

**优点**：
- ✓ 无需 PowerShell
- ✓ Windows 原生支持

### 选项3：手动启动
```powershell
cd d:\MyProjects\SmartRoute
python -m streamlit run app.py
```

---

## 🌐 访问应用

启动后在浏览器打开：
```
http://localhost:8501
```

---

## ⏹️ 停止应用

在运行终端中按：
```
Ctrl + C
```

---

## ❌ 如果终端卡死

### 方案1：强制杀死进程
```powershell
# 查看Python进程
Get-Process python

# 杀死指定PID的进程
Stop-Process -Id <PID> -Force
```

### 方案2：使用任务管理器
1. 按 `Ctrl+Shift+Esc` 打开任务管理器
2. 找到 `python.exe`
3. 右键 → "结束任务"

---

## 🕵️ 检查端口占用

如果 8501 端口被占用，改用其他端口：

```powershell
python -m streamlit run app.py --server.port 8502
```

或者查看占用端口的进程：

```powershell
# 查看占用 8501 的进程
netstat -ano | findstr :8501

# 杀死指定PID
taskkill /PID <PID> /F
```

---

## 📊 应用功能

1. **文本输入框**：输入你的问题
2. **实时路由**：系统自动判断复杂度
3. **智能调度**：选择 DeepSeek 或 豆包
4. **成本统计**：侧边栏显示节省金额
5. **对话历史**：保存所有交互记录

### 测试用例

**简单查询**（使用 DeepSeek）：
```
你好，今天天气怎么样？
```

**复杂查询**（使用豆包）：
```
请用机器学习方法优化微观市场执行算法
假设有限价单簿数据和历史成交数据
```

---

## 🔧 故障排查

| 问题 | 解决方案 |
|-----|--------|
| 终端卡死 | 按 Ctrl+C 或使用任务管理器杀死进程 |
| 端口被占用 | 改用 `--server.port 8502` |
| 模块导入失败 | 运行 `check_requirements.py` 检查依赖 |
| 页面无响应 | 刷新浏览器或重启应用 |
| API 返回错误 | 检查 `.env` 中的 API Key 配置 |

---

**版本**: 1.0  
**最后更新**: 2026-04-11
