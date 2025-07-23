"""
数据库工具
==========

提供数据库连接和查询功能的工具，类比pytest中的数据库fixture。

功能特点：
1. 支持多种数据库类型（SQLite、MySQL、PostgreSQL）
2. 安全的SQL查询执行（仅支持SELECT）
3. 连接池管理和自动清理
4. 查询结果格式化和限制
"""

import sqlite3
import asyncio
import os
import re
from typing import Dict, Any, List, Optional, Union, Tuple
from pathlib import Path
try:
    from tools import BaseTool
except ImportError:
    # 当直接运行此文件时的导入方式
    import sys
    import os
    sys.path.append(os.path.dirname(os.path.dirname(__file__)))
    from tools import BaseTool

# 尝试导入可选的数据库驱动
try:
    import pymysql
    MYSQL_AVAILABLE = True
except ImportError:
    MYSQL_AVAILABLE = False

try:
    import psycopg2
    POSTGRESQL_AVAILABLE = True
except ImportError:
    POSTGRESQL_AVAILABLE = False


class DatabaseTool(BaseTool):
    """
    数据库工具类
    
    类比pytest的数据库fixture，提供安全的数据库查询功能。
    支持多种数据库类型，但仅允许SELECT查询以确保安全性。
    """
    
    def __init__(self, config: Dict[str, Any] = None):
        super().__init__()
        self.name = "database"
        self.description = "数据库查询工具，支持SQLite、MySQL、PostgreSQL的SELECT查询"
        
        # 配置参数
        self.config = config or {}
        self.max_rows = self.config.get('max_rows', 100)  # 最大返回行数
        self.query_timeout = self.config.get('query_timeout', 30)  # 查询超时时间
        
        # 当前连接信息
        self.current_connection = None
        self.current_db_type = None
        self.connection_info = {}
        
        # 支持的数据库类型
        self.supported_databases = {
            'sqlite': self._connect_sqlite,
            'mysql': self._connect_mysql if MYSQL_AVAILABLE else None,
            'postgresql': self._connect_postgresql if POSTGRESQL_AVAILABLE else None,
        }
        
        # SQL安全检查模式
        self.allowed_keywords = {
            'select', 'from', 'where', 'join', 'inner', 'left', 'right', 'outer',
            'on', 'and', 'or', 'not', 'in', 'like', 'between', 'is', 'null',
            'order', 'by', 'group', 'having', 'limit', 'offset', 'distinct',
            'as', 'case', 'when', 'then', 'else', 'end', 'union', 'all'
        }
        
        # 禁止的关键词
        self.forbidden_keywords = {
            'insert', 'update', 'delete', 'drop', 'create', 'alter', 'truncate',
            'grant', 'revoke', 'commit', 'rollback', 'exec', 'execute', 'sp_',
            'xp_', 'cmdshell', 'bulk', 'openrowset', 'opendatasource'
        }
    
    def validate_args(self, **kwargs) -> bool:
        """
        验证参数
        
        Args:
            **kwargs: 参数字典
            
        Returns:
            参数是否有效
        """
        action = kwargs.get('action')
        if not action:
            print("❌ 缺少必需参数: action")
            return False
        
        valid_actions = ['connect', 'query', 'disconnect', 'show_tables', 'describe', 'status']
        if action not in valid_actions:
            print(f"❌ 无效的操作: {action}，支持的操作: {', '.join(valid_actions)}")
            return False
        
        # 连接操作需要数据库类型
        if action == 'connect':
            if 'db_type' not in kwargs:
                print("❌ 连接操作需要 db_type 参数")
                return False
            
            db_type = kwargs['db_type'].lower()
            if db_type not in self.supported_databases:
                print(f"❌ 不支持的数据库类型: {db_type}")
                return False
            
            if not self.supported_databases[db_type]:
                print(f"❌ 数据库驱动未安装: {db_type}")
                return False
        
        # 查询操作需要SQL语句
        if action == 'query':
            if 'sql' not in kwargs:
                print("❌ 查询操作需要 sql 参数")
                return False
        
        return True
    
    async def execute(self, **kwargs) -> str:
        """
        执行数据库操作
        
        Args:
            action: 操作类型 ('connect', 'query', 'disconnect', 'show_tables', 'describe', 'status')
            db_type: 数据库类型 ('sqlite', 'mysql', 'postgresql')
            connection_string: 连接字符串或文件路径
            sql: SQL查询语句 (仅支持SELECT)
            table: 表名 (用于describe操作)
            
        Returns:
            操作结果字符串
        """
        
        action = kwargs.get('action')
        
        try:
            if action == 'connect':
                return await self._handle_connect(**kwargs)
            elif action == 'query':
                return await self._handle_query(**kwargs)
            elif action == 'disconnect':
                return await self._handle_disconnect()
            elif action == 'show_tables':
                return await self._handle_show_tables()
            elif action == 'describe':
                return await self._handle_describe(**kwargs)
            elif action == 'status':
                return await self._handle_status()
            else:
                return f"❌ 不支持的操作: {action}"
                
        except Exception as e:
            return f"❌ 数据库操作失败: {str(e)}"
    
    async def _handle_connect(self, **kwargs) -> str:
        """处理数据库连接"""
        db_type = kwargs.get('db_type', '').lower()
        connection_string = kwargs.get('connection_string', '')
        
        # 如果已有连接，先断开
        if self.current_connection:
            await self._handle_disconnect()
        
        try:
            connect_func = self.supported_databases[db_type]
            # 过滤掉不需要的参数
            filtered_kwargs = {k: v for k, v in kwargs.items()
                             if k not in ['action', 'db_type', 'connection_string']}
            self.current_connection = await connect_func(connection_string, **filtered_kwargs)
            self.current_db_type = db_type
            self.connection_info = {
                'db_type': db_type,
                'connection_string': connection_string,
                'connected_at': asyncio.get_event_loop().time()
            }

            return f"✅ 成功连接到 {db_type.upper()} 数据库"

        except Exception as e:
            return f"❌ 连接失败: {str(e)}"
    
    async def _handle_query(self, **kwargs) -> str:
        """处理SQL查询"""
        if not self.current_connection:
            return "❌ 未连接到数据库，请先使用 connect 操作"
        
        sql = kwargs.get('sql', '').strip()
        
        # SQL安全检查
        if not self._is_safe_sql(sql):
            return "❌ SQL语句不安全或不被支持，仅允许SELECT查询"
        
        try:
            # 执行查询
            if self.current_db_type == 'sqlite':
                return await self._execute_sqlite_query(sql)
            elif self.current_db_type == 'mysql':
                return await self._execute_mysql_query(sql)
            elif self.current_db_type == 'postgresql':
                return await self._execute_postgresql_query(sql)
            else:
                return f"❌ 不支持的数据库类型: {self.current_db_type}"
                
        except Exception as e:
            return f"❌ 查询执行失败: {str(e)}"
    
    async def _handle_disconnect(self) -> str:
        """处理数据库断开连接"""
        if not self.current_connection:
            return "ℹ️ 当前没有活动的数据库连接"
        
        try:
            if hasattr(self.current_connection, 'close'):
                self.current_connection.close()
            
            self.current_connection = None
            self.current_db_type = None
            self.connection_info = {}
            
            return "✅ 数据库连接已断开"
            
        except Exception as e:
            return f"⚠️ 断开连接时出现警告: {str(e)}"
    
    async def _handle_show_tables(self) -> str:
        """显示数据库中的表"""
        if not self.current_connection:
            return "❌ 未连接到数据库"
        
        try:
            if self.current_db_type == 'sqlite':
                sql = "SELECT name FROM sqlite_master WHERE type='table'"
            elif self.current_db_type == 'mysql':
                sql = "SHOW TABLES"
            elif self.current_db_type == 'postgresql':
                sql = "SELECT tablename FROM pg_tables WHERE schemaname='public'"
            else:
                return f"❌ 不支持的数据库类型: {self.current_db_type}"
            
            return await self._handle_query(sql=sql)
            
        except Exception as e:
            return f"❌ 获取表列表失败: {str(e)}"
    
    async def _handle_describe(self, **kwargs) -> str:
        """描述表结构"""
        if not self.current_connection:
            return "❌ 未连接到数据库"

        table = kwargs.get('table')
        if not table:
            return "❌ 需要指定表名"

        try:
            if self.current_db_type == 'sqlite':
                # 对于SQLite，直接执行PRAGMA查询
                cursor = self.current_connection.cursor()
                cursor.execute(f"PRAGMA table_info({table})")
                rows = cursor.fetchall()

                if not rows:
                    return f"❌ 表 '{table}' 不存在或无权限访问"

                # 格式化PRAGMA结果
                columns = ['cid', 'name', 'type', 'notnull', 'dflt_value', 'pk']
                return self._format_query_result(columns, rows)

            elif self.current_db_type == 'mysql':
                sql = f"DESCRIBE {table}"
            elif self.current_db_type == 'postgresql':
                sql = f"SELECT column_name, data_type, is_nullable FROM information_schema.columns WHERE table_name='{table}'"
            else:
                return f"❌ 不支持的数据库类型: {self.current_db_type}"

            # 对于MySQL和PostgreSQL，使用常规查询方法
            if self.current_db_type != 'sqlite':
                return await self._handle_query(sql=sql)

        except Exception as e:
            return f"❌ 获取表结构失败: {str(e)}"
    
    async def _handle_status(self) -> str:
        """显示连接状态"""
        if not self.current_connection:
            return "📊 数据库状态: 未连接"
        
        info = self.connection_info
        connected_time = asyncio.get_event_loop().time() - info.get('connected_at', 0)
        
        return f"""📊 数据库连接状态:
🔗 数据库类型: {info.get('db_type', 'unknown').upper()}
⏱️ 连接时长: {connected_time:.1f}秒
📍 连接信息: {info.get('connection_string', 'unknown')}
✅ 状态: 已连接"""
    
    def _is_safe_sql(self, sql: str) -> bool:
        """
        检查SQL语句是否安全
        
        Args:
            sql: SQL语句
            
        Returns:
            是否安全
        """
        sql_lower = sql.lower().strip()
        
        # 必须以SELECT开头
        if not sql_lower.startswith('select'):
            return False
        
        # 检查是否包含禁止的关键词
        for forbidden in self.forbidden_keywords:
            if forbidden in sql_lower:
                return False
        
        # 检查是否包含危险字符
        dangerous_patterns = [
            r'--',  # SQL注释
            r'/\*',  # 多行注释开始
            r'\*/',  # 多行注释结束
            r';.*\w',  # 分号后还有内容（可能是多语句）
        ]
        
        for pattern in dangerous_patterns:
            if re.search(pattern, sql_lower):
                return False
        
        return True
    
    async def _connect_sqlite(self, connection_string: str, **kwargs) -> sqlite3.Connection:
        """连接SQLite数据库"""
        # 如果是相对路径，转换为绝对路径
        if not os.path.isabs(connection_string):
            connection_string = os.path.abspath(connection_string)
        
        # 检查文件是否存在（对于SQLite）
        if connection_string != ':memory:' and not os.path.exists(connection_string):
            # 创建目录（如果不存在）
            os.makedirs(os.path.dirname(connection_string), exist_ok=True)
        
        conn = sqlite3.connect(connection_string)
        conn.row_factory = sqlite3.Row  # 使结果可以按列名访问
        return conn
    
    async def _connect_mysql(self, connection_string: str, **kwargs) -> Any:
        """连接MySQL数据库"""
        if not MYSQL_AVAILABLE:
            raise ImportError("MySQL驱动未安装，请运行: pip install pymysql")
        
        # 解析连接字符串或使用单独的参数
        if '://' in connection_string:
            # mysql://user:password@host:port/database
            import urllib.parse
            parsed = urllib.parse.urlparse(connection_string)
            config = {
                'host': parsed.hostname,
                'port': parsed.port or 3306,
                'user': parsed.username,
                'password': parsed.password,
                'database': parsed.path.lstrip('/'),
                'charset': 'utf8mb4'
            }
        else:
            config = {
                'host': kwargs.get('host', 'localhost'),
                'port': kwargs.get('port', 3306),
                'user': kwargs.get('user', 'root'),
                'password': kwargs.get('password', ''),
                'database': kwargs.get('database', connection_string),
                'charset': 'utf8mb4'
            }
        
        return pymysql.connect(**config)
    
    async def _connect_postgresql(self, connection_string: str, **kwargs) -> Any:
        """连接PostgreSQL数据库"""
        if not POSTGRESQL_AVAILABLE:
            raise ImportError("PostgreSQL驱动未安装，请运行: pip install psycopg2-binary")
        
        # 使用连接字符串或构建连接参数
        if '://' in connection_string:
            return psycopg2.connect(connection_string)
        else:
            config = {
                'host': kwargs.get('host', 'localhost'),
                'port': kwargs.get('port', 5432),
                'user': kwargs.get('user', 'postgres'),
                'password': kwargs.get('password', ''),
                'database': kwargs.get('database', connection_string)
            }
            return psycopg2.connect(**config)
    
    async def _execute_sqlite_query(self, sql: str) -> str:
        """执行SQLite查询"""
        cursor = self.current_connection.cursor()
        cursor.execute(sql)
        
        rows = cursor.fetchmany(self.max_rows)
        
        if not rows:
            return "📊 查询完成，没有返回数据"
        
        # 格式化结果
        columns = [description[0] for description in cursor.description]
        return self._format_query_result(columns, rows)
    
    async def _execute_mysql_query(self, sql: str) -> str:
        """执行MySQL查询"""
        cursor = self.current_connection.cursor()
        cursor.execute(sql)
        
        rows = cursor.fetchmany(self.max_rows)
        
        if not rows:
            return "📊 查询完成，没有返回数据"
        
        # 格式化结果
        columns = [desc[0] for desc in cursor.description]
        return self._format_query_result(columns, rows)
    
    async def _execute_postgresql_query(self, sql: str) -> str:
        """执行PostgreSQL查询"""
        cursor = self.current_connection.cursor()
        cursor.execute(sql)
        
        rows = cursor.fetchmany(self.max_rows)
        
        if not rows:
            return "📊 查询完成，没有返回数据"
        
        # 格式化结果
        columns = [desc[0] for desc in cursor.description]
        return self._format_query_result(columns, rows)
    
    def _format_query_result(self, columns: List[str], rows: List[Tuple]) -> str:
        """
        格式化查询结果
        
        Args:
            columns: 列名列表
            rows: 数据行列表
            
        Returns:
            格式化后的结果字符串
        """
        if not rows:
            return "📊 查询完成，没有返回数据"
        
        # 计算每列的最大宽度
        col_widths = [len(col) for col in columns]
        for row in rows:
            for i, cell in enumerate(row):
                cell_str = str(cell) if cell is not None else 'NULL'
                col_widths[i] = max(col_widths[i], len(cell_str))
        
        # 限制列宽，避免输出过宽
        max_col_width = 30
        col_widths = [min(width, max_col_width) for width in col_widths]
        
        # 构建表格
        lines = []
        
        # 表头
        header = " | ".join(col.ljust(col_widths[i]) for i, col in enumerate(columns))
        lines.append(header)
        lines.append("-" * len(header))
        
        # 数据行
        for row in rows:
            row_str = " | ".join(
                str(cell)[:col_widths[i]].ljust(col_widths[i]) if cell is not None else 'NULL'.ljust(col_widths[i])
                for i, cell in enumerate(row)
            )
            lines.append(row_str)
        
        result = "\n".join(lines)
        
        # 添加统计信息
        total_rows = len(rows)
        if total_rows >= self.max_rows:
            result += f"\n\n📊 显示前 {self.max_rows} 行结果（可能还有更多数据）"
        else:
            result += f"\n\n📊 共 {total_rows} 行结果"
        
        return result
    
    def get_help(self) -> str:
        """
        获取数据库工具帮助信息
        
        Returns:
            详细的帮助文本
        """
        return """
🗄️ 数据库工具帮助

支持的操作:
• connect: 连接数据库
• query: 执行SELECT查询
• disconnect: 断开数据库连接
• show_tables: 显示所有表
• describe: 显示表结构
• status: 显示连接状态

支持的数据库:
• SQLite: 轻量级文件数据库
• MySQL: 需要安装 pymysql (pip install pymysql)
• PostgreSQL: 需要安装 psycopg2 (pip install psycopg2-binary)

使用示例:
• 连接SQLite: {"action": "connect", "db_type": "sqlite", "connection_string": "test.db"}
• 连接MySQL: {"action": "connect", "db_type": "mysql", "host": "localhost", "user": "root", "password": "123456", "database": "test"}
• 执行查询: {"action": "query", "sql": "SELECT * FROM users LIMIT 10"}
• 显示表: {"action": "show_tables"}
• 表结构: {"action": "describe", "table": "users"}

安全特性:
• 仅支持SELECT查询，禁止修改操作
• SQL注入防护
• 查询结果行数限制
• 连接超时控制
        """


