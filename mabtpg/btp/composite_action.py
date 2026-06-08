"""
CABTP — Composite-Action Behavior Tree Planning.

Specialization of ``PlanningAgent`` that plans a *single* composite (sub-tree)
action by walking a fixed action sequence in reverse and back-chaining
preconditions one step at a time.

It is used by ``CompositeActionPlanner`` (mabtpg/utils/composite_action_tools.py)
to synthesize the BT for one named composite action such as
``GetKeyAndOpenDoor`` or ``Move0BetweenRooms``.
"""

from __future__ import annotations

import copy
from typing import List, Optional

from mabtpg.btp.base import PlanningAgent, PlanningCondition
from mabtpg.utils.tools import print_colored


class CABTP(PlanningAgent):
    """Composite-Action Behavior Tree Planner (single agent, fixed sequence)."""

    def __init__(
        self,
        action_list,
        goal,
        id=None,
        verbose: bool = False,
        env=None,
    ):
        super().__init__(action_list, goal, id=id, verbose=verbose, env=env)

        # Walk the user-supplied action sequence backward from goal -> start.
        self.action_list = copy.deepcopy(action_list)
        self.action_list.reverse()

        self.collect_explored_cond_act: List = []
        self.env = env

    def one_step_expand(self, planning_condition, next_action) -> Optional[PlanningCondition]:
        """Expand exactly one step using the prescribed ``next_action``."""
        condition = planning_condition.condition_set
        if not self.is_consequence(condition, next_action):
            return None

        premise_condition = frozenset(
            (next_action.pre | condition) - next_action.add
        )
        if not self.has_no_subset(premise_condition):
            return None
        if self.env is not None and self.env.check_conflict(premise_condition):
            return None

        new_planning_condition = PlanningCondition(premise_condition, next_action.name)
        self.expanded_condition_dict[premise_condition] = new_planning_condition
        new_planning_condition.parent_cond = planning_condition

        self.inside_expand(planning_condition, [new_planning_condition])
        return new_planning_condition

    def planning(self) -> Optional[bool]:
        """Walk ``action_list`` from goal backward; return ``True`` on success."""
        self.goal_condition = PlanningCondition(self.goal)
        cond = self.goal_condition
        for planning_action in self.action_list:
            if self.verbose:
                print_colored(
                    f"C:{cond}  Index:{planning_action.name}", "green"
                )
            cond = self.one_step_expand(cond, planning_action)
            if cond is None:
                return None
        return True
