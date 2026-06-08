# MRBTP: Efficient Multi-Robot Behavior Tree Planning and Collaboration (AAAI Oral)    

<div align="center">


[[Website]](https://dids-ei.github.io/Project/MRBTP/)
[[arXiv]](https://arxiv.org/abs/2502.18072)
[[PDF]](https://arxiv.org/pdf/2502.18072)

![Python Version](images/python310.svg)
![GitHub license](images/license.svg)



![](images/framework.png)
</div>

## 🛠️ Installation

### Environment Setup
Create and activate a new conda environment:
```shell
conda create --name mabtpg python=3.10
conda activate mabtpg
```

### Installation of MABTPG
```shell
cd MABTPG
pip install -e .
```

### 1. Download the VirtualHome executable for your platform (Only Windows is tested now):

| Operating System | Download Link                                                                      |
|:-----------------|:-----------------------------------------------------------------------------------|
| Linux            | [Download](http://virtual-home.org/release/simulator/v2.0/v2.3.0/linux_exec.zip)   |
| MacOS            | [Download](http://virtual-home.org/release/simulator/v2.0/v2.3.0/macos_exec.zip)   |
| Windows          | [Download](http://virtual-home.org/release/simulator/v2.0/v2.3.0/windows_exec.zip) |

### 2.  Execute Existing MiniGrid and BabyAI Environments:
#### (1) Running Existing Environments
1. Select a scenario from the `MiniGrid_all_scenarios.txt` file.
2. Edit `env_id` and `num_agent` at the top of `test_multi_minigrid_single_demo/main.py`
   (or `main2.py`). Agents will load with a default set of random behavior trees.

#### (2) Custom Environment Setup
Subclass `MiniGridToMAGridEnv` (see `mabtpg/envs/gridenv/minigrid/minigrid_env.py`)
or register a custom MiniGrid env via `gymnasium.envs.registration.register`
(see the `register(...)` block in `test_multi_minigrid_single_demo/main2.py` for a working
example) to construct your own room layouts.


## 📂 Directory Structure

```
mabtpg
│
├── agent - Configuration for intelligent agents.
├── llm_client - Standalone module for large language model integration
│   ├── base.py     - BaseLLMClient (chat / tool-calling / embeddings)
│   ├── llms        - Concrete clients (LLMGPT3, LLMGPT4, LLMGPT4o)
│   └── schemas     - Pydantic schemas used as OpenAI tools.
├── btp - Behavior-tree planning algorithms (see mabtpg/btp/README.md).
│   ├── base/                   - PlanningAgent / PlanningCondition.
│   ├── multi_robot_basic.py    - MABTP   (Multi-Robot BTP, FIFO baseline).
│   ├── multi_robot_optimal.py  - MAOBTP  (cost-priority heap; composite
│   │                                      actions supported).
│   ├── composite_action.py     - CABTP   (single-agent macro builder).
│   └── multi_robot.py          - MRBTP   (top-level paper-aligned facade
│                                          returning runnable BTs;
│                                          exports ``DMR = MRBTP`` alias).
├── behavior_tree - Components of the behavior tree engine.
├── envs - Environments for agent interaction.
│   ├── base - Foundational elements for environments.
│   ├── gridenv - Grid-based testing environment.
│   │   └── minigrid - Warehouse Management scenario.
│   ├── virtualhome - Home Service scenario.
│   │   └── simulation - VirtualHome Unity / evolving-graph simulators.
│   └── numericenv - Numerical simulation platform.
└── utils - Supporting functions and utilities.

simulators - Platforms for realistic training environments.

test_experiment - Modules for testing behavior trees planning, LLMs, and scene interactions.
│
├── exp1_robustness_parallelism
│   ├── code
│   └── results
└── exp2_subtree_llms
    ├── code
    │   ├── data
    │   └─ llm_data
    └── results
```



## 🚀 Getting Started
Execute multi-robot behavior tree planning algorithms in our extended MiniGrid environment:

``` shell
python test_multi_minigrid_single_demo/main.py
```

<img src="images/4_robots.gif" alt="4 robots" width="300"/>



## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
