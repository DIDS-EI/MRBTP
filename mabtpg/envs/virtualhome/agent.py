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
        self.act_cur_step = 0


    def step(self, action=None):
        self.action = None

        self.dong_accept_task=False
        tick_time = 0

        if action is None:
            if self.bt:

                while self.dong_accept_task or tick_time==0:
                    tick_time += 1
                    self.dong_accept_task = False

                    self.current_task = None
                    self.current_composite_task = None

                    self.bt.tick(verbose=True,bt_name=f'{self.agent_id} tick_time={tick_time} bt')
                    self.bt_success = self.bt.root.status == Status.SUCCESS

                    # print_colored(f"cur: {self.current_task}", color='orange')
                    # print_colored(f"accp: {self.last_accept_task} ", color='orange')


                    if self.current_composite_task is not None:
                        self.current_task = self.current_composite_task
                        # 組合動作中的最後一個原子動作也完成 = 組合動作已經完成
                        if self.current_task["sub_goal"] <= self.env.state and (
                                (self.current_task["sub_del"] & self.env.state) == set()):
                            self.current_task = None
                    # 判斷原子動作是否完成
                    elif self.last_action != None and self.last_action.is_finish:

                        # print("self.last_action:",self.last_action)
                        # print("current_task:", self.current_task)

                        self.current_task = None
                        if self.last_action!=None:
                            self.last_action.is_finish = False
                        self.last_action = None


                    # 更新 假設空間
                    if self.current_task != self.last_accept_task:
                        if self.current_composite_task is None: # 如果是原子動作，
                            if self.env.use_atom_subtask_chain:
                                self.finish_current_task()
                                self.update_current_task()
                            else:
                                self.last_accept_task = copy.deepcopy(self.current_task) # 不用任務連就需要更新
                        else:
                            if self.env.use_comp_subtask_chain:
                                self.finish_current_task()
                                self.update_current_task()
                            else:
                                self.last_accept_task = copy.deepcopy(self.current_task)


                        # 判斷要不要再循環 tick
                        if self.current_task != None:
                            self.dong_accept_task = True

                    if self.current_composite_task is None:
                        break

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
