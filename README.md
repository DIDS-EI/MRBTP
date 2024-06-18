# MABTPG


# Installation

Create a conda environment.
```shell
conda create --name mabtpg python=3.10
conda activate mabtpg
```

Install MABTPG.
```shell
cd MABTPG
pip install -e .
```

# 使用

## 运行 MiniGrid 和 BabyAI 原有环境

1. 在 MiniGrid所有场景.txt 中选择一个想要运行的场景
2. 在 test_gridworld/minigrid_env.py 文件中，输入想要运行的场景和 num_agent，智能体会默认加载随机动作的行为树


## 自定义环境

在 test_gridworld/custom_env.py 文件中，自定义一个房间，用 self.grid.horz_wall, self.put_obj 等函数来创建场景