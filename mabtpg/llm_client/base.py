"""Base LLM client wrapping the OpenAI-compatible chat-completions API.

All concrete clients (``LLMGPT3``, ``LLMGPT4``, ``LLMGPT4o``, …) only need to
override class attributes such as ``DEFAULT_MODEL``.  Shared behaviour
(``request``, ``tool_request``, ``embedding`` …) lives in this base class so
the subclasses stay tiny and free of duplication.

Credentials/base URL are resolved with the following precedence:

1. arguments passed to ``__init__``
2. environment variables ``OPENAI_BASE_URL`` / ``OPENAI_API_KEY``
3. the placeholder values ``"YOUR_URL"`` / ``"YOUR_KEY"`` (which makes the
   missing-config error obvious when a user forgets to configure anything).
"""

from __future__ import annotations

import os
from typing import Any, Iterable, List

from openai import OpenAI


class BaseLLMClient:
    """Minimal OpenAI-compatible LLM client used across MABTPG."""

    #: Default chat-completion model used by ``request`` / ``tool_request``.
    DEFAULT_MODEL: str = "gpt-3.5-turbo"

    #: Default embedding model used by ``embedding``.
    EMBEDDING_MODEL: str = "text-embedding-3-small"

    def __init__(
        self,
        model: str | None = None,
        base_url: str | None = None,
        api_key: str | None = None,
    ) -> None:
        self.model = model or self.DEFAULT_MODEL
        self.client = OpenAI(
            base_url=base_url or os.getenv("OPENAI_BASE_URL", "YOUR_URL"),
            api_key=api_key or os.getenv("OPENAI_API_KEY", "YOUR_KEY"),
        )

    # ------------------------------------------------------------------ #
    # Chat completion
    # ------------------------------------------------------------------ #
    def request(self, messages: Iterable[dict]) -> str:
        """Plain chat completion. Returns ``message.content``."""
        completion = self.client.chat.completions.create(
            model=self.model,
            messages=list(messages),
        )
        return completion.choices[0].message.content

    def tool_request(self, messages: Iterable[dict], tools: list) -> str:
        """Structured-output request via OpenAI tool calling.

        Returns the JSON arguments string of the first tool call.  Callers
        usually do ``eval(result)`` / ``json.loads(result)`` on it.
        """
        completion = self.client.chat.completions.create(
            model=self.model,
            messages=list(messages),
            tools=tools,
        )
        return completion.choices[0].message.tool_calls[0].function.arguments

    # ------------------------------------------------------------------ #
    # Embeddings
    # ------------------------------------------------------------------ #
    def embedding(self, text: str | list[str]):
        return self.client.embeddings.create(
            model=self.EMBEDDING_MODEL,
            input=text,
        )

    # ------------------------------------------------------------------ #
    # Introspection helpers
    # ------------------------------------------------------------------ #
    def list_models(self) -> List[Any]:
        return self.client.models.list().data

    def list_embedding_models(self) -> List[str]:
        return [m.id for m in self.list_models() if "embedding" in m.id]
