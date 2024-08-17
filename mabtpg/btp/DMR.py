from mabtpg.utils.tools import print_colored
from mabtpg.btp.mabtp import MABTP
from mabtpg.btp.maobtp import MAOBTP
import numpy as np
import pandas as pd
import time
from mabtpg.behavior_tree.behavior_tree import BehaviorTree

class DMR:
    def __init__(self, env,goal, start, action_lists, num_agent=None, with_comp_action=False,save_dot=False,max_time_limit=20):
        self.env = env
        self.goal = goal
        self.start = start
        self.action_lists = action_lists
        self.num_agent = num_agent
        if num_agent != len(self.action_lists):
            print_colored(f"Error num_agent {num_agent} != len(self.action_lists) {len(self.action_lists)}!",color="red")

        self.planning_algorithm = None
        self.btml_ls = None
        self.bt_ls = None
        self.default_bt_ls=None

        self.with_comp_action = with_comp_action

        self.save_dot=save_dot
        self.record_expanded_num = 0
        self.expanded_time = 0
        self.max_time_limit = max_time_limit

    def planning(self):
        print_colored(f"Start Multi-Robot Behavior Tree Planning...", color="green")
        start_time = time.time()

        if not self.with_comp_action:
            # self.planning_algorithm = MABTP_test(verbose = False,start=self.start)
            self.planning_algorithm = MABTP(env=self.env,verbose=False, start=self.start,max_time_limit = self.max_time_limit)
            self.planning_algorithm.planning(frozenset(self.goal),action_lists=self.action_lists)
        else:
            # self.planning_algorithm = MAOBTP_test(verbose=False, start=self.start)
            self.planning_algorithm = MAOBTP(env=self.env,verbose=False, start=self.start,max_time_limit = self.max_time_limit)
            self.planning_algorithm.bfs_planning(frozenset(self.goal), action_lists=self.action_lists)


        print_colored(f"Finish Multi-Robot Behavior Tree Planning!", color="green")
        print_colored(f"Time: {time.time() - start_time}", color="green")

        self.record_expanded_num = self.planning_algorithm.record_expanded_num
        self.expanded_time = time.time() - start_time


    def get_btml_and_bt_ls(self,behavior_lib=None,comp_btml_ls=None, comp_planning_act_ls=None):
        # get btml and bt
        self.btml_ls = self.planning_algorithm.get_btml_list()
        self.bt_ls = []


        # add composition action
        if comp_planning_act_ls is not None:
            for agent_id in range(self.num_agent):
                self.btml_ls[agent_id].sub_btml_dict = comp_btml_ls[agent_id].sub_btml_dict

                if self.save_dot:
                    for name,sub_btml in self.btml_ls[agent_id].sub_btml_dict.items():
                        if sub_btml!=[]:
                            tmp_bt = BehaviorTree(btml=sub_btml, behavior_lib=behavior_lib[agent_id])
                            tmp_bt.draw(file_name = f"data/{agent_id}-{name}")


            # if comp_agents_ls_dic!=None:
            #
            #     for cmp_act_name, agent_id_ls in comp_agents_ls_dic.items():
            #         agent_id_ls = comp_agents_ls_dic[cmp_act_name]
            #
            #         for agent_id in agent_id_ls:
            #             agent = self.planning_algorithm.planned_agent_list[agent_id]
            #             btml = comp_actions_BTML_dic[cmp_act_name]
            #             self.btml_ls[agent_id].anytree_root = agent.anytree_root
            #             self.btml_ls[agent_id].sub_btml_dict[cmp_act_name] = btml
            #
            #             tmp_bt = BehaviorTree(btml=btml, behavior_lib=behavior_lib[agent_id])
            #             if self.save_dot:
            #                 tmp_bt.draw(file_name = f"data/{cmp_act_name}")


        for i in range(self.num_agent):
            bt = BehaviorTree(btml=self.btml_ls[i],behavior_lib=behavior_lib[i])
            self.bt_ls.append(bt)

            if self.save_dot:
                self.bt_ls[i].save_btml(f"robot-{i}.bt")
                self.bt_ls[i].draw(file_name=f"robot-{i}",png_only=True)
