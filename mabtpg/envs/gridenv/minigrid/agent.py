from minigrid.core.actions import Actions
from mabtpg.behavior_tree.utils import Status

class Agent(object):
    def __init__(self,env=None,id=0):
        self.env = env
        self.id = id
        self.subgoal = None
        self.subtree = None

        self.behavior_lib = None

        self.action = Actions.done
        self.bt_success = None

        self.position = (-1, -1)
        self.direction = -1
        self.carrying = None

        self.last_tick_output = None

        self.accept_task = None
        self.current_task = None

    def planning_for_subgoal(self,subgoal):
        from mabtpg.btp.pbtp import PBTP

        if self.env.action_lists is None:
            self.env.action_lists = self.env.get_action_lists()

        subgoal_set = self.env.blackboard['subgoal_map'][subgoal]
        precondition = frozenset(self.env.blackboard['precondition'])

        action_list = self.env.action_lists[self.id]

        planning_algorithm = PBTP(action_list,subgoal_set,verbose=False,precondition=precondition)
        planning_algorithm.planning()
        bt = planning_algorithm.output_bt(self.behavior_lib)

        bt.bind_agent(self)
        self.subtree = bt

        print('-----------------')
        print(f'{self.agent_id} planning for {subgoal}: {subgoal_set}, output bt:')
        bt.print()
        bt.draw(f'{self.agent_id} {subgoal}')



    @property
    def agent_id(self):
        return f'agent-{self.id}'

    def bind_bt(self,bt):
        self.bt = bt
        bt.bind_agent(self)

    def step(self):
        self.action = Actions.done
        self.bt.tick(verbose=True,bt_name=f'{self.agent_id} bt')
        print("cur",self.current_task,"acp",self.accept_task)
        if self.current_task != self.accept_task:
            if self.current_task!=None:

                self.env.blackboard["predict_condition"] -= self.current_task["subgoal"]

                # 先遍历这个键值，删除里面对应的任务里 depend
                task_key = (self.current_task["task_id"],self.current_task["subgoal"])
                # 如果有受它依赖的任务，那么解除这些任务的依赖
                if task_key in self.env.blackboard["dependent_tasks_dic"]:
                    successor_tasks = self.env.blackboard["dependent_tasks_dic"][task_key]
                    for st in successor_tasks:
                        self.env.blackboard["task_predict_condition"][st] -= self.current_task["subgoal"]
                    # 这个任务的记录，删除记录依赖
                    del self.env.blackboard["dependent_tasks_dic"][task_key]



                # self.env.blackboard["premise_dep2subgoal"] = {k: v for k, v in self.env.blackboard["premise_dep2subgoal"].items() if v != \
                #                                               (self.current_task["task_id"],self.current_task["subgoal"])}
                    # if self.current_task["subgoal"] in self.env.blackboard["condition_dependency"]:
                    #     del self.env.blackboard["condition_dependency"][self.current_task["subgoal"]]


        self.bt_success = self.bt.root.status == Status.SUCCESS
        return self.action
