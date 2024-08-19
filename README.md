# MABTPG

MRBTP: Efficient Multi-Robot Behavior Tree Planning and Collaboration.

![Python Version](images/python310.svg)
![GitHub license](images/license.svg)
![](images/framework.png)


## 🛠️ Installation

### Create a conda environment
```shell
conda create --name mabtpg python=3.10
conda activate mabtpg
```

### Install MABTPG.
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

### 2. 运行 MiniGrid 和 BabyAI 原有环境:
1. 在 MiniGrid所有场景.txt 中选择一个想要运行的场景
2. 在 test_gridworld/minigrid_env.py 文件中，输入想要运行的场景和 num_agent，智能体会默认加载随机动作的行为树


## 自定义环境
在 test_gridworld/custom_env.py 文件中，自定义一个房间，用 self.grid.horz_wall, self.put_obj 等函数来创建场景



## 📂 Directory Structure

```
mabtpg
│
├── agent - Configuration for intelligent agents.
├── algo - Training and decision-making algorithms.
│   └── llm_client - Modules for large language model integration.
├── btp - Behavior tree planning algorithms.
│   └── base
│        └── planning_agent
│        └── planning_condition
│   ├── DMR
│   ├── mabtp
│   ├── maobtp
│   └── captp
├── behavior_tree - Behavior tree engine components.
├── envs - Scene environments for agent interaction.
│   ├── base - Foundational elements for environments.
│   ├── gridenv - Grid-based testing environment.
│   │    └── minigrid - WareHouse Management scenario.
│   ├── virtualhome -  Everyday Service scenario.
│   └── numericenv  - 
└── utils - Supporting functions and utilities.

simulators - Platforms for realistic training environments.

test_experiment - Testing modules for behavior trees planning, LLMs, and scene environments.
│
├── exp1_robustness_parallelism
│   ├── code
│   └── results
└── exp2_subtree_llms
│   ├── code
│   ├── data
│   ├── llm_data
│   └── results

```



## 🚀 Getting Started
``` shell
python test_multi_minigrid_single_demo/main.py
```