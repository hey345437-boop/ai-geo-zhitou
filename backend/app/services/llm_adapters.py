"""
LLM Engine Adapters
Implements adapter pattern for different LLM providers
"""
from abc import ABC, abstractmethod
from typing import List, Dict, Optional
from dataclasses import dataclass
import asyncio
import logging

logger = logging.getLogger(__name__)


@dataclass
class LLMResponse:
    """Standard response format from LLM"""
    text: str
    model: str
    tokens_used: int
    cost: float
    provider: str


@dataclass
class QueryParams:
    """Query parameters for LLM"""
    temperature: float = 0.7
    max_tokens: int = 1000
    seed: Optional[int] = 42


class LLMEngineAdapter(ABC):
    """Abstract base class for LLM adapters"""
    
    def __init__(self, api_key: str):
        self.api_key = api_key
        self.provider = self.__class__.__name__.replace('Adapter', '')
    
    @abstractmethod
    async def query(self, question: str, params: QueryParams) -> LLMResponse:
        """Execute query against LLM"""
        pass
    
    def calculate_cost(self, tokens: int, model: str) -> float:
        """Calculate API cost based on tokens"""
        cost_per_1k = {
            'gpt-4o': 0.005,
            'gpt-4-turbo': 0.01,
            'gpt-4': 0.03,
            'gpt-3.5-turbo': 0.0015,
            'claude-3.5-sonnet': 0.003,
            'claude-3-opus': 0.015,
            'claude-3-sonnet': 0.003,
            'gemini-2.0-flash': 0.0001,
            'gemini-1.5-pro': 0.00125,
            'deepseek-v3': 0.00027,
            'qwen-max': 0.002,
            'qwen-plus': 0.0008,
            'doubao-pro': 0.0008,
            'glm-4-plus': 0.0005,
            'spark-4.0': 0.0005,
            'perplexity-sonar': 0.001,
        }
        return (tokens / 1000) * cost_per_1k.get(model, 0.01)


class GPT4Adapter(LLMEngineAdapter):
    """Adapter for OpenAI GPT-4o/GPT-4 Turbo"""
    
    async def query(self, question: str, params: QueryParams) -> LLMResponse:
        """Query GPT-4o"""
        try:
            logger.info(f"Querying GPT-4o: {question[:50]}...")
            await asyncio.sleep(0.5)
            response_text = f"GPT-4o response for: {question}"
            tokens = len(response_text.split()) * 2
            
            return LLMResponse(
                text=response_text,
                model="gpt-4o",
                tokens_used=tokens,
                cost=self.calculate_cost(tokens, "gpt-4o"),
                provider="OpenAI"
            )
        except Exception as e:
            logger.error(f"GPT-4o query failed: {e}")
            raise


class Claude3Adapter(LLMEngineAdapter):
    """Adapter for Anthropic Claude 3.5 Sonnet"""
    
    async def query(self, question: str, params: QueryParams) -> LLMResponse:
        """Query Claude 3.5 Sonnet"""
        try:
            logger.info(f"Querying Claude 3.5 Sonnet: {question[:50]}...")
            await asyncio.sleep(0.5)
            response_text = f"Claude 3.5 Sonnet response for: {question}"
            tokens = len(response_text.split()) * 2
            
            return LLMResponse(
                text=response_text,
                model="claude-3.5-sonnet",
                tokens_used=tokens,
                cost=self.calculate_cost(tokens, "claude-3.5-sonnet"),
                provider="Anthropic"
            )
        except Exception as e:
            logger.error(f"Claude 3.5 Sonnet query failed: {e}")
            raise


