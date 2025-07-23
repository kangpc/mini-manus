"""
计算器工具
==========

提供数学计算功能的工具，类比pytest中的数值断言工具。

功能特点：
1. 支持基本数学运算
2. 支持复杂表达式计算
3. 安全的表达式求值
4. 详细的错误处理
"""

import ast
import operator
import math
import re
from typing import Any, Dict, Union
from tools import BaseTool


class Calculator(BaseTool):
    """
    计算器工具类
    
    类比pytest中的数值比较工具，提供安全的数学计算功能。
    使用AST解析确保安全性，避免eval()的安全风险。
    """
    
    def __init__(self):
        super().__init__()
        self.name = "calculator"
        self.description = "数学计算工具，支持基本运算、函数计算和复杂表达式"
        
        # 支持的运算符 (类比pytest的比较运算符)
        self.operators = {
            ast.Add: operator.add,      # +
            ast.Sub: operator.sub,      # -
            ast.Mult: operator.mul,     # *
            ast.Div: operator.truediv,  # /
            ast.FloorDiv: operator.floordiv,  # //
            ast.Mod: operator.mod,      # %
            ast.Pow: operator.pow,      # **
            ast.USub: operator.neg,     # -x (负号)
            ast.UAdd: operator.pos,     # +x (正号)
        }
        
        # 支持的数学函数 (类比pytest的辅助函数)
        self.functions = {
            'abs': abs,
            'round': round,
            'max': max,
            'min': min,
            'sum': sum,
            'sqrt': math.sqrt,
            'sin': math.sin,
            'cos': math.cos,
            'tan': math.tan,
            'log': math.log,
            'log10': math.log10,
            'exp': math.exp,
            'ceil': math.ceil,
            'floor': math.floor,
            'pi': math.pi,
            'e': math.e,
        }
    
    def validate_args(self, **kwargs) -> bool:
        """
        验证参数
        
        Args:
            **kwargs: 参数字典，应包含 'expression' 键
            
        Returns:
            参数是否有效
        """
        if 'expression' not in kwargs:
            print("❌ 缺少必需参数: expression")
            return False
        
        expression = kwargs['expression']
        if not isinstance(expression, str):
            print("❌ expression 必须是字符串类型")
            return False
        
        if not expression.strip():
            print("❌ expression 不能为空")
            return False
        
        return True
    
    async def execute(self, **kwargs) -> str:
        """
        执行数学计算
        
        Args:
            expression: 数学表达式字符串
            precision: 结果精度 (可选)
            
        Returns:
            计算结果字符串
            
        示例:
            await calculator.execute(expression="2 + 3 * 4")
            await calculator.execute(expression="sqrt(16) + sin(pi/2)")
        """
        
        expression = kwargs.get('expression', '').strip()
        precision = kwargs.get('precision', None)
        
        try:
            # 预处理表达式 (类比pytest的测试数据预处理)
            processed_expr = self._preprocess_expression(expression)
            
            # 解析和计算 (类比pytest的断言执行)
            result = self._safe_eval(processed_expr)
            
            # 格式化结果 (类比pytest的结果格式化)
            formatted_result = self._format_result(result, precision)
            
            return f"计算结果: {expression} = {formatted_result}"
            
        except ZeroDivisionError:
            return f"❌ 除零错误: {expression}"
        except ValueError as e:
            return f"❌ 数值错误: {str(e)}"
        except SyntaxError as e:
            return f"❌ 语法错误: {str(e)}"
        except Exception as e:
            return f"❌ 计算失败: {str(e)}"
    
    def _preprocess_expression(self, expression: str) -> str:
        """
        预处理数学表达式
        
        Args:
            expression: 原始表达式
            
        Returns:
            处理后的表达式
            
        处理内容：
        1. 替换常见的数学符号
        2. 处理隐式乘法 (如 2x -> 2*x)
        3. 替换数学常数
        """
        
        # 替换常见符号
        replacements = {
            '×': '*',
            '÷': '/',
            '²': '**2',
            '³': '**3',
            '√': 'sqrt',
        }
        
        processed = expression
        for old, new in replacements.items():
            processed = processed.replace(old, new)
        
        # 处理隐式乘法 (数字后跟字母)
        processed = re.sub(r'(\d)([a-zA-Z])', r'\1*\2', processed)
        
        # 处理括号前的隐式乘法 (如 2(3+4) -> 2*(3+4))
        processed = re.sub(r'(\d)\(', r'\1*(', processed)
        
        return processed
    
    def _safe_eval(self, expression: str) -> Union[int, float]:
        """
        安全地计算数学表达式
        
        使用AST解析而不是eval()，确保安全性
        类比pytest的安全断言机制
        
        Args:
            expression: 数学表达式
            
        Returns:
            计算结果
        """
        
        try:
            # 解析表达式为AST
            node = ast.parse(expression, mode='eval')
            return self._eval_node(node.body)
        except Exception as e:
            raise SyntaxError(f"表达式解析失败: {str(e)}")
    
    def _eval_node(self, node: ast.AST) -> Union[int, float]:
        """
        递归计算AST节点
        
        Args:
            node: AST节点
            
        Returns:
            节点计算结果
        """
        
        # 数字节点
        if isinstance(node, ast.Constant):
            return node.value
        elif isinstance(node, ast.Num):  # Python < 3.8 兼容性
            return node.n
        
        # 变量节点 (数学常数)
        elif isinstance(node, ast.Name):
            if node.id in self.functions:
                return self.functions[node.id]
            else:
                raise NameError(f"未知变量: {node.id}")
        
        # 二元运算节点
        elif isinstance(node, ast.BinOp):
            left = self._eval_node(node.left)
            right = self._eval_node(node.right)
            op = self.operators.get(type(node.op))
            if op:
                return op(left, right)
            else:
                raise TypeError(f"不支持的运算符: {type(node.op)}")
        
        # 一元运算节点
        elif isinstance(node, ast.UnaryOp):
            operand = self._eval_node(node.operand)
            op = self.operators.get(type(node.op))
            if op:
                return op(operand)
            else:
                raise TypeError(f"不支持的一元运算符: {type(node.op)}")
        
        # 函数调用节点
        elif isinstance(node, ast.Call):
            func_name = node.func.id if isinstance(node.func, ast.Name) else None
            if func_name in self.functions:
                func = self.functions[func_name]
                args = [self._eval_node(arg) for arg in node.args]
                return func(*args)
            else:
                raise NameError(f"未知函数: {func_name}")
        
        # 比较运算节点 (用于条件计算)
        elif isinstance(node, ast.Compare):
            left = self._eval_node(node.left)
            for op, comparator in zip(node.ops, node.comparators):
                right = self._eval_node(comparator)
                if isinstance(op, ast.Lt):
                    result = left < right
                elif isinstance(op, ast.LtE):
                    result = left <= right
                elif isinstance(op, ast.Gt):
                    result = left > right
                elif isinstance(op, ast.GtE):
                    result = left >= right
                elif isinstance(op, ast.Eq):
                    result = left == right
                elif isinstance(op, ast.NotEq):
                    result = left != right
                else:
                    raise TypeError(f"不支持的比较运算符: {type(op)}")
                
                if not result:
                    return False
                left = right
            return True
        
        else:
            raise TypeError(f"不支持的节点类型: {type(node)}")
    
    def _format_result(self, result: Union[int, float], precision: int = None) -> str:
        """
        格式化计算结果
        
        Args:
            result: 计算结果
            precision: 小数精度
            
        Returns:
            格式化后的结果字符串
        """
        
        # 如果是整数，直接返回
        if isinstance(result, int) or (isinstance(result, float) and result.is_integer()):
            return str(int(result))
        
        # 如果是浮点数
        if isinstance(result, float):
            if precision is not None:
                return f"{result:.{precision}f}"
            else:
                # 自动选择合适的精度
                if abs(result) >= 1000:
                    return f"{result:.2e}"  # 科学计数法
                elif abs(result) >= 1:
                    return f"{result:.6g}"  # 最多6位有效数字
                else:
                    return f"{result:.6g}"  # 小数也用6位有效数字
        
        # 布尔值 (比较运算结果)
        if isinstance(result, bool):
            return "True" if result else "False"
        
        return str(result)
    
    def get_help(self) -> str:
        """
        获取计算器帮助信息
        
        Returns:
            详细的帮助文本
        """
        return """
🧮 计算器工具帮助

基本运算:
  + - * /     基本四则运算
  **          幂运算 (如 2**3 = 8)
  //          整除
  %           取余

数学函数:
  sqrt(x)     平方根
  sin(x)      正弦函数
  cos(x)      余弦函数
  tan(x)      正切函数
  log(x)      自然对数
  log10(x)    常用对数
  exp(x)      指数函数
  abs(x)      绝对值
  round(x)    四舍五入
  ceil(x)     向上取整
  floor(x)    向下取整
  max(a,b,c)  最大值
  min(a,b,c)  最小值

数学常数:
  pi          圆周率 (3.14159...)
  e           自然常数 (2.71828...)

使用示例:
  2 + 3 * 4           → 14
  sqrt(16) + 2        → 6.0
  sin(pi/2)           → 1.0
  2**3 + log10(100)   → 10.0
  max(1, 2, 3)        → 3

注意事项:
  - 支持括号改变运算优先级
  - 角度单位为弧度
  - 除零会返回错误信息
  - 支持科学计数法显示大数
        """


# 便捷函数 (类比pytest的辅助函数)
async def calculate(expression: str, precision: int = None) -> str:
    """
    便捷的计算函数
    
    Args:
        expression: 数学表达式
        precision: 结果精度
        
    Returns:
        计算结果
    """
    calculator = Calculator()
    return await calculator.execute(expression=expression, precision=precision)


# 测试函数 (类比pytest的测试用例)
if __name__ == "__main__":
    import asyncio
    
    async def test_calculator():
        """测试计算器功能"""
        calc = Calculator()
        
        test_cases = [
            "2 + 3",
            "2 * 3 + 4",
            "sqrt(16)",
            "sin(pi/2)",
            "2**3",
            "max(1, 2, 3)",
            "10 / 3",
            "abs(-5)",
        ]
        
        print("🧮 计算器测试:")
        print("=" * 40)
        
        for expr in test_cases:
            result = await calc.execute(expression=expr)
            print(f"  {result}")
        
        print("\n✅ 测试完成")
    
    asyncio.run(test_calculator())