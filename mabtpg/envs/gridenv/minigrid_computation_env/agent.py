from mabtpg.behavior_tree.utils import Status
from mabtpg.behavior_tree.behavior_library import BehaviorLibrary
import copy
from mabtpg.utils.tools import print_colored
from mabtpg.envs.numerical_env.agent import Agent as NumAgent

class Agent(NumAgent):
    def __init__(self,env=None,id=0,behavior_lib=None):
        super().__init__(env,id,behavior_lib)

        self.behavior_dict = {
            "Action": [],
            "Condition": []
        }

        self.is_fail = False


    def step(self, action=None):
        self.action = None

        self.dong_accept_task=False
        tick_time = 0



        if action is None:
            if self.bt:

                    tick_time += 1
                    self.dong_accept_task = False

                    self.current_task = None

                    self.bt.tick(verbose=True,bt_name=f'{self.agent_id} tick_time={tick_time} bt')
                    self.bt_success = self.bt.root.status == Status.SUCCESS

                    # print_colored(f"cur: {self.current_task}", color='orange')
                    # print_colored(f"accp: {self.last_accept_task} ", color='orange')

                    if self.env.use_atom_subtask_chain:

                        if self.last_action != None and self.last_action.is_finish:

                            # print("self.last_action:",self.last_action)
                            # print("current_task:", self.current_task)

                            self.finish_current_task()
                            self.env.communication_times += 1

                            if self.last_action!=None:
                                self.last_action.is_finish = False
                            self.last_action = None

                        if self.current_task != self.last_accept_task:
                            self.update_current_task()
                            self.env.communication_times += 1


                    # if self.current_task != self.last_accept_task:
                    #     self.finish_current_task()
                    #     self.update_current_task()
                    #
                    #     if self.last_action!=None:
                    #         self.last_action.is_finish = False
                    #     self.last_action = None

        else:
            self.action = action

        return self.action


    def create_behavior_lib(self):
        self.behavior_lib = BehaviorLibrary()
        self.behavior_lib.load_from_dict(self.behavior_dict)
