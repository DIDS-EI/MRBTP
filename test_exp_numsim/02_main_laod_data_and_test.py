import random
from data_generate import DataGenerator
from mabtpg.envs.numericenv.numsim_tools import load_data_from_directory
from mabtpg.utils.tools import print_colored
import numpy as np
import csv

random.seed(0)
np.random.seed(0)


def simulation():
    start = dataset["start_num"]
    goal = dataset["goal_num"]
    from mabtpg.envs.numericenv.numeric_env import NumericEnv
    env = NumericEnv(num_agent=num_agent,start=start,goal=goal)
    env.set_agent_actions(agents_actions)

    behavior_lib = [agent.behavior_lib for agent in env.agents]
    dmr.get_btml_and_bt_ls(behavior_lib=behavior_lib,comp_actions_BTML_dic=dataset['comp_actions_BTML_dic'])

    for i,agent in enumerate(env.agents):
        agent.bind_bt(dmr.bt_ls[i])


    print_colored(f"start: {start}", "blue")
    env.print_ticks = True
    done = False
    max_env_step=20
    env_steps = 0
    new_env_step = 0
    agents_steps=0
    obs = set()
    while not done:
        print_colored("======================================================================================","blue")
        obs,done,_,_,agents_one_step = env.step()
        env_steps += 1
        agents_steps += agents_one_step
        print_colored(f"state: {obs}","blue")
        if obs>=goal:
            done = True
            break
        if env_steps>=max_env_step:
            break
    print(f"\ntask finished!")
    print_colored(f"goal:{goal}", "blue")
    print("obs>=goal:",obs>=goal)
    if obs>=goal:
        done = True

    return done,env_steps,agents_steps




max_depth = 1


max_branch = 5
max_leaves = 20

cmp_ratio = 0.5
max_cmp_act_split = 5


num_agent = 2

# Define the directory name based on the input parameters
dir_name = f"vaild_data_leaf={max_leaves}_branch={max_branch}_cmpr={cmp_ratio}_cmpn={max_cmp_act_split}_agent={num_agent}"
data_generator = DataGenerator(max_depth=max_depth, max_branch=max_branch,max_leaves=max_leaves,cmp_ratio=cmp_ratio,max_cmp_act_split=max_cmp_act_split,need_split_action=True)
# Load data from the directory
loaded_data = load_data_from_directory(dir_name)
print(f"Loaded {len(loaded_data)} data files.")


# Initialize variables to calculate averages
total_CABTP_record_expanded_num = 0
total_record_expanded_num = 0
total_expanded_time = 0
total_success = 0
total_env_steps = 0
total_agents_step = 0
total_entries = 0

results = []
with_comp_action = True

for data_id,dataset in enumerate(loaded_data[:]):

    print("data_id:", data_id)


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

    if with_comp_action:
        CABTP_expanded_num=dataset['CABTP_expanded_num']
        record_expanded_num = dataset['CABTP_expanded_num'] + dmr.record_expanded_num
    else:
        CABTP_expanded_num=0
        record_expanded_num = dmr.record_expanded_num
    expanded_time = dmr.expanded_time

    # #########################
    # Simulation
    # #########################
    # 要tick进行测试，能否从 start 到 goal。
    # 要几步
    success,env_steps,agents_step = simulation()

    # #########################
    # Evaluation
    # #########################
    # Record results
    results.append({
        'CABTP_expanded_num':CABTP_expanded_num,
        'record_expanded_num': record_expanded_num,
        'expanded_time': expanded_time,
        'success': success,
        'env_steps': env_steps,
        'agents_step': agents_step
    })

    # Update totals
    total_success += 1 if success else 0
    # if success:
    total_CABTP_record_expanded_num += CABTP_expanded_num
    total_record_expanded_num += record_expanded_num
    total_expanded_time += expanded_time

    total_env_steps += env_steps
    total_agents_step += agents_step
    total_entries += 1


# 统计 队列中扩展的次数
# 统计每个智能体 action 的总步数
# 统计 env 的总步数
# 统计成功率是不是百分百

# Calculate averages
average_CABTP_record_expanded_num = total_CABTP_record_expanded_num / total_entries if total_entries > 0 else 0
average_record_expanded_num = total_record_expanded_num / total_entries if total_entries > 0 else 0
average_expanded_time = total_expanded_time / total_entries if total_entries > 0 else 0
success_rate = total_success / len(loaded_data) if len(loaded_data) > 0 else 0
average_env_steps = total_env_steps / total_entries if total_entries > 0 else 0
average_agents_step = total_agents_step / total_entries if total_entries > 0 else 0

# Output results
print(f"Average CABTP_expanded_num: {average_CABTP_record_expanded_num}")
print(f"Average record_expanded_num: {average_record_expanded_num}")
print(f"Average expanded_time: {average_expanded_time}")
print(f"Success rate: {success_rate}")
print(f"Average env_steps: {average_env_steps}")
print(f"Average agents_step: {average_agents_step}")

# Save results to CSV
csv_file_name = f"{dir_name}_cmp={with_comp_action}.csv"
with open(csv_file_name, 'w', newline='') as csvfile:
    fieldnames = ['CABTP_expanded_num','record_expanded_num', 'expanded_time', 'success', 'env_steps', 'agents_step']
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

    writer.writeheader()
    for result in results:
        writer.writerow(result)

print(f"Results saved to {csv_file_name}")



