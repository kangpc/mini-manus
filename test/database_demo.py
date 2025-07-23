#!/usr/bin/env python3
"""
数据库工具使用示例
==================

演示如何使用 database 工具进行各种数据库操作
"""

import asyncio
from tools.database import DatabaseTool


async def demo_sqlite_operations():
    """演示SQLite数据库操作"""
    
    print("🗄️ SQLite数据库工具使用示例")
    print("=" * 50)
    
    # 创建数据库工具实例
    db_tool = DatabaseTool()
    
    # 1. 连接到SQLite数据库
    print("\n1️⃣ 连接SQLite数据库")
    result = await db_tool.execute(
        action="connect",
        db_type="sqlite",
        connection_string="demo.db"
    )
    print(f"连接结果: {result}")
    
    if "✅" not in result:
        print("❌ 连接失败，退出演示")
        return
    
    # 2. 显示连接状态
    print("\n2️⃣ 显示连接状态")
    result = await db_tool.execute(action="status")
    print(f"连接状态:\n{result}")
    
    # 3. 创建测试数据（注意：实际使用中数据库工具只支持SELECT）
    print("\n3️⃣ 准备测试数据")
    # 这里我们直接操作连接来创建测试数据
    cursor = db_tool.current_connection.cursor()
    cursor.execute("DROP TABLE IF EXISTS employees")
    cursor.execute("""
        CREATE TABLE employees (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            department TEXT,
            salary REAL,
            hire_date TEXT
        )
    """)
    
    # 插入测试数据
    test_data = [
        ('张三', '技术部', 8000.0, '2023-01-15'),
        ('李四', '销售部', 6500.0, '2023-02-20'),
        ('王五', '技术部', 9500.0, '2022-12-10'),
        ('赵六', '人事部', 7000.0, '2023-03-05'),
        ('钱七', '技术部', 8500.0, '2023-01-30'),
    ]
    
    cursor.executemany(
        "INSERT INTO employees (name, department, salary, hire_date) VALUES (?, ?, ?, ?)",
        test_data
    )
    db_tool.current_connection.commit()
    print("✅ 测试数据准备完成")
    
    # 4. 显示所有表
    print("\n4️⃣ 显示所有表")
    result = await db_tool.execute(action="show_tables")
    print(f"表列表:\n{result}")
    
    # 5. 查看表结构
    print("\n5️⃣ 查看employees表结构")
    result = await db_tool.execute(action="describe", table="employees")
    print(f"表结构:\n{result}")
    
    # 6. 基本查询
    print("\n6️⃣ 查询所有员工")
    result = await db_tool.execute(
        action="query",
        sql="SELECT * FROM employees"
    )
    print(f"查询结果:\n{result}")
    
    # 7. 条件查询
    print("\n7️⃣ 查询技术部员工")
    result = await db_tool.execute(
        action="query",
        sql="SELECT name, salary FROM employees WHERE department = '技术部'"
    )
    print(f"查询结果:\n{result}")
    
    # 8. 聚合查询
    print("\n8️⃣ 统计各部门平均工资")
    result = await db_tool.execute(
        action="query",
        sql="SELECT department, AVG(salary) as avg_salary, COUNT(*) as count FROM employees GROUP BY department"
    )
    print(f"查询结果:\n{result}")
    
    # 9. 排序查询
    print("\n9️⃣ 按工资降序排列")
    result = await db_tool.execute(
        action="query",
        sql="SELECT name, department, salary FROM employees ORDER BY salary DESC LIMIT 3"
    )
    print(f"查询结果:\n{result}")
    
    # 10. 复杂查询
    print("\n🔟 查询工资高于平均工资的员工")
    result = await db_tool.execute(
        action="query",
        sql="SELECT name, department, salary FROM employees WHERE salary > (SELECT AVG(salary) FROM employees)"
    )
    print(f"查询结果:\n{result}")
    
    # 11. 断开连接
    print("\n1️⃣1️⃣ 断开数据库连接")
    result = await db_tool.execute(action="disconnect")
    print(f"断开结果: {result}")
    
    print("\n✅ SQLite演示完成！")


async def demo_security_features():
    """演示安全特性"""
    
    print("\n" + "=" * 50)
    print("🔒 数据库安全特性演示")
    print("=" * 50)
    
    db_tool = DatabaseTool()
    
    # 连接数据库
    await db_tool.execute(
        action="connect",
        db_type="sqlite",
        connection_string=":memory:"
    )
    
    # 测试危险SQL语句
    dangerous_queries = [
        "DROP TABLE users",
        "INSERT INTO users VALUES (1, 'hacker')",
        "UPDATE users SET password = 'hacked'",
        "DELETE FROM users",
        "SELECT * FROM users; DROP TABLE users;",
        "SELECT * FROM users -- comment",
        "SELECT * FROM users /* comment */",
    ]
    
    print("\n🚨 测试危险SQL语句（应该被阻止）:")
    for i, sql in enumerate(dangerous_queries, 1):
        print(f"\n{i}. 测试: {sql}")
        result = await db_tool.execute(action="query", sql=sql)
        print(f"   结果: {result}")
    
    # 测试安全的SQL语句
    safe_queries = [
        "SELECT 1 as test",
        "SELECT 'Hello' as greeting, 'World' as target",
        "SELECT datetime('now') as current_time",
    ]
    
    print("\n✅ 测试安全SQL语句（应该被允许）:")
    for i, sql in enumerate(safe_queries, 1):
        print(f"\n{i}. 测试: {sql}")
        result = await db_tool.execute(action="query", sql=sql)
        print(f"   结果: {result}")
    
    await db_tool.execute(action="disconnect")
    print("\n✅ 安全特性演示完成！")


