import random
import pickle
from data_generate import DataGenerator
from mabtpg.envs.numerical_env.numerical_env.numsim_tools import create_directory_if_not_exists, print_action_data_table
from mabtpg.utils.tools import print_colored
import numpy as np

random.seed(0)
np.random.seed(0)

#  get data
num_data = 1

max_branch = 3 # 选多少个分支聚合
max_depth= 2

cmp_ratio = 0.5  # 组合动作占比
max_cmp_act_split = 3 # 每个组合被切成多少个原子动作
max_action_steps = 5 # 每个原子动作的最大步数

num_agent = 2

data_generator = DataGenerator(max_depth=max_depth,max_branch=max_branch, cmp_ratio=cmp_ratio,
                               max_action_steps = max_action_steps,
                               max_cmp_act_split=max_cmp_act_split, need_split_action=True)
datasets = [data_generator.generate_data() for _ in range(num_data)]

print("======================")

vaild_data = 0
max_vaild_data = 1

# with_comp_action = True

for data_id, dataset in enumerate(datasets[:1]):
    print_action_data_table(dataset['goal'], dataset['start'], dataset['actions_with_cmp'])
    data_generator.save_tree_as_dot(dataset, f'data/{data_id}_generated_tree.dot')
    print("data_id:", data_id)

    for with_comp_action in [True, False]:
        # 每个数据，再根据给定的智能体数量，得到 agents_actions
        agents_actions = data_generator.assign_actions_to_agents(dataset, num_agent, with_comp_action=with_comp_action)
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

        if dmr.expanded_time >= 5:
            continue

        # 计算的时候用 C(num)，模拟和输出用 num
        # #########################
        # Simulation
        # #########################
        # 要tick进行测试，能否从 start 到 goal。
        # 要几步
        from mabtpg.envs.numerical_env.numerical_env import NumEnv

        env = NumEnv(num_agent=num_agent, start=dataset['start_num'], goal=dataset['goal_num'])
        env.set_agent_actions(agents_actions)

        behavior_lib = [agent.behavior_lib for agent in env.agents]
        dmr.get_btml_and_bt_ls(behavior_lib=behavior_lib, comp_actions_BTML_dic=dataset['comp_actions_BTML_dic'])

        for i, agent in enumerate(env.agents):
            agent.bind_bt(dmr.bt_ls[i])

        print_colored(f"start: {dataset['start_num']}", "blue")
        env.print_ticks = True
        done = False
        max_env_step = 500
        env_step = 0
        total_agents_step = 0
        obs = set()
        while not done:
            print_colored("======================================================================================", "blue")
            obs, done, _, _, agents_step = env.step()
            env_step += 1
            total_agents_step += agents_step
            print_colored(f"state: {obs}", "blue")
            if env_step >= max_env_step:
                break
            if obs >= dataset['goal_num']:
                done = True
                break
        print(f"\ntask finished!")
        print_colored(f"goal:{dataset['goal_num']}", "blue")
        print("obs>=goal:", obs >= dataset['goal_num'])

        print("env_step:", env_step)
        print("total_agents_step:", total_agents_step)
        print("start:", start)

        # save data
        if done == True and (obs >= dataset['goal_num']):
            # Define the directory name based on the input parameters
            dir_name = f"vaild_data_depth={max_depth}_branch={max_branch}_cmpr={cmp_ratio}_cmpn={max_cmp_act_split}_agent={num_agent}"
            # Create the directory if it does not exist
            create_directory_if_not_exists(dir_name)

            with open(f"{dir_name}/id={vaild_data}.pkl", 'wb') as file:
                pickle.dump(dataset, file)
            data_generator.save_tree_as_dot(dataset, f'{dir_name}/id={vaild_data}_generated_tree.dot')
            vaild_data += 1

        if vaild_data >= max_vaild_data:
            break
