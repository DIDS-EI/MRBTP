"""GPT-4o-mini client (kept under the ``gpt4`` name for backward compat)."""

from mabtpg.llm_client.base import BaseLLMClient


class LLMGPT4(BaseLLMClient):
    DEFAULT_MODEL = "gpt-4o-mini-2024-07-18"
