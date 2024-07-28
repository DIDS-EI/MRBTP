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

        self.accept_task = None
        self.current_task = None
        self.last_accept_task = None


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


    def step(self, action=None):
        self.action = None

        if action is None:
            if self.bt:

                self.current_task = None

                self.bt.tick(verbose=True,bt_name=f'{self.agent_id} bt')
                self.bt_success = self.bt.root.status == Status.SUCCESS

                print(f"cur: {self.current_task}")

                print_colored(f"accp: {self.accept_task} ", color='orange')
                print_colored(f"last: {self.last_accept_task}", color='orange')
                if self.current_task != self.accept_task and self.last_accept_task != None:
                    print_colored(f"Have Finish Last Task! cur_task = {self.current_task}", color='orange')

                    self.env.blackboard["predict_condition"] -= self.last_accept_task["subgoal"]
                    # 先遍历这个键值，删除里面对应的任务里 depend
                    task_key = (self.last_accept_task["task_id"], self.last_accept_task["subgoal"])

                    # 如果有受它依赖的任务，那么解除这些任务的依赖
                    print_colored(f"Task Dependency: {self.env.blackboard['dependent_tasks_dic']}", color='orange')
                    if task_key in self.env.blackboard["dependent_tasks_dic"]:
                        successor_tasks = self.env.blackboard["dependent_tasks_dic"][task_key]
                        for st in successor_tasks:
                            self.env.blackboard["task_predict_condition"][st] -= self.last_accept_task["subgoal"]
                            print_colored("Release Task Dependency....", color='orange')
                            print_colored(f"{st} \t {self.env.blackboard['task_predict_condition'][st]}",
                                          color='orange')
                        # 这个任务的记录，删除记录依赖
                        del self.env.blackboard["dependent_tasks_dic"][task_key]

                self.last_accept_task = copy.deepcopy(self.accept_task)




        else:
            self.action = action
        return self.action

