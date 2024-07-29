from mabtpg.behavior_tree.base_nodes import Condition
from mabtpg.behavior_tree import Status

class IsSelfTask(Condition):
    num_args = 1

    def __init__(self,task_id,action_name,sub_goal,sub_del=set()):
        super().__init__(sub_goal)
        self.task_id = task_id
        self.task_action_name = action_name
        self.sub_goal = sub_goal
        self.sub_del = sub_del

    def update(self) -> Status:

        if self.agent.last_accept_task != None and self.task_id == self.agent.last_accept_task["task_id"]:
            self.agent.current_task = {"task_id":self.task_id, "sub_goal":self.sub_goal,  "sub_del":self.sub_del}
            return Status.SUCCESS
        else:
            return Status.FAILURE
