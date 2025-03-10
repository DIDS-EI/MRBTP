from mabtpg.behavior_tree.base_nodes import Action
from mabtpg.behavior_tree import Status
from mabtpg.envs.numerical_env.numsim_tools import convert_to_num_frozenset,get_action_name


class SelfAcceptTask(Action):
    can_be_expanded = False
    num_args = 1

    def __init__(self, task_id,action_name,sub_goal,sub_del):
        super().__init__(sub_goal)
        self.task_id = task_id
        self.task_action_name = action_name
        self.sub_goal = sub_goal
        self.sub_del = sub_del

    def update(self) -> Status:

        self.agent.current_composite_task = {"task_id": self.task_id,
                                  "sub_goal": self.sub_goal,
                                  "sub_del": self.sub_del}

        return Status.RUNNING

