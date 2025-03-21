from mabtpg.behavior_tree.utils import Status
from mabtpg.behavior_tree.behavior_library import BehaviorLibrary
import copy
from mabtpg.utils.tools import print_colored

class Agent(object):
    behavior_dict = {
        "Action": [],
        "Condition": []
    }
    response_frequency = 1

    def __init__(self,env=None,id=0,behavior_lib=None):
        super().__init__()
        self.env = env
        self.id = id
        if behavior_lib:
            self.behavior_lib = behavior_lib
        else:
            self.create_behavior_lib()

        self.bt = None
        self.bt_success = None

        self.position = (-1, -1)
        self.direction = 3
        self.carrying = None

        self.condition_set = set()
        self.init_statistics()

        self.last_tick_output = None

        self.last_accept_task = None
        self.last_accept_composite_task = None
        self.current_task = None
        self.current_composite_task = None
        self.predict_condition = {
            "success":set(),
            "fail":set(),
        }

        self.last_action = None
        self.verbose = True


    def init_statistics(self):
        self.step_num = 1
        self.next_response_time = self.response_frequency
        self.last_tick_output = None

    def create_behavior_lib(self):
        self.behavior_lib = BehaviorLibrary()
        self.behavior_lib.load_from_dict(self.behavior_dict)

    @property
    def agent_id(self):
        return f'agent-{self.id}'

    def bind_bt(self,bt):
        self.bt = bt
        bt.bind_agent(self)


    def step(self, action=None,verbose=True):
        self.verbose=verbose
        self.action = None

        self.dong_accept_task=False
        tick_time = 0

        if action is None:
            if self.bt:

                while self.dong_accept_task or tick_time==0:
                    tick_time += 1
                    self.dong_accept_task = False

                    self.current_task = None

                    self.bt.tick(verbose=True,bt_name=f'{self.agent_id} tick_time={tick_time} bt')
                    self.bt_success = self.bt.root.status == Status.SUCCESS

                    # print_colored(f"cur: {self.current_task}", color='orange')
                    # print_colored(f"accp: {self.last_accept_task} ", color='orange')

                    if self.current_task != self.last_accept_task:
                        self.finish_current_task()
                        self.update_current_task()

                        if self.current_task != None:
                            self.dong_accept_task = True


                        # if self.current_task!=None:
                        #     self.bt.tick(verbose=True, bt_name=f'Twice {self.agent_id} bt')
                        #     self.bt_success = self.bt.root.status == Status.SUCCESS

        else:
            self.action = action
        return self.action


    def finish_current_task(self):
        # 上次有任务完成了
        if self.last_accept_task != None:
            if self.env.verbose: print_colored(f"Have Finish Last Task! last_accept_task = {self.last_accept_task}", color='orange')

            try:
                # self.env.blackboard["task_agents_queue"].remove(self)  # 直接移除对象
                index = self.env.blackboard["task_agents_queue"].index(self)  # 查找 self 的索引
                self.env.blackboard["task_agents_queue"].pop(index)  # 通过索引移除

                # 更新队列里所有智能体的假设空间
                last_predict_condition = {
                    "success": set(),
                    "fail": set(),
                }
                last_sub_goal = set()
                last_sub_del = set()
                for i, agent in enumerate(self.env.blackboard["task_agents_queue"]):
                    if i == 0:
                        agent.predict_condition = {
                            "success": set(),
                            "fail": set(),
                        }
                    else:
                        agent.predict_condition["success"] = (last_predict_condition[
                                                                  "success"] | last_sub_goal) - last_sub_del
                        agent.predict_condition["fail"] = (last_predict_condition[
                                                               "fail"] | last_sub_del) - last_sub_goal

                    last_predict_condition = agent.predict_condition
                    if agent.current_task!=None: #new 0806
                        last_sub_goal = agent.current_task["sub_goal"]
                        last_sub_del = agent.current_task["sub_del"]
                    else:
                        last_sub_goal=set()
                        last_sub_del=set()

                # 更新队列外面的智能体的假设空间
                self.env.blackboard["predict_condition"]["success"] = (last_predict_condition[
                                                                           "success"] | last_sub_goal) - last_sub_del
                self.env.blackboard["predict_condition"]["fail"] = (last_predict_condition[
                                                                        "fail"] | last_sub_del) - last_sub_goal
                for agent in self.env.agents:
                    if agent not in self.env.blackboard["task_agents_queue"]:
                        agent.predict_condition = self.env.blackboard["predict_condition"]

                self.env.communication_times += 1

            except ValueError:
                if self.env.verbose: print("The agent is not in the queue.")  # self 不在队列中
                for agent in self.env.agents:
                    if agent not in self.env.blackboard["task_agents_queue"]:
                        agent.predict_condition = self.env.blackboard["predict_condition"]
            except IndexError:
                if self.env.verbose: print("Index out of range.")  # 索引超出范围，理论上不会发生，因为索引是从 list.index 获取的



    def update_current_task(self):

        # 把最新的任务加到队尾
        if self.current_task != None:
            self.env.blackboard["task_agents_queue"].append(self)
            self.predict_condition = copy.deepcopy(self.env.blackboard["predict_condition"])

            # now the new_predict_condition
            self.env.blackboard["predict_condition"]["success"] = (self.env.blackboard["predict_condition"]["success"] |
                                                                   self.current_task["sub_goal"]) - self.current_task[
                                                                      "sub_del"]
            self.env.blackboard["predict_condition"]["fail"] = (self.env.blackboard["predict_condition"]["fail"] |
                                                                self.current_task["sub_del"]) - self.current_task[
                                                                   "sub_goal"]
            for agent in self.env.agents:
                if agent != self and agent not in self.env.blackboard["task_agents_queue"]:
                    agent.predict_condition = copy.deepcopy(self.env.blackboard["predict_condition"])
            self.env.communication_times += 1

        self.last_accept_task = copy.deepcopy(self.current_task)