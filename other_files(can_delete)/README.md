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



## MiniGrid 里的动作模型和条件模型

### Action

`PutInRoom(agent, obj, roomid)`

```

```

`GoToRoom(agent, room_id)`

### Condition

`IsInRoom(agent/obj, room_id)`



### 对于 GoTo action

到门的 pre 是什么呢

```python
            # The premise is that the agent must be in the room where the object is located.
            if "door" not in obj_id:
                room_index = env.get_room_index(env.id2obj[obj_id].cur_pos)
                action_model["pre"] = {f"IsInRoom(agent-{agent.id},{room_index})"}
            else:
                # door
                action_model["pre"] = set()
```

### 对于 PutInRoom

智能体0把物体0放到房间0的 pre 是什么呢

```python
                # error:if the agent go to in another room it will fail
                # action_model["pre"]= {f"IsHolding(agent-{agent.id},{obj_id})",f"IsInRoom(agent-{agent.id},{room_id})"}
                action_model["pre"] = {f"IsHolding(agent-{agent.id},{obj_id})", f"IsInRoom({obj_id},{room_id})"}
                action_model["add"]={f"IsHandEmpty(agent-{agent.id})",f"IsInRoom({obj_id},{room_id})"}
                action_model["del_set"] = {f"IsHolding(agent-{agent.id},{obj_id})"}
```



钥匙用过以后还能放下



PutInRoom 会改变 IsNear 条件 

Condition IsInRoom(agent-0,1): SUCCESS  在门上也算是 IsIn 两边任何一个room

CanGoTo({obj_id}) 要不要涉及 智能体也作为参数呢？增加这个 条件 的原因是：一个智能体拿起这个物体后，其它智能体 再 GoTo 会找不到路径报错