class GeminiProAdapter(LLMEngineAdapter):
    """Adapter for Google Gemini 2.0 Flash"""
    
    async def query(self, question: str, params: QueryParams) -> LLMResponse:
        """Query Gemini 2.0 Flash"""
        try:
            logger.info(f"Querying Gemini 2.0 Flash: {question[:50]}...")
            await asyncio.sleep(0.5)
            response_text = f"Gemini 2.0 Flash response for: {question}"
            tokens = len(response_text.split()) * 2
            
            return LLMResponse(
                text=response_text,
                model="gemini-2.0-flash",
                tokens_used=tokens,
                cost=self.calculate_cost(tokens, "gemini-2.0-flash"),
                provider="Google"
            )
        except Exception as e:
            logger.error(f"Gemini 2.0 Flash query failed: {e}")
            raise

    class PerplexityAdapter(LLMEngineAdapter):
        """Adapter for Perplexity AI"""

        async def query(self, question: str, params: QueryParams) -> LLMResponse:
            """Query Perplexity"""
            try:
                logger.info(f"Querying Perplexity: {question[:50]}...")
                await asyncio.sleep(0.5)
                response_text = f"Perplexity response for: {question}\n\nSources:\n[1] https://example.com/source1\n[2] https://example.com/source2"
                tokens = len(response_text.split()) * 2

                return LLMResponse(
                    text=response_text,
                    model="perplexity-online",
                    tokens_used=tokens,
                    cost=self.calculate_cost(tokens, "perplexity"),
                    provider="Perplexity"
                )
            except Exception as e:
                logger.error(f"Perplexity query failed: {e}")
                raise


    class BingChatAdapter(LLMEngineAdapter):
        """Adapter for Microsoft Bing Chat"""

        async def query(self, question: str, params: QueryParams) -> LLMResponse:
            """Query Bing Chat"""
            try:
                logger.info(f"Querying Bing Chat: {question[:50]}...")
                await asyncio.sleep(0.5)
                response_text = f"Bing Chat response for: {question} [1][2]\n\nLearn more:\n1. example.com/ref1\n2. example.com/ref2"
                tokens = len(response_text.split()) * 2

                return LLMResponse(
                    text=response_text,
                    model="bing-chat",
                    tokens_used=tokens,
                    cost=self.calculate_cost(tokens, "bing-chat"),
                    provider="Microsoft"
                )
            except Exception as e:
                logger.error(f"Bing Chat query failed: {e}")
                raise


    class YouChatAdapter(LLMEngineAdapter):
        """Adapter for You.com Chat"""

        async def query(self, question: str, params: QueryParams) -> LLMResponse:
            """Query You.com"""
            try:
                logger.info(f"Querying You.com: {question[:50]}...")
                await asyncio.sleep(0.5)
                response_text = f"You.com response for: {question}\n\nReferences:\n• https://source1.com\n• https://source2.com"
                tokens = len(response_text.split()) * 2

                return LLMResponse(
                    text=response_text,
                    model="you-chat",
                    tokens_used=tokens,
                    cost=self.calculate_cost(tokens, "you-chat"),
                    provider="You.com"
                )
            except Exception as e:
                logger.error(f"You.com query failed: {e}")
                raise


    class QwenAdapter(LLMEngineAdapter):
        """Adapter for Alibaba Qwen (通义千问)"""

        async def query(self, question: str, params: QueryParams) -> LLMResponse:
            """Query Qwen"""
            try:
                logger.info(f"Querying Qwen: {question[:50]}...")
                await asyncio.sleep(0.5)
                response_text = f"通义千问回答: {question}\n\n参考来源:\n[1] 示例来源1\n[2] 示例来源2"
                tokens = len(response_text) * 2  # Chinese characters

                return LLMResponse(
                    text=response_text,
                    model="qwen-max",
                    tokens_used=tokens,
                    cost=self.calculate_cost(tokens, "qwen"),
                    provider="Alibaba"
                )
            except Exception as e:
                logger.error(f"Qwen query failed: {e}")
                raise


    class ErnieBotAdapter(LLMEngineAdapter):
        """Adapter for Baidu Ernie Bot (文心一言)"""

        async def query(self, question: str, params: QueryParams) -> LLMResponse:
            """Query Ernie Bot"""
            try:
                logger.info(f"Querying Ernie Bot: {question[:50]}...")
                await asyncio.sleep(0.5)
                response_text = f"文心一言回答: {question}\n\n来源:\n1. 百度百科\n2. 相关网站"
                tokens = len(response_text) * 2  # Chinese characters

                return LLMResponse(
                    text=response_text,
                    model="ernie-bot-4",
                    tokens_used=tokens,
                    cost=self.calculate_cost(tokens, "ernie"),
                    provider="Baidu"
                )
            except Exception as e:
                logger.error(f"Ernie Bot query failed: {e}")
                raise


class PerplexityAdapter(LLMEngineAdapter):
    """Adapter for Perplexity AI"""
    
    async def query(self, question: str, params: QueryParams) -> LLMResponse:
        """Query Perplexity"""
        try:
            logger.info(f"Querying Perplexity: {question[:50]}...")
            await asyncio.sleep(0.5)
            response_text = f"Perplexity response for: {question}\n\nSources:\n[1] https://example.com/source1\n[2] https://example.com/source2"
            tokens = len(response_text.split()) * 2
            return LLMResponse(
                text=response_text,
                model="perplexity-online",
                tokens_used=tokens,
                cost=self.calculate_cost(tokens, "perplexity"),
                provider="Perplexity"
            )
        except Exception as e:
            logger.error(f"Perplexity query failed: {e}")
            raise


