"""Composite-action sub-tree planner.

Given, for each agent, a dictionary of "composite action sequences"
(``{comp_act_name: [action_name_1, action_name_2, ...]}``), this module
plans a sub-behavior-tree per composite action and synthesises a single
``PlanningAction`` whose ``pre / add / del_set`` summarises the whole
sequence.  The resulting BTMLs are merged into the multi-robot plan by
:meth:`mabtpg.btp.multi_robot.MRBTP.get_btml_and_bt_ls`.
"""

from __future__ import annotations

import time
from typing import Dict, List, Tuple

from mabtpg.behavior_tree.btml.BTML import BTML
from mabtpg.btp.composite_action import CABTP
from mabtpg.envs.gridenv.minigrid.planning_action import PlanningAction
from mabtpg.utils import parse_predicate_logic


class CompositeActionPlanner:
    """Build per-agent sub-trees for composite (multi-step) actions."""

    def __init__(self, action_model, composition_action, env=None):
        self.env = env
        self.action_model = action_model
        # Per-agent dict: ``{comp_act_name: [action_name_1, ...]}``.
        self.action_sequences = composition_action

        # Filled in by :meth:`get_composite_action`.
        self.planning_ls: List[List[PlanningAction]] = []
        self.btml_ls: List[BTML] = []
        self.btml_dic: Dict[str, BTML] = {}

        # Stats.
        self.expanded_num: int = 0
        self.expanded_time: float = 0.0

    # --------------------------------------------------------------------- #
    # Per-sequence planning
    # --------------------------------------------------------------------- #

    def plan_sub_bt_from_filtered_actions(
        self,
        agent_comp_sequence: List[PlanningAction],
        comp_act_name: str,
    ) -> Tuple[PlanningAction, BTML]:
        """Plan a sub-BT for one composite-action sequence and summarise it.

        Returns ``(planning_action, sub_btml)`` where ``planning_action``
        is a :class:`PlanningAction` whose effect set is the union of the
        sequence's effects, and ``sub_btml`` is the corresponding BTML.

        Returns ``([], [])`` if planning fails.
        """
        sub_goal = agent_comp_sequence[-1].add
        planner = CABTP(
            env=self.env,
            verbose=False,
            goal=frozenset(sub_goal),
            action_list=agent_comp_sequence,
        )
        if planner.planning() is None:
            return [], []

        # Collapse the whole sequence into one PlanningAction.
        composite_action_model = {
            "pre":     set(),
            "add":     set(),
            "del_set": set(),
            "cost":    0,
        }
        sum_add: set = set()
        for a in agent_comp_sequence:
            composite_action_model["pre"]     |= a.pre - sum_add

            composite_action_model["add"]     |= a.add
            composite_action_model["add"]     -= a.del_set

            composite_action_model["del_set"] |= a.del_set
            composite_action_model["del_set"] -= a.add

            sum_add |= a.add

        composite_action_model["del_set"] -= composite_action_model["add"]
        composite_action_model["add"]     -= composite_action_model["pre"]

        planning_action = PlanningAction(f"{comp_act_name}()", **composite_action_model)

        planner.create_anytree()
        sub_btml = BTML()
        sub_btml.cls_name = comp_act_name
        sub_btml.anytree_root = planner.anytree_root

        return planning_action, sub_btml

    # --------------------------------------------------------------------- #
    # Per-agent dispatch
    # --------------------------------------------------------------------- #

    def get_single_agent_composite_action(
        self,
        comp_act_name: str,
        comp_sequence: List[str],
        agent_id: int,
        action_model,
    ):
        """Plan one composite action for ``agent_id``.

        ``agent_id == -1`` is a (legacy) "no-agent" mode where ``action_model``
        is allowed to be a list-of-lists; it is flattened and de-duplicated.
        """
        if agent_id != -1:
            agent_name = f"agent-{agent_id}"

            # Substitute "self" -> the concrete agent name.
            agent_comp_name_sequence = []
            for action_name in comp_sequence:
                cls_name, args = parse_predicate_logic(action_name)
                new_args = [agent_name if arg == "self" else arg for arg in args]
                agent_comp_name_sequence.append(f"{cls_name}({','.join(new_args)})")

            action_model_dic = {a.name: a for a in action_model}
        else:
            # Flatten and de-duplicate a list-of-lists action model.
            if isinstance(action_model, list) and action_model and isinstance(action_model[0], list):
                seen: set = set()
                flat: List = []
                for sub in action_model:
                    for action in sub:
                        if action.name not in seen:
                            flat.append(action)
                            seen.add(action.name)
                action_model = flat

            agent_comp_name_sequence = list(comp_sequence)
            action_model_dic = {a.name: a for a in action_model}

        # Resolve the action sequence; bail out early if any step is missing.
        agent_comp_sequence = []
        for action_name in agent_comp_name_sequence:
            if action_name not in action_model_dic:
                return [], []
            agent_comp_sequence.append(action_model_dic[action_name])

        return self.plan_sub_bt_from_filtered_actions(agent_comp_sequence, comp_act_name)

    # --------------------------------------------------------------------- #
    # Top-level entry
    # --------------------------------------------------------------------- #

    def get_composite_action(self):
        """Plan every composite action for every agent.

        Returns:
            A pair ``(planning_ls, btml_ls)`` where:
              * ``planning_ls[i]`` is the list of synthesised
                :class:`PlanningAction` objects for agent ``i``.
              * ``btml_ls[i]`` is a :class:`BTML` whose
                ``sub_btml_dict`` maps each composite-action name to its
                sub-BTML.
        """
        for agent_id, agent_composition_action_dic in enumerate(self.action_sequences):
            btml = BTML()
            planning_action_ls: List[PlanningAction] = []

            for comp_act_name, comp_sequence in agent_composition_action_dic.items():
                start_time = time.time()
                planning_action, sub_btml = self.get_single_agent_composite_action(
                    comp_act_name,
                    comp_sequence,
                    agent_id,
                    self.action_model[agent_id],
                )
                end_time = time.time()

                planning_action_ls.append(planning_action)
                btml.sub_btml_dict[comp_act_name] = sub_btml

                # Only count each composite action once across the whole batch.
                if comp_act_name not in self.btml_dic:
                    self.btml_dic[comp_act_name] = sub_btml
                    self.expanded_num += len(comp_sequence)
                    self.expanded_time += (end_time - start_time)

            self.planning_ls.append(planning_action_ls)
            self.btml_ls.append(btml)

        return self.planning_ls, self.btml_ls
