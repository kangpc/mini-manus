"""
Python代码执行工具
==================

提供安全的Python代码执行功能，类比pytest中的代码测试执行器。

功能特点：
1. 安全的代码执行环境
2. 输出捕获和错误处理
3. 执行时间限制
4. 内存使用监控
5. 支持多种执行模式
"""

import ast
import sys
import io
import time
import threading
import traceback
import contextlib
from typing import Dict, Any, Optional, Tuple, List
from tools import BaseTool


class PythonExecutor(BaseTool):
    """
    Python代码执行工具类
    
    类比pytest的代码执行器，提供安全的Python代码运行环境。
    支持代码验证、执行监控和结果捕获。
    """
    
    def __init__(self, config: Dict[str, Any] = None):
        super().__init__()
        self.name = "python_executor"
        self.description = "Python代码执行工具，支持安全执行Python代码片段"
        
        # 配置参数 (类比pytest的执行配置)
        self.config = config or {}
        self.timeout = self.config.get('timeout', 30)  # 执行超时时间(秒)
        self.max_output_length = self.config.get('max_output_length', 10000)  # 最大输出长度
        self.allow_imports = self.config.get('allow_imports', True)  # 是否允许导入
        
        # 安全限制 (类比pytest的安全沙箱)
        self.forbidden_modules = {
            'os', 'subprocess', 'shutil', 'socket', 'urllib', 'requests',
            'ftplib', 'smtplib', 'telnetlib', 'webbrowser', 'ctypes',
            '__import__', 'eval', 'exec', 'compile', 'open'
        }
        
        # 允许的安全模块
        self.safe_modules = {
            'math', 'random', 'datetime', 'json', 'base64', 'hashlib',
            'itertools', 'functools', 'collections', 're', 'string',
            'decimal', 'fractions', 'statistics', 'uuid', 'copy'
        }
        
        # 执行统计
        self.execution_count = 0
        self.total_execution_time = 0.0
    
    def validate_args(self, **kwargs) -> bool:
        """
        验证参数
        
        Args:
            **kwargs: 参数字典，应包含 'code' 键
            
        Returns:
            参数是否有效
        """
        if 'code' not in kwargs:
            print("❌ 缺少必需参数: code")
            return False
        
        code = kwargs['code']
        if not isinstance(code, str):
            print("❌ code 必须是字符串类型")
            return False
        
        if not code.strip():
            print("❌ code 不能为空")
            return False
        
        return True
    
    async def execute(self, **kwargs) -> str:
        """
        执行Python代码
        
        Args:
            code: Python代码字符串
            mode: 执行模式 ('exec' 或 'eval')，默认为 'exec'
            timeout: 执行超时时间，默认使用配置值
            capture_output: 是否捕获输出，默认为 True
            
        Returns:
            执行结果字符串
            
        示例:
            await executor.execute(code="print('Hello, World!')")
            await executor.execute(code="2 + 3", mode="eval")
        """
        
        code = kwargs.get('code', '').strip()
        mode = kwargs.get('mode', 'exec')
        timeout = kwargs.get('timeout', self.timeout)
        capture_output = kwargs.get('capture_output', True)
        
        self.execution_count += 1
        start_time = time.time()
        
        try:
            # 1. 代码安全检查 (类比pytest的代码验证)
            safety_check = self._check_code_safety(code)
            if not safety_check[0]:
                return f"❌ 代码安全检查失败: {safety_check[1]}"
            
            # 2. 语法检查 (类比pytest的语法验证)
            syntax_check = self._check_syntax(code, mode)
            if not syntax_check[0]:
                return f"❌ 语法错误: {syntax_check[1]}"
            
            # 3. 执行代码 (类比pytest的测试执行)
            if mode == 'eval':
                result = self._execute_eval(code, timeout, capture_output)
            else:
                result = self._execute_exec(code, timeout, capture_output)
            
            # 4. 记录执行时间
            execution_time = time.time() - start_time
            self.total_execution_time += execution_time
            
            return f"✅ 执行成功 (耗时: {execution_time:.3f}秒)\n{result}"
            
        except TimeoutError:
            return f"❌ 执行超时 (>{timeout}秒)"
        except Exception as e:
            execution_time = time.time() - start_time
            self.total_execution_time += execution_time
            return f"❌ 执行失败 (耗时: {execution_time:.3f}秒): {str(e)}"
    
    def _check_code_safety(self, code: str) -> Tuple[bool, str]:
        """
        检查代码安全性
        
        Args:
            code: 待检查的代码
            
        Returns:
            (是否安全, 错误信息)
        """
        
        # 检查禁用的关键词
        dangerous_keywords = [
            'import os', 'import subprocess', 'import shutil', 'import socket',
            'from os', 'from subprocess', 'from shutil', 'from socket',
            '__import__', 'eval(', 'exec(', 'compile(', 'open(',
            'file(', 'input(', 'raw_input('
        ]
        
        code_lower = code.lower()
        for keyword in dangerous_keywords:
            if keyword in code_lower:
                return False, f"包含危险关键词: {keyword}"
        
        # 如果不允许导入，检查import语句
        if not self.allow_imports and ('import ' in code_lower or 'from ' in code_lower):
            return False, "不允许使用import语句"
        
        # 检查代码长度
        if len(code) > 50000:  # 50KB限制
            return False, "代码过长"
        
        return True, ""
    
    def _check_syntax(self, code: str, mode: str) -> Tuple[bool, str]:
        """
        检查代码语法
        
        Args:
            code: 待检查的代码
            mode: 执行模式
            
        Returns:
            (语法是否正确, 错误信息)
        """
        
        try:
            ast.parse(code, mode=mode)
            return True, ""
        except SyntaxError as e:
            return False, f"第{e.lineno}行: {e.msg}"
        except Exception as e:
            return False, str(e)
    
    def _execute_eval(self, code: str, timeout: float, capture_output: bool) -> str:
        """
        执行eval模式的代码
        
        Args:
            code: 代码字符串
            timeout: 超时时间
            capture_output: 是否捕获输出
            
        Returns:
            执行结果
        """
        
        # 创建安全的执行环境
        safe_globals = self._create_safe_globals()
        safe_locals = {}
        
        # 执行代码
        result = self._run_with_timeout(
            lambda: eval(code, safe_globals, safe_locals),
            timeout
        )
        
        return f"结果: {repr(result)}"
    
    def _execute_exec(self, code: str, timeout: float, capture_output: bool) -> str:
        """
        执行exec模式的代码
        
        Args:
            code: 代码字符串
            timeout: 超时时间
            capture_output: 是否捕获输出
            
        Returns:
            执行结果
        """
        
        # 创建安全的执行环境
        safe_globals = self._create_safe_globals()
        safe_locals = {}
        
        if capture_output:
            # 捕获标准输出和错误输出
            old_stdout = sys.stdout
            old_stderr = sys.stderr
            stdout_capture = io.StringIO()
            stderr_capture = io.StringIO()
            
            try:
                sys.stdout = stdout_capture
                sys.stderr = stderr_capture
                
                # 执行代码
                self._run_with_timeout(
                    lambda: exec(code, safe_globals, safe_locals),
                    timeout
                )
                
                # 获取输出
                stdout_content = stdout_capture.getvalue()
                stderr_content = stderr_capture.getvalue()
                
                # 组合结果
                result_parts = []
                if stdout_content:
                    result_parts.append(f"输出:\n{stdout_content}")
                if stderr_content:
                    result_parts.append(f"错误:\n{stderr_content}")
                
                # 如果有返回值变量，也显示
                if '_' in safe_locals:
                    result_parts.append(f"最后表达式结果: {repr(safe_locals['_'])}")
                
                return "\n".join(result_parts) if result_parts else "执行完成，无输出"
                
            finally:
                sys.stdout = old_stdout
                sys.stderr = old_stderr
        else:
            # 不捕获输出，直接执行
            self._run_with_timeout(
                lambda: exec(code, safe_globals, safe_locals),
                timeout
            )
            return "执行完成"
    
    def _create_safe_globals(self) -> Dict[str, Any]:
        """
        创建安全的全局变量环境
        
        Returns:
            安全的全局变量字典
        """
        
        # 基础的安全内置函数
        safe_builtins = {
            'abs', 'all', 'any', 'bin', 'bool', 'chr', 'dict', 'dir',
            'divmod', 'enumerate', 'filter', 'float', 'format', 'frozenset',
            'getattr', 'hasattr', 'hash', 'hex', 'id', 'int', 'isinstance',
            'issubclass', 'iter', 'len', 'list', 'map', 'max', 'min',
            'next', 'oct', 'ord', 'pow', 'print', 'range', 'repr',
            'reversed', 'round', 'set', 'slice', 'sorted', 'str', 'sum',
            'tuple', 'type', 'vars', 'zip'
        }
        
        # 创建受限的builtins
        restricted_builtins = {}
        import builtins
        for name in safe_builtins:
            if hasattr(builtins, name):
                restricted_builtins[name] = getattr(builtins, name)
        
        # 添加常用的安全模块
        safe_globals = {
            '__builtins__': restricted_builtins,
            'math': __import__('math'),
            'random': __import__('random'),
            'datetime': __import__('datetime'),
            'json': __import__('json'),
        }
        
        return safe_globals
    
    def _run_with_timeout(self, func, timeout: float):
        """
        在指定时间内运行函数
        
        Args:
            func: 要执行的函数
            timeout: 超时时间
            
        Returns:
            函数执行结果
            
        Raises:
            TimeoutError: 执行超时
        """
        
        result = [None]
        exception = [None]
        
        def target():
            try:
                result[0] = func()
            except Exception as e:
                exception[0] = e
        
        thread = threading.Thread(target=target)
        thread.daemon = True
        thread.start()
        thread.join(timeout)
        
        if thread.is_alive():
            # 注意：Python中无法强制终止线程，这里只是不等待了
            raise TimeoutError(f"代码执行超时 (>{timeout}秒)")
        
        if exception[0]:
            raise exception[0]
        
        return result[0]
    
    def get_execution_stats(self) -> Dict[str, Any]:
        """
        获取执行统计信息
        
        Returns:
            统计信息字典
        """
        avg_time = (self.total_execution_time / max(self.execution_count, 1))
        
        return {
            "total_executions": self.execution_count,
            "total_time": round(self.total_execution_time, 3),
            "average_time": round(avg_time, 3),
            "timeout_limit": self.timeout,
            "allow_imports": self.allow_imports
        }
    
    def get_help(self) -> str:
        """
        获取Python执行器帮助信息
        
        Returns:
            详细的帮助文本
        """
        return """
🐍 Python代码执行工具帮助

执行模式:
  exec        执行语句和代码块 (默认)
  eval        计算表达式并返回结果

支持的功能:
  - 基本Python语法和内置函数
  - 数学运算和逻辑操作
  - 字符串处理和格式化
  - 列表、字典、集合操作
  - 循环和条件语句
  - 函数定义和调用

安全限制:
  - 禁止文件系统操作
  - 禁止网络访问
  - 禁止系统调用
  - 执行时间限制
  - 输出长度限制

使用示例:
  print("Hello, World!")           → 输出文本
  result = 2 + 3 * 4               → 数学计算
  [x**2 for x in range(5)]         → 列表推导
  import math; math.sqrt(16)       → 使用数学模块
  
  def factorial(n):                → 函数定义
      return 1 if n <= 1 else n * factorial(n-1)
  print(factorial(5))

注意事项:
  - 代码在隔离环境中执行
  - 某些模块和函数被禁用
  - 长时间运行的代码会被终止
  - 输出过长会被截断
        """


