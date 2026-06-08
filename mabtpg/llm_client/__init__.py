"""LLM client module for MABTPG.

Provides a thin OpenAI-compatible wrapper (``BaseLLMClient``) and the
concrete model clients used by the experiments (``LLMGPT3``, ``LLMGPT4``,
``LLMGPT4o``).  Pydantic schemas for structured tool-calling outputs live
under :mod:`mabtpg.llm_client.schemas`.
"""

from mabtpg.llm_client.base import BaseLLMClient
from mabtpg.llm_client.llms import LLMGPT3, LLMGPT4, LLMGPT4o
from mabtpg.llm_client.schemas import Action, AgentSubtreeList, Query

__all__ = [
    "BaseLLMClient",
    "LLMGPT3",
    "LLMGPT4",
    "LLMGPT4o",
    "Action",
    "AgentSubtreeList",
    "Query",
]
