"""
``mabtpg.envs`` — environment adapters used by the planner.

Layout
------

* ``mabtpg.envs.base``           — abstract base classes shared by every env.
* ``mabtpg.envs.gridenv``        — MiniGrid-based 2-D grid environments
                                   (sub-packages ``minigrid``, ``minigrid_computation_env``).
* ``mabtpg.envs.numerical_env``  — purely numeric / symbolic simulator used
                                   for benchmarking the planner without a
                                   physics engine.
* ``mabtpg.envs.virtualhome``    — VirtualHome adapter (3-D household scenes).

Naming convention
-----------------

All sub-packages use ``snake_case`` lowercase identifiers.  Compact compound
words such as ``gridenv`` and ``virtualhome`` are kept without an underscore
because they are well-established short forms across the codebase.  Longer
names (``numerical_env``, ``minigrid_computation_env``) keep the underscore
to remain readable.  For backward compatibility the historical import paths
are preserved verbatim and **must not** be renamed without a deprecation
shim — they are referenced by 100+ external experiment scripts.
"""
