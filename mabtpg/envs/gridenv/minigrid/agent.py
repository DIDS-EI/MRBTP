from minigrid.core.actions import Actions
from mabtpg.behavior_tree.utils import Status
from mabtpg.utils.tools import print_colored
import copy

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

        self.last_accept_task = None
        self.current_task = None
        self.predict_condition = {
            "success":set(),
            "fail":set(),
        }



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
        self.current_task = None
        self.bt.tick(verbose=True,bt_name=f'{self.agent_id} bt')

        # print_colored(f"cur: {self.current_task}", color='orange')
        # print_colored(f"accp: {self.last_accept_task} ", color='orange')

        if self.current_task != self.last_accept_task:
            self.finish_current_task()
            self.update_current_task()
            if self.current_task != None:
                self.bt.tick(verbose=True, bt_name=f'Twice {self.agent_id} bt')
                self.bt_success = self.bt.root.status == Status.SUCCESS

        self.bt_success = self.bt.root.status == Status.SUCCESS
        return self.action


    def finish_current_task(self):
        if self.last_accept_task!=None:
            print_colored(f"Have Finish Last Task! last_accept_task = {self.last_accept_task}", color='orange')

            try:
                # self.env.blackboard["task_agents_queue"].remove(self)  # 直接移除对象
                index = self.env.blackboard["task_agents_queue"].index(self)  # 查找 self 的索引
                self.env.blackboard["task_agents_queue"].pop(index)  # 通过索引移除
            except ValueError:
                print("The agent is not in the queue.")  # self 不在队列中
            except IndexError:
                print("Index out of range.")  # 索引超出范围，理论上不会发生，因为索引是从 list.index 获取的

            # 更新队列里所有智能体的假设空间
            last_predict_condition = {
                "success":set(),
                "fail":set(),
            }
            last_sub_goal = set()
            last_sub_del = set()
            for i,agent in enumerate(self.env.blackboard["task_agents_queue"]):
                if i==0:
                    agent.predict_condition = {
                        "success":set(),
                        "fail":set(),
                    }
                else:
                    agent.predict_condition["success"] = (last_predict_condition["success"] | last_sub_goal) -last_sub_del
                    agent.predict_condition["fail"] = (last_predict_condition[ "fail"] | last_sub_del) - last_sub_goal

                last_predict_condition = agent.predict_condition
                last_sub_goal = agent.current_task["sub_goal"]
                last_sub_del = agent.current_task["sub_del"]



    def update_current_task(self):

        # get last agent's predict_condition
        if self.env.blackboard["task_agents_queue"]!=[]:
            last_predict_condition = self.env.blackboard["task_agents_queue"][-1].predict_condition
        else:
            last_predict_condition = {
                "success":set(),
                "fail":set(),
            }

        if self.current_task!=None:
            self.env.blackboard["task_agents_queue"].append(self)
            self.predict_condition = copy.deepcopy(last_predict_condition)

            # now the new_predict_condition
            new_predict_condition = {
                "success":set(),
                "fail":set(),
            }
            new_predict_condition["success"] = (last_predict_condition["success"] | self.current_task["sub_goal"]) - self.current_task["sub_del"]
            new_predict_condition["fail"] = (last_predict_condition["fail"] | self.current_task["sub_del"]) - self.current_task["sub_goal"]
            for agent in self.env.agents:
                if agent!=self and agent not in self.env.blackboard["task_agents_queue"]:
                    agent.predict_condition = copy.deepcopy(new_predict_condition)

        self.last_accept_task = copy.deepcopy(self.current_task)