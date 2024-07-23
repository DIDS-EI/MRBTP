from mabtpg.behavior_tree.base_nodes import Condition
from mabtpg.behavior_tree import Status

class IsSelfTask(Condition):
    num_args = 1

    def __init__(self,subgoal):
        super().__init__(subgoal)
        # self.task_id = task_id
        self.subgoal = subgoal

    def update(self) -> Status:

        if self.agent.accept_task!=None and self.subgoal == self.agent.accept_task["subgoal"]:
            self.agent.current_task = {"task_id":self.agent.accept_task["task_id"], "subgoal":self.subgoal}
            return Status.SUCCESS
        else:
            return Status.FAILURE


        # if self.agent.accept_task!=None and self.task_id == self.agent.accept_task["task_id"]:
        #     self.agent.current_task = {"task_id":self.task_id, "subgoal":self.subgoal}
        #     return Status.SUCCESS
        # else:
        #     return Status.FAILURE



        # if self.subgoal == self.agent.accept_task:
        #     self.agent.current_task = self.subgoal
        #     return Status.SUCCESS
        # else:
        #     return Status.FAILURE
