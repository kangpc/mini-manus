#!/usr/bin/env python3
"""
文件编辑工具使用示例
===================

演示如何使用 file_editor 工具进行各种文件操作
"""

import asyncio
from tools.file_editor import FileEditor


async def demo_file_operations():
    """演示文件编辑工具的各种操作"""
    
    print("📝 文件编辑工具使用示例")
    print("=" * 50)
    
    # 创建文件编辑器实例
    editor = FileEditor()
    
    # 1. 创建一个测试文件
    print("\n1️⃣ 创建文件")
    result = await editor.execute(
        action="create",
        path="demo.txt",
        content="Hello, World!\n这是一个测试文件。\n第三行内容。"
    )
    print(f"结果: {result}")
    
    # 2. 读取文件内容
    print("\n2️⃣ 读取文件")
    result = await editor.execute(
        action="read",
        path="demo.txt"
    )
    print(f"结果: {result}")
    
    # 3. 获取文件信息
    print("\n3️⃣ 获取文件信息")
    result = await editor.execute(
        action="info",
        path="demo.txt"
    )
    print(f"结果: {result}")
    
    # 4. 备份文件
    print("\n4️⃣ 备份文件")
    result = await editor.execute(
        action="backup",
        path="demo.txt"
    )
    print(f"结果: {result}")
    
    # 5. 修改文件内容
    print("\n5️⃣ 修改文件内容")
    result = await editor.execute(
        action="write",
        path="demo.txt",
        content="Hello, Updated World!\n文件内容已更新。\n新的第三行。\n添加了第四行。"
    )
    print(f"结果: {result}")
    
    # 6. 再次读取文件确认修改
    print("\n6️⃣ 确认文件修改")
    result = await editor.execute(
        action="read",
        path="demo.txt"
    )
    print(f"结果: {result}")
    
    # 7. 列出当前目录
    print("\n7️⃣ 列出当前目录")
    result = await editor.execute(
        action="list",
        path="."
    )
    print(f"结果: {result}")
    
    # 8. 恢复文件
    print("\n8️⃣ 恢复文件")
    result = await editor.execute(
        action="restore",
        path="demo.txt"
    )
    print(f"结果: {result}")
    
    # 9. 确认恢复结果
    print("\n9️⃣ 确认恢复结果")
    result = await editor.execute(
        action="read",
        path="demo.txt"
    )
    print(f"结果: {result}")
    
    # 10. 清理：删除测试文件
    print("\n🔟 清理测试文件")
    result = await editor.execute(
        action="delete",
        path="demo.txt"
    )
    print(f"结果: {result}")
    
    # 删除备份文件
    result = await editor.execute(
        action="delete",
        path="demo.txt.backup"
    )
    print(f"删除备份: {result}")
    
    print("\n✅ 文件编辑工具演示完成！")


async def demo_error_handling():
    """演示错误处理"""
    
    print("\n" + "=" * 50)
    print("🚨 错误处理演示")
    print("=" * 50)
    
    editor = FileEditor()
    
    # 1. 读取不存在的文件
    print("\n1️⃣ 读取不存在的文件")
    result = await editor.execute(
        action="read",
        path="nonexistent.txt"
    )
    print(f"结果: {result}")
    
    # 2. 无效的操作
    print("\n2️⃣ 无效的操作")
    result = await editor.execute(
        action="invalid_action",
        path="test.txt"
    )
    print(f"结果: {result}")
    
    # 3. 缺少必需参数
    print("\n3️⃣ 缺少必需参数")
    result = await editor.execute(
        action="write"
        # 缺少 path 和 content 参数
    )
    print(f"结果: {result}")


def show_help():
    """显示帮助信息"""
    
    print("\n" + "=" * 50)
    print("📖 文件编辑工具帮助")
    print("=" * 50)
    
    editor = FileEditor()
    print(editor.get_help())


async def interactive_demo():
    """交互式演示"""
    
    print("\n" + "=" * 50)
    print("🎮 交互式文件操作")
    print("=" * 50)
    
    editor = FileEditor()
    
    while True:
        print("\n可用操作:")
        print("1. 创建文件 (create)")
        print("2. 读取文件 (read)")
        print("3. 写入文件 (write)")
        print("4. 删除文件 (delete)")
        print("5. 列出目录 (list)")
        print("6. 文件信息 (info)")
        print("7. 备份文件 (backup)")
        print("8. 恢复文件 (restore)")
        print("9. 显示帮助")
        print("0. 退出")
        
        choice = input("\n请选择操作 (0-9): ").strip()
        
        if choice == "0":
            print("👋 再见！")
            break
        elif choice == "9":
            print(editor.get_help())
            continue
        
        # 获取操作参数
        action_map = {
            "1": "create", "2": "read", "3": "write", "4": "delete",
            "5": "list", "6": "info", "7": "backup", "8": "restore"
        }
        
        if choice not in action_map:
            print("❌ 无效选择")
            continue
        
        action = action_map[choice]
        path = input("请输入文件路径: ").strip()
        
        kwargs = {"action": action, "path": path}
        
        if action in ["create", "write"]:
            content = input("请输入文件内容: ").strip()
            kwargs["content"] = content
        elif action == "restore":
            backup_path = input("备份文件路径 (可选): ").strip()
            if backup_path:
                kwargs["backup_path"] = backup_path
        
        # 执行操作
        result = await editor.execute(**kwargs)
        print(f"\n📊 执行结果: {result}")


if __name__ == "__main__":
    print("🚀 启动文件编辑工具演示")
    
    # 运行基础演示
    asyncio.run(demo_file_operations())
    
    # 运行错误处理演示
    asyncio.run(demo_error_handling())
    
    # 显示帮助信息
    show_help()
    
    # 询问是否运行交互式演示
    if input("\n是否运行交互式演示？(y/N): ").lower().startswith('y'):
        asyncio.run(interactive_demo())
