import random
from data_generate import DataGenerator
from numsim_tools import print_action_data_table,split_action
from mabtpg.utils.tools import print_colored
import numpy as np
random.seed(0)
np.random.seed(0)

#  get data
num_data = 1
num_elements = 30
max_depth = 3

# num_data = 1
# num_elements = 10
# max_depth = 2

data_generator = DataGenerator(num_elements=num_elements,  max_depth=max_depth)
datasets = [data_generator.generate_dataset() for _ in range(num_data)]

for i,dataset in enumerate(datasets[:]):
    print_action_data_table(dataset['goal'], dataset['start'], dataset['actions'])
    data_generator.save_tree_as_dot(dataset, f'data/{i}_generated_tree.dot')



# BTP inside and outside



for data_id,dataset in  enumerate(datasets[:]):
    print("data_id:",data_id)
    # BTP with composition action
    # dataset = datasets[0]
    goal = dataset['goal']
    start = dataset['start']
    num_agent = 2

    # 拆分组合动作为子动作
    split_actions_dict = {}

    new_actions = list(dataset['actions'])
    for action in dataset['actions']:
        # print_colored(f"act:{action.name} pre:{action.pre} add:{action.add} del:{action.del_set}",color='blue')
        if len(action.add)>=3:
            split_action_ls = data_generator.split_action(action,min_splits=2,max_splits=5)
            print_colored(f"Act Split :{action.name} pre:{action.pre} add:{action.add} del:{action.del_set}", color='blue')

            # 考虑保留组合动作，子动作不保留？
            # new_actions.remove(action)
            # action.cost=0
            new_actions.extend(split_action_ls) #???? 如果还保留子动作，则需要再条数

            split_actions_dict[action] = split_action_ls
            action.cost = 0

    # 将每个组合动作的 btml 保存起来
    # 得到一个 comp_act_BTML_dic[action.name] = sub_btml
    from num_cabtp import Num_CABTP
    from mabtpg.behavior_tree.btml.BTML import BTML
    from mabtpg.behavior_tree.behavior_tree import BehaviorTree
    comp_actions_BTML_dic = {}
    for comp_act, split_action_ls in split_actions_dict.items():
        sub_goal = frozenset((comp_act.pre | comp_act.add) - comp_act.del_set)
        planning_algorithm = Num_CABTP(verbose=False, goal=sub_goal, sequence=split_action_ls,action_list=split_action_ls)
        planning_algorithm.planning()

        planning_algorithm.create_anytree()

        sub_btml = BTML()
        sub_btml.cls_name = comp_act.name
        sub_btml.var_args = None
        sub_btml.anytree_root = planning_algorithm.anytree_root

        comp_actions_BTML_dic[comp_act.name] = sub_btml


    # 为每个智能体分配动作
    # 分配动作给智能体
    agent_actions = [[] for _ in range(num_agent)]
    for action in new_actions:
        # 随机选择至少一个智能体
        num_assignments = random.randint(1, num_agent)
        assigned_agents = random.sample(range(num_agent), num_assignments)
        for agent_index in assigned_agents:
            agent_actions[agent_index].append(action)
    # 检查每个智能体是否有动作，如果没有则随机分配一个动作
    for i in range(num_agent):
        if not agent_actions[i]:  # 如果该智能体没有被分配任何动作
            # 随机选择一个动作分配给这个智能体
            action_to_assign = random.choice(new_actions)
            agent_actions[i].append(action_to_assign)
    # 打印分配结果，查看每个智能体的动作列表
    for i, actions in enumerate(agent_actions):
        print(f"Agent {i + 1} actions:")
        for action in actions:
            print(f"  act:{action.name} pre:{action.pre} add:{action.add} del:{action.del_set}")


    # 运行多智能体算法
    from DMR import DMR
    dmr = DMR(goal, start, agent_actions, num_agent, with_comp_action=True)  # False 也还需要再调试
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
    print_colored(f"goal:{goal}", "blue")
    print("obs>=goal:",obs>=goal)



