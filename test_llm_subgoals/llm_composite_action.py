from mabtpg.algo.llm_client.llms.gpt3 import LLMGPT3
import gymnasium as gym
from mabtpg import MiniGridToMAGridEnv
from minigrid.core.world_object import Ball, Box,Door
from mabtpg.utils import get_root_path
from mabtpg import BehaviorLibrary
root_path = get_root_path()
from itertools import permutations

num_agent = 2
env_id = "MiniGrid-DoorKey-16x16-v0"
tile_size = 32
agent_view_size =7
screen_size = 1024

mingrid_env = gym.make(
    env_id,
    tile_size=tile_size,
    render_mode=None,
    agent_view_size=agent_view_size,
    screen_size=screen_size
)


env = MiniGridToMAGridEnv(mingrid_env, num_agent=num_agent)
env.reset(seed=0)

# add objs
# ball = Ball('red')
# env.place_object_in_room(ball,0)
# ball = Ball('yellow')
# env.place_object_in_room(ball,1)
env.reset(seed=0)


goal = "IsNear(ball-0,ball-1)"
action_lists = env.get_action_lists()
start = env.get_initial_state()
print(start)
# print(action_lists[0])

# action_list = action_lists[0]

composition_actions_ls = {}
composition_actions_BTML_ls={}

sub_act_ls = ['GoToInRoom', 'PickUp', 'GoToInRoom', 'Toggle']
# GoToInRoom(agent,key-0,1)
# PickUp(agent,key-0)
# GoToInRoom(agent,door-0,1)
# Toggle(key-0)

from mabtpg.btp.cabtp import CABTP
from mabtpg.envs.gridenv.minigrid.planning_action import PlanningAction
from mabtpg.utils.tools import extract_parameters_from_action_name,extract_predicate_from_action_name,extract_agent_id_from_action_name

for i,action_list in enumerate(action_lists):

    agent_id = "agent-{}".format(i)

    # 过滤出与子动作列表匹配的动作
    filtered_actions = [action for action in action_list if any(sub_act in action.name for sub_act in sub_act_ls)]
    # 进行反向扩展,拿到条件动作对
    for act in filtered_actions:

        # if act.name == 'Toggle(agent-0,door-0)':
        if "Toggle" in act.name:

            # agent_id = extract_agent_id_from_action_name(act.name)

            goal = (act.pre | act.add ) - act.del_set
            print("goal:",goal)

            planning_algorithm = CABTP(verbose=False,goal = frozenset(goal), action_list=filtered_actions,sub_act_ls=sub_act_ls)
            planning_algorithm.planning()

            # 收集所有的参数
            args_ls = []
            # 计算组合动作的 pre add del 构造 PlanningAgent

            action_model = {}
            action_model["pre"] = set()
            action_model["add"] = set()
            action_model["del_set"] = set()
            action_model["cost"] = 0

            cond_act_ls = planning_algorithm.collect_explored_cond_act
            cond_act_ls = list(reversed(cond_act_ls))
            for i,(cond,act) in enumerate(cond_act_ls):
                print(cond)
                print(act)
                print("   ")

                # pre
                if i==len(cond_act_ls)-1:
                    action_model["pre"] = act.pre
                # add del
                action_model["add"] |= act.add
                action_model["del_set"] |= act.del_set

                args_ls.extend(extract_parameters_from_action_name(act.name))

            args_ls = list(sorted(set(args_ls)))
            planning_action = PlanningAction(f"GetKeyAndOpenDoor({','.join(args_ls)})",**action_model)

            if agent_id not in composition_actions_ls:
                composition_actions_ls[agent_id] = []
            composition_actions_ls[agent_id].append(planning_action)


            # 构建BTML
            from mabtpg.behavior_tree.btml.BTML import BTML
            btml = BTML()

            from mabtpg.utils.any_tree_node import AnyTreeNode
            sequence_node = AnyTreeNode("sequence")

            for (cond, act) in cond_act_ls:
                print("act:",act)

                fallback_node = AnyTreeNode("sequence")

                # condition
                node_list = []
                for c in cond:
                    c_args = extract_parameters_from_action_name(c)
                    node = AnyTreeNode("Condition", cls_name=extract_predicate_from_action_name(c), args=c_args)
                    node_list.append(node)
                sequence_node_tmp = AnyTreeNode('sequence')
                sequence_node_tmp.add_children(node_list)
                sub_btml_tmp = BTML()
                sub_btml_tmp.anytree_root = sequence_node_tmp
                fallback_node.add_child(AnyTreeNode("composite_condition",cls_name=None, info={"sub_btml":sub_btml_tmp}))

                # action
                act_args_ls = extract_parameters_from_action_name(act.name)
                predicate = extract_predicate_from_action_name(act.name)
                fallback_node.add_child(AnyTreeNode("Action", predicate, (act_args_ls)))

                sequence_node.add_child(fallback_node)

            sub_btml = BTML()
            sub_btml.cls_name = 'GetKeyAndOpenDoor'
            sub_btml.var_args = args_ls
            sub_btml.anytree_root = sequence_node

            if agent_id not in composition_actions_BTML_ls:
                composition_actions_BTML_ls[agent_id]=[]
            composition_actions_BTML_ls[agent_id].append(sub_btml)


