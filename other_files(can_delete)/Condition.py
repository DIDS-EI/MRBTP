import py_trees as ptree
from mabtpg.behavior_tree.base_nodes.BehaviorNode import BahaviorNode, Status

class Condition(BahaviorNode):
    print_name_prefix = "condition "
    type = 'Condition'

    def __init__(self,*args):
        super().__init__(*args)

    def check_if_in_predict_condition(self):

        # 在自己假设空间里的就是假设已完成
        # 没有在执行任务，就是总假设空间
        if self.agent.accept_task == None:
            if self.name in self.env.blackboard["predict_condition"]:
                return True
        else:
            # 没有在执行任务，就是总假设空间
            task_id = self.agent.accept_task["task_id"]
            subgoal = self.agent.accept_task["subgoal"]
            if (task_id,subgoal) not in self.env.blackboard["task_predict_condition"]:
                if self.name in self.env.blackboard["task_predict_condition"]:
                    return True

            # 任务的假设空间
            if self.name in self.env.blackboard["task_predict_condition"][(task_id,subgoal)]:
                return True
        return False





        # # # 什么情况不可以直接判断
        # if self.agent.accept_task != None:
        #     # 我正在执行的任务不能假设已完成
        #     dep = set()
        #     if (self.agent.accept_task["task_id"],self.agent.accept_task["subgoal"])\
        #             in self.env.blackboard["premise_dep2subgoal"]:
        #         dep = self.env.blackboard["premise_dep2subgoal"][(self.agent.accept_task["task_id"],self.agent.accept_task["subgoal"])]
        #     if self.name in self.agent.accept_task["subgoal"] - dep:
        #         return False
        #
        #     # 当前状态的成立依赖于我正在执行的任务
        #     # 我正在执行的任务是在 dependency 里面
        #     # if self.agent.accept_task["subgoal"] in self.env.blackboard["condition_dependency"].values():
        #     #     return False
        #
        #     # self.name = "0"
        #     # self.env.blackboard["predict_condition"][self.dependency] = (self.task_id,self.subgoal)
        #     for dep,id_cond in  self.env.blackboard["premise_dep2subgoal"].items():
        #         task_id,cond = id_cond
        #         if dep==self.agent.accept_task["subgoal"]:
        #             if self.name in cond:
        #                 return False

                # {1: frozenset({'CanGoTo(door-0)',
                #                'CanGoTo(key-0)',
                #                'IsClose(door-0)',
                #                'IsHandEmpty(agent-0)',
                #                'IsInRoom(agent-0,room-0)'}),
                #  0: frozenset({'IsInRoom(agent-1,room-0)', 'IsOpen(door-0)'} ---1)}
        #       #  0: isinroom(ball,1)

        subgoal = set()
        if self.agent.accept_task!=None:
            subgoal = self.agent.accept_task['subgoal']

        if self.name in self.env.blackboard["predict_condition"]-subgoal:
            return True





        # 排除上面的情况以后，什么情况可以直接判断为True
        # 自己做的任务 - 他依赖的任务 = 不能假设已完成
        # my_task = set()
        # if self.agent.accept_task!=None:
        #     my_task =self.agent.accept_task["subgoal"]
        #
        # dependency = set()
        # if self.agent.accept_task!=None and self.agent.accept_task["task_id"] in self.env.blackboard["condition_dependency"]:
        #     dependency = self.env.blackboard["condition_dependency"][self.agent.accept_task["task_id"]]
        #     print("xxx:",self.env.blackboard["condition_dependency"])
        #
        # print("-----------------------------")
        # print("pre_cond:",self.env.blackboard["predict_condition"])
        # print("my_task:", my_task)
        # print("dependency",dependency)
        # print("final:",self.env.blackboard["predict_condition"]-(my_task-dependency))
        # print("-----------------------------")
        #
        # if self.name in self.env.blackboard["predict_condition"]-(my_task-dependency):
        #     return True


        # Other Agents Besides Myself
        # if self.agent.accept_task != None and self.name in self.agent.accept_task:
        #     return False
        # if self.name in self.env.blackboard["predict_condition"]:
        #     return True
        # return False