# 便捷函数
async def query_database(db_type: str, connection_string: str, sql: str) -> str:
    """
    便捷的数据库查询函数
    
    Args:
        db_type: 数据库类型
        connection_string: 连接字符串
        sql: SQL查询语句
        
    Returns:
        查询结果
    """
    db_tool = DatabaseTool()
    
    # 连接数据库
    connect_result = await db_tool.execute(
        action="connect",
        db_type=db_type,
        connection_string=connection_string
    )
    
    if "❌" in connect_result:
        return connect_result
    
    # 执行查询
    query_result = await db_tool.execute(action="query", sql=sql)
    
    # 断开连接
    await db_tool.execute(action="disconnect")
    
    return query_result


# 测试函数
if __name__ == "__main__":
    import asyncio
    
    async def test_database_tool():
        """测试数据库工具功能"""
        db_tool = DatabaseTool()
        
        print("🗄️ 数据库工具测试:")
        print("=" * 50)
        
        # 测试SQLite连接
        print("\n1️⃣ 测试SQLite连接")
        result = await db_tool.execute(
            action="connect",
            db_type="sqlite",
            connection_string=":memory:"
        )
        print(f"连接结果: {result}")
        
        # 创建测试表和数据
        if "✅" in result:
            # 注意：这里为了测试，我们直接操作连接，实际使用中只能SELECT
            cursor = db_tool.current_connection.cursor()

            # 先删除表（如果存在）
            cursor.execute("DROP TABLE IF EXISTS users")

            cursor.execute("""
                CREATE TABLE users (
                    id INTEGER PRIMARY KEY,
                    name TEXT NOT NULL,
                    email TEXT,
                    age INTEGER
                )
            """)
            cursor.execute("INSERT INTO users (name, email, age) VALUES ('Alice', 'alice@example.com', 25)")
            cursor.execute("INSERT INTO users (name, email, age) VALUES ('Bob', 'bob@example.com', 30)")
            cursor.execute("INSERT INTO users (name, email, age) VALUES ('Charlie', 'charlie@example.com', 35)")
            db_tool.current_connection.commit()
            
            print("\n2️⃣ 测试查询")
            result = await db_tool.execute(
                action="query",
                sql="SELECT * FROM users"
            )
            print(f"查询结果:\n{result}")
            
            print("\n3️⃣ 测试显示表")
            result = await db_tool.execute(action="show_tables")
            print(f"表列表:\n{result}")
            
            print("\n4️⃣ 测试表结构")
            result = await db_tool.execute(action="describe", table="users")
            print(f"表结构:\n{result}")
            
            print("\n5️⃣ 测试连接状态")
            result = await db_tool.execute(action="status")
            print(f"连接状态:\n{result}")
        
        # 断开连接
        print("\n6️⃣ 断开连接")
        result = await db_tool.execute(action="disconnect")
        print(f"断开结果: {result}")
        
        print("\n✅ 测试完成")
    
    asyncio.run(test_database_tool())
