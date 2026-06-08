"""
MABTP — Multi-Robot Behavior Tree Planning.

Drives a back-chaining search across multiple per-agent ``PlanningAgent``s
to produce one cooperating behavior tree per agent.

The search is a queue-based traversal of premise conditions; each popped
condition is expanded by every agent in turn. Termination conditions:
    - the queue is empty,
    - ``self.start`` (initial state) already satisfies the current
      condition (i.e. the plan is grounded), or
    - the wall-clock time exceeds ``max_time_limit`` seconds.
"""

from __future__ import annotations

import time
from typing import List, Optional

from mabtpg.btp.base.planning_agent import PlanningAgent
from mabtpg.utils.tools import print_colored


class MABTP:
    """Multi-Robot Behavior Tree Planner."""

    def __init__(
        self,
        verbose: bool = False,
        start=None,
        env=None,
        max_time_limit: float = 20.0,
    ):
        self.verbose = verbose
        self.start = start
        self.env = env
        self.max_time_limit = max_time_limit

        self.planned_agent_list: Optional[List[PlanningAgent]] = None
        self.record_expanded_num: int = 0
        self.expanded_time: float = 0.0

    # ------------------------------------------------------------------ #
    # Search
    # ------------------------------------------------------------------ #

    def planning(self, goal, action_lists) -> None:
        """Run the multi-robot back-chaining search to populate every agent's plan."""
        start_time = time.time()

        planning_agent_list = [
            PlanningAgent(action_list, goal, id=i, verbose=self.verbose, env=self.env)
            for i, action_list in enumerate(action_lists)
        ]

        explored_condition_list = [goal]
        while explored_condition_list:
            self.record_expanded_num += 1

            condition = explored_condition_list.pop(0)
            if self.verbose:
                print_colored(f"C:{condition}", "green")

            for agent in planning_agent_list:
                if self.verbose:
                    print_colored(f"Agent:{agent.id}", "purple")
                premise_condition_list = agent.one_step_expand(condition)
                explored_condition_list += [
                    pc.condition_set for pc in premise_condition_list
                ]

            if self.start is not None and self.start >= condition:
                break
            if time.time() - start_time > self.max_time_limit:
                self.expanded_time = time.time() - start_time
                break

        self.planned_agent_list = planning_agent_list

    # ------------------------------------------------------------------ #
    # Behavior-tree extraction (uses each agent's own conversion methods)
    # ------------------------------------------------------------------ #

    def _require_planned(self) -> List[PlanningAgent]:
        if self.planned_agent_list is None:
            raise RuntimeError(
                "planning() must be called before output_*() / get_btml_list()."
            )
        return self.planned_agent_list

    def output_bt_list(self, behavior_libs):
        """Return a list of ``BehaviorTree`` objects, one per agent."""
        return [
            agent.output_bt(behavior_libs[i])
            for i, agent in enumerate(self._require_planned())
        ]

    def output_pruned_bt_list(self, behavior_libs):
        """Return per-agent BTs with composite-action branches pruned."""
        return [
            agent.output_pruned_bt(behavior_libs[i])
            for i, agent in enumerate(self._require_planned())
        ]

    def get_btml_list(self):
        """Return a list of ``BTML`` objects, one per agent (rebuilds them)."""
        btml_list = []
        for agent in self._require_planned():
            agent.create_btml()
            btml_list.append(agent.btml)
        return btml_list
