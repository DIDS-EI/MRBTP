"""Pydantic schemas used as OpenAI structured-output tools.

These are convenience defaults — callers typically build their own
``Action`` enum dynamically (with the task-specific action names) and
re-use ``AgentSubtreeList`` / ``Query`` as they are.
"""

from __future__ import annotations

from enum import Enum

from pydantic import BaseModel


class Action(str, Enum):
    """Stub action enum.

    The default enum is intentionally empty; concrete callers usually
    rebuild this enum at runtime with the names of the actions allowed
    in the current task and pass it through the ``tools`` argument.
    """

    actions_name_str_ls = []


class AgentSubtreeList(BaseModel):
    """``subtree_dict`` contains multiple combined-action pairs.

    Each entry maps a composite-action name to the ordered list of
    atomic actions that compose it (typically 2-4 entries).
    """

    subtree_dict: dict[str, list[Action]]


class Query(BaseModel):
    """Top-level structured response.

    ``multi_subtree_list`` has ``n`` dicts, where ``n`` is the number of
    agents (i.e. the number of action lists in ``action_space``).
    """

    multi_subtree_list: list[AgentSubtreeList]
