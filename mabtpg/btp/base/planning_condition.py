"""
PlanningCondition
-----------------

A node in the planning back-chaining graph maintained by ``PlanningAgent``.

Each ``PlanningCondition`` represents one *state precondition* that the agent
has discovered while expanding the goal backward through its action set.
The graph it lives in is later turned into a behavior tree by
``PlanningAgent.create_anytree``.
"""

from __future__ import annotations
from typing import FrozenSet, List, Optional


class PlanningCondition:
    """A precondition node in a back-chaining planning graph.

    Attributes:
        condition_set: Frozen set of literal strings that must hold.
        action: Name of the action that produces ``condition_set`` as
            premise (or ``None`` for the goal node).
        children: Child ``PlanningCondition`` nodes expanded from this one.
        composition_action_flag: ``True`` if ``action`` is a composite
            (sub-tree) action — used by ``CABTP`` / ``MAOBTP``.
        sub_goal: Sub-goal frozen set associated with a composite action.
        sub_del: Delete-set associated with a composite action.
        parent_cond: Optional parent in a sequential expansion (used by
            ``CABTP`` to recover the action chain).
        parent_node: Reserved for back-references when building behavior
            trees (set externally by ``PlanningAgent.create_anytree``).
    """

    def __init__(
        self,
        condition: FrozenSet[str],
        action: Optional[str] = None,
        composition_action_flag: bool = False,
        sub_goal: Optional[FrozenSet[str]] = None,
        sub_del: Optional[FrozenSet[str]] = None,
    ):
        self.condition_set: FrozenSet[str] = condition
        self.action: Optional[str] = action
        self.children: List["PlanningCondition"] = []

        # Composite-action metadata (CABTP / MAOBTP only).
        self.composition_action_flag: bool = composition_action_flag
        self.sub_goal: Optional[FrozenSet[str]] = sub_goal
        self.sub_del: Optional[FrozenSet[str]] = sub_del

        # Back-references filled in during behavior-tree generation.
        self.parent_cond: Optional["PlanningCondition"] = None
        self.parent_node = None

    def __repr__(self) -> str:  # pragma: no cover - debug helper
        return (
            f"PlanningCondition(action={self.action!r}, "
            f"|conds|={len(self.condition_set)}, "
            f"|children|={len(self.children)})"
        )
