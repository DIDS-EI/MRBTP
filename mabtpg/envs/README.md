# `mabtpg/envs/` — Environment Adapters

Every planner in this project consumes one of the environment adapters
defined here. The package is split by **physical simulator** because each
of them models actions, perception and rewards differently. The job of
this sub-package is to expose them all behind a small set of common base
classes.

## High-level layout

```
mabtpg/envs/
├── __init__.py
├── base/                          Shared abstract base
│   ├── env.py                     Env       — root env class
│   └── agent.py                   Agent     — root agent class
│
├── gridenv/                       2-D grid worlds (built on Farama-Minigrid)
│   ├── base/                       └── ⬇ generic MAGrid + actions/components
│   │   ├── magrid.py              MAGrid          (gym.Env-style)
│   │   ├── magrid_env.py          MAGridEnv       (gym.Env-style)
│   │   ├── actions.py             Action enum     (PEP 8: snake_case)
│   │   ├── components.py          Component base  (PEP 8: snake_case)
│   │   ├── object.py              Object/Wall
│   │   ├── agent.py               Agent (grid)
│   │   ├── window.py / icon.py / keyboard_control.py / constants.py
│   ├── minigrid/                   └── ⬇ Farama-Minigrid library adapter
│   │   ├── minigrid_env.py        MiniGridToMAGridEnv ← REGISTERED with gym.make
│   │   ├── magrid_env.py          MiniGridMAGridEnv   (intermediate mixin)
│   │   ├── magrid.py              MiniGridMAGrid      (Grid subclass)
│   │   ├── planning_action.py     PlanningAction
│   │   ├── agent.py               Agent (minigrid)
│   │   └── behavior_lib/          per-action / per-condition leaves
│   └── minigrid_computation_env/   └── ⬇ symbolic version used by exp1/exp2
│       ├── mini_comp_env.py       MiniCompEnv         ← used by experiment scripts
│       └── …
│
├── numerical_env/                  Pure symbolic simulator (no rendering)
│   ├── numerical_env.py           NumericalEnv
│   ├── numsim_tools.py            helpers (CSV writers, summary tables)
│   └── behavior_lib/
│
└── virtualhome/                    3-D household scenes (VirtualHome)
    ├── envs/vh_computation_env.py VHCompEnv           ← used by exp2
    ├── simulation/                 Unity simulator client
    └── behavior_lib/
```

## Which env class do I use?

| Use case                                     | Class                                                     | Module path                                                           |
| -------------------------------------------- | --------------------------------------------------------- | --------------------------------------------------------------------- |
| Quick visual demo on Farama-Minigrid         | `MiniGridToMAGridEnv` (auto-registered)                    | `mabtpg.envs.gridenv.minigrid.minigrid_env`                           |
| Robustness / parallelism benchmark (exp1/2)  | `MiniCompEnv`                                              | `mabtpg.envs.gridenv.minigrid_computation_env.mini_comp_env`           |
| Pure-symbolic benchmark (no rendering)       | `NumericalEnv`                                             | `mabtpg.envs.numerical_env.numerical_env`                             |
| Household / VirtualHome benchmark (exp2)     | `VHCompEnv`                                                | `mabtpg.envs.virtualhome.envs.vh_computation_env`                     |

> The **`*_computation_env`** suffix means *symbolic / state-graph
> evaluator only* — actions update an internal state set instead of
> rendering pixels. The corresponding non-`computation` module is the
> visualisable counterpart.

## Naming conventions

* Module files are `snake_case.py` (the historical TitleCase outliers
  `Actions.py` / `Components.py` were renamed in this refactor).
* Class names are `TitleCase`. Acronyms like `MABTP`, `BTML`, `MAGrid`
  are kept upper-case because they are how the paper refers to them.
* The two halves of `gridenv/` (`base/` vs `minigrid/`) used to both
  contain a class called `MAGrid` / `MAGridEnv`, which made debugging
  hard. The **`minigrid/`** side is now prefixed (`MiniGridMAGrid`,
  `MiniGridMAGridEnv`) so it is unambiguous which one is in scope.
* `gridenv/` is a single word on purpose (it predates `numerical_env/`
  and is referenced by 100+ external scripts). Renaming would be a
  major breaking change, so we keep it.

## Stability of import paths

The following module paths are **part of the public API** and are
imported by archived experiment scripts under `test_experiment/` and
`test_experiment_history_saved_*/`. Do **not** rename them without
adding a deprecation shim:

```
mabtpg.envs.gridenv.minigrid.minigrid_env
mabtpg.envs.gridenv.minigrid.planning_action
mabtpg.envs.gridenv.minigrid_computation_env.mini_comp_env
mabtpg.envs.numerical_env.numsim_tools
mabtpg.envs.virtualhome.envs.vh_computation_env
```
