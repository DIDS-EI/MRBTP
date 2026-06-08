"""
PlanningAgent
-------------

Single-agent backward-chaining behavior-tree planner.

Given a goal condition and an action library, it expands the goal through
the actions whose effects (``add``) intersect the goal, building a graph of
``PlanningCondition`` nodes. The graph is then converted to a behavior
tree via ``create_anytree`` -> ``create_btml`` -> ``output_bt``.

Subclasses (e.g. ``CABTP``, ``BfsPlanningAgent``) reuse the same expansion
primitives but specialize the search loop.
"""

from __future__ import annotations

import re
from typing import List, Optional

from mabtpg.behavior_tree.behavior_tree import BehaviorTree
from mabtpg.behavior_tree.btml.BTML import BTML
from mabtpg.behavior_tree.constants import NODE_TYPE
from mabtpg.btp.base.planning_condition import PlanningCondition
from mabtpg.utils import parse_predicate_logic
from mabtpg.utils.any_tree_node import AnyTreeNode
from mabtpg.utils.tools import print_colored


# Regex patterns used by ``check_conflict`` to detect mutually-exclusive
# literals such as IsNear(a,x) & IsNear(a,y) or IsOpen(o) & IsClose(o).
_RE_NEAR = re.compile(r"IsNear\(([^)]+)\)")
_RE_HOLDING = re.compile(r"IsHolding\(([^)]+)\)")
_RE_HAND_EMPTY = re.compile(r"IsHandEmpty\(([^)]+)\)")
_RE_IN_ROOM = re.compile(r"IsInRoom\(([^,]+),(\d+)\)")
_RE_OPEN = re.compile(r"IsOpen\(([^)]+)\)")
_RE_CLOSE = re.compile(r"IsClose\(([^)]+)\)")


