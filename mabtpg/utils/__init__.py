"""Generic, environment-agnostic helpers used across :mod:`mabtpg`.

This module deliberately re-exports a handful of small, frequently-used
utilities so that callers can write a single short import line, e.g.::

    from mabtpg.utils import ROOT_PATH, get_root_path, parse_predicate_logic

Layout
------
``mabtpg.utils.path``                Project-root resolution.
``mabtpg.utils.random``              Seeded NumPy RNG wrapper (``Random``).
``mabtpg.utils.string_format``       Predicate-logic string parsing.
``mabtpg.utils.tools``               Coloured printing, action filtering,
                                     experiment summary helpers.
``mabtpg.utils.any_tree_node``       Generic n-ary tree node + traversals.
``mabtpg.utils.composite_action_tools``  Composite-action sub-tree planner
                                     (``CompositeActionPlanner``) — only
                                     needed by the composite-action
                                     experiments.
"""

from mabtpg.utils.path import ROOT_PATH, get_root_path
from mabtpg.utils.string_format import parse_predicate_logic

__all__ = [
    "ROOT_PATH",
    "get_root_path",
    "parse_predicate_logic",
]
