import json
import sys
import time
import random
import math
import numpy as np
import pandas as pd
from mabtpg.algo.llm_client.llms.gpt3 import LLMGPT3
import gymnasium as gym
from mabtpg import MiniGridToMAGridEnv
from minigrid.core.world_object import Ball, Box,Door,Key
from mabtpg.utils import get_root_path
from mabtpg import BehaviorLibrary
root_path = get_root_path()
from itertools import permutations
import time
from mabtpg.utils.composite_action_tools import CompositeActionPlanner
from mabtpg.utils.tools import print_colored,filter_action_lists
from mabtpg.envs.gridenv.minigrid_computation_env.mini_comp_env import MiniCompEnv
from mabtpg.envs.virtualhome.envs.vh_computation_env import VHCompEnv
from mabtpg.envs.numerical_env.numsim_tools import create_directory_if_not_exists, print_action_data_table,print_summary_table

def bind_bt(bt_list):
    from mabtpg.behavior_tree.behavior_tree import BehaviorTree
    # new
    # bt_list = []
    # for i, agent in enumerate(planning_algorithm.planned_agent_list):
    #     bt = BehaviorTree(btml=btml_list[i], behavior_lib=behavior_lib[i])
    #     bt_list.append(bt)
    for i in range(env.num_agent):
        bt_list[i].save_btml(f"robot-{i}.bt")
        if bt_draw:
            bt_list[i].draw(file_name=f"agent-{i}")
    # bind the behavior tree to agents
    for i, agent in enumerate(env.agents):
        agent.bind_bt(bt_list[i])


json_path = "vh1.json"
with open(json_path, 'r') as file:
    json_datasets = json.load(file)


for _,json_data in enumerate(json_datasets[:1]):

    data_id = json_data['id']
    print_colored(f"========= data_id: {data_id} ===============","blue")
    goal = frozenset(json_data["goal"])
    start = set(json_data["init_state"])
    objects = json_data["objects"]
    action_space = json_data["action_space"]
    num_agent = len(action_space)

    for i in range(num_agent):
        start.add(f"IsRightHandEmpty(agent-{i})")
        start.add(f"IsLeftHandEmpty(agent-{i})")
    start = frozenset(start)


    # #########################
    # Initialize Environment
    # #########################
    env = VHCompEnv(num_agent=num_agent, goal=goal, start=start)
    env.objects = objects
    env.filter_objects_to_get_category(objects)

    env.with_comp_action = True # 是否有組合動作
    env.use_atom_subtask_chain = False # 是否使用任務鏈
    env.use_comp_subtask_chain = True  # 是否使用任務鏈

    bt_draw = True


    # #####################
    # get action model
    # #####################
    behavior_lib_path = f"{root_path}/envs/virtualhome/behavior_lib"
    behavior_lib = BehaviorLibrary(behavior_lib_path)

    agents_act_cls_ls = [[] for _ in range(num_agent)]
    for i,act_cls_name_ls in enumerate(action_space):
        for act_cls_name in act_cls_name_ls:
            act_cls = type(f"{act_cls_name}", (behavior_lib["Action"][act_cls_name],), {})
            agents_act_cls_ls[i].append(act_cls)

    for i, agent in enumerate(env.agents):
        agent.behavior_dict = {
            "Action": agents_act_cls_ls[i]+[behavior_lib["Action"]['SelfAcceptTask'],behavior_lib["Action"]['FinishTask']],
            "Condition": behavior_lib["Condition"].values(),
        }
        agent.create_behavior_lib()
    agent_actions_model = env.create_action_model()


    # #########################
    # Composition Action
    # Pre-plan get BTML and PlanningAction
    # #########################
    composition_action = []
    comp_actions_BTML_dic=None
    comp_agents_ls_dic = None
    if "composition_action" in json_data:
        composition_action = json_data["composition_action"]

        composition_action_flattened_dict = {}
        for sublist in composition_action:
            for item in sublist:
                composition_action_flattened_dict.update(item)

        if env.with_comp_action:
            cap = CompositeActionPlanner(agent_actions_model, composition_action_flattened_dict,env=env)
            cap.get_composite_action()
            # {'agent-0': [WalkToOpen(agent-0,fridge), WalkToOpen(agent-0,milk)], 'agent-1': []}
            comp_planning_act_dic = cap.comp_actions_dic
            # {'WalkToOpen': <mabtpg.behavior_tree.btml.BTML.BTML object at 0x000002156A9FECB0>}
            comp_actions_BTML_dic = cap.comp_actions_BTML_dic
            #
            comp_agents_ls_dic = cap.comp_agents_ls_dic

            for i in range(env.num_agent):
                agent_id = "agent-"+str(i)
                # agent_actions_model[i]=[] # if only composition action
                if agent_id in comp_planning_act_dic:
                    agent_actions_model[i].extend(comp_planning_act_dic["agent-"+str(i)])
                # sorted by cost
                agent_actions_model[i] = sorted(agent_actions_model[i], key=lambda x: x.cost)



    # #########################
    # Run Decentralized multi-agent BT algorithm
    # #########################
    # print_colored(f"Start Multi-Robot Behavior Tree Planning...", color="green")
    start_time = time.time()

    from mabtpg.btp.DMR import DMR
    dmr = DMR(env, goal, start, agent_actions_model, num_agent, with_comp_action=env.with_comp_action,
              save_dot=True)  # False 也还需要再调试
    dmr.planning()

    # print_colored(f"Finish Multi-Robot Behavior Tree Planning!", color="green")
    # print_colored(f"Time: {time.time() - start_time}", color="green")

    # Convert to BT and bind the BT to the agent
    behavior_lib = [agent.behavior_lib for agent in env.agents]
    dmr.get_btml_and_bt_ls(behavior_lib=behavior_lib,comp_actions_BTML_dic=comp_actions_BTML_dic,comp_agents_ls_dic=comp_agents_ls_dic)
    bind_bt(dmr.bt_ls)


    # calculate time and expanded num
    if env.with_comp_action:
        CABTP_expanded_num = 0
        record_expanded_num = CABTP_expanded_num + dmr.record_expanded_num
    else:
        CABTP_expanded_num = 0
        record_expanded_num = dmr.record_expanded_num
    expanded_time = dmr.expanded_time



    # #########################
    # Simulation
    # #########################
    print_colored(f"start: {start}", "blue")
    env.print_ticks = True
    env.verbose = True
    env.reset()
    done = False
    max_env_step = 50
    env_steps = 0
    new_env_step = 0
    agents_steps = 0
    obs = set(start)
    env.state = obs
    while not done:
        obs, done, _, _, agents_one_step, _ = env.step()
        env_steps += 1
        agents_steps += agents_one_step
        if env_steps % 50 == 0:
            print_colored(f"========= env_steps: {env_steps} ===============",
                          "blue")
            print_colored(f"state: {obs}", "blue")
        if obs >= goal:
            done = True
            break
        if env_steps >= max_env_step:
            break
    print(f"\ntask finished!")
    print_colored(f"goal:{goal}", "blue")
    if obs>=goal:
        print_colored(f"obs>=goal: {obs >= goal}",color="green")
    else:
        print_colored(f"obs>=goal: {obs >= goal}", color="red")
        sys.exit()
    print("env_steps:",env_steps, "expanded num:",record_expanded_num)
    print("expanded time:",dmr.expanded_time)

