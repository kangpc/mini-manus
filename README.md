<p align="center">
  <img src="assets/logo.jpg" width="200"/>
</p>

English | [中文](README_zh.md) | [한국어](README_ko.md) | [日本語](README_ja.md)

[![GitHub stars](https://img.shields.io/github/stars/FoundationAgents/OpenManus?style=social)](https://github.com/FoundationAgents/OpenManus/stargazers)
&ensp;
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT) &ensp;
[![Discord Follow](https://dcbadge.vercel.app/api/server/DYn29wFk9z?style=flat)](https://discord.gg/DYn29wFk9z)
[![Demo](https://img.shields.io/badge/Demo-Hugging%20Face-yellow)](https://huggingface.co/spaces/lyh-917/OpenManusDemo)
[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.15186407.svg)](https://doi.org/10.5281/zenodo.15186407)

# 👋 OpenManus

Manus is incredible, but OpenManus can achieve any idea without an *Invite Code* 🛫!

Our team members [@Xinbin Liang](https://github.com/mannaandpoem) and [@Jinyu Xiang](https://github.com/XiangJinyu) (core authors), along with [@Zhaoyang Yu](https://github.com/MoshiQAQ), [@Jiayi Zhang](https://github.com/didiforgithub), and [@Sirui Hong](https://github.com/stellaHSR), we are from [@MetaGPT](https://github.com/geekan/MetaGPT). The prototype is launched within 3 hours and we are keeping building!

It's a simple implementation, so we welcome any suggestions, contributions, and feedback!

Enjoy your own agent with OpenManus!

We're also excited to introduce [OpenManus-RL](https://github.com/OpenManus/OpenManus-RL), an open-source project dedicated to reinforcement learning (RL)- based (such as GRPO) tuning methods for LLM agents, developed collaboratively by researchers from UIUC and OpenManus.

## Project Demo

<video src="https://private-user-images.githubusercontent.com/61239030/420168772-6dcfd0d2-9142-45d9-b74e-d10aa75073c6.mp4?jwt=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJnaXRodWIuY29tIiwiYXVkIjoicmF3LmdpdGh1YnVzZXJjb250ZW50LmNvbSIsImtleSI6ImtleTUiLCJleHAiOjE3NDEzMTgwNTksIm5iZiI6MTc0MTMxNzc1OSwicGF0aCI6Ii82MTIzOTAzMC80MjAxNjg3NzItNmRjZmQwZDItOTE0Mi00NWQ5LWI3NGUtZDEwYWE3NTA3M2M2Lm1wND9YLUFtei1BbGdvcml0aG09QVdTNC1ITUFDLVNIQTI1NiZYLUFtei1DcmVkZW50aWFsPUFLSUFWQ09EWUxTQTUzUFFLNFpBJTJGMjAyNTAzMDclMkZ1cy1lYXN0LTElMkZzMyUyRmF3czRfcmVxdWVzdCZYLUFtei1EYXRlPTIwMjUwMzA3VDAzMjIzOVomWC1BbXotRXhwaXJlcz0zMDAmWC1BbXotU2lnbmF0dXJlPTdiZjFkNjlmYWNjMmEzOTliM2Y3M2VlYjgyNDRlZDJmOWE3NWZhZjE1MzhiZWY4YmQ3NjdkNTYwYTU5ZDA2MzYmWC1BbXotU2lnbmVkSGVhZGVycz1ob3N0In0.UuHQCgWYkh0OQq9qsUWqGsUbhG3i9jcZDAMeHjLt5T4" data-canonical-src="https://private-user-images.githubusercontent.com/61239030/420168772-6dcfd0d2-9142-45d9-b74e-d10aa75073c6.mp4?jwt=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJnaXRodWIuY29tIiwiYXVkIjoicmF3LmdpdGh1YnVzZXJjb250ZW50LmNvbSIsImtleSI6ImtleTUiLCJleHAiOjE3NDEzMTgwNTksIm5iZiI6MTc0MTMxNzc1OSwicGF0aCI6Ii82MTIzOTAzMC80MjAxNjg3NzItNmRjZmQwZDItOTE0Mi00NWQ5LWI3NGUtZDEwYWE3NTA3M2M2Lm1wND9YLUFtei1BbGdvcml0aG09QVdTNC1ITUFDLVNIQTI1NiZYLUFtei1DcmVkZW50aWFsPUFLSUFWQ09EWUxTQTUzUFFLNFpBJTJGMjAyNTAzMDclMkZ1cy1lYXN0LTElMkZzMyUyRmF3czRfcmVxdWVzdCZYLUFtei1EYXRlPTIwMjUwMzA3VDAzMjIzOVomWC1BbXotRXhwaXJlcz0zMDAmWC1BbXotU2lnbmF0dXJlPTdiZjFkNjlmYWNjMmEzOTliM2Y3M2VlYjgyNDRlZDJmOWE3NWZhZjE1MzhiZWY4YmQ3NjdkNTYwYTU5ZDA2MzYmWC1BbXotU2lnbmVkSGVhZGVycz1ob3N0In0.UuHQCgWYkh0OQq9qsUWqGsUbhG3i9jcZDAMeHjLt5T4" controls="controls" muted="muted" class="d-block rounded-bottom-2 border-top width-fit" style="max-height:640px; min-height: 200px"></video>

## Installation

We provide two installation methods. Method 2 (using uv) is recommended for faster installation and better dependency management.

### Method 1: Using conda

1. Create a new conda environment:

```bash
conda create -n open_manus python=3.12
conda activate open_manus
```

2. Clone the repository:

```bash
git clone https://github.com/FoundationAgents/OpenManus.git
cd OpenManus
```

3. Install dependencies:

```bash
pip install -r requirements.txt
```

### Method 2: Using uv (Recommended)

1. Install uv (A fast Python package installer and resolver):

```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

2. Clone the repository:

```bash
git clone https://github.com/FoundationAgents/OpenManus.git
cd OpenManus
```

3. Create a new virtual environment and activate it:

```bash
uv venv --python 3.12
source .venv/bin/activate  # On Unix/macOS
# Or on Windows:
# .venv\Scripts\activate
```

4. Install dependencies:

```bash
uv pip install -r requirements.txt
```

### Browser Automation Tool (Optional)
```bash
playwright install
```

## Configuration

OpenManus requires configuration for the LLM APIs it uses. Follow these steps to set up your configuration:

1. Create a `config.toml` file in the `config` directory (you can copy from the example):

```bash
cp config/config.example.toml config/config.toml
```

2. Edit `config/config.toml` to add your API keys and customize settings:

```toml
# Global LLM configuration
[llm]
model = "gpt-4o"
base_url = "https://api.openai.com/v1"
api_key = "sk-..."  # Replace with your actual API key
max_tokens = 4096
temperature = 0.0

# Optional configuration for specific LLM models
[llm.vision]
model = "gpt-4o"
base_url = "https://api.openai.com/v1"
api_key = "sk-..."  # Replace with your actual API key
```

## Quick Start

One line for run OpenManus:

```bash
python main.py
```

Then input your idea via terminal!

For MCP tool version, you can run:
```bash
python run_mcp.py
```

For unstable multi-agent version, you also can run:

```bash
python run_flow.py
```

### Custom Adding Multiple Agents

Currently, besides the general OpenManus Agent, we have also integrated the DataAnalysis Agent, which is suitable for data analysis and data visualization tasks. You can add this agent to `run_flow` in `config.toml`.

```toml
# Optional configuration for run-flow
[runflow]
use_data_analysis_agent = true     # Disabled by default, change to true to activate
```
In addition, you need to install the relevant dependencies to ensure the agent runs properly: [Detailed Installation Guide](app/tool/chart_visualization/README.md##Installation)

## How to contribute

We welcome any friendly suggestions and helpful contributions! Just create issues or submit pull requests.

Or contact @mannaandpoem via 📧email: mannaandpoem@gmail.com

**Note**: Before submitting a pull request, please use the pre-commit tool to check your changes. Run `pre-commit run --all-files` to execute the checks.

## Community Group
Join our networking group on Feishu and share your experience with other developers!

<div align="center" style="display: flex; gap: 20px;">
    <img src="assets/community_group.jpg" alt="OpenManus 交流群" width="300" />
</div>

## Star History

[![Star History Chart](https://api.star-history.com/svg?repos=FoundationAgents/OpenManus&type=Date)](https://star-history.com/#FoundationAgents/OpenManus&Date)

## Sponsors
Thanks to [PPIO](https://ppinfra.com/user/register?invited_by=OCPKCN&utm_source=github_openmanus&utm_medium=github_readme&utm_campaign=link) for computing source support.
> PPIO: The most affordable and easily-integrated MaaS and GPU cloud solution.


## Acknowledgement

Thanks to [anthropic-computer-use](https://github.com/anthropics/anthropic-quickstarts/tree/main/computer-use-demo)
and [browser-use](https://github.com/browser-use/browser-use) for providing basic support for this project!

Additionally, we are grateful to [AAAJ](https://github.com/metauto-ai/agent-as-a-judge), [MetaGPT](https://github.com/geekan/MetaGPT), [OpenHands](https://github.com/All-Hands-AI/OpenHands) and [SWE-agent](https://github.com/SWE-agent/SWE-agent).

We also thank stepfun(阶跃星辰) for supporting our Hugging Face demo space.

OpenManus is built by contributors from MetaGPT. Huge thanks to this agent community!

## Cite
```bibtex
@misc{openmanus2025,
  author = {Xinbin Liang and Jinyu Xiang and Zhaoyang Yu and Jiayi Zhang and Sirui Hong and Sheng Fan and Xiao Tang},
  title = {OpenManus: An open-source framework for building general AI agents},
  year = {2025},
  publisher = {Zenodo},
  doi = {10.5281/zenodo.15186407},
  url = {https://doi.org/10.5281/zenodo.15186407},
}
```

# OpenManus 迷你版

一个简化版的AI智能体框架，用于学习和理解OpenManus的核心架构设计。

## 🎯 项目目标

通过构建一个迷你版本，帮助开发者快速理解：
- AI智能体的基本架构和工作原理
- 工具系统的插件化设计模式
- 配置管理和环境变量的最佳实践
- 异步编程在AI应用中的应用
- 真实LLM API的集成和使用

## ✨ 主要特性

- 🤖 **真实LLM集成**: 支持OpenAI、Anthropic、Qwen等多种LLM API
- 🔧 **插件化工具系统**: 计算器、文件编辑器、Python执行器等
- ⚙️ **灵活配置管理**: 支持.env文件、环境变量、JSON配置
- 🔒 **安全执行环境**: 文件操作安全检查、代码执行沙箱
- 📊 **详细执行统计**: 工具调用统计、性能监控
- 🎯 **类比学习设计**: 基于pytest框架的设计理念

## 🏗️ 架构设计

### 核心组件

```
用户输入 → LLM理解 → 计划生成 → 工具执行 → 结果反馈
   ↓         ↓         ↓         ↓         ↓
"计算2+3" → Qwen分析 → JSON计划 → Calculator → "结果: 5"
```

### 类比pytest框架

| OpenManus组件 | pytest对应组件 | 作用 |
|---------------|----------------|------|
| BaseAgent | TestCase | 组织和执行逻辑 |
| BaseTool | Fixture | 提供具体功能 |
| ToolCollection | 插件管理器 | 管理工具集合 |
| Config | pytest.ini | 配置管理 |
| LLMClient | 测试运行器 | 核心执行引擎 |

## 🚀 快速开始

### 1. 环境准备

```bash
# 克隆项目
git clone <repository-url>
cd mini-manus

# 安装依赖
pip install openai python-dotenv

# 可选：安装Anthropic支持
pip install anthropic

# 可选：安装数据库驱动
pip install pymysql          # MySQL支持
pip install psycopg2-binary  # PostgreSQL支持
```

### 2. 配置API密钥

创建 `.env` 文件并配置您的API信息：

```bash
# .env 文件示例
MODEL="Qwen/Qwen3-8B"
BASE_URL="https://api.siliconflow.cn/v1"
API_KEY="your-api-key-here"

# 或者使用OpenAI
# MODEL="gpt-3.5-turbo"
# BASE_URL="https://api.openai.com/v1"
# API_KEY="sk-your-openai-key"
```

### 3. 运行智能体

```bash
# 启动智能体
python main.py
```

### 4. 交互示例

```
🤖 欢迎使用 OpenManus 迷你版!
==================================================
🔧 从 .env 文件加载配置: .env
🌍 从环境变量加载: model = Qwen/Qwen3-8B
✅ 配置验证通过
🔧 使用 OpenAI 兼容客户端，模型: Qwen/Qwen3-8B
🚀 智能体 'MiniManus' 初始化完成
📦 可用工具: calculator, file_editor, python_executor, database

💡 输入您的指令，输入 'quit' 退出
------------------------------

👤 您: 计算 2 + 3 * 4

🤔 智能体正在思考...
🎯 开始执行任务: 计算 2 + 3 * 4
� 执行计划: 计算表达式 2 + 3 * 4 的值
📍 执行步骤 1/1: 使用计算器工具计算数学表达式

🤖 智能体: 步骤1: ✅ calculator: 计算结果: 2 + 3 * 4 = 14
```

## 📁 项目结构

```
mini-manus/
├── __init__.py              # 包初始化和导出
├── main.py                  # 主入口文件
├── config.py                # 配置管理（支持.env文件）
├── agent.py                 # 智能体核心逻辑
├── llm.py                   # LLM客户端（OpenAI/Anthropic）
├── .env                     # 环境变量配置文件
├── file_editor_demo.py      # 文件编辑工具演示
├── database_demo.py         # 数据库工具演示
├── tools/                   # 工具系统
│   ├── __init__.py          # 工具基类和管理器
│   ├── calculator.py        # 数学计算器工具
│   ├── file_editor.py       # 文件编辑工具
│   ├── python_executor.py   # Python代码执行工具
│   └── database.py          # 数据库查询工具
└── README.md               # 项目说明文档
```

## 🔧 配置说明

### 环境变量配置 (.env)

推荐使用 `.env` 文件进行配置：

```bash
# 必需配置
MODEL="Qwen/Qwen3-8B"                    # 模型名称
BASE_URL="https://api.siliconflow.cn/v1" # API基础URL
API_KEY="your-api-key-here"              # API密钥

# 可选配置
MAX_TOKENS="2000"                        # 最大token数
TEMPERATURE="0.7"                        # 温度参数
```

### 支持的LLM提供商

| 提供商 | 模型示例 | BASE_URL |
|--------|----------|----------|
| **硅基流动** | Qwen/Qwen3-8B, deepseek-chat | https://api.siliconflow.cn/v1 |
| **OpenAI** | gpt-3.5-turbo, gpt-4 | https://api.openai.com/v1 |
| **Anthropic** | claude-3-sonnet | https://api.anthropic.com |
| **月之暗面** | moonshot-v1-8k | https://api.moonshot.cn/v1 |
| **智谱AI** | glm-4 | https://open.bigmodel.cn/api/paas/v4 |

### 传统JSON配置（可选）

也可以使用 `config.json` 文件：

```json
{
  "model": "gpt-3.5-turbo",
  "api_key": "your-api-key",
  "base_url": "https://api.openai.com/v1",
  "max_tokens": 2000,
  "temperature": 0.7,
  "tools": {
    "calculator": {"enabled": true},
    "file_editor": {"enabled": true, "max_file_size": 1048576},
    "python_executor": {"enabled": true, "timeout": 30},
    "database": {"enabled": true, "max_rows": 100, "query_timeout": 30}
  }
}
```

## 🛠️ 工具系统详解

### 内置工具

#### 1. 计算器工具 (Calculator)
- **功能**: 安全的数学表达式计算
- **支持**: 基本运算、数学函数、常数
- **示例**: `计算 2 + 3 * sqrt(16)`

```python
# 支持的功能
expressions = [
    "2 + 3 * 4",           # 基本运算
    "sqrt(16) + sin(pi/2)", # 数学函数
    "max(1, 2, 3)",        # 聚合函数
    "2**3 + log10(100)"    # 幂运算和对数
]
```

#### 2. 文件编辑工具 (FileEditor)
- **功能**: 安全的文件操作
- **支持**: 读取、写入、创建、删除、备份、恢复
- **安全**: 路径检查、文件类型限制、大小限制

```python
# 支持的操作
operations = {
    "read": "读取文件内容",
    "write": "写入文件内容",
    "create": "创建新文件",
    "delete": "删除文件",
    "list": "列出目录内容",
    "info": "获取文件信息",
    "backup": "备份文件",
    "restore": "恢复文件"
}
```

#### 3. Python执行工具 (PythonExecutor)
- **功能**: 安全的Python代码执行
- **安全**: 沙箱环境、禁用危险模块、执行超时
- **支持**: 基本语法、数学计算、数据处理

```python
# 支持的Python功能
code_examples = [
    "print('Hello, World!')",
    "[x**2 for x in range(5)]",
    "import math; math.sqrt(16)",
    "def factorial(n): return 1 if n <= 1 else n * factorial(n-1)"
]
```

#### 4. 数据库工具 (DatabaseTool)
- **功能**: 安全的数据库查询操作
- **支持**: SQLite、MySQL、PostgreSQL（仅SELECT查询）
- **安全**: SQL注入防护、查询结果限制、连接管理

```python
# 支持的操作
operations = {
    "connect": "连接数据库",
    "query": "执行SELECT查询",
    "show_tables": "显示所有表",
    "describe": "显示表结构",
    "status": "显示连接状态",
    "disconnect": "断开连接"
}

# 使用示例
examples = [
    '连接SQLite: {"action": "connect", "db_type": "sqlite", "connection_string": "test.db"}',
    '查询数据: {"action": "query", "sql": "SELECT * FROM users LIMIT 10"}',
    '显示表: {"action": "show_tables"}',
    '表结构: {"action": "describe", "table": "users"}'
]
```

### 创建自定义工具

```python
from tools import BaseTool

class WeatherTool(BaseTool):
    def __init__(self):
        super().__init__()
        self.name = "weather"
        self.description = "获取天气信息"

    def validate_args(self, **kwargs) -> bool:
        return 'city' in kwargs

    async def execute(self, **kwargs) -> str:
        city = kwargs.get('city')
        # 实现天气查询逻辑
        return f"{city}的天气：晴天，25°C"
```

### 创建专业智能体

```python
from agent import BaseAgent

class WeatherAgent(BaseAgent):
    def _setup_tools(self):
        # 只加载天气相关工具
        self.tools.add_tool(WeatherTool())
        self.tools.add_tool(Calculator())  # 用于温度转换

    async def _generate_plan(self, user_input: str):
        # 专门处理天气查询的计划生成
        if "天气" in user_input:
            return {
                "summary": "天气查询任务",
                "steps": [{"tool": "weather", "args": {"city": "北京"}}]
            }
        return await super()._generate_plan(user_input)
```

## 🧪 测试和调试

### 运行工具测试

```bash
# 测试计算器工具
python tools/calculator.py

# 测试文件编辑工具演示
python file_editor_demo.py

# 测试数据库工具演示
python database_demo.py

# 测试Python执行工具
python tools/python_executor.py

# 测试LLM客户端配置
python llm.py

# 生成示例配置文件
python config.py
```

### 使用示例

#### 数学计算示例
```bash
👤 您: 计算圆的面积，半径是5
🤖 智能体: ✅ calculator: 计算结果: pi * 5**2 = 78.54
```

#### 文件操作示例
```bash
👤 您: 创建一个hello.txt文件，内容是"Hello World"
🤖 智能体: ✅ file_editor: 文件创建成功: hello.txt

👤 您: 读取hello.txt的内容
🤖 智能体: ✅ file_editor: 文件内容: Hello World
```

#### Python代码示例
```bash
👤 您: 用Python生成1到10的平方数列表
🤖 智能体: ✅ python_executor: 执行结果: [1, 4, 9, 16, 25, 36, 49, 64, 81, 100]
```

#### 数据库查询示例
```bash
👤 您: 连接SQLite数据库demo.db并查询所有用户
🤖 智能体: ✅ database: 成功连接到 SQLITE 数据库
🤖 智能体: ✅ database: 查询结果:
id | name | email             | age
----------------------------------
1  | 张三   | zhang@example.com | 25
2  | 李四   | li@example.com    | 30
```

### 调试技巧

- 🔍 **查看执行统计**: 每个工具都有调用统计和性能监控
- 📝 **启用详细日志**: 修改配置中的日志级别为DEBUG
- 🛡️ **安全模式测试**: 尝试危险操作验证安全机制
- ⏱️ **性能测试**: 使用大文件或复杂计算测试性能限制

## 📚 核心设计理念

### 1. 异步编程模式

所有组件都采用异步设计，提高并发性能：

```python
# 工具异步执行
async def execute(self, **kwargs) -> str:
    # 可以并发执行多个操作
    await asyncio.sleep(0.1)  # 模拟IO操作
    return result

# 智能体异步运行
result = await agent.run(user_input)

# LLM异步调用
response = await llm_client.generate(system_prompt, user_prompt)
```

### 2. 插件化架构

基于pytest插件系统的设计理念：

```python
# 工具注册机制（类比pytest插件注册）
tools = ToolCollection()
tools.add_tool(Calculator())      # 注册计算器插件
tools.add_tool(FileEditor())      # 注册文件编辑插件
tools.add_tool(PythonExecutor())  # 注册代码执行插件

# 动态工具发现和调用（类比pytest的测试发现）
available_tools = tools.get_tool_names()
tool = tools.get_tool("calculator")
result = await tool.execute(expression="2+3")

# 工具统计和监控（类比pytest的测试报告）
stats = tools.get_tool_stats()
```

### 3. 配置驱动设计

配置决定系统行为，支持多种配置源：

```python
# 配置优先级：.env > config.json > 环境变量 > 默认值
config = load_config()

# 工具启用控制
if config["tools"]["calculator"]["enabled"]:
    self.tools.add_tool(Calculator())

# LLM客户端选择
if "claude" in config["model"]:
    client = AnthropicClient(config)
else:
    client = OpenAIClient(config)
```

### 4. 安全设计原则

多层安全防护机制：

```python
# 文件操作安全检查
def _is_safe_path(self, path: str) -> bool:
    # 路径遍历攻击防护
    # 敏感目录访问限制
    # 文件类型白名单检查

# Python代码执行沙箱
def _create_safe_globals(self) -> Dict[str, Any]:
    # 限制可用的内置函数
    # 禁用危险模块导入
    # 执行时间限制
```

## 🔍 与原版OpenManus的对比

| 特性 | 原版OpenManus | 迷你版 |
|------|---------------|--------|
| **复杂度** | 生产级，功能完整 | 简化版，易于理解 |
| **依赖** | 多个外部库，复杂环境 | 最小依赖，易于安装 |
| **工具数量** | 20+ 专业工具 | 3个核心工具 |
| **LLM支持** | 多种API，复杂配置 | 真实API，简单配置 |
| **配置格式** | TOML，多文件 | .env + JSON，灵活配置 |
| **部署方式** | Docker，多种模式 | 单一模式，直接运行 |
| **学习曲线** | 陡峭，需要深入理解 | 平缓，快速上手 |
| **扩展性** | 高度可扩展 | 适度可扩展 |
| **安全性** | 企业级安全 | 基础安全机制 |

## 🎓 学习路径建议

### 初学者路径 (1-2天)
1. **🚀 快速体验** - 按照快速开始指南运行系统
2. **🔧 配置理解** - 学习.env文件和配置管理
3. **🛠️ 工具使用** - 尝试各种工具的基本功能
4. **💬 交互测试** - 与智能体进行多轮对话

### 进阶学习路径 (3-5天)
1. **📖 架构理解** - 深入阅读 `agent.py` 和 `llm.py`
2. **🔍 工具系统** - 研究 `tools/` 目录的插件化设计
3. **⚙️ 配置系统** - 理解 `config.py` 的多源配置机制
4. **🧪 测试调试** - 运行各种测试和调试工具

### 高级实践路径 (1-2周)
1. **🛠️ 自定义工具** - 创建自己的工具插件
2. **🤖 专业智能体** - 开发特定领域的智能体
3. **🔒 安全增强** - 理解和改进安全机制
4. **📊 性能优化** - 分析和优化系统性能
5. **🔄 与原版对比** - 对比学习原版OpenManus

## 🚨 注意事项

- ⚠️ **API费用**: 使用真实LLM API会产生费用，请注意控制使用量
- 🔒 **API密钥安全**: 不要将API密钥提交到版本控制系统
- 🛡️ **安全限制**: 文件操作和代码执行有安全限制，适合学习使用
- 📚 **学习目的**: 本项目主要用于学习，不建议直接用于生产环境

## 🤝 贡献指南

欢迎提交Issue和PR来改进这个学习项目！

### 贡献方式
- 🐛 **Bug报告**: 发现问题请提交Issue
- 💡 **功能建议**: 欢迎提出改进建议
- 📝 **文档改进**: 帮助完善文档和注释
- 🛠️ **代码贡献**: 提交PR改进代码质量

## 📄 许可证

MIT License - 主要用于学习和教育目的

## 🙏 致谢

感谢原版OpenManus项目提供的设计灵感和架构参考！
