"""
LLM客户端模块
=============

提供与大语言模型交互的客户端，支持多种API提供商。
类比pytest的测试运行器，负责执行核心逻辑。

设计理念：
1. 统一接口，支持多种LLM提供商
2. 异步支持，提高性能
3. 错误处理和重试机制
4. Mock模式，便于测试和演示
"""

import asyncio
from typing import Dict, Any
from abc import ABC, abstractmethod


class BaseLLMClient(ABC):
    """
    LLM客户端基类
    
    类比pytest的测试运行器基类，定义统一接口
    """
    
    def __init__(self, config: Dict[str, Any]):
        self.config = config
        self.model = config.get('model', 'unknown')
        self.api_key = config.get('api_key', '')
        self.base_url = config.get('base_url', '')
        self.max_tokens = config.get('max_tokens', 1000)
        self.temperature = config.get('temperature', 0.7)
    
    @abstractmethod
    async def generate(self, system_prompt: str, user_prompt: str) -> str:
        """
        生成文本响应
        
        Args:
            system_prompt: 系统提示词
            user_prompt: 用户提示词
            
        Returns:
            生成的文本
        """
        pass


# Mock 客户端已移除，现在只使用真实的 LLM API


class OpenAIClient(BaseLLMClient):
    """
    OpenAI API客户端
    
    真实的OpenAI API调用实现 (需要安装openai库)
    """
    
    def __init__(self, config: Dict[str, Any]):
        super().__init__(config)
        try:
            import openai
            self.client = openai.AsyncOpenAI(
                api_key=self.api_key,
                base_url=self.base_url
            )
        except ImportError:
            raise ImportError("需要安装openai库: pip install openai")
    
    async def generate(self, system_prompt: str, user_prompt: str) -> str:
        """使用OpenAI API生成响应"""
        try:
            response = await self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt}
                ],
                max_tokens=self.max_tokens,
                temperature=self.temperature
            )
            return response.choices[0].message.content
        except Exception as e:
            raise RuntimeError(f"OpenAI API调用失败: {str(e)}")


class AnthropicClient(BaseLLMClient):
    """
    Anthropic Claude API客户端
    
    真实的Claude API调用实现 (需要安装anthropic库)
    """
    
    def __init__(self, config: Dict[str, Any]):
        super().__init__(config)
        try:
            import anthropic
            self.client = anthropic.AsyncAnthropic(
                api_key=self.api_key,
                base_url=self.base_url
            )
        except ImportError:
            raise ImportError("需要安装anthropic库: pip install anthropic")
    
    async def generate(self, system_prompt: str, user_prompt: str) -> str:
        """使用Anthropic API生成响应"""
        try:
            response = await self.client.messages.create(
                model=self.model,
                system=system_prompt,
                messages=[{"role": "user", "content": user_prompt}],
                max_tokens=self.max_tokens,
                temperature=self.temperature
            )
            return response.content[0].text
        except Exception as e:
            raise RuntimeError(f"Anthropic API调用失败: {str(e)}")


class LLMClient:
    """
    LLM客户端工厂类
    
    根据配置自动选择合适的LLM客户端
    类比pytest的插件加载机制
    """
    
    def __init__(self, config: Dict[str, Any]):
        self.config = config
        self.client = self._create_client()
    
    def _create_client(self) -> BaseLLMClient:
        """
        根据配置创建LLM客户端

        Returns:
            LLM客户端实例
        """
        model = self.config.get('model', '').lower()
        api_type = self.config.get('api_type', '').lower()
        base_url = self.config.get('base_url', '').lower()

        # 根据模型名称、API类型或base_url选择客户端
        if 'claude' in model or 'anthropic' in api_type:
            print(f"🔧 使用 Anthropic 客户端，模型: {self.config.get('model')}")
            return AnthropicClient(self.config)
        else:
            # 默认使用 OpenAI 兼容客户端 (支持 OpenAI, Qwen, GLM, 硅基流动等)
            print(f"🔧 使用 OpenAI 兼容客户端，模型: {self.config.get('model')}")
            return OpenAIClient(self.config)
    
    async def generate(self, system_prompt: str, user_prompt: str) -> str:
        """
        生成文本响应
        
        Args:
            system_prompt: 系统提示词
            user_prompt: 用户提示词
            
        Returns:
            生成的文本
        """
        return await self.client.generate(system_prompt, user_prompt)
    
    def get_model_info(self) -> Dict[str, Any]:
        """
        获取模型信息
        
        Returns:
            模型信息字典
        """
        return {
            'model': self.client.model,
            'type': self.client.__class__.__name__,
            'max_tokens': self.client.max_tokens,
            'temperature': self.client.temperature
        }


# 便捷函数
async def create_llm_client(config: Dict[str, Any]) -> LLMClient:
    """
    创建LLM客户端的便捷函数
    
    Args:
        config: 配置字典
        
    Returns:
        LLM客户端实例
    """
    return LLMClient(config)


# 测试函数
if __name__ == "__main__":
    async def test_llm_clients():
        """测试LLM客户端配置"""
        from config import load_config

        print("🧪 测试LLM客户端配置:")
        print("-" * 30)

        config = load_config()
        client = LLMClient(config)

        print(f"📊 模型信息: {client.get_model_info()}")
        print("\n✅ 配置测试完成")
        print("💡 要测试实际API调用，请确保配置了有效的API密钥")

    asyncio.run(test_llm_clients())