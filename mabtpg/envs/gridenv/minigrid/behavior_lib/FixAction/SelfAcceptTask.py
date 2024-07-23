import copy

from mabtpg.behavior_tree.base_nodes import Action
from mabtpg.behavior_tree import Status
from minigrid.core.actions import Actions
import random

class SelfAcceptTask(Action):
    can_be_expanded = False
    num_args = 1

    def __init__(self, subgoal):
        super().__init__(subgoal)
        self.task_id = None
        self.subgoal = subgoal

    def update(self) -> Status:


        self.agent.accept_task = {"task_id": self.env.blackboard["task_num"],
                                  "subgoal":self.subgoal}
        self.task_id = self.agent.accept_task["task_id"]
        self.env.blackboard["task_num"]+=1

        # 记录每个任务的假设空间
        self.env.blackboard["task_predict_condition"][(self.task_id, self.subgoal)] = copy.deepcopy(self.env.blackboard[
            "predict_condition"])
        # 更新总的假设空间
        self.env.blackboard["predict_condition"] |= self.subgoal

        # 在之前的所有任务里，加上这个现在新的 会受影响 的任务
        for key in self.env.blackboard["dependent_tasks_dic"].keys():
            self.env.blackboard["dependent_tasks_dic"][key].append(( self.task_id, self.subgoal))
        # 可能别的智能体有在做
        if ( self.task_id, self.subgoal) not in self.env.blackboard["dependent_tasks_dic"].keys():
            self.env.blackboard["dependent_tasks_dic"][( self.task_id, self.subgoal)] = []

        # self.env.blackboard["premise_dep2subgoal"][frozenset(self.dependency)] = (self.task_id,frozenset(self.subgoal))
        # self.env.blackboard["condition_dependency"][(self.task_id,self.subgoal)] = self.dependency
        # self.env.blackboard["condition_dependency"][self.task_id] = self.dependency

        # # 是否有人做了，如果没人做我就做
        # if self.subgoal not in self.env.blackboard["predict_condition"]:
        #     self.agent.accept_task = self.subgoal
        #     self.env.blackboard["predict_condition"] |= self.subgoal

        # self.env.blackboard['task'][self.subgoal] = self.agent.agent_id
        #
        # subgoal_set = self.env.blackboard['subgoal_map'][self.subgoal]
        #
        # self.agent.planning_for_subgoal(self.subgoal)
        #
        # self.env.blackboard['precondition'].update(subgoal_set)
        # self.agent.subgoal = self.subgoal

        return Status.RUNNING
