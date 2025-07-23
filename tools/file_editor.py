"""
文件编辑工具
============

提供文件读写、编辑功能的工具，类比pytest中的文件fixture和临时文件管理。

功能特点：
1. 安全的文件操作
2. 支持多种编码格式
3. 文件备份和恢复
4. 路径安全检查
"""

import os
import shutil
import tempfile
from pathlib import Path
from typing import Dict, Any, Optional, List
from tools import BaseTool


class FileEditor(BaseTool):
    """
    文件编辑工具类
    
    类比pytest的文件fixture，提供安全的文件操作功能。
    包含路径安全检查，防止恶意文件操作。
    """
    
    def __init__(self, config: Dict[str, Any] = None):
        super().__init__()
        self.name = "file_editor"
        self.description = "文件编辑工具，支持读取、写入、创建、删除文件"
        
        # 配置参数 (类比pytest的配置)
        self.config = config or {}
        self.max_file_size = self.config.get('max_file_size', 1024 * 1024)  # 1MB
        self.allowed_extensions = self.config.get('allowed_extensions', [
            '.txt', '.py', '.js', '.html', '.css', '.json', '.xml', '.csv',
            '.md', '.yml', '.yaml', '.toml', '.ini', '.cfg', '.log'
        ])
        self.backup_enabled = self.config.get('backup_enabled', True)
        
        # 安全路径限制 (类比pytest的安全沙箱)
        self.safe_base_paths = [
            os.getcwd(),  # 当前工作目录
            tempfile.gettempdir(),  # 临时目录
        ]
        
        # 禁止访问的路径
        self.forbidden_paths = [
            '/etc', '/usr', '/bin', '/sbin', '/var', '/root',
            'C:\\Windows', 'C:\\Program Files', 'C:\\System32'
        ]
    
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
        
        valid_actions = ['read', 'write', 'create', 'delete', 'list', 'info', 'backup', 'restore']
        if action not in valid_actions:
            print(f"❌ 无效的操作: {action}，支持的操作: {', '.join(valid_actions)}")
            return False
        
        # 大部分操作需要文件路径
        if action in ['read', 'write', 'create', 'delete', 'info', 'backup', 'restore']:
            if 'path' not in kwargs:
                print(f"❌ 操作 '{action}' 需要 path 参数")
                return False
        
        # 写入和创建操作需要内容
        if action in ['write', 'create'] and 'content' not in kwargs:
            print(f"❌ 操作 '{action}' 需要 content 参数")
            return False
        
        return True
    
    async def execute(self, **kwargs) -> str:
        """
        执行文件操作
        
        Args:
            action: 操作类型 ('read', 'write', 'create', 'delete', 'list', 'info')
            path: 文件路径 (大部分操作需要)
            content: 文件内容 (写入操作需要)
            encoding: 文件编码 (可选，默认utf-8)
            
        Returns:
            操作结果字符串
        """
        
        action = kwargs.get('action')
        path = kwargs.get('path')
        content = kwargs.get('content', '')
        encoding = kwargs.get('encoding', 'utf-8')
        
        try:
            # 路径安全检查 (类比pytest的安全检查)
            if path and not self._is_safe_path(path):
                return f"❌ 路径不安全或不被允许: {path}"
            
            # 根据操作类型执行相应功能
            if action == 'read':
                return await self._read_file(path, encoding)
            elif action == 'write':
                return await self._write_file(path, content, encoding)
            elif action == 'create':
                return await self._create_file(path, content, encoding)
            elif action == 'delete':
                return await self._delete_file(path)
            elif action == 'list':
                return await self._list_directory(path or '.')
            elif action == 'info':
                return await self._get_file_info(path)
            elif action == 'backup':
                return await self._backup_file(path)
            elif action == 'restore':
                backup_path = kwargs.get('backup_path')
                return await self._restore_file(path, backup_path)
            else:
                return f"❌ 不支持的操作: {action}"
                
        except Exception as e:
            return f"❌ 执行文件操作时出错: {str(e)}"
    
    def _is_safe_path(self, path: str) -> bool:
        """
        检查路径是否安全
        
        类比pytest的安全沙箱机制，防止访问危险路径
        
        Args:
            path: 要检查的路径
            
        Returns:
            路径是否安全
        """
        try:
            # 转换为绝对路径
            abs_path = os.path.abspath(path)
            
            # 检查是否在禁止路径中
            for forbidden in self.forbidden_paths:
                if abs_path.startswith(forbidden):
                    return False
            
            # 检查是否在允许的基础路径中
            for safe_base in self.safe_base_paths:
                if abs_path.startswith(os.path.abspath(safe_base)):
                    return True
            
            return False
            
        except Exception:
            return False
    
    def _check_file_extension(self, path: str) -> bool:
        """
        检查文件扩展名是否被允许
        
        Args:
            path: 文件路径
            
        Returns:
            扩展名是否被允许
        """
        if not self.allowed_extensions:
            return True
        
        ext = Path(path).suffix.lower()
        return ext in self.allowed_extensions
    
    async def _read_file(self, path: str, encoding: str = 'utf-8') -> str:
        """
        读取文件内容
        
        类比pytest中读取测试数据文件
        
        Args:
            path: 文件路径
            encoding: 文件编码
            
        Returns:
            文件内容或错误信息
        """
        try:
            if not os.path.exists(path):
                return f"❌ 文件不存在: {path}"
            
            if not os.path.isfile(path):
                return f"❌ 路径不是文件: {path}"
            
            # 检查文件大小
            file_size = os.path.getsize(path)
            if file_size > self.max_file_size:
                return f"❌ 文件过大 ({file_size} bytes)，超过限制 ({self.max_file_size} bytes)"
            
            # 检查文件扩展名
            if not self._check_file_extension(path):
                return f"❌ 不支持的文件类型: {Path(path).suffix}"
            
            with open(path, 'r', encoding=encoding) as f:
                content = f.read()
            
            return f"✅ 文件读取成功 ({len(content)} 字符):\n\n{content}"
            
        except UnicodeDecodeError:
            return f"❌ 文件编码错误，请尝试其他编码格式"
        except Exception as e:
            return f"❌ 读取文件失败: {str(e)}"
    
    async def _write_file(self, path: str, content: str, encoding: str = 'utf-8') -> str:
        """
        写入文件内容
        
        类比pytest中写入测试结果文件
        
        Args:
            path: 文件路径
            content: 文件内容
            encoding: 文件编码
            
        Returns:
            操作结果
        """
        try:
            # 检查文件扩展名
            if not self._check_file_extension(path):
                return f"❌ 不支持的文件类型: {Path(path).suffix}"
            
            # 检查内容大小
            if len(content.encode(encoding)) > self.max_file_size:
                return f"❌ 内容过大，超过限制 ({self.max_file_size} bytes)"
            
            # 如果文件存在且启用备份，先备份
            if os.path.exists(path) and self.backup_enabled:
                backup_result = await self._backup_file(path)
                if not backup_result.startswith("✅"):
                    return f"❌ 备份失败，取消写入操作: {backup_result}"
            
            # 确保目录存在
            os.makedirs(os.path.dirname(path), exist_ok=True)
            
            with open(path, 'w', encoding=encoding) as f:
                f.write(content)
            
            return f"✅ 文件写入成功: {path} ({len(content)} 字符)"
            
        except Exception as e:
            return f"❌ 写入文件失败: {str(e)}"
    
    async def _create_file(self, path: str, content: str, encoding: str = 'utf-8') -> str:
        """
        创建新文件
        
        Args:
            path: 文件路径
            content: 文件内容
            encoding: 文件编码
            
        Returns:
            操作结果
        """
        try:
            if os.path.exists(path):
                return f"❌ 文件已存在: {path}"
            
            return await self._write_file(path, content, encoding)
            
        except Exception as e:
            return f"❌ 创建文件失败: {str(e)}"
    
    async def _delete_file(self, path: str) -> str:
        """
        删除文件
        
        Args:
            path: 文件路径
            
        Returns:
            操作结果
        """
        try:
            if not os.path.exists(path):
                return f"❌ 文件不存在: {path}"
            
            if not os.path.isfile(path):
                return f"❌ 路径不是文件: {path}"
            
            # 备份文件（如果启用）
            if self.backup_enabled:
                backup_result = await self._backup_file(path)
                if not backup_result.startswith("✅"):
                    return f"❌ 备份失败，取消删除操作: {backup_result}"
            
            os.remove(path)
            return f"✅ 文件删除成功: {path}"
            
        except Exception as e:
            return f"❌ 删除文件失败: {str(e)}"
    
    async def _list_directory(self, path: str) -> str:
        """
        列出目录内容
        
        Args:
            path: 目录路径
            
        Returns:
            目录内容列表
        """
        try:
            if not os.path.exists(path):
                return f"❌ 目录不存在: {path}"
            
            if not os.path.isdir(path):
                return f"❌ 路径不是目录: {path}"
            
            items = []
            for item in sorted(os.listdir(path)):
                item_path = os.path.join(path, item)
                if os.path.isdir(item_path):
                    items.append(f"📁 {item}/")
                else:
                    size = os.path.getsize(item_path)
                    items.append(f"📄 {item} ({size} bytes)")
            
            if not items:
                return f"📂 目录为空: {path}"
            
            return f"📂 目录内容 ({len(items)} 项):\n" + "\n".join(items)
            
        except Exception as e:
            return f"❌ 列出目录失败: {str(e)}"
    
    async def _get_file_info(self, path: str) -> str:
        """
        获取文件信息
        
        Args:
            path: 文件路径
            
        Returns:
            文件信息
        """
        try:
            if not os.path.exists(path):
                return f"❌ 文件不存在: {path}"
            
            stat = os.stat(path)
            path_obj = Path(path)
            
            info = [
                f"📄 文件信息: {path}",
                f"📏 大小: {stat.st_size} bytes",
                f"📅 修改时间: {stat.st_mtime}",
                f"🔧 扩展名: {path_obj.suffix}",
                f"📂 父目录: {path_obj.parent}",
                f"📝 类型: {'目录' if os.path.isdir(path) else '文件'}",
            ]
            
            return "\n".join(info)
            
        except Exception as e:
            return f"❌ 获取文件信息失败: {str(e)}"
    
    async def _backup_file(self, path: str) -> str:
        """
        备份文件
        
        Args:
            path: 要备份的文件路径
            
        Returns:
            备份结果
        """
        try:
            if not os.path.exists(path):
                return f"❌ 文件不存在: {path}"
            
            # 生成备份文件名
            backup_path = f"{path}.backup"
            counter = 1
            while os.path.exists(backup_path):
                backup_path = f"{path}.backup.{counter}"
                counter += 1
            
            shutil.copy2(path, backup_path)
            return f"✅ 文件备份成功: {backup_path}"
            
        except Exception as e:
            return f"❌ 备份文件失败: {str(e)}"
    
    async def _restore_file(self, path: str, backup_path: str = None) -> str:
        """
        恢复文件
        
        Args:
            path: 要恢复的文件路径
            backup_path: 备份文件路径（可选）
            
        Returns:
            恢复结果
        """
        try:
            # 如果没有指定备份路径，自动查找
            if not backup_path:
                backup_path = f"{path}.backup"
                if not os.path.exists(backup_path):
                    return f"❌ 找不到备份文件: {backup_path}"
            
            if not os.path.exists(backup_path):
                return f"❌ 备份文件不存在: {backup_path}"
            
            shutil.copy2(backup_path, path)
            return f"✅ 文件恢复成功: {path} <- {backup_path}"
            
        except Exception as e:
            return f"❌ 恢复文件失败: {str(e)}"
    
    def get_help(self) -> str:
        """
        获取工具帮助信息
        
        Returns:
            帮助信息字符串
        """
        return """
📝 文件编辑工具帮助
==================

支持的操作:
• read: 读取文件内容
• write: 写入文件内容
• create: 创建新文件
• delete: 删除文件
• list: 列出目录内容
• info: 获取文件信息
• backup: 备份文件
• restore: 恢复文件

参数说明:
• action: 操作类型 (必需)
• path: 文件/目录路径 (大部分操作需要)
• content: 文件内容 (写入/创建操作需要)
• encoding: 文件编码 (可选，默认utf-8)
• backup_path: 备份文件路径 (恢复操作可选)

使用示例:
• 读取文件: {"action": "read", "path": "test.txt"}
• 写入文件: {"action": "write", "path": "test.txt", "content": "Hello World"}
• 创建文件: {"action": "create", "path": "new.txt", "content": "New file"}
• 删除文件: {"action": "delete", "path": "old.txt"}
• 列出目录: {"action": "list", "path": "."}
• 文件信息: {"action": "info", "path": "test.txt"}

安全特性:
• 路径安全检查，防止访问系统敏感目录
• 文件大小限制 (默认1MB)
• 支持的文件类型限制
• 自动备份功能
        """
