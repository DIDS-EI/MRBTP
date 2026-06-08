"""
MAOBTP — Multi-Robot Optimal Behavior Tree Planning.

Same back-chaining structure as ``MABTP`` but the search frontier is a
priority queue ordered by accumulated action cost, which lets the planner
prefer cheaper plans and integrates *composite* (sub-tree) actions whose
cost is recorded as 0.

The companion class ``CostAwarePlanningAgent`` is a drop-in replacement for
``PlanningAgent`` that propagates the action cost and tags premises with
composite-action metadata.
"""

from __future__ import annotations

import functools
import heapq
import time
from typing import List, Optional

from mabtpg.btp.base.planning_agent import PlanningAgent
from mabtpg.btp.base.planning_condition import PlanningCondition
from mabtpg.btp.multi_robot_basic import MABTP
from mabtpg.utils.tools import print_colored


@functools.total_ordering
class CondCostPair:
    """A (condition, cumulative-cost) pair ordered by cost (heap entry)."""

    __slots__ = ("cond", "cost")

    def __init__(self, cond, cost):
        self.cond = cond
        self.cost = cost

    def __eq__(self, other):
        return isinstance(other, CondCostPair) and self.cost == other.cost

    def __lt__(self, other):
        return self.cost < other.cost


class CostAwarePlanningAgent(PlanningAgent):
    """``PlanningAgent`` variant that tracks per-action cost and composite-action metadata."""

    def one_step_expand(self, condition_cost: CondCostPair) -> List[CondCostPair]:
        condition, cost = condition_cost.cond, condition_cost.cost

        # Decide tree-internal vs tree-external expansion *before* expanding.
        inside_condition = self.expanded_condition_dict.get(condition, None)

        premise_condition_list: List[PlanningCondition] = []
        premise_condition_cost_list: List[CondCostPair] = []
        for action in self.action_list:
            if not self.is_consequence(condition, action):
                continue
            premise_condition = frozenset((action.pre | condition) - action.add)
            if not self.has_no_subset(premise_condition):
                continue

            if self.env is not None and self.env.check_conflict(premise_condition):
                continue

            composition_action_flag = action.cost == 0
            sub_goal = frozenset(condition & frozenset(action.add))
            sub_del = action.del_set

            planning_condition = PlanningCondition(
                premise_condition,
                action.name,
                composition_action_flag,
                sub_goal,
                sub_del,
            )
            premise_condition_list.append(planning_condition)
            self.expanded_condition_dict[premise_condition] = planning_condition

            new_cost = cost + action.cost
            premise_condition_cost_list.append(
                CondCostPair(premise_condition, new_cost)
            )

            if self.verbose:
                print_colored("inside" if inside_condition else "outside", "purple")
                print_colored(
                    f"a:{action.name} \t c_attr:{premise_condition}", "orange"
                )

        if inside_condition:
            self.inside_expand(inside_condition, premise_condition_list)
        elif premise_condition_list:
            self.outside_expand(condition, premise_condition_list)

        return premise_condition_cost_list


# Backward-compatible alias (older scripts import ``BfsPlanningAgent``).
BfsPlanningAgent = CostAwarePlanningAgent


class MAOBTP(MABTP):
    """Cost-aware multi-robot behavior-tree planner with composite actions."""

    def bfs_planning(self, goal, action_lists) -> None:
        """Best-first multi-robot back-chaining search ordered by accumulated cost."""
        start_time = time.time()

        planning_agent_list = [
            CostAwarePlanningAgent(
                action_list, goal, id=i, verbose=self.verbose, env=self.env
            )
            for i, action_list in enumerate(action_lists)
        ]

        frontier: List[CondCostPair] = []
        heapq.heappush(frontier, CondCostPair(goal, 0))

        while frontier:
            self.record_expanded_num += 1

            condition_cost = heapq.heappop(frontier)
            condition = condition_cost.cond

            if self.verbose:
                print_colored(f"C:{condition}", "green")
            for agent in planning_agent_list:
                if self.verbose:
                    print_colored(f"Agent:{agent.id}", "purple")
                premise_condition_cost_list = agent.one_step_expand(condition_cost)
                for cond_cost in premise_condition_cost_list:
                    heapq.heappush(frontier, cond_cost)

            if self.start is not None and self.start >= condition:
                break
            if time.time() - start_time > self.max_time_limit:
                self.expanded_time = time.time() - start_time
                break

        self.planned_agent_list = planning_agent_list