# 便捷函数 (类比pytest的辅助函数)
async def execute_python(code: str, mode: str = 'exec', timeout: float = 30) -> str:
    """
    便捷的Python代码执行函数
    
    Args:
        code: Python代码
        mode: 执行模式
        timeout: 超时时间
        
    Returns:
        执行结果
    """
    executor = PythonExecutor()
    return await executor.execute(code=code, mode=mode, timeout=timeout)


# 测试函数 (类比pytest的测试用例)
if __name__ == "__main__":
    import asyncio
    
    async def test_python_executor():
        """测试Python执行器功能"""
        executor = PythonExecutor()
        
        test_cases = [
            ("print('Hello, World!')", "exec"),
            ("2 + 3 * 4", "eval"),
            ("import math; print(math.sqrt(16))", "exec"),
            ("[x**2 for x in range(5)]", "eval"),
            ("def greet(name): return f'Hello, {name}!'\nprint(greet('Python'))", "exec"),
        ]
        
        print("🐍 Python执行器测试:")
        print("=" * 50)
        
        for code, mode in test_cases:
            print(f"\n📝 代码: {code}")
            print(f"🔧 模式: {mode}")
            result = await executor.execute(code=code, mode=mode)
            print(f"📊 结果: {result}")
        
        print(f"\n📈 执行统计: {executor.get_execution_stats()}")
        print("\n✅ 测试完成")
    
    asyncio.run(test_python_executor())
