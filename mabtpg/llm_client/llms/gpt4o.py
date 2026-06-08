"""GPT-4o client."""

from mabtpg.llm_client.base import BaseLLMClient


class LLMGPT4o(BaseLLMClient):
    DEFAULT_MODEL = "gpt-4o-2024-08-06"
