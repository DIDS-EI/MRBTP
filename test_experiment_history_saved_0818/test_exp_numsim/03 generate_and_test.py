import random
# from data_generate import DataGenerator
from mabtpg.envs.numerical_env.numerical_env.numsim_tools import print_action_data_table
from simulation import simulation
from mabtpg.utils.tools import *
import numpy as np
from mabtpg.envs.numerical_env.numerical_env.numsim_tools import load_data_from_directory,save_tree_as_dot
random.seed(0)
np.random.seed(0)


num_data = -1


# max_depth_ls = [2,3,5]
# max_branch_ls  = [2,3,5]
# num_agent_ls = [2,3,5]

max_depth_ls = [2]
max_branch_ls  = [3]
num_agent_ls = [2]


cmp_ratio = 0.5  # 组合动作占比
max_cmp_act_split = 3 # 每个组合被切成多少个原子动作
max_action_steps = 2 # 每个原子动作的最大步数


results = []
summary_results = []

for max_depth in max_depth_ls:
    for max_branch in max_branch_ls:
        for num_agent in num_agent_ls:
            print_colored(f"Processing: max_depth={max_depth}, max_branch={max_branch}, num_agent={num_agent}", "blue")

            # Define the directory name based on the input parameters
            dir_name = f"valid_data_depth={max_depth}_branch={max_branch}_agent={num_agent}_cmpr={cmp_ratio}_cmpn={max_cmp_act_split}_cmpstp={max_action_steps}"
            loaded_data = load_data_from_directory(dir_name)
            # data_generator = DataGenerator(max_depth=max_depth, max_branch=max_branch, cmp_ratio=cmp_ratio,
            #                                max_action_steps=max_action_steps,
            #                                max_cmp_act_split=max_cmp_act_split, need_split_action=True)
            print(f"Loaded {len(loaded_data)} data files.")
            print("====== Data Generated Finished! =========")

            for with_comp_action in [False,True]:

                print_colored(f"Algorithm: with_comp_action={with_comp_action}","blue")

                totals = {
                    'action_num': 0,
                    'CABTP_expanded_num': 0,
                    'record_expanded_num': 0,
                    'expanded_time': 0,
                    'success': 0,
                    'env_steps': 0,
                    'agents_step': 0
                }
                total_entries = 0

                for data_id, dataset in enumerate(loaded_data[:]):
                    print("data_id:", data_id, "actions num:",dataset["action_num"])
                    if with_comp_action==True:
                        print_action_data_table(dataset['goal'], dataset['start'], dataset['actions_cmp'])
                        save_tree_as_dot(dataset, f'data/{data_id}_generated_tree.dot')

                    # agents_actions = data_generator.assign_actions_to_agents(dataset, num_agent)
                    if with_comp_action:
                        agents_actions = dataset["agent_actions_with_cmp"]
                    else:
                        agents_actions = dataset["agent_actions_without_cmp"]

                    ##################
                    # for act_ls in agents_actions:
                    #     for act in act_ls:
                    #         act.cost = 0
                    ###############

                    goal = dataset['goal']
                    start = dataset['start']



                    # #########################
                    # Run Decentralized multi-agent BT algorithm
                    # #########################
                    from mabtpg.btp.DMR import DMR
                    dmr = DMR(goal, start, agents_actions, num_agent, with_comp_action=with_comp_action,save_dot=False)  # False 也还需要再调试
                    dmr.planning()

                    # dmr.expanded_time?

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
                    if dmr.expanded_time<=10:
                        success,env_steps,agents_step = simulation(dataset,num_agent,agents_actions,dmr)
                    else:
                        success, env_steps, agents_step = False, 50, 50 #???
                        print_colored(f"-------- Time Out ---------", "red")



                    # #########################
                    # Evaluation
                    # #########################
                    # Record results
                    totals['action_num'] += dataset['action_num']
                    totals['CABTP_expanded_num'] += CABTP_expanded_num
                    totals['record_expanded_num'] += record_expanded_num
                    totals['expanded_time'] += expanded_time
                    totals['success'] += int(success)
                    totals['env_steps'] += env_steps
                    totals['agents_step'] += agents_step
                    total_entries += 1

                    results.append({
                        'data_id': data_id,
                        'max_depth': max_depth,
                        'max_branch': max_branch,
                        'num_agent': num_agent,
                        'with_comp_action': with_comp_action,
                        'CABTP_expanded_num': CABTP_expanded_num,
                        'record_expanded_num': record_expanded_num,
                        'expanded_time': expanded_time,
                        'success': success,
                        'env_steps': env_steps,
                        'agents_step': agents_step,
                        'action_num': dataset['action_num']
                    })

                if total_entries > 0:
                    append_summary_results(results, summary_results, max_depth, max_branch, num_agent, with_comp_action,
                                           total_entries, totals)

            detailed_csv_filename = f'detailed_results_depth_{max_depth}_branch_{max_branch}_agents_{num_agent}.csv'
            summary_csv_filename = f'summary_results_depth_{max_depth}_branch_{max_branch}_agents_{num_agent}.csv'
            save_results_to_csv(results, detailed_csv_filename)
            save_results_to_csv(summary_results, summary_csv_filename)

# Print summary table in both formats
print_summary_table(summary_results, formatted=True)
print_summary_table(summary_results, formatted=False)
