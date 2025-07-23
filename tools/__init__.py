"""
工具系统模块
============

这是框架的工具系统，类比pytest的插件系统：
1. BaseTool = 插件基类
2. ToolCollection = 插件管理器
3. 各种具体工具 = 具体插件实现

设计理念：
- 插件化架构，易于扩展
- 统一接口，便于管理
- 异步支持，提高性能
- 错误处理，保证稳定性
"""

from abc import ABC, abstractmethod
from typing import Dict, Any, List, Optional, Union
import asyncio


class BaseTool(ABC):
    """
    工具基类
    
    类比pytest插件的基类，定义了所有工具的通用接口：
    - name: 工具名称 (类比插件名称)
    - description: 工具描述 (类比插件说明)
    - execute: 执行方法 (类比插件的hook函数)
    """
    
    def __init__(self):
        """初始化工具"""
        self.name = self.__class__.__name__.lower()
        self.description = "基础工具"
        self.version = "1.0.0"
    
    @abstractmethod
    async def execute(self, **kwargs) -> str:
        """
        执行工具的核心方法
        
        Args:
            **kwargs: 工具参数
            
        Returns:
            执行结果字符串
            
        类比pytest插件的hook函数，这是工具的核心逻辑
        """
        pass
    
    def validate_args(self, **kwargs) -> bool:
        """
        验证参数有效性
        
        Args:
            **kwargs: 待验证的参数
            
        Returns:
            参数是否有效
            
        类比pytest的参数验证机制
        """
        return True
    
    def get_help(self) -> str:
        """
        获取工具帮助信息
        
        Returns:
            帮助文本
            
        类比pytest --help显示插件帮助
        """
        return f"""
        工具名称: {self.name}
        描述: {self.description}
        版本: {self.version}
        
        使用方法: 请查看具体工具的文档
        """
    
    def __str__(self) -> str:
        return f"{self.name}({self.description})"
    
    def __repr__(self) -> str:
        return f"<{self.__class__.__name__}: {self.name}>"