class BingChatAdapter(LLMEngineAdapter):
    """Adapter for Microsoft Bing Chat"""
    
    async def query(self, question: str, params: QueryParams) -> LLMResponse:
        """Query Bing Chat"""
        try:
            logger.info(f"Querying Bing Chat: {question[:50]}...")
            await asyncio.sleep(0.5)
            response_text = f"Bing Chat response for: {question} [1][2]\n\nLearn more:\n1. example.com/ref1\n2. example.com/ref2"
            tokens = len(response_text.split()) * 2
            return LLMResponse(
                text=response_text,
                model="bing-chat",
                tokens_used=tokens,
                cost=self.calculate_cost(tokens, "bing-chat"),
                provider="Microsoft"
            )
        except Exception as e:
            logger.error(f"Bing Chat query failed: {e}")
            raise


class YouChatAdapter(LLMEngineAdapter):
    """Adapter for You.com Chat"""
    
    async def query(self, question: str, params: QueryParams) -> LLMResponse:
        """Query You.com"""
        try:
            logger.info(f"Querying You.com: {question[:50]}...")
            await asyncio.sleep(0.5)
            response_text = f"You.com response for: {question}\n\nReferences:\n• https://source1.com\n• https://source2.com"
            tokens = len(response_text.split()) * 2
            return LLMResponse(
                text=response_text,
                model="you-chat",
                tokens_used=tokens,
                cost=self.calculate_cost(tokens, "you-chat"),
                provider="You.com"
            )
        except Exception as e:
            logger.error(f"You.com query failed: {e}")
            raise


class QwenAdapter(LLMEngineAdapter):
    """Adapter for Alibaba Qwen (通义千问)"""
    
    async def query(self, question: str, params: QueryParams) -> LLMResponse:
        """Query Qwen"""
        try:
            logger.info(f"Querying Qwen: {question[:50]}...")
            await asyncio.sleep(0.5)
            response_text = f"通义千问回答: {question}\n\n参考来源:\n[1] 示例来源1\n[2] 示例来源2"
            tokens = len(response_text) * 2
            return LLMResponse(
                text=response_text,
                model="qwen-max",
                tokens_used=tokens,
                cost=self.calculate_cost(tokens, "qwen"),
                provider="Alibaba"
            )
        except Exception as e:
            logger.error(f"Qwen query failed: {e}")
            raise


class ErnieBotAdapter(LLMEngineAdapter):
    """Adapter for Baidu Ernie Bot (文心一言)"""
    
    async def query(self, question: str, params: QueryParams) -> LLMResponse:
        """Query Ernie Bot"""
        try:
            logger.info(f"Querying Ernie Bot: {question[:50]}...")
            await asyncio.sleep(0.5)
            response_text = f"文心一言回答: {question}\n\n来源:\n1. 百度百科\n2. 相关网站"
            tokens = len(response_text) * 2
            return LLMResponse(
                text=response_text,
                model="ernie-bot-4",
                tokens_used=tokens,
                cost=self.calculate_cost(tokens, "ernie"),
                provider="Baidu"
            )
        except Exception as e:
            logger.error(f"Ernie Bot query failed: {e}")
            raise


class LLMAdapterFactory:
    """Factory for creating LLM adapters"""
    
    _adapters = {
        'gpt-4o': GPT4Adapter,
        'gpt-4': GPT4Adapter,
        'claude-3.5-sonnet': Claude3Adapter,
        'claude-3': Claude3Adapter,
        'gemini-2.0-flash': GeminiProAdapter,
        'gemini-pro': GeminiProAdapter,
        'perplexity': PerplexityAdapter,
        'bing-chat': BingChatAdapter,
        'you-chat': YouChatAdapter,
        'qwen': QwenAdapter,
        'ernie-bot': ErnieBotAdapter,
    }
    
    @classmethod
    def create(cls, engine: str, api_key: str) -> LLMEngineAdapter:
        """Create adapter for specified engine"""
        adapter_class = cls._adapters.get(engine)
        if not adapter_class:
            raise ValueError(f"Unknown LLM engine: {engine}")
        return adapter_class(api_key)
    
    @classmethod
    def get_available_engines(cls) -> List[str]:
        """Get list of available engines"""
        return list(cls._adapters.keys())
