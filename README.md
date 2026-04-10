# 🧭 SmartRoute: 智能大模型路由网关 (MVP)

![Python Version](https://img.shields.io/badge/Python-3.10%2B-blue)
![Streamlit](https://img.shields.io/badge/Streamlit-1.30%2B-red)
![License](https://img.shields.io/badge/License-MIT-green)

> **SmartRoute** 是一个极简、低延迟的大模型 (LLM) API 动态路由中间件。它基于纯数学启发式算法评估 Prompt 复杂度，自动将简单任务路由给低成本模型，复杂任务路由给高智商模型，在不损失体验的前提下大幅降低 AI API 调用成本。

🌐 **[在线体验 Demo (Streamlit Cloud)](https://smartroute-osonlee.streamlit.app/)** 

---

## 💡 背景与痛点

目前企业和开发者接入 AI 时，往往采用“一刀切”的全局顶配模型（如 GPT-4o 或 Claude 3.5 Sonnet）。然而，日常对话中有大量基础翻译、简单闲聊或文本格式化任务，全量使用高智商模型造成了极大的算力浪费与资金损耗。

**核心洞察：** 并非所有 Prompt 都需要昂贵的模型。通过精准评估任务复杂度，我们可以实现分流调配。

## ✨ 核心功能 (MVP 阶段)

* **⚡️ 极速特征提取：** 毫秒级解析用户输入的文本特征（长度、逻辑词密度、特殊符号）。
* **🧠 启发式动态路由：** 摒弃笨重的机器学习模型，采用纯数学向量运算输出复杂度概率。
* **💰 成本节省可视化：** 前端直观展示本次路由决策、调用的具体模型，并实时测算为您节省的 API 费用。

## 📐 核心数学逻辑 (启发式路由引擎)

本项目的路由引擎 (`router.py`) 基于逻辑回归思想构建：

**1. 特征向量构建**
提取文本特征构建向量 $\mathbf{v} \in \mathbb{R}^3$：
* $v_1$：文本长度归一化
* $v_2$：逻辑关联词（如“因为”、“证明”）密度
* $v_3$：特殊符号（如代码块、数学符号）密度

**2. 复杂度线性组合与概率映射**
利用权重向量 $\mathbf{w}$ 和偏置项 $b$ 计算得分 $S(x)$，并通过 Sigmoid 函数映射为高复杂度概率 $P(\text{hard})$：
$$P(\text{hard}) = \frac{1}{1 + e^{-(\mathbf{w}^T \mathbf{v} + b)}}$$

**3. 动态分发**
预设阈值 $\tau = 0.6$。若概率超标，触发 **High-IQ Route (如 Qwen-Plus)**；反之触发 **Low-Cost Route (如 DeepSeek-Chat)**。

## 🛠️ 技术栈与支持模型

* **核心语言：** Python 3.10+
* **底层数学框架：** `NumPy`
* **前端交互/可视化：** `Streamlit`
* **大模型调用：** 基于 `openai` 官方库封装的兼容层
    * *Low-Cost 组：* DeepSeek API
    * *High-IQ 组：* 火山引擎豆包 (Doubao)

---

## 🚀 快速上手 (Local Quick Start)

### 1. 克隆仓库

```bash
git clone https://github.com/yourusername/SmartRoute.git
cd SmartRoute
```

### 2. 创建虚拟环境并安装依赖

```bash
# 创建虚拟环境
python -m venv venv

# Windows 激活
venv\Scripts\activate

# Mac/Linux 激活
source venv/bin/activate

# 安装依赖
pip install -r requirements.txt
```

### 3. 配置环境变量

在项目根目录创建 `.env` 文件，并填入以下内容（不可包含中文）：

```env
# Low-Cost 路由 (DeepSeek)
DEEPSEEK_API_KEY="sk-xxxxxxxxxxxx"
DEEPSEEK_BASE_URL="https://api.deepseek.com/v1"

# High-IQ 路由 (豆包)
DOUBAO_API_KEY="sk-xxxxxxxxxxxx"
DOUBAO_BASE_URL="https://api.doubao.com/v1"
```

### 4. 启动可视化界面

```bash
streamlit run app.py
```

然后在浏览器打开：`http://localhost:8501`

---

## 📂 项目结构

```
SmartRoute/
├── app.py                  # Streamlit Web UI 与交互逻辑
├── router.py               # 数学启发式路由引擎 (大脑)
├── llm_client.py           # 大模型 API 兼容调度器 (神经)
├── check_requirements.py    # 依赖检查工具
├── requirements.txt        # 依赖清单
├── .env.example            # 环境变量模板
├── .gitignore              # Git 忽略文件 (防止密钥泄露)
├── CONFIG_GUIDE.md         # 配置指南
├── STARTUP_GUIDE.md        # 启动指南
├── CHANGELOG.md            # 改动日志
└── README.md               # 本项目说明
```

---

## 🗺️ 未来规划 (Roadmap)

- [ ] **数据持久化**：接入轻量级云数据库存储历史路由决策
- [ ] **算法自进化**：引入用户反馈机制，基于真实语料训练微调路由权重
- [ ] **多模型熔断**：当首选 API 宕机时，自动降级切换至备用模型
- [ ] **性能优化**：缓存路由结果，支持批量请求
- [ ] **监控告警**：实时成本监控和异常告警机制

---

## 📝 许可证

MIT License - 详见 [LICENSE](LICENSE) 文件

---

## 🤝 贡献

欢迎提交 Issue 和 Pull Request！

---

**最后更新**：2026-04-11  
**版本**：1.0 (MVP)

