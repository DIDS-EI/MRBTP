# MABTP

MRBTP: Efficient Multi-Robot Behavior Tree Planning and Collaboration.

![Python Version](images/python310.svg)
![GitHub license](images/license.svg)
![](images/framework.png)


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
1. Select a scenario from the MiniGrid_all_scenarios.txt file.
2. Input the chosen scenario and num_agent in the test_gridworld/minigrid_env.py file. Agents will load with a default set of random behavior trees.

#### (2) Custom Environment Setup
Design custom room layouts in test_gridworld/custom_env.py using functions like self.grid.horz_wall and self.put_obj to construct your scenes.


## 📂 Directory Structure

```
mabtpg
│
├── agent - Configuration for intelligent agents.
├── algo - Training and decision-making algorithms.
│   └── llm_client - Modules for large language model integration.
├── btp - Behavior tree planning algorithms.
│   └── base
│       └── planning_agent
│       └── planning_condition
│   ├── DMR - Planning algorithm interface.
│   ├── mabtp - Multi-robot behavior tree planning algorithms.
│   ├── maobtp - Priority-queue-based multi-robot behavior tree planning algorithms.
│   └── captp - Subtree pre-planning algorithms.
├── behavior_tree - Components of the behavior tree engine.
├── envs - Environments for agent interaction.
│   ├── base - Foundational elements for environments.
│   ├── gridenv - Grid-based testing environment.
│   │   └── minigrid - Warehouse Management scenario.
│   ├── virtualhome - Home Service scenario.
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
Execute multi-agent behavior tree planning algorithms in our extended MiniGrid environment:

``` shell
python test_multi_minigrid_single_demo/main.py
```

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
