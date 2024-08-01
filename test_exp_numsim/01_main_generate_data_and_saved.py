import random
import pickle
from data_generate import DataGenerator
from mabtpg.envs.numericenv.numsim_tools import create_directory_if_not_exists,print_action_data_table
from mabtpg.utils.tools import print_colored
import numpy as np

random.seed(0)
np.random.seed(0)

#  get data
num_data = 200
max_depth = 1


max_branch = 5
max_leaves = 20

cmp_ratio = 0.5
max_cmp_act_split = 5


num_agent = 2


data_generator = DataGenerator(max_depth=max_depth, max_branch=max_branch,max_leaves=max_leaves,cmp_ratio=cmp_ratio,max_cmp_act_split=max_cmp_act_split,need_split_action=True)
datasets = [data_generator.generate_dataset() for _ in range(num_data)]

print("======================")

vaild_data = 0
max_vaild_data = 100

for data_id,dataset in enumerate(datasets[:]):
    print_action_data_table(dataset['goal'], dataset['start'], dataset['actions_with_cmp'])
    data_generator.save_tree_as_dot(dataset, f'data/{data_id}_generated_tree.dot')

    print("data_id:", data_id)
    with_comp_action = False

    # 每个数据，再根据给定的智能体数量，得到 agents_actions
    agents_actions = data_generator.assign_actions_to_agents(dataset,num_agent,with_comp_action=with_comp_action)
    goal = dataset['goal']
    start = dataset['start']


    # #########################
    # Run Decentralized multi-agent BT algorithm
    # #########################
    # 运行多智能体算法
    from DMR import DMR
    dmr = DMR(goal, start, agents_actions, num_agent, with_comp_action=with_comp_action,save_dot=False)  # False 也还需要再调试
    dmr.planning()

    if dmr.expanded_time >= 5:
        continue

    # 计算的时候用 C(num)，模拟和输出用 num
    # #########################
    # Simulation
    # #########################
    # 要tick进行测试，能否从 start 到 goal。
    # 要几步
    from mabtpg.envs.numericenv.numeric_env import NumericEnv
    env = NumericEnv(num_agent=num_agent,start=dataset['start_num'],goal=dataset['goal_num'])
    env.set_agent_actions(agents_actions)

    behavior_lib = [agent.behavior_lib for agent in env.agents]
    dmr.get_btml_and_bt_ls(behavior_lib=behavior_lib,comp_actions_BTML_dic=dataset['comp_actions_BTML_dic'])

    for i,agent in enumerate(env.agents):
        agent.bind_bt(dmr.bt_ls[i])

    print_colored(f"start: {dataset['start_num']}", "blue")
    env.print_ticks = True
    done = False
    max_env_step=20
    env_step = 0
    total_agents_step = 0
    obs = set()
    while not done:
        print_colored("======================================================================================","blue")
        obs,done,_,_,agents_step = env.step()
        env_step += 1
        total_agents_step += agents_step
        print_colored(f"state: {obs}","blue")
        if env_step>=max_env_step:
            break
        if obs>=dataset['goal_num']:
            done = True
            break
    print(f"\ntask finished!")
    print_colored(f"goal:{dataset['goal_num']}", "blue")
    print("obs>=goal:",obs>=dataset['goal_num'])

    print("env_step:",env_step)
    print("total_agents_step:",total_agents_step)
    print("start:",start)

    # save data
    if done==True and (obs>=dataset['goal_num']):
        # Define the directory name based on the input parameters
        dir_name = f"vaild_data_leaf={max_leaves}_branch={max_branch}_cmpr={cmp_ratio}_cmpn={max_cmp_act_split}_agent={num_agent}"
        # Create the directory if it does not exist
        create_directory_if_not_exists(dir_name)

        with open(f"{dir_name}/id={vaild_data}.pkl", 'wb') as file:
            pickle.dump(dataset, file)
        data_generator.save_tree_as_dot(dataset, f'{dir_name}/id={vaild_data}_generated_tree.dot')
        vaild_data+=1

    if vaild_data>=max_vaild_data:
        break



