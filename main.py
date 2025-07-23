#!/usr/bin/env python3
"""
OpenManus 迷你版 - 主入口文件
=================================

这是一个简化版的AI智能体框架，展示了OpenManus的核心设计理念：
1. 用户输入自然语言指令
2. AI智能体理解指令并选择合适的工具
3. 执行工具并返回结果

类比pytest框架：
- Agent = 测试类 (组织和执行逻辑)
- Tool = fixture (提供具体功能)
- ToolCollection = 插件系统 (管理工具集合)
"""

import asyncio
import json
from typing import Dict, Any, Optional
from agent import MiniManus
from config import load_config


async def main():
    """
    主函数 - 类比pytest的main()函数
    
    执行流程：
    1. 加载配置 (类比pytest.ini)
    2. 初始化智能体 (类比测试收集器)
    3. 接收用户输入 (类比测试用例)
    4. 执行任务 (类比测试执行)
    5. 返回结果 (类比测试报告)
    """
    print("🤖 欢迎使用 OpenManus 迷你版!")
    print("=" * 50)
    
    # 1. 加载配置文件 (类比pytest读取配置)
    try:
        config = load_config()
        print(f"✅ 配置加载成功，使用模型: {config.get('model', 'mock')}")
    except Exception as e:
        print(f"⚠️  配置加载失败，使用默认配置: {e}")
        config = {"model": "mock", "api_key": "mock"}
    
    # 2. 创建智能体实例 (类比pytest创建测试实例)
    agent = MiniManus(config)
    print(f"🚀 智能体 '{agent.name}' 初始化完成")
    print(f"📦 可用工具: {', '.join(agent.get_available_tools())}")
    
    # 3. 交互式对话循环 (类比pytest的测试执行循环)
    print("\n💡 输入您的指令，输入 'quit' 退出")
    print("-" * 30)
    
    while True:
        try:
            # 获取用户输入
            user_input = input("\n👤 您: ").strip()
            
            # 退出条件
            if user_input.lower() in ['quit', 'exit', 'q']:
                print("👋 再见!")
                break
                
            if not user_input:
                print("⚠️  请输入有效指令")
                continue
            
            # 4. 执行任务 (类比pytest执行测试)
            print(f"\n🤔 智能体正在思考...")
            result = await agent.run(user_input)
            
            # 5. 显示结果 (类比pytest测试报告)
            print(f"\n🤖 智能体: {result}")
            
        except KeyboardInterrupt:
            print("\n\n👋 程序被用户中断，再见!")
            break
        except Exception as e:
            print(f"\n❌ 执行出错: {e}")


if __name__ == "__main__":
    # 运行异步主函数 (现代Python的标准做法)
    asyncio.run(main())