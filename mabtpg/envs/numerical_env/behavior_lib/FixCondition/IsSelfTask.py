from mabtpg.behavior_tree.base_nodes import Condition
from mabtpg.behavior_tree import Status
from mabtpg.envs.numerical_env.numsim_tools import convert_to_num_frozenset,get_action_name

class IsSelfTask(Condition):
    num_args = 1

    def __init__(self,task_id,action_name,sub_goal,sub_del=set()):
        self.task_id = task_id
        self.task_action_name = get_action_name(action_name)
        self.sub_goal = convert_to_num_frozenset(sub_goal)
        self.sub_del = convert_to_num_frozenset(sub_del)
        super().__init__(sub_goal)


    def get_ins_name(self):
        sub_goal_str = ', '.join(str(x) for x in sorted(self.sub_goal))
        ins_name = f'IsSelfTask({sub_goal_str})'
        return ins_name

    @property
    def print_name(self):
        return f'{self.print_name_prefix}{self.get_ins_name()} id={self.task_id} act={self.task_action_name}'


    def update(self) -> Status:

        if self.agent.last_accept_task != None and self.task_id == self.agent.last_accept_task["task_id"]:
            self.agent.current_task = {"task_id":self.task_id, "sub_goal":self.sub_goal,  "sub_del":self.sub_del}
            return Status.SUCCESS
        else:
            return Status.FAILURE
