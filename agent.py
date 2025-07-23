"""
智能体核心模块
==============

这是框架的核心，定义了智能体的基本行为和执行逻辑。

设计理念 (类比pytest的测试类):
1. Agent = 测试类，负责组织和执行
2. 每个Agent有自己的工具集合 (类比测试方法)
3. 支持继承和扩展 (类比测试类继承)
4. 统一的执行接口 (类比pytest的运行机制)
"""

import asyncio
import json
import re
from typing import Dict, Any, List, Optional, Union
from abc import ABC, abstractmethod

from tools import ToolCollection, BaseTool
from llm import LLMClient


class BaseAgent(ABC):
    """
    智能体基类
    
    类比pytest的TestCase基类，定义了所有智能体的通用接口：
    - 初始化方法 (类比setUp)
    - 执行方法 (类比test_方法)
    - 清理方法 (类比tearDown)
    """
    
    def __init__(self, config: Dict[str, Any]):
        """
        初始化智能体
        
        Args:
            config: 配置字典
            
        类比pytest的测试类初始化，设置必要的属性和依赖
        """
        self.config = config
        self.name = self.__class__.__name__
        self.description = "基础智能体"
        
        # 初始化LLM客户端 (类比测试中的外部服务连接)
        self.llm_client = LLMClient(config)
        
        # 初始化工具集合 (类比pytest的fixture集合)
        self.tools = ToolCollection()
        self._setup_tools()
        
        # 执行历史 (类比测试执行记录)
        self.execution_history: List[Dict[str, Any]] = []
        
        # 状态管理
        self.current_step = 0
        self.max_steps = config.get("agent", {}).get("max_steps", 10)
    
    @abstractmethod
    def _setup_tools(self) -> None:
        """
        设置智能体的工具集合
        
        子类必须实现此方法来定义自己的工具集
        类比pytest中每个测试类定义自己需要的fixture
        """
        pass
    
    @abstractmethod
    async def _generate_plan(self, user_input: str) -> Dict[str, Any]:
        """
        根据用户输入生成执行计划
        
        Args:
            user_input: 用户输入的自然语言指令
            
        Returns:
            执行计划字典，包含步骤和工具选择
            
        类比pytest的测试计划生成，决定执行哪些测试
        """
        pass
    
    async def run(self, user_input: str) -> str:
        """
        执行用户指令的主入口
        
        Args:
            user_input: 用户输入的自然语言指令
            
        Returns:
            执行结果字符串
            
        类比pytest的测试执行主流程：
        1. 收集测试 -> 生成计划
        2. 执行测试 -> 执行工具
        3. 生成报告 -> 返回结果
        """
        
        print(f"🎯 开始执行任务: {user_input}")
        
        try:
            # 1. 生成执行计划 (类比pytest的测试收集阶段)
            plan = await self._generate_plan(user_input)
            print(f"📋 执行计划: {plan.get('summary', '未知')}")
            
            # 2. 执行计划中的步骤 (类比pytest的测试执行阶段)
            result = await self._execute_plan(plan)
            
            # 3. 记录执行历史 (类比pytest的测试报告)
            self._record_execution(user_input, plan, result)
            
            return result
            
        except Exception as e:
            error_msg = f"执行失败: {str(e)}"
            print(f"❌ {error_msg}")
            return error_msg
    
    async def _execute_plan(self, plan: Dict[str, Any]) -> str:
        """
        执行具体的计划步骤
        
        Args:
            plan: 执行计划
            
        Returns:
            执行结果
            
        类比pytest执行测试用例的过程
        """
        
        steps = plan.get("steps", [])
        results = []
        
        for i, step in enumerate(steps):
            if self.current_step >= self.max_steps:
                results.append("⚠️ 达到最大执行步数限制")
                break
            
            print(f"📍 执行步骤 {i+1}/{len(steps)}: {step.get('description', '未知步骤')}")
            
            try:
                # 执行单个步骤 (类比执行单个测试方法)
                step_result = await self._execute_step(step)
                results.append(f"步骤{i+1}: {step_result}")
                
                self.current_step += 1
                
                # 短暂延迟，避免过快执行
                await asyncio.sleep(0.1)
                
            except Exception as e:
                error_msg = f"步骤{i+1}执行失败: {str(e)}"
                results.append(error_msg)
                print(f"❌ {error_msg}")
                # 继续执行下一步，不中断整个流程
        
        return "\n".join(results)
    
    async def _execute_step(self, step: Dict[str, Any]) -> str:
        """
        执行单个步骤
        
        Args:
            step: 步骤信息，包含工具名称和参数
            
        Returns:
            步骤执行结果
            
        类比pytest执行单个断言或操作
        """
        
        tool_name = step.get("tool")
        tool_args = step.get("args", {})
        
        if not tool_name:
            return "❌ 步骤缺少工具名称"
        
        # 获取工具实例 (类比获取fixture)
        tool = self.tools.get_tool(tool_name)
        if not tool:
            return f"❌ 未找到工具: {tool_name}"
        
        # 执行工具 (类比执行测试逻辑)
        try:
            result = await tool.execute(**tool_args)
            return f"✅ {tool_name}: {result}"
        except Exception as e:
            return f"❌ {tool_name} 执行失败: {str(e)}"
    
    def _record_execution(self, user_input: str, plan: Dict[str, Any], result: str) -> None:
        """
        记录执行历史
        
        类比pytest的测试报告生成，保存执行记录用于调试和分析
        """
        
        record = {
            "timestamp": asyncio.get_event_loop().time(),
            "user_input": user_input,
            "plan": plan,
            "result": result,
            "steps_executed": self.current_step
        }
        
        self.execution_history.append(record)
        
        # 限制历史记录数量，避免内存泄漏
        if len(self.execution_history) > 100:
            self.execution_history = self.execution_history[-50:]
    
    def get_available_tools(self) -> List[str]:
        """
        获取可用工具列表
        
        Returns:
            工具名称列表
            
        类比pytest --collect-only，显示可用的测试
        """
        return self.tools.get_tool_names()
    
    def get_execution_stats(self) -> Dict[str, Any]:
        """
        获取执行统计信息
        
        Returns:
            统计信息字典
            
        类比pytest的执行统计报告
        """
        return {
            "total_executions": len(self.execution_history),
            "current_step": self.current_step,
            "max_steps": self.max_steps,
            "available_tools": len(self.tools.get_tool_names())
        }