class ToolCollection:
    """
    工具集合管理器
    
    类比pytest的插件管理器，负责：
    1. 工具注册和发现
    2. 工具生命周期管理
    3. 工具调用和错误处理
    4. 工具依赖关系管理
    """
    
    def __init__(self):
        """初始化工具集合"""
        self._tools: Dict[str, BaseTool] = {}
        self._tool_stats: Dict[str, Dict[str, Any]] = {}
    
    def add_tool(self, tool: BaseTool) -> None:
        """
        添加工具到集合
        
        Args:
            tool: 工具实例
            
        类比pytest注册插件
        """
        if not isinstance(tool, BaseTool):
            raise TypeError(f"工具必须继承自BaseTool，当前类型: {type(tool)}")
        
        tool_name = tool.name
        
        if tool_name in self._tools:
            print(f"⚠️ 工具 '{tool_name}' 已存在，将被覆盖")
        
        self._tools[tool_name] = tool
        self._tool_stats[tool_name] = {
            "calls": 0,
            "successes": 0,
            "failures": 0,
            "total_time": 0.0
        }
        
        print(f"✅ 工具 '{tool_name}' 注册成功")
    
    def remove_tool(self, tool_name: str) -> bool:
        """
        移除工具
        
        Args:
            tool_name: 工具名称
            
        Returns:
            是否成功移除
            
        类比pytest卸载插件
        """
        if tool_name in self._tools:
            del self._tools[tool_name]
            del self._tool_stats[tool_name]
            print(f"🗑️ 工具 '{tool_name}' 已移除")
            return True
        return False
    
    def get_tool(self, tool_name: str) -> Optional[BaseTool]:
        """
        获取工具实例
        
        Args:
            tool_name: 工具名称
            
        Returns:
            工具实例或None
            
        类比pytest获取插件实例
        """
        return self._tools.get(tool_name)
    
    def get_tool_names(self) -> List[str]:
        """
        获取所有工具名称
        
        Returns:
            工具名称列表
            
        类比pytest --collect-only显示所有插件
        """
        return list(self._tools.keys())
    
    def get_tools(self) -> Dict[str, BaseTool]:
        """
        获取所有工具
        
        Returns:
            工具字典
        """
        return self._tools.copy()
    
    async def execute_tool(self, tool_name: str, **kwargs) -> str:
        """
        执行指定工具
        
        Args:
            tool_name: 工具名称
            **kwargs: 工具参数
            
        Returns:
            执行结果
            
        类比pytest执行特定插件的hook
        """
        
        tool = self.get_tool(tool_name)
        if not tool:
            return f"❌ 未找到工具: {tool_name}"
        
        # 记录统计信息
        stats = self._tool_stats[tool_name]
        stats["calls"] += 1
        
        start_time = asyncio.get_event_loop().time()
        
        try:
            # 参数验证
            if not tool.validate_args(**kwargs):
                stats["failures"] += 1
                return f"❌ 工具 '{tool_name}' 参数验证失败"
            
            # 执行工具
            result = await tool.execute(**kwargs)
            
            # 记录成功
            stats["successes"] += 1
            execution_time = asyncio.get_event_loop().time() - start_time
            stats["total_time"] += execution_time
            
            return result
            
        except Exception as e:
            # 记录失败
            stats["failures"] += 1
            execution_time = asyncio.get_event_loop().time() - start_time
            stats["total_time"] += execution_time
            
            error_msg = f"❌ 工具 '{tool_name}' 执行失败: {str(e)}"
            print(error_msg)
            return error_msg
    
    def get_tool_stats(self, tool_name: str = None) -> Dict[str, Any]:
        """
        获取工具统计信息
        
        Args:
            tool_name: 工具名称，如果为None则返回所有工具的统计
            
        Returns:
            统计信息字典
            
        类比pytest的执行统计报告
        """
        if tool_name:
            return self._tool_stats.get(tool_name, {})
        else:
            return self._tool_stats.copy()
    
    def list_tools(self) -> str:
        """
        列出所有工具的信息
        
        Returns:
            工具列表的格式化字符串
            
        类比pytest --collect-only的输出
        """
        if not self._tools:
            return "📭 没有注册任何工具"
        
        lines = ["📦 已注册的工具:"]
        lines.append("-" * 40)
        
        for name, tool in self._tools.items():
            stats = self._tool_stats[name]
            success_rate = (stats["successes"] / max(stats["calls"], 1)) * 100
            avg_time = stats["total_time"] / max(stats["calls"], 1)
            
            lines.append(f"🔧 {name}")
            lines.append(f"   描述: {tool.description}")
            lines.append(f"   调用次数: {stats['calls']}")
            lines.append(f"   成功率: {success_rate:.1f}%")
            lines.append(f"   平均耗时: {avg_time:.3f}秒")
            lines.append("")
        
        return "\n".join(lines)
    
    def __len__(self) -> int:
        """返回工具数量"""
        return len(self._tools)
    
    def __contains__(self, tool_name: str) -> bool:
        """检查是否包含指定工具"""
        return tool_name in self._tools
    
    def __iter__(self):
        """迭代工具"""
        return iter(self._tools.values())


# 工具装饰器 (类比pytest的标记装饰器)
def tool(name: str = None, description: str = None):
    """
    工具装饰器，用于快速创建工具类
    
    Args:
        name: 工具名称
        description: 工具描述
        
    类比pytest的@pytest.mark装饰器
    """
    def decorator(cls):
        if name:
            cls._tool_name = name
        if description:
            cls._tool_description = description
        return cls
    return decorator


# 异步工具包装器
class AsyncToolWrapper(BaseTool):
    """
    异步工具包装器
    
    将同步工具包装为异步工具，类比pytest的异步测试支持
    """
    
    def __init__(self, sync_tool: BaseTool):
        super().__init__()
        self.sync_tool = sync_tool
        self.name = sync_tool.name
        self.description = f"异步包装: {sync_tool.description}"
    
    async def execute(self, **kwargs) -> str:
        """异步执行同步工具"""
        # 在线程池中执行同步代码，避免阻塞事件循环
        loop = asyncio.get_event_loop()
        return await loop.run_in_executor(None, self.sync_tool.execute, **kwargs)


# 工具工厂函数
def create_tool_collection(*tools: BaseTool) -> ToolCollection:
    """
    创建工具集合的便捷函数

    Args:
        *tools: 工具实例

    Returns:
        工具集合

    类比pytest的插件集合创建
    """
    collection = ToolCollection()
    for tool in tools:
        collection.add_tool(tool)
    return collection


# 导入具体工具类
from .calculator import Calculator
from .file_editor import FileEditor
from .python_executor import PythonExecutor
from .database import DatabaseTool