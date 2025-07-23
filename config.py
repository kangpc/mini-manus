"""
配置管理模块
============

负责加载和管理系统配置，类比pytest的配置系统：
- pytest.ini -> config.json
- conftest.py -> 这个模块

设计理念：
1. 配置与代码分离
2. 支持多种配置源
3. 提供合理的默认值
4. 配置验证和错误处理
"""

import json
import os
from typing import Dict, Any, Optional
from pathlib import Path

# 尝试导入 python-dotenv，如果没有安装则提供降级方案
try:
    from dotenv import load_dotenv
    DOTENV_AVAILABLE = True
except ImportError:
    DOTENV_AVAILABLE = False
    print("⚠️  python-dotenv 未安装，将跳过 .env 文件加载")
    print("💡 安装方法: pip install python-dotenv")


def load_config(config_path: Optional[str] = None) -> Dict[str, Any]:
    """
    加载配置文件

    Args:
        config_path: 配置文件路径，如果为None则使用默认路径

    Returns:
        配置字典

    类比pytest的配置加载：
    - pytest会依次查找 pytest.ini, pyproject.toml, setup.cfg
    - 我们依次查找 .env, config.json, 环境变量, 默认配置
    """

    # 0. 首先加载 .env 文件 (如果存在)
    load_dotenv_file()

    # 1. 确定配置文件路径 (类比pytest查找配置文件)
    if config_path is None:
        # 查找顺序：当前目录 -> 用户目录 -> 默认配置
        possible_paths = [
            "config.json",
            "mini-manus/config.json",
            os.path.expanduser("~/.mini-manus.json")
        ]

        config_path = None
        for path in possible_paths:
            if os.path.exists(path):
                config_path = path
                break

    # 2. 加载配置 (优先级：.env > 文件 > 环境变量 > 默认值)
    config = get_default_config()

    # 从文件加载
    if config_path and os.path.exists(config_path):
        try:
            with open(config_path, 'r', encoding='utf-8') as f:
                file_config = json.load(f)
                config.update(file_config)
                print(f"📁 从文件加载配置: {config_path}")
        except Exception as e:
            print(f"⚠️  配置文件读取失败: {e}")

    # 从环境变量加载 (类比pytest的环境变量支持)
    env_config = load_from_env()
    config.update(env_config)

    # 3. 验证配置
    validate_config(config)

    return config


def get_default_config() -> Dict[str, Any]:
    """
    获取默认配置

    类比pytest的默认配置，提供合理的默认值
    注意：现在需要真实的API配置才能运行
    """
    return {
        # LLM配置 (类比pytest的测试发现配置)
        "model": "gpt-3.5-turbo",  # 默认使用 GPT-3.5
        "api_key": "",  # 需要用户提供真实的API密钥
        "base_url": "https://api.openai.com/v1",
        "max_tokens": 1000,
        "temperature": 0.7,

        # 智能体配置 (类比pytest的执行配置)
        "agent": {
            "name": "MiniManus",
            "max_steps": 10,
            "timeout": 30
        },

        # 工具配置 (类比pytest的插件配置)
        "tools": {
            "python_execute": {"enabled": True, "timeout": 10},
            "file_editor": {"enabled": True, "max_file_size": 1024*1024},
            "calculator": {"enabled": True},
            "database": {"enabled": True, "max_rows": 100, "query_timeout": 30},
            "web_search": {"enabled": False}  # 默认关闭需要网络的工具
        },

        # 日志配置 (类比pytest的日志配置)
        "logging": {
            "level": "INFO",
            "format": "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
        }
    }


def load_dotenv_file() -> None:
    """
    加载 .env 文件到环境变量

    查找顺序：
    1. 当前目录的 .env
    2. mini-manus 目录的 .env
    """
    if not DOTENV_AVAILABLE:
        return

    # 可能的 .env 文件位置
    possible_env_files = [
        ".env",
        "mini-manus/.env",
        os.path.join(os.path.dirname(__file__), ".env")
    ]

    for env_file in possible_env_files:
        if os.path.exists(env_file):
            load_dotenv(env_file)
            print(f"🔧 从 .env 文件加载配置: {env_file}")
            break


