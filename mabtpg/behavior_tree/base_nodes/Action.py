from mabtpg.behavior_tree.base_nodes.BehaviorNode import BahaviorNode

class Action(BahaviorNode):
    print_name_prefix = "action "
    type = 'Action'

    def __init__(self,*args):
        super().__init__(*args)
        self.info = self.get_info(*args)

    # def update(self):
    #     self.agent =

    @classmethod
    def get_info(self,*arg):
        return None


    def check_if_pre_in_predict_condition(self):

        act_pre = self.env.blackboard["action_pre"][self.name]

        if self.agent.accept_task == None:
            # 总的假设空间
            if act_pre & self.env.blackboard["predict_condition"] !=set():
                return True
        else:
            # 任务已完成，总的假设空间
            task_id = self.agent.accept_task["task_id"]
            subgoal = self.agent.accept_task["subgoal"]
            if (task_id,subgoal) not in self.env.blackboard["task_predict_condition"]:
                if act_pre & self.env.blackboard["task_predict_condition"] !=set():
                    return True

            # 任务的假设空间
            task_prediction_condition = self.env.blackboard["task_predict_condition"][(task_id,subgoal)]
            if act_pre & task_prediction_condition !=set():
                return True


        # if self.env.blackboard["predict_condition"] & self.env.blackboard["action_pre"][self.name]!= set():
        #     return True

        # subgoal = set()
        # if self.agent.accept_task!=None:
        #     subgoal = self.agent.accept_task['subgoal']
        #
        # if ((self.env.blackboard["predict_condition"] - subgoal ) &
        #         self.env.blackboard["action_pre"][self.name]!= set()):
        #     return True