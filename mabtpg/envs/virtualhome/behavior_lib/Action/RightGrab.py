from mabtpg.envs.virtualhome.behavior_lib._base.VHAction import VHAction
from mabtpg.envs.virtualhome.behavior_lib.Action.Grab import Grab
from mabtpg.envs.gridenv.minigrid.planning_action import PlanningAction

class RightGrab(Grab):
    can_be_expanded = True
    num_args = 1
    # obj1 is reachable (not inside some closed container)

    def __init__(self, *args):
        super().__init__(*args)
        self.agent_id = args[0]
        self.target_obj = args[1]

        self.act_max_step = 2
        self.act_cur_step = 0

    # @property
    # def action_class_name(self):
    #     # 根据需要，这里可以返回当前类名或父类名
    #     # 例如，直接返回父类的名字
    #     return Grab.__name__
    def get_action_model(self):
        self.pre = {f"IsRightHandEmpty({self.agent_id})", f"IsNear({self.agent_id},{self.target_obj})"}
        self.add = {f"IsRightHolding({self.agent_id},{self.target_obj})", f"IsRightHandFull({self.agent_id})"}
        self.del_set = {f"IsRightHandEmpty({self.agent_id})"}
        self.del_set |= {f'IsOn({self.target_obj},{place})' for place in self.env.category_to_objects["SURFACES"]}
        self.del_set |= {f'IsIn({self.target_obj},{place})' for place in self.env.category_to_objects["CAN_OPEN"]}



    @classmethod
    def get_planning_action_list(cls, agent, env):
        planning_action_list = []

        obj_ls = env.category_to_objects["GRABBABLE"]
        for obj in obj_ls:
            action_model = {}

            action_model["pre"] = {f"IsRightHandEmpty(agent-{agent.id})", f"IsNear(agent-{agent.id},{obj})"}
            action_model["add"] = {f"IsRightHolding(agent-{agent.id},{obj})", f"IsRightHandFull(agent-{agent.id})"}
            action_model["del_set"] = {f"IsRightHandEmpty(agent-{agent.id})"}
            action_model["del_set"] |= {f'IsOn({obj},{place})' for place in env.category_to_objects["SURFACES"]}
            action_model["del_set"] |= {f'IsIn({obj},{place})' for place in env.category_to_objects["CAN_OPEN"]}
            action_model["cost"] = 1
            planning_action_list.append(PlanningAction(f"RightGrab(agent-{agent.id},{obj})", **action_model))
        return planning_action_list