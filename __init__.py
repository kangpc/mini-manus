"""
OpenManus 迷你版
================

一个简化版的AI智能体框架，用于学习和理解OpenManus的核心架构。

主要组件：
- Agent: 智能体核心
- Tools: 工具系统
- Config: 配置管理
- LLM: 语言模型客户端
"""

__version__ = "0.1.0"
__author__ = "OpenManus Mini Team"

from agent import MiniManus, BaseAgent
from tools import BaseTool, ToolCollection
from config import load_config

__all__ = [
    "MiniManus",
    "BaseAgent", 
    "BaseTool",
    "ToolCollection",
    "load_config"
]