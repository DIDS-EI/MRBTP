from mabtpg.utils.tools import print_colored
from mabtpg.btp.mabtp import MABTP
from mabtp_test import MABTP_test
from maobtp_test import MAOBTP_test
import numpy as np
import pandas as pd
import time
from mabtpg.behavior_tree.behavior_tree import BehaviorTree

class DMR:
    def __init__(self, goal, start, action_lists, num_agent=None, with_comp_action=False):
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

    def planning(self):
        print_colored(f"Start Multi-Robot Behavior Tree Planning...", color="green")
        start_time = time.time()

        if not self.with_comp_action:
            self.planning_algorithm = MABTP_test(verbose = False)
            self.planning_algorithm.planning(frozenset(self.goal),action_lists=self.action_lists)
        else:
            self.planning_algorithm = MAOBTP_test(verbose=False, start=self.start)
            self.planning_algorithm.bfs_planning(frozenset(self.goal), action_lists=self.action_lists)


        print_colored(f"Finish Multi-Robot Behavior Tree Planning!", color="green")
        print_colored(f"Time: {time.time() - start_time}", color="green")


    def get_btml_and_bt_ls(self,behavior_lib=None,comp_actions_BTML_dic=None):
        # get btml and bt
        self.btml_ls = self.planning_algorithm.get_btml_list()
        self.bt_ls = []


        # add composition action
        if comp_actions_BTML_dic is not None:
            for i,agent in enumerate(self.planning_algorithm.planned_agent_list):
                for j, (name, btml) in enumerate(comp_actions_BTML_dic.items()):
                    self.btml_ls[i].anytree_root = agent.anytree_root
                    self.btml_ls[i].sub_btml_dict[name] = btml

                    tmp_bt = BehaviorTree(btml=btml, behavior_lib=behavior_lib[i])
                    tmp_bt.draw(file_name = f"data/{name}")

        for i in range(self.num_agent):
            bt = BehaviorTree(btml=self.btml_ls[i],behavior_lib=behavior_lib[i])
            self.bt_ls.append(bt)

            self.bt_ls[i].save_btml(f"robot-{i}.bt")
            self.bt_ls[i].draw(file_name=f"robot-{i}")
