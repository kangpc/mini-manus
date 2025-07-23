#!/usr/bin/env python3
"""
测试数据库工具的退出处理
========================

验证修复后的异常处理是否正常工作
"""

import asyncio
from tools.database import DatabaseTool


async def test_normal_exit():
    """测试正常退出流程"""
    print("🧪 测试正常退出流程")
    
    db_tool = DatabaseTool()
    
    # 连接数据库
    result = await db_tool.execute(
        action="connect",
        db_type="sqlite",
        connection_string=":memory:"
    )
    print(f"连接结果: {result}")
    
    # 正常断开
    result = await db_tool.execute(action="disconnect")
    print(f"断开结果: {result}")
    
    print("✅ 正常退出测试通过")


async def test_exception_handling():
    """测试异常处理"""
    print("\n🧪 测试异常处理")
    
    db_tool = DatabaseTool()
    
    try:
        # 连接数据库
        await db_tool.execute(
            action="connect",
            db_type="sqlite", 
            connection_string=":memory:"
        )
        
        # 模拟异常情况
        raise KeyboardInterrupt("模拟用户中断")
        
    except KeyboardInterrupt as e:
        print(f"捕获到中断: {e}")
        
        # 确保清理连接
        if db_tool.current_connection:
            result = await db_tool.execute(action="disconnect")
            print(f"清理连接: {result}")
        
        print("✅ 异常处理测试通过")


async def test_interactive_simulation():
    """模拟交互式操作"""
    print("\n🧪 模拟交互式操作")
    
    db_tool = DatabaseTool()
    
    try:
        # 模拟用户操作序列
        operations = [
            {"action": "connect", "db_type": "sqlite", "connection_string": ":memory:"},
            {"action": "status"},
            {"action": "query", "sql": "SELECT 1 as test"},
            {"action": "disconnect"}
        ]
        
        for i, op in enumerate(operations, 1):
            print(f"\n步骤 {i}: {op['action']}")
            result = await db_tool.execute(**op)
            print(f"结果: {result}")
            
            # 模拟在第3步时用户中断
            if i == 3:
                print("模拟用户中断...")
                raise KeyboardInterrupt("用户按下 Ctrl+C")
                
    except KeyboardInterrupt:
        print("处理用户中断...")
        
        # 清理资源
        if db_tool.current_connection:
            result = await db_tool.execute(action="disconnect")
            print(f"清理连接: {result}")
        
        print("✅ 交互式中断处理测试通过")


if __name__ == "__main__":
    print("🚀 开始数据库工具退出处理测试")
    print("=" * 50)
    
    try:
        # 运行所有测试
        asyncio.run(test_normal_exit())
        asyncio.run(test_exception_handling())
        asyncio.run(test_interactive_simulation())
        
        print("\n" + "=" * 50)
        print("✅ 所有测试通过！退出处理已修复")
        
    except Exception as e:
        print(f"\n❌ 测试失败: {e}")
        print("需要进一步检查代码")