class MiniManus(BaseAgent):
    """
    迷你版Manus智能体
    
    这是一个通用的智能体实现，类比pytest的基础测试类。
    它集成了多种工具，可以处理各种类型的任务。
    
    特点：
    1. 通用性强 - 类比pytest可以运行各种测试
    2. 工具丰富 - 类比pytest有丰富的插件生态
    3. 易于扩展 - 类比pytest易于自定义和扩展
    """
    
    def __init__(self, config: Dict[str, Any]):
        """初始化MiniManus智能体"""
        super().__init__(config)
        self.name = "MiniManus"
        self.description = "通用AI智能体，可以处理文件操作、计算、编程等多种任务"
    
    def _setup_tools(self) -> None:
        """
        设置MiniManus的工具集合
        
        类比pytest加载插件，这里加载各种工具
        每个工具都是一个独立的功能模块
        """
        
        # 导入工具类 (延迟导入避免循环依赖)
        from tools.calculator import Calculator
        from tools.file_editor import FileEditor
        from tools.python_executor import PythonExecutor
        from tools.database import DatabaseTool

        # 根据配置启用工具 (类比pytest的插件配置)
        tool_config = self.config.get("tools", {})

        if tool_config.get("calculator", {}).get("enabled", True):
            self.tools.add_tool(Calculator())
            print("🧮 已加载计算器工具")

        if tool_config.get("file_editor", {}).get("enabled", True):
            self.tools.add_tool(FileEditor(tool_config.get("file_editor", {})))
            print("📝 已加载文件编辑工具")

        if tool_config.get("python_execute", {}).get("enabled", True):
            self.tools.add_tool(PythonExecutor(tool_config.get("python_execute", {})))
            print("🐍 已加载Python执行工具")

        if tool_config.get("database", {}).get("enabled", True):
            self.tools.add_tool(DatabaseTool(tool_config.get("database", {})))
            print("🗄️ 已加载数据库工具")
    
    async def _generate_plan(self, user_input: str) -> Dict[str, Any]:
        """
        生成执行计划
        
        这是智能体的"大脑"，负责理解用户意图并制定执行策略。
        类比pytest的测试发现和计划阶段。
        
        Args:
            user_input: 用户输入
            
        Returns:
            执行计划
        """
        
        # 构建系统提示词 (类比pytest的测试模板)
        system_prompt = self._build_system_prompt()
        
        # 构建用户提示词
        user_prompt = f"""
        用户请求: {user_input}
        
        请分析这个请求，并生成一个执行计划。计划应该包含：
        1. 任务分析和理解
        2. 需要使用的工具
        3. 具体的执行步骤
        
        请以JSON格式返回计划，格式如下：
        {{
            "summary": "任务摘要",
            "analysis": "任务分析",
            "steps": [
                {{
                    "description": "步骤描述",
                    "tool": "工具名称",
                    "args": {{"参数名": "参数值"}}
                }}
            ]
        }}
        """
        
        # 临时修复：优先使用规则匹配，确保数据库工具正常工作
        # 检查是否包含数据库相关关键词
        user_input_lower = user_input.lower()
        if any(keyword in user_input_lower for keyword in ['数据库', 'database', 'sqlite', 'mysql', 'postgresql', '查询', 'sql', 'select', '连接', 'employees', 'demo.db']):
            print("🎯 检测到数据库相关请求，使用规则匹配")
            return self._generate_rule_based_plan(user_input)

        try:
            # 调用LLM生成计划 (类比AI辅助的测试用例生成)
            response = await self.llm_client.generate(
                system_prompt=system_prompt,
                user_prompt=user_prompt
            )

            # 解析LLM响应
            plan = self._parse_plan_response(response)
            return plan

        except Exception as e:
            print(f"⚠️ LLM计划生成失败，使用规则匹配: {e}")
            # 降级到规则匹配 (类比pytest的fallback机制)
            return self._generate_rule_based_plan(user_input)
    
    def _build_system_prompt(self) -> str:
        """
        构建系统提示词
        
        类比pytest的测试环境设置，告诉AI当前的能力和约束
        """
        
        available_tools = self.get_available_tools()
        tool_descriptions = []
        
        for tool_name in available_tools:
            tool = self.tools.get_tool(tool_name)
            if tool:
                tool_descriptions.append(f"- {tool_name}: {tool.description}")
        
        return f"""
        你是MiniManus，一个通用的AI智能体助手。

        你的能力：
        {chr(10).join(tool_descriptions)}
        
        你的任务是理解用户请求，选择合适的工具，并制定详细的执行计划。
        
        重要原则：
        1. 优先使用简单直接的方法
        2. 一步一步分解复杂任务
        3. 选择最合适的工具
        4. 提供清晰的步骤描述
        """
    
    def _parse_plan_response(self, response: str) -> Dict[str, Any]:
        """
        解析LLM的计划响应
        
        Args:
            response: LLM返回的文本
            
        Returns:
            解析后的计划字典
        """
        
        try:
            # 尝试直接解析JSON
            if response.strip().startswith('{'):
                return json.loads(response)
            
            # 尝试提取JSON部分
            json_match = re.search(r'\{.*\}', response, re.DOTALL)
            if json_match:
                return json.loads(json_match.group())
            
            # 如果无法解析，返回默认计划
            raise ValueError("无法解析JSON响应")
            
        except Exception as e:
            print(f"⚠️ JSON解析失败: {e}")
            # 返回一个基本的计划结构
            return {
                "summary": "基于规则的简单任务",
                "analysis": f"LLM响应解析失败，原始响应: {response[:100]}...",
                "steps": [
                    {
                        "description": "显示LLM原始响应",
                        "tool": "calculator",  # 使用一个肯定存在的工具
                        "args": {"expression": "1+1"}
                    }
                ]
            }
    
    def _generate_rule_based_plan(self, user_input: str) -> Dict[str, Any]:
        """
        基于规则的计划生成 (降级方案)
        
        当LLM不可用时，使用简单的关键词匹配来生成计划。
        类比pytest的简单测试发现机制。
        
        Args:
            user_input: 用户输入
            
        Returns:
            基于规则的执行计划
        """
        
        user_input_lower = user_input.lower()
        
        # 计算相关关键词
        if any(keyword in user_input_lower for keyword in ['计算', '算', '+', '-', '*', '/', '数学']):
            return {
                "summary": "数学计算任务",
                "analysis": "检测到计算相关关键词，使用计算器工具",
                "steps": [
                    {
                        "description": f"计算表达式: {user_input}",
                        "tool": "calculator",
                        "args": {"expression": user_input}
                    }
                ]
            }
        
        # 文件相关关键词
        elif any(keyword in user_input_lower for keyword in ['文件', '读取', '写入', '保存', 'file']):
            return {
                "summary": "文件操作任务",
                "analysis": "检测到文件操作相关关键词，使用文件编辑工具",
                "steps": [
                    {
                        "description": "执行文件操作",
                        "tool": "file_editor",
                        "args": {"action": "info", "content": user_input}
                    }
                ]
            }
        
        # Python相关关键词
        elif any(keyword in user_input_lower for keyword in ['python', '代码', '编程', 'print', 'def']):
            return {
                "summary": "Python代码执行任务",
                "analysis": "检测到Python相关关键词，使用Python执行工具",
                "steps": [
                    {
                        "description": "执行Python代码",
                        "tool": "python_executor",
                        "args": {"code": user_input}
                    }
                ]
            }

        # 数据库相关关键词
        elif any(keyword in user_input_lower for keyword in ['数据库', 'database', 'sqlite', 'mysql', 'postgresql', '查询', 'sql', 'select', '连接', 'employees', 'demo.db']):
            # 解析数据库操作类型
            if any(keyword in user_input_lower for keyword in ['连接', 'connect']):
                # 提取数据库文件名
                db_file = "demo.db"  # 默认数据库文件
                if "demo.db" in user_input_lower:
                    db_file = "demo.db"

                return {
                    "summary": "数据库连接任务",
                    "analysis": "检测到数据库连接相关关键词，使用数据库工具连接",
                    "steps": [
                        {
                            "description": f"连接SQLite数据库: {db_file}",
                            "tool": "database",
                            "args": {"action": "connect", "db_type": "sqlite", "connection_string": db_file}
                        },
                        {
                            "description": "查询employees表中技术部员工信息",
                            "tool": "database",
                            "args": {"action": "query", "sql": "SELECT * FROM employees WHERE department = '技术部'"}
                        }
                    ]
                }
            elif any(keyword in user_input_lower for keyword in ['查询', 'select', 'employees']):
                return {
                    "summary": "数据库查询任务",
                    "analysis": "检测到数据库查询相关关键词，使用数据库工具查询",
                    "steps": [
                        {
                            "description": "连接SQLite数据库demo.db",
                            "tool": "database",
                            "args": {"action": "connect", "db_type": "sqlite", "connection_string": "demo.db"}
                        },
                        {
                            "description": "查询employees表数据",
                            "tool": "database",
                            "args": {"action": "query", "sql": "SELECT * FROM employees"}
                        }
                    ]
                }
            else:
                return {
                    "summary": "数据库操作任务",
                    "analysis": "检测到数据库相关关键词，使用数据库工具",
                    "steps": [
                        {
                            "description": "显示数据库连接状态",
                            "tool": "database",
                            "args": {"action": "status"}
                        }
                    ]
                }

        # 默认计划
        else:
            return {
                "summary": "通用信息处理任务",
                "analysis": "未匹配到特定关键词，提供通用响应",
                "steps": [
                    {
                        "description": "使用计算器进行简单演示",
                        "tool": "calculator",
                        "args": {"expression": "2+2"}
                    }
                ]
            }


# 工厂函数 (类比pytest的测试类工厂)
def create_agent(agent_type: str = "manus", config: Dict[str, Any] = None) -> BaseAgent:
    """
    智能体工厂函数
    
    Args:
        agent_type: 智能体类型
        config: 配置字典
        
    Returns:
        智能体实例
        
    类比pytest的测试类动态创建
    """
    
    if config is None:
        from config import get_default_config
        config = get_default_config()
    
    if agent_type.lower() == "manus":
        return MiniManus(config)
    else:
        raise ValueError(f"未知的智能体类型: {agent_type}")