"""mabtpg — Multi-Robot Behavior-Tree Planning toolkit.

This top-level package re-exports the most commonly used symbols so user
code can simply do::

    import mabtpg
    bt  = mabtpg.BehaviorTree(...)
    lib = mabtpg.BehaviorLibrary(...)
    env = mabtpg.make("MABTPG-MiniGrid-...-v0")

Sub-packages
------------
``mabtpg.btp``           Multi-robot / multi-robot BT planners
                         (``DMR``, ``MABTP``, ``MAOBTP``, ``CABTP``).
``mabtpg.behavior_tree`` Behavior-tree runtime, ``BTML`` parser,
                         ``BehaviorLibrary``.
``mabtpg.envs``          Environments (MiniGrid, NumericalEnv, VirtualHome…).
``mabtpg.llm_client``    Thin OpenAI-compatible LLM client + schemas.
``mabtpg.utils``         Generic helpers (paths, RNG, string parsing).
"""

import os
import warnings

# Silence the noisy gymnasium "the environment is passed a reset..." warning.
warnings.filterwarnings("ignore", category=UserWarning, module="gymnasium.core")

# Hide the pygame "Hello from the pygame community" banner.
os.environ.setdefault("PYGAME_HIDE_SUPPORT_PROMPT", "True")

import gymnasium  # noqa: E402  (must come after the env tweaks above)

from mabtpg.behavior_tree.behavior_library import BehaviorLibrary  # noqa: E402
from mabtpg.behavior_tree.behavior_tree import BehaviorTree  # noqa: E402
from mabtpg.envs.gridenv.minigrid.minigrid_env import MiniGridToMAGridEnv  # noqa: E402
from mabtpg.utils import ROOT_PATH  # noqa: E402
from mabtpg.utils.random import Random  # noqa: E402

# Initialise the global RNG once at import time.
Random.initialize()

# Convenience alias so users can write ``mabtpg.make(env_id)``.
make = gymnasium.make

__all__ = [
    "BehaviorTree",
    "BehaviorLibrary",
    "MiniGridToMAGridEnv",
    "Random",
    "ROOT_PATH",
    "make",
]
