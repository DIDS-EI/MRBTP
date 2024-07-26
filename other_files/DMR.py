from mabtpg.utils.tools import print_colored
from mabtpg.btp.mabtp import MABTP
from mabtp_test import MABTP_test
import numpy as np
import pandas as pd
import time
from mabtpg.behavior_tree.behavior_tree import BehaviorTree

class DMR:
    def __init__(self, goal, start, action_lists, num_agent=None):
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

    def planning(self):
        print_colored(f"Start Multi-Robot Behavior Tree Planning...", color="red")
        start_time = time.time()

        self.planning_algorithm = MABTP_test(verbose = False)
        self.planning_algorithm.planning(frozenset(self.goal),action_lists=self.action_lists)

        print_colored(f"Finish Multi-Robot Behavior Tree Planning!", color="red")
        print_colored(f"Time: {time.time() - start_time}", color="red")


        # get default bt
        self.default_bt_ls = self.planning_algorithm.create_default_bt()


    def get_btml_and_bt_ls(self):
        # get btml and bt
        self.btml_ls = self.planning_algorithm.get_btml_list()
        self.bt_ls = []
        for i in range(self.num_agent):
            bt = BehaviorTree(btml=self.btml_ls[i])
            self.bt_ls.append(bt)

            self.bt_ls[i].save_btml(f"robot-{i}.bt")
            self.bt_ls[i].draw(file_name=f"robot-{i}")
