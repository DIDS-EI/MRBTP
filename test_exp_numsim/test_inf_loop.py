import random
from data_generate import DataGenerator
from numsim_tools import print_action_data_table,split_action
from mabtpg.utils.tools import print_colored
from mabtpg.envs.gridenv.minigrid.planning_action import PlanningAction
from mabtpg.behavior_tree.btml.BTML import BTML
from mabtpg.utils.any_tree_node import AnyTreeNode

num_agent = 2

data = {
    'goal': frozenset({3}),
    'start': frozenset({}),
    'actions': [
        PlanningAction('A(1)',frozenset({}),frozenset({1}),frozenset({2})),
        PlanningAction('A(2)',frozenset({1}),frozenset({3}),frozenset({})),

        PlanningAction('A(3)',frozenset({}),frozenset({2}),frozenset({1})),
        PlanningAction('A(4)',frozenset({2}),frozenset({3}),frozenset({})),
    ]
}

agent_actions = [
    [
        data['actions'][0],
        data['actions'][1],
    ],
    [
        data['actions'][2],
        data['actions'][3]
    ],
]

comp_actions_BTML_dic = {}

# sub_btml = BTML()
# sub_btml.var_args = ['x']
# sub_btml.cls_name = 'CA'
# sequence = AnyTreeNode('sequence')
# sequence.add_child(AnyTreeNode('action','A','x'))
# sub_btml.anytree_root=sequence

# comp_actions_BTML_dic = {'CA':sub_btml}


for i, actions in enumerate(agent_actions):
    print(f"Agent {i + 1} actions:")
    for action in actions:
        print(f"  act:{action.name} pre:{action.pre} add:{action.add} del:{action.del_set}")


# BTP with composition action
goal = data['goal']
start = data['start']


# 拆分组合动作为子动作
# split_actions_dict = {}
#
# new_actions = list(dataset['actions'])
# for action in dataset['actions']:
#     # print_colored(f"act:{action.name} pre:{action.pre} add:{action.add} del:{action.del_set}",color='blue')
#     if len(action.add)>=3:
#         split_action_ls = data_generator.split_action(action,min_splits=2,max_splits=5)
#         print_colored(f"Act Split :{action.name} pre:{action.pre} add:{action.add} del:{action.del_set}", color='blue')
#
#         # 考虑保留组合动作，子动作不保留？
#         # new_actions.remove(action)
#         action.cost=0
#         # new_actions.extend(split_action_ls)
#
#         split_actions_dict[action] = split_action_ls
#
#
# # 将每个组合动作的 btml 保存起来
# # 得到一个 comp_act_BTML_dic[action.name] = sub_btml
# from num_cabtp import Num_CABTP
# from mabtpg.behavior_tree.btml.BTML import BTML
# from mabtpg.behavior_tree.behavior_tree import BehaviorTree
# comp_actions_BTML_dic = {}
# for comp_act, split_action_ls in split_actions_dict.items():
#     sub_goal = frozenset((comp_act.pre | comp_act.add) - comp_act.del_set)
#     planning_algorithm = Num_CABTP(verbose=False, goal=sub_goal, sequence=split_action_ls,action_list=split_action_ls)
#     planning_algorithm.planning()
#
#     planning_algorithm.create_anytree()
#
#     sub_btml = BTML()
#     sub_btml.cls_name = comp_act.name
#     sub_btml.var_args = None
#     sub_btml.anytree_root = planning_algorithm.anytree_root
#
#     comp_actions_BTML_dic[comp_act.name] = sub_btml

# 运行多智能体算法
from DMR import DMR
dmr = DMR(goal, start, agent_actions, num_agent, with_comp_action=True)
dmr.planning()


# #########################
# Simulation
# #########################
# 要tick进行测试，能否从 start 到 goal。
# 要几步
from mabtpg.envs.numericenv.numeric_env import NumericEnv
env = NumericEnv(num_agent=num_agent,start=start,goal=goal)
env.set_agent_actions(agent_actions)

behavior_lib = [agent.behavior_lib for agent in env.agents]
dmr.get_btml_and_bt_ls(behavior_lib=behavior_lib,comp_actions_BTML_dic=comp_actions_BTML_dic)

for i,agent in enumerate(env.agents):
    agent.bind_bt(dmr.bt_ls[i])

env.print_ticks = True
done = False
print_colored(f"start: {start}","blue")
obs = set()
while not done:
    print_colored("======================================================================================","blue")
    obs,done,_,_ = env.step()
    print_colored(f"state: {obs}","blue")
    # print("==========================\n")
    # done = True
print(f"\ntask finished!")
print("obs>=goal:",obs>=goal)



