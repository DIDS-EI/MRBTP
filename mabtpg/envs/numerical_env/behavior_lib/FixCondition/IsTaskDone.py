from mabtpg.behavior_tree.base_nodes import Condition
from mabtpg.behavior_tree import Status
from mabtpg.utils.tools import print_colored
class IsTaskDone(Condition):
    num_args = 1

    def __init__(self,subgoal):
        super().__init__(subgoal)
        self.subgoal = subgoal

    def update(self) -> Status:

        # task done
        if self.subgoal in self.env.state:
            print_colored(f"Have Finish Last Task! cur_task = {self.agent.current_task}", color='orange')

            task_id = self.agent.current_task["task_id"]
            subgoal = self.agent.current_task["subgoal"]
            task_key = (task_id, subgoal)

            self.env.blackboard["predict_condition"] -= subgoal
            # 先遍历这个键值，删除里面对应的任务里 depend
            # 如果有受它依赖的任务，那么解除这些任务的依赖
            print_colored(f"Task Dependency: {self.env.blackboard['dependent_tasks_dic']}", color='orange')
            if task_key in self.env.blackboard["dependent_tasks_dic"]:
                successor_tasks = self.env.blackboard["dependent_tasks_dic"][task_key]
                for st in successor_tasks:
                    self.env.blackboard["task_predict_condition"][st] -= subgoal
                    print_colored("Release Task Dependency....", color='orange')
                    print_colored(f"{st} \t {self.env.blackboard['task_predict_condition'][st]}",
                                  color='orange')
                # 这个任务的记录，删除记录依赖
                del self.env.blackboard["dependent_tasks_dic"][task_key]

            return Status.SUCCESS
        else:
            return Status.FAILURE

