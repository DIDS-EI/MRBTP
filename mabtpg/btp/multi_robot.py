"""MRBTP — Multi-Robot Behavior-Tree Planning facade.

This is the high-level driver described in the paper

    *MRBTP: Efficient Multi-Robot Behavior Tree Planning and Collaboration*
    (AAAI Oral, https://arxiv.org/abs/2502.18072)

It is a thin facade over the two underlying back-chaining searches —
``MABTP`` (FIFO, no composite actions) and ``MAOBTP`` (cost-priority
heap, supports composite actions) — picks the right one based on
``with_comp_action``, runs the search, and turns the resulting per-agent
``BTML`` into runnable ``BehaviorTree`` objects (optionally drawing them
and saving ``robot-i.bt`` artifacts).

Naming history
--------------
The class was originally called ``DMR`` (*Decentralized Multi-Robot*) in
the codebase, while the paper introduces it as **MRBTP**. To make the
code match the paper without breaking the many experiment scripts that
already import the legacy name, the canonical class is now ``MRBTP`` and
``DMR`` is re-exported as a class-level alias::

    # New, paper-aligned (recommended)
    from mabtpg.btp import MRBTP
    from mabtpg.btp.multi_robot import MRBTP

    # Legacy — still works, identical class object
    from mabtpg.btp import DMR        # DMR is MRBTP  →  True
"""

from __future__ import annotations

import time
from typing import List, Optional

from mabtpg.behavior_tree.behavior_tree import BehaviorTree
from mabtpg.btp.multi_robot_basic import MABTP
from mabtpg.btp.multi_robot_optimal import MAOBTP
from mabtpg.utils.tools import print_colored


class MRBTP:
    """High-level driver around the MA-BTP / MAO-BTP planners.

    This is the algorithm referred to as **MRBTP** in the paper. The old
    name ``DMR`` is kept as a module-level alias for backward
    compatibility (see the bottom of this file).
    """

    def __init__(
        self,
        env,
        goal,
        start,
        action_lists,
        num_agent: Optional[int] = None,
        with_comp_action: bool = False,
        save_dot: bool = False,
        max_time_limit: float = 20.0,
        output_dir: Optional[str] = None,
    ):
        self.env = env
        self.goal = goal
        self.start = start
        self.action_lists = action_lists
        self.num_agent = num_agent
        self.with_comp_action = with_comp_action
        self.save_dot = save_dot
        self.max_time_limit = max_time_limit
        # Where to drop the generated .bt / .svg / .png files.
        # When ``None`` we fall back to the current working directory so
        # the previous behaviour is preserved for callers that don't care.
        self.output_dir = output_dir

        if num_agent != len(action_lists):
            print_colored(
                f"Error num_agent {num_agent} != len(action_lists) {len(action_lists)}!",
                color="red",
            )

        self.planning_algorithm: Optional[MABTP] = None

        # Public outputs filled in after planning / behavior-tree synthesis.
        # Names ending with ``_ls`` are kept for backward-compatibility with
        # existing experiment scripts; ``_list`` aliases are added below.
        self.btml_ls: Optional[List] = None
        self.bt_ls: Optional[List[BehaviorTree]] = None
        self.default_bt_ls: Optional[List[BehaviorTree]] = None

        self.record_expanded_num: int = 0
        self.expanded_time: float = 0.0

    # Forward-compatible ``_list`` aliases for the legacy ``_ls`` fields.
    @property
    def btml_list(self):
        return self.btml_ls

    @property
    def bt_list(self):
        return self.bt_ls

    def planning(self) -> None:
        print_colored("Start Multi-Robot Behavior Tree Planning...", color="green")
        start_time = time.time()

        if not self.with_comp_action:
            self.planning_algorithm = MABTP(
                env=self.env,
                verbose=False,
                start=self.start,
                max_time_limit=self.max_time_limit,
            )
            self.planning_algorithm.planning(
                frozenset(self.goal), action_lists=self.action_lists
            )
        else:
            self.planning_algorithm = MAOBTP(
                env=self.env,
                verbose=False,
                start=self.start,
                max_time_limit=self.max_time_limit,
            )
            self.planning_algorithm.bfs_planning(
                frozenset(self.goal), action_lists=self.action_lists
            )

        elapsed = time.time() - start_time
        print_colored("Finish Multi-Robot Behavior Tree Planning!", color="green")
        print_colored(f"Time: {elapsed}", color="green")

        self.record_expanded_num = self.planning_algorithm.record_expanded_num
        self.expanded_time = elapsed

    def get_btml_and_bt_ls(
        self,
        behavior_lib=None,
        comp_btml_ls=None,
        comp_planning_act_ls=None,
    ):
        """Build per-agent BTMLs / BTs, merging composite-action sub-trees if any.

        Args:
            behavior_lib: per-agent ``BehaviorLibrary`` list.
            comp_btml_ls: per-agent BTML carrying composite-action sub-trees,
                produced by ``CompositeActionPlanner``.
            comp_planning_act_ls: kept for signature compatibility (currently
                unused; merging is done through ``comp_btml_ls.sub_btml_dict``).
        """
        del comp_planning_act_ls  # accepted for backward compatibility

        self.btml_ls = self.planning_algorithm.get_btml_list()
        self.bt_ls = []

        # Resolve output directory. Default to ``./output`` so generated
        # behavior-tree artifacts don't litter the caller's CWD.
        out_dir = None
        if self.save_dot:
            from pathlib import Path

            out_dir = Path(self.output_dir) if self.output_dir else Path("output")
            out_dir.mkdir(parents=True, exist_ok=True)

        if comp_btml_ls is not None:
            for agent_id in range(self.num_agent):
                self.btml_ls[agent_id].sub_btml_dict = (
                    comp_btml_ls[agent_id].sub_btml_dict
                )
                if self.save_dot:
                    for name, sub_btml in self.btml_ls[agent_id].sub_btml_dict.items():
                        if sub_btml:
                            tmp_bt = BehaviorTree(
                                btml=sub_btml, behavior_lib=behavior_lib[agent_id]
                            )
                            tmp_bt.draw(
                                file_name=f"{agent_id}-{name}",
                                target_directory=str(out_dir),
                            )

        for i in range(self.num_agent):
            bt = BehaviorTree(btml=self.btml_ls[i], behavior_lib=behavior_lib[i])
            self.bt_ls.append(bt)
            if self.save_dot:
                self.bt_ls[i].save_btml(str(out_dir / f"robot-{i}.bt"))
                self.bt_ls[i].draw(
                    file_name=f"robot-{i}",
                    png_only=True,
                    target_directory=str(out_dir),
                )


# ---------------------------------------------------------------------------
# Backward-compatibility alias.
#
# The class used to be called ``DMR`` (Decentralized Multi-Robot). Many
# experiment scripts and external callers do
#
#     from mabtpg.btp import DMR
#     dmr = DMR(...)
#
# Keeping ``DMR`` as a name pointing to the *same* class object means
# ``isinstance(obj, DMR)`` and ``isinstance(obj, MRBTP)`` are both true and
# there is no second class hierarchy.
# ---------------------------------------------------------------------------
DMR = MRBTP

__all__ = ["MRBTP", "DMR"]