class PlanningAgent:
    """Backward-chaining planner producing a behavior tree for one agent."""

    def __init__(
        self,
        action_list,
        goal,
        id: Optional[int] = None,
        verbose: bool = False,
        env=None,
    ):
        self.id = id
        self.action_list = action_list
        self.goal = goal
        self.goal_condition = PlanningCondition(goal)
        self.expanded_condition_dict = {goal: self.goal_condition}

        self.verbose = verbose
        self.env = env

        # Filled in during behavior-tree generation.
        self.anytree_root: Optional[AnyTreeNode] = None
        self.btml: Optional[BTML] = None

    # ------------------------------------------------------------------ #
    # Expansion primitives
    # ------------------------------------------------------------------ #

    def one_step_expand(self, condition) -> List[PlanningCondition]:
        """Expand a single condition and attach the new premises to the graph."""
        # Decide tree-internal vs tree-external expansion *before* expanding.
        inside_condition = self.expanded_condition_dict.get(condition, None)

        premise_condition_list: List[PlanningCondition] = []
        for action in self.action_list:
            if not self.is_consequence(condition, action):
                continue
            premise_condition = frozenset((action.pre | condition) - action.add)
            if not self.has_no_subset(premise_condition):
                continue

            # Skip premises that violate environment-level conflicts.
            if self.env is not None and self.env.check_conflict(premise_condition):
                continue

            planning_condition = PlanningCondition(premise_condition, action.name)
            premise_condition_list.append(planning_condition)
            self.expanded_condition_dict[premise_condition] = planning_condition

            if self.verbose:
                print_colored("inside" if inside_condition else "outside", "purple")
                print_colored(
                    f"a:{action.name} \t c_attr:{premise_condition}", "orange"
                )

        # Insert premise conditions into the back-chaining tree.
        if inside_condition:
            self.inside_expand(inside_condition, premise_condition_list)
        elif premise_condition_list:
            self.outside_expand(condition, premise_condition_list)

        return premise_condition_list

    def is_consequence(self, condition, action) -> bool:
        """Return ``True`` if ``action`` can produce ``condition`` as effect."""
        if condition & ((action.pre | action.add) - action.del_set) <= set():
            return False
        if (condition - action.del_set) != condition:
            return False
        return True

    def has_no_subset(self, condition) -> bool:
        """Return ``True`` iff no already-expanded condition is a subset of ``condition``."""
        for expanded_condition in self.expanded_condition_dict:
            if expanded_condition <= condition:
                return False
        return True

    def inside_expand(self, inside_condition, premise_condition_list):
        """Append premises as children of an already-expanded condition."""
        inside_condition.children += premise_condition_list

    def outside_expand(self, condition, premise_condition_list):
        """Attach a new precondition node under the goal root."""
        planning_condition = PlanningCondition(condition)
        planning_condition.children += premise_condition_list
        self.goal_condition.children.append(planning_condition)

    # ------------------------------------------------------------------ #
    # Conflict detection (used by environments that don't expose a
    # native ``check_conflict`` — kept here for backward compatibility).
    # ------------------------------------------------------------------ #

    def check_conflict(self, premise_condition) -> bool:
        """Detect mutually-exclusive literals in a candidate precondition.

        Returns ``True`` if a conflict is found (e.g. an agent reported as
        both holding and hand-empty, or an object both open and closed).
        """
        near_state_dict: dict = {}
        holding_state_dict: dict = {}
        empty_hand_dict: dict = {}
        room_state_dict: dict = {}
        toggle_state_dict: dict = {}

        for c in premise_condition:
            m = _RE_NEAR.search(c)
            if m:
                agent_id, obj_id = (s.strip() for s in m.group(1).split(",", 1))
                if near_state_dict.setdefault(agent_id, obj_id) != obj_id:
                    self._log_conflict(
                        f"{agent_id} is near more than one object: "
                        f"{near_state_dict[agent_id]} and {obj_id}."
                    )
                    return True

            m = _RE_HOLDING.search(c)
            if m:
                agent_id, obj_id = (s.strip() for s in m.group(1).split(",", 1))
                if agent_id in holding_state_dict and holding_state_dict[agent_id] != obj_id:
                    self._log_conflict(
                        f"{agent_id} is holding more than one object: "
                        f"{holding_state_dict[agent_id]} and {obj_id}."
                    )
                    return True
                if agent_id in empty_hand_dict:
                    self._log_conflict(
                        f"{agent_id} is reported both holding {obj_id} "
                        f"and having an empty hand."
                    )
                    return True
                holding_state_dict[agent_id] = obj_id

            m = _RE_HAND_EMPTY.search(c)
            if m:
                agent_id = m.group(1).strip()
                if agent_id in holding_state_dict:
                    self._log_conflict(
                        f"{agent_id} is reported both having an empty hand "
                        f"and holding {holding_state_dict[agent_id]}."
                    )
                    return True
                empty_hand_dict[agent_id] = True

            m = _RE_IN_ROOM.search(c)
            if m:
                entity_id = m.group(1).strip()
                room_id = m.group(2).strip()
                if entity_id in room_state_dict and room_state_dict[entity_id] != room_id:
                    self._log_conflict(
                        f"{entity_id} is reported in more than one room: "
                        f"{room_state_dict[entity_id]} and {room_id}."
                    )
                    return True
                room_state_dict[entity_id] = room_id

            m = _RE_OPEN.search(c)
            if m:
                obj_id = m.group(1).strip()
                if toggle_state_dict.get(obj_id) == "close":
                    self._log_conflict(f"{obj_id} is reported both open and close.")
                    return True
                toggle_state_dict[obj_id] = "open"

            m = _RE_CLOSE.search(c)
            if m:
                obj_id = m.group(1).strip()
                if toggle_state_dict.get(obj_id) == "open":
                    self._log_conflict(f"{obj_id} is reported both open and close.")
                    return True
                toggle_state_dict[obj_id] = "close"

        return False

    def _log_conflict(self, msg: str) -> None:
        if self.verbose:
            print(f"Conflict detected: {msg}")

    # ------------------------------------------------------------------ #
    # Behavior-tree synthesis
    # ------------------------------------------------------------------ #

    def create_anytree(self) -> None:
        """Build the AnyTree representation of the planned behavior tree."""
        task_num = 0
        anytree_root = AnyTreeNode(NODE_TYPE.selector)

        # Push goal-node children onto the work stack.
        self.add_conditions(self.goal_condition, anytree_root)
        stack: List[PlanningCondition] = []
        for child in self.goal_condition.children:
            child.parent = anytree_root
            stack.append(child)

        while stack:
            current_condition = stack.pop(0)

            if not current_condition.composition_action_flag:
                # ---- atomic action branch ---------------------------------
                if current_condition.action:
                    sequence_node = AnyTreeNode(NODE_TYPE.sequence)
                    if not current_condition.children:
                        condition_parent = sequence_node
                    else:
                        condition_parent = AnyTreeNode(NODE_TYPE.selector)
                        sequence_node.add_child(condition_parent)
                        for child in current_condition.children:
                            child.parent = condition_parent
                            stack.append(child)

                    self.add_conditions(current_condition, condition_parent)
                    cls_name, args = parse_predicate_logic(current_condition.action)
                    action_node = AnyTreeNode(NODE_TYPE.action, cls_name, args)

                    if (
                        not current_condition.children
                        and len(current_condition.condition_set) == 0
                    ):
                        current_condition.parent.add_child(action_node)
                    else:
                        sequence_node.add_child(action_node)
                        current_condition.parent.add_child(sequence_node)
                else:
                    selector_node = AnyTreeNode(NODE_TYPE.selector)
                    self.add_conditions(current_condition, selector_node)
                    current_condition.parent.add_child(selector_node)
                    for child in current_condition.children:
                        child.parent = selector_node
                        stack.append(child)

            else:
                # ---- composite-action branch ------------------------------
                if current_condition.action:
                    sel_comp_parent = AnyTreeNode(NODE_TYPE.selector)
                    seq_task_parent = AnyTreeNode(NODE_TYPE.sequence)

                    task_flag_condition = AnyTreeNode(
                        NODE_TYPE.condition,
                        "IsSelfTask",
                        [
                            task_num,
                            current_condition.action,
                            current_condition.sub_goal,
                            current_condition.sub_del,
                        ],
                    )
                    cls_name, args = parse_predicate_logic(current_condition.action)
                    task_comp_action = AnyTreeNode(NODE_TYPE.action, cls_name, args)
                    seq_task_parent.add_child(task_flag_condition)
                    seq_task_parent.add_child(task_comp_action)
                    seq_task_parent.add_child(AnyTreeNode(NODE_TYPE.action, "FinishTask"))
                    sel_comp_parent.add_child(seq_task_parent)

                    sequence_node = AnyTreeNode(NODE_TYPE.sequence)
                    if not current_condition.children:
                        condition_parent = sequence_node
                    else:
                        condition_parent = AnyTreeNode(NODE_TYPE.selector)
                        sequence_node.add_child(condition_parent)
                        for child in current_condition.children:
                            child.parent = condition_parent
                            stack.append(child)

                    self.add_conditions(current_condition, condition_parent)
                    action_node = AnyTreeNode(
                        NODE_TYPE.action,
                        "SelfAcceptTask",
                        (
                            task_num,
                            current_condition.action,
                            current_condition.sub_goal,
                            current_condition.sub_del,
                        ),
                    )
                    task_num += 1

                    sequence_node.add_child(action_node)
                    current_condition.parent.add_child(sel_comp_parent)
                    sel_comp_parent.add_child(sequence_node)
                else:
                    selector_node = AnyTreeNode(NODE_TYPE.selector)
                    self.add_conditions(current_condition, selector_node)
                    current_condition.parent.add_child(selector_node)
                    for child in current_condition.children:
                        child.parent = selector_node
                        stack.append(child)

        self.anytree_root = anytree_root

    def create_pruned_anytree(self) -> None:
        """Build an AnyTree skipping composite actions (atomic-only tree)."""
        anytree_root = AnyTreeNode(NODE_TYPE.selector)

        self.add_conditions(self.goal_condition, anytree_root)
        stack: List[PlanningCondition] = []
        for child in self.goal_condition.children:
            child.parent = anytree_root
            stack.append(child)

        while stack:
            current_condition = stack.pop(0)
            if current_condition.composition_action_flag:
                continue

            sequence_node = AnyTreeNode(NODE_TYPE.sequence)
            if not current_condition.children:
                condition_parent = sequence_node
            else:
                condition_parent = AnyTreeNode(NODE_TYPE.selector)
                sequence_node.add_child(condition_parent)
                for child in current_condition.children:
                    child.parent = condition_parent
                    stack.append(child)

            self.add_conditions(current_condition, condition_parent)
            cls_name, args = parse_predicate_logic(current_condition.action)
            action_node = AnyTreeNode(NODE_TYPE.action, cls_name, args)

            if (
                not current_condition.children
                and len(current_condition.condition_set) == 0
            ):
                current_condition.parent.add_child(action_node)
            else:
                sequence_node.add_child(action_node)
                current_condition.parent.add_child(sequence_node)

        self.anytree_root = anytree_root

    def create_btml(self) -> None:
        """Compute ``self.btml`` from the current planning graph."""
        self.create_anytree()
        btml = BTML()
        btml.anytree_root = self.anytree_root
        self.btml = btml

    def output_bt(self, behavior_lib=None) -> BehaviorTree:
        """Return a runnable ``BehaviorTree`` from the current plan."""
        self.create_btml()
        return BehaviorTree(btml=self.btml, behavior_lib=behavior_lib)

    def output_pruned_bt(self, behavior_lib=None) -> BehaviorTree:
        """Return a ``BehaviorTree`` that skips composite-action branches."""
        self.create_pruned_anytree()
        btml = BTML()
        btml.anytree_root = self.anytree_root
        self.btml = btml
        return BehaviorTree(btml=self.btml, behavior_lib=behavior_lib)

    @classmethod
    def add_conditions(cls, planning_condition, parent) -> None:
        """Attach the literals of ``planning_condition`` under ``parent``."""
        condition_set = planning_condition.condition_set
        if len(condition_set) == 0:
            return

        if len(condition_set) == 1:
            cls_name, args = parse_predicate_logic(list(condition_set)[0])
            parent.add_child(AnyTreeNode(NODE_TYPE.condition, cls_name, args))
            return

        sequence_node = AnyTreeNode(NODE_TYPE.sequence)
        cls_name = None
        for condition_node_name in condition_set:
            cls_name, args = parse_predicate_logic(condition_node_name)
            sequence_node.add_child(AnyTreeNode(NODE_TYPE.condition, cls_name, args))

        sub_btml = BTML()
        sub_btml.anytree_root = sequence_node
        composite_condition = AnyTreeNode(
            "composite_condition", cls_name=None, info={"sub_btml": sub_btml}
        )
        parent.add_child(composite_condition)

    # ------------------------------------------------------------------ #
    # Stand-alone single-agent search loop
    # (used by ``CABTP``; ``MABTP`` / ``MAOBTP`` drive their own loop)
    # ------------------------------------------------------------------ #

    def planning(self) -> None:
        explored_condition_list = [self.goal]
        while explored_condition_list:
            condition = explored_condition_list.pop(0)
            if self.verbose:
                print_colored(f"C:{condition}", "green")
            premise_condition_list = self.one_step_expand(condition)
            explored_condition_list += [
                pc.condition_set for pc in premise_condition_list
            ]