def load_from_env() -> Dict[str, Any]:
    """
    从环境变量加载配置

    支持的环境变量：
    - MODEL: 模型名称
    - API_KEY: API密钥
    - BASE_URL: API基础URL
    - 以及带前缀的版本: mini-manus_MODEL 等

    类比pytest支持 PYTEST_CURRENT_TEST 等环境变量
    """
    env_config = {}

    # 映射环境变量到配置键 (支持直接变量名和带前缀的变量名)
    env_mappings = {
        # 直接变量名 (优先级更高，来自 .env 文件)
        "MODEL": "model",
        "API_KEY": "api_key",
        "BASE_URL": "base_url",
        "MAX_TOKENS": "max_tokens",
        "TEMPERATURE": "temperature",
        # 带前缀的变量名 (向后兼容)
        "mini-manus_MODEL": "model",
        "mini-manus_API_KEY": "api_key",
        "mini-manus_BASE_URL": "base_url",
        "mini-manus_MAX_TOKENS": "max_tokens",
        "mini-manus_TEMPERATURE": "temperature"
    }

    for env_key, config_key in env_mappings.items():
        env_value = os.getenv(env_key)
        if env_value:
            # 类型转换
            if config_key in ["max_tokens"]:
                try:
                    env_config[config_key] = int(env_value)
                except ValueError:
                    print(f"⚠️  {env_key} 值无效，跳过: {env_value}")
                    continue
            elif config_key in ["temperature"]:
                try:
                    env_config[config_key] = float(env_value)
                except ValueError:
                    print(f"⚠️  {env_key} 值无效，跳过: {env_value}")
                    continue
            else:
                env_config[config_key] = env_value

            print(f"🌍 从环境变量加载: {config_key} = {env_value}")

    return env_config


def validate_config(config: Dict[str, Any]) -> None:
    """
    验证配置的有效性

    类比pytest的配置验证，确保配置项符合要求
    避免运行时错误
    """

    # 必需的配置项
    required_keys = ["model", "api_key"]
    for key in required_keys:
        if key not in config:
            raise ValueError(f"缺少必需的配置项: {key}")

    # 验证API密钥不能为空
    api_key = config.get("api_key", "")
    if not api_key or api_key.strip() == "":
        raise ValueError("API密钥不能为空，请在 .env 文件中设置 API_KEY")

    # 验证模型名称不能为空
    model = config.get("model", "")
    if not model or model.strip() == "":
        raise ValueError("模型名称不能为空，请在 .env 文件中设置 MODEL")

    # 数值范围验证
    if "max_tokens" in config:
        max_tokens = config["max_tokens"]
        if not isinstance(max_tokens, int) or max_tokens <= 0:
            raise ValueError(f"max_tokens 必须是正整数，当前值: {max_tokens}")

    if "temperature" in config:
        temperature = config["temperature"]
        if not isinstance(temperature, (int, float)) or not 0 <= temperature <= 2:
            raise ValueError(f"temperature 必须在0-2之间，当前值: {temperature}")

    print("✅ 配置验证通过")


def save_config(config: Dict[str, Any], config_path: str = "config.json") -> None:
    """
    保存配置到文件
    
    Args:
        config: 配置字典
        config_path: 保存路径
    """
    try:
        # 确保目录存在
        os.makedirs(os.path.dirname(config_path) if os.path.dirname(config_path) else ".", exist_ok=True)
        
        with open(config_path, 'w', encoding='utf-8') as f:
            json.dump(config, f, indent=2, ensure_ascii=False)
        
        print(f"💾 配置已保存到: {config_path}")
    except Exception as e:
        print(f"❌ 配置保存失败: {e}")


# 示例配置文件生成
if __name__ == "__main__":
    """
    运行此模块可以生成示例配置文件
    类比 pytest --generate-config
    """
    print("🔧 生成示例配置文件...")
    
    example_config = get_default_config()
    example_config.update({
        "model": "gpt-3.5-turbo",
        "api_key": "your-api-key-here",
        "base_url": "https://api.openai.com/v1"
    })
    
    save_config(example_config, "config.example.json")
    print("✅ 示例配置文件已生成: config.example.json")
    print("📝 请复制为 config.json 并填入真实的API密钥")