async def demo_error_handling():
    """演示错误处理"""
    
    print("\n" + "=" * 50)
    print("🚨 错误处理演示")
    print("=" * 50)
    
    db_tool = DatabaseTool()
    
    # 1. 未连接时查询
    print("\n1️⃣ 未连接时查询")
    result = await db_tool.execute(action="query", sql="SELECT 1")
    print(f"结果: {result}")
    
    # 2. 连接不存在的数据库类型
    print("\n2️⃣ 连接不支持的数据库类型")
    result = await db_tool.execute(
        action="connect",
        db_type="oracle",
        connection_string="test"
    )
    print(f"结果: {result}")
    
    # 3. 无效的操作
    print("\n3️⃣ 无效的操作")
    result = await db_tool.execute(action="invalid_action")
    print(f"结果: {result}")
    
    # 4. 缺少必需参数
    print("\n4️⃣ 缺少必需参数")
    result = await db_tool.execute(action="connect")
    print(f"结果: {result}")
    
    print("\n✅ 错误处理演示完成！")


def show_help():
    """显示帮助信息"""
    
    print("\n" + "=" * 50)
    print("📖 数据库工具帮助")
    print("=" * 50)
    
    db_tool = DatabaseTool()
    print(db_tool.get_help())


async def interactive_demo():
    """交互式演示"""

    print("\n" + "=" * 50)
    print("🎮 交互式数据库操作")
    print("=" * 50)

    db_tool = DatabaseTool()

    try:
        while True:
            print("\n可用操作:")
            print("1. 连接数据库 (connect)")
            print("2. 执行查询 (query)")
            print("3. 显示表列表 (show_tables)")
            print("4. 显示表结构 (describe)")
            print("5. 显示连接状态 (status)")
            print("6. 断开连接 (disconnect)")
            print("7. 显示帮助")
            print("0. 退出")

            choice = input("\n请选择操作 (0-7): ").strip()

            if choice == "0":
                print("👋 再见！")
                # 确保断开数据库连接
                if db_tool.current_connection:
                    await db_tool.execute(action="disconnect")
                break
            elif choice == "7":
                print(db_tool.get_help())
                continue
        
            # 获取操作参数
            action_map = {
                "1": "connect", "2": "query", "3": "show_tables",
                "4": "describe", "5": "status", "6": "disconnect"
            }

            if choice not in action_map:
                print("❌ 无效选择")
                continue

            action = action_map[choice]
            kwargs = {"action": action}

            if action == "connect":
                db_type = input("数据库类型 (sqlite/mysql/postgresql): ").strip().lower()
                connection_string = input("连接字符串或文件路径: ").strip()
                kwargs.update({"db_type": db_type, "connection_string": connection_string})
            elif action == "query":
                sql = input("请输入SQL查询语句: ").strip()
                kwargs["sql"] = sql
            elif action == "describe":
                table = input("请输入表名: ").strip()
                kwargs["table"] = table

            # 执行操作
            result = await db_tool.execute(**kwargs)
            print(f"\n📊 执行结果:\n{result}")

    except KeyboardInterrupt:
        print("\n\n👋 用户中断，退出交互式演示！")
        # 确保断开数据库连接
        if db_tool.current_connection:
            await db_tool.execute(action="disconnect")
    except Exception as e:
        print(f"\n❌ 交互式演示出错: {e}")
        # 确保断开数据库连接
        if db_tool.current_connection:
            await db_tool.execute(action="disconnect")


if __name__ == "__main__":
    print("🚀 启动数据库工具演示")

    try:
        # 运行SQLite操作演示
        asyncio.run(demo_sqlite_operations())

        # 运行安全特性演示
        asyncio.run(demo_security_features())

        # 运行错误处理演示
        asyncio.run(demo_error_handling())

        # 显示帮助信息
        show_help()

        # 询问是否运行交互式演示
        if input("\n是否运行交互式演示？(y/N): ").lower().startswith('y'):
            try:
                asyncio.run(interactive_demo())
            except KeyboardInterrupt:
                print("\n\n👋 用户中断，演示结束！")
            except Exception as e:
                print(f"\n❌ 交互式演示出错: {e}")

    except KeyboardInterrupt:
        print("\n\n👋 用户中断，演示结束！")
    except Exception as e:
        print(f"\n❌ 演示过程中出错: {e}")

    print("\n✅ 数据库工具演示完成！")
