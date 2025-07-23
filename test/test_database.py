#!/usr/bin/env python3
"""
测试数据库工具的直接调用
"""

import asyncio
import sys
import os

# 添加当前目录到Python路径
sys.path.append(os.path.dirname(__file__))

from tools.database import DatabaseTool


async def test_database_direct():
    """直接测试数据库工具"""
    print("🧪 直接测试数据库工具")
    print("=" * 50)
    
    db_tool = DatabaseTool()
    
    # 测试1: 连接数据库
    print("\n1️⃣ 测试连接数据库")
    result = await db_tool.execute(
        action="connect",
        db_type="sqlite", 
        connection_string="demo.db"
    )
    print(f"连接结果: {result}")
    
    if "✅" in result:
        # 测试2: 查询所有数据
        print("\n2️⃣ 测试查询所有员工")
        result = await db_tool.execute(
            action="query",
            sql="SELECT * FROM employees"
        )
        print(f"查询结果:\n{result}")
        
        # 测试3: 查询技术部员工
        print("\n3️⃣ 测试查询技术部员工")
        result = await db_tool.execute(
            action="query",
            sql="SELECT * FROM employees WHERE department = '技术部'"
        )
        print(f"技术部员工:\n{result}")
        
        # 测试4: 显示表结构
        print("\n4️⃣ 测试显示表结构")
        result = await db_tool.execute(
            action="describe",
            table="employees"
        )
        print(f"表结构:\n{result}")
        
        # 测试5: 断开连接
        print("\n5️⃣ 测试断开连接")
        result = await db_tool.execute(action="disconnect")
        print(f"断开结果: {result}")
    
    print("\n✅ 测试完成")


async def test_agent_rule_matching():
    """测试智能体的规则匹配"""
    print("\n🤖 测试智能体规则匹配")
    print("=" * 50)
    
    from agent import MiniManus
    from config import load_config
    
    # 加载配置
    config = load_config()
    
    # 创建智能体（不使用LLM）
    agent = MiniManus(config)
    
    # 测试数据库相关的规则匹配
    test_inputs = [
        "连接SQLite数据库demo.db",
        "查询employees表的数据",
        "数据库查询employees表中技术部的员工",
        "连接demo.db并查询所有员工信息"
    ]
    
    for user_input in test_inputs:
        print(f"\n📝 测试输入: {user_input}")
        plan = agent._generate_rule_based_plan(user_input)
        print(f"生成计划: {plan}")


if __name__ == "__main__":
    print("🚀 开始测试...")
    
    # 运行直接数据库测试
    asyncio.run(test_database_direct())
    
    # 运行智能体规则匹配测试
    asyncio.run(test_agent_rule_matching())