for i in range(env.num_agent):
    agent_id = "agent-"+str(i)
    if agent_id in composition_actions_ls:
        action_lists[i].extend(composition_actions_ls["agent-"+str(i)])

    # sorted by cost
    action_lists[i] = sorted(action_lists[i], key=lambda x: x.cost)



# 规划新的
from mabtpg.btp.maobtp import MAOBTP
# goal = {"IsInRoom(ball-0,room-1)"}
goal = {"IsOpen(door-0)"}
planning_algorithm = MAOBTP(verbose = False,start=start)
# planning_algorithm.planning(frozenset(goal),action_lists=action_lists)
planning_algorithm.bfs_planning(frozenset(goal),action_lists=action_lists)
behavior_lib = [agent.behavior_lib for agent in env.agents]
btml_list = planning_algorithm.get_btml_list()

# bt_list = planning_algorithm.output_bt_list([agent.behavior_lib for agent in env.agents])
# for i in range(env.num_agent):
#     print("\n" + "-" * 10 + f" Planned BT for agent {i} " + "-" * 10)
#     bt_list[i].save_btml(f"robot-{i}.bt")
#     bt_list[i].draw(file_name=f"agent-{i}")


# 在规划出来的 BTML 里面加上 新的sub_btml_dict
from mabtpg.behavior_tree.behavior_tree import BehaviorTree
from mabtpg.utils.any_tree_node import AnyTreeNode
from mabtpg.behavior_tree.constants import NODE_TYPE
bt_list=[]
for i,agent in enumerate(planning_algorithm.planned_agent_list):
    btml_list[i].anytree_root = agent.anytree_root
    btml_list[i].sub_btml_dict['GetKeyAndOpenDoor'] = composition_actions_BTML_ls["agent-"+str(i)][0]
    print("\n" + "-" * 10 + f" Planned BT for agent {i} " + "-" * 10)

    bt = BehaviorTree(btml=btml_list[i], behavior_lib=behavior_lib[i])
    bt_list.append(bt)

    tmp_bt = BehaviorTree(btml=composition_actions_BTML_ls["agent-"+str(i)][0], behavior_lib=behavior_lib[i])
    tmp_bt.draw()

for i in range(env.num_agent):
    bt_list[i].save_btml(f"robot-{i}.bt")
    bt_list[i].draw(file_name=f"agent-{i}")

# bind the behavior tree to agents
for i,agent in enumerate(env.agents):
    agent.bind_bt(bt_list[i])


# run
env.render()
env.print_ticks = True
done = False
while not done:
    obs,done,_,_ = env.step()
print(f"\ntask finished!")

# continue rendering after task finished
while True:
    env.render()
