import random
import pickle
from data_generate import DataGenerator
from mabtpg.envs.numericenv.numsim_tools import create_directory_if_not_exists, print_action_data_table
from simulation import simulation
from mabtpg.utils.tools import print_colored
import numpy as np
random.seed(0)
np.random.seed(0)


num_data = 1


max_depth_ls = [2,3,5]
max_branch_ls  = [2,3,5]
num_agent_ls = [2,3,5]



cmp_ratio = 0.5  # 组合动作占比
max_cmp_act_split = 3 # 每个组合被切成多少个原子动作
max_action_steps = 5 # 每个原子动作的最大步数

for max_depth in max_depth_ls:
    for max_branch in max_branch_ls:
        for num_agent in num_agent_ls:

            data_generator = DataGenerator(max_depth=max_depth, max_branch=max_branch, cmp_ratio=cmp_ratio,
                                           max_action_steps=max_action_steps,
                                           max_cmp_act_split=max_cmp_act_split, need_split_action=True)
            datasets = [data_generator.generate_data() for _ in range(num_data)]
            print("====== Data Generated Finished! =========")

            for with_comp_action in [True,False]:

                for data_id, dataset in enumerate(datasets[:]):
                    print("data_id:", data_id)
                    if with_comp_action==True:
                        print_action_data_table(dataset['goal'], dataset['start'], dataset['actions_with_cmp'])
                        data_generator.save_tree_as_dot(dataset, f'data/{data_id}_generated_tree.dot')

                    agents_actions = data_generator.assign_actions_to_agents(dataset,num_agent,with_comp_action=with_comp_action)
                    goal = dataset['goal']
                    start = dataset['start']



                    # #########################
                    # Run Decentralized multi-agent BT algorithm
                    # #########################
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
                    success,env_steps,agents_step = simulation(dataset,num_agent,agents_actions,dmr)



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

