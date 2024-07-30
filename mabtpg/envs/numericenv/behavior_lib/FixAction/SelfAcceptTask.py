import copy

from mabtpg.behavior_tree.base_nodes import Action
from mabtpg.behavior_tree import Status
from minigrid.core.actions import Actions
from mabtpg.envs.numericenv.numsim_tools import convert_to_num_frozenset,get_action_name
import random

class SelfAcceptTask(Action):
    can_be_expanded = False
    num_args = 1

    def __init__(self, task_id,action_name,sub_goal,sub_del=set()):
        self.task_id = task_id
        self.task_action_name = get_action_name(action_name)
        self.sub_goal = convert_to_num_frozenset(sub_goal)
        self.sub_del = convert_to_num_frozenset(sub_del)

        super().__init__(sub_goal)


    def get_ins_name(self):
        sub_goal_str = ', '.join(str(x) for x in sorted(self.sub_goal))
        ins_name = f'SelfAcceptTask({sub_goal_str})'
        return ins_name


    @property
    def print_name(self):
        return f'{self.print_name_prefix}{self.get_ins_name()} id={self.task_id} act={self.task_action_name}'

    def update(self) -> Status:


        self.agent.current_task = {"task_id": self.task_id,
                                  "sub_goal": self.sub_goal,
                                  "sub_del": self.sub_del}
        return Status.RUNNING



        # 如果自己没有做这个, 还已经有人做了，自己的接受到的任务叶为空
        # if (self.agent.accept_task==None or self.agent.accept_task["task_id"]!=self.task_id):
        #     if (self.task_id,self.subgoal)  in  self.env.blackboard["dependent_tasks_dic"].keys():
        #         # self.agent.accept_task = None
        #         # 任务也给它接受着，尽管它可能因为里面的动作没有 putdown 做不了
        #         self.agent.accept_task = {"task_id": self.task_id,
        #                                   "subgoal": self.subgoal,
        #                                   "subdel": self.subdel}
        #         return Status.RUNNING

        # self.agent.accept_task = {"task_id": self.task_id,
        #                           "subgoal": self.subgoal,
        #                           "subdel": self.subdel}
        #
        # # 记录每个任务的假设空间
        # self.env.blackboard["task_predict_condition"][(self.task_id, self.subgoal)] = copy.deepcopy(self.env.blackboard[
        #     "predict_condition"])
        # # 更新总的假设空间
        # # self.env.blackboard["predict_condition"] |= self.subgoal
        # self.env.blackboard["predict_condition"] = (self.env.blackboard["predict_condition"] | self.subgoal) -self.subdel
        #
        # # 在之前的所有任务里，加上这个现在新的 会受影响 的任务
        # for key in self.env.blackboard["dependent_tasks_dic"].keys():
        #     if key!=( self.task_id, self.subgoal):
        #         self.env.blackboard["dependent_tasks_dic"][key].append(( self.task_id, self.subgoal))
        # # 可能别的智能体有在做
        # if ( self.task_id, self.subgoal) not in self.env.blackboard["dependent_tasks_dic"].keys():
        #     self.env.blackboard["dependent_tasks_dic"][( self.task_id, self.subgoal)] = []



