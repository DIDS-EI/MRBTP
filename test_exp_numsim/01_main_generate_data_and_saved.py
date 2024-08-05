import random
import pickle
from data_generate import DataGenerator
from mabtpg.envs.numerical_env.numsim_tools import create_directory_if_not_exists, print_action_data_table
import numpy as np
from simulation import simulation
random.seed(0)
np.random.seed(0)




max_depth= 2
max_branch = 3 # 选多少个分支聚合
num_agent = 2

cmp_ratio = 0.5  # 组合动作占比
max_cmp_act_split = 3 # 每个组合被切成多少个原子动作
max_action_steps = 2 # 每个原子动作的最大步数


#  get data
max_num_data = 1
data_generator = DataGenerator(max_depth=max_depth,max_branch=max_branch, cmp_ratio=cmp_ratio,
                               max_action_steps = max_action_steps,
                               max_cmp_act_split=max_cmp_act_split, need_split_action=True,max_num_data=max_num_data)
# datasets = [data_generator.generate_data() for _ in range(num_data)]

print("======================")

valid_data = 0
max_valid_data = 1

data_id = 0
# with_comp_action = True

for dataset in data_generator.datasets:
    print_action_data_table(dataset['goal'], dataset['start'], dataset['actions_cmp'])
    data_generator.save_tree_as_dot(dataset, f'data/{data_id}_generated_tree.dot')
    print("data_id:", data_id)
    if data_id==5:
        xx=1
    data_id+=1

    all_success = True
    for with_comp_action in [True,False]: #False,
        # 每个数据，再根据给定的智能体数量，得到 agents_actions
        # agents_actions = data_generator.assign_actions_to_agents(dataset, num_agent)
        if with_comp_action:
            agents_actions = dataset["agent_actions_with_cmp"]
        else:
            agents_actions = dataset["agent_actions_without_cmp"]

        # for act_ls in  agents_actions:
        #     for act in act_ls:
        #         act.cost = 0

        goal = dataset['goal']
        start = dataset['start']

        # #########################
        # Run Decentralized multi-agent BT algorithm
        # #########################
        # 运行多智能体算法
        from DMR import DMR

        dmr = DMR(goal, start, agents_actions, num_agent, with_comp_action=with_comp_action,
                  save_dot=False)  # False 也还需要再调试
        dmr.planning()

        # if dmr.expanded_time >= 5:
        #     continue

        # #########################
        # Simulation
        # #########################
        if dmr.expanded_time <= 10:
            success, env_steps, agents_step = simulation(dataset, num_agent, agents_actions, dmr)
        else:
            all_success = False
            break


    # save data
    if all_success:
        dir_name = f"valid_data_depth={max_depth}_branch={max_branch}_agent={num_agent}_cmpr={cmp_ratio}_cmpn={max_cmp_act_split}_cmpstp={max_action_steps}"
        create_directory_if_not_exists(dir_name)
        with open(f"{dir_name}/id={valid_data}.pkl", 'wb') as file:
            pickle.dump(dataset, file)
        data_generator.save_tree_as_dot(dataset, f'{dir_name}/id={valid_data}_generated_tree.dot')
        valid_data += 1

    if valid_data >= max_valid_data:
        break

print("valid_data < max_valid_data:",valid_data < max_valid_data)
print("max_valid_data:",max_valid_data)
print("valid_data:",valid_data)