from mabtpg.envs.virtualhome.behavior_lib._base.VHAction import VHAction
from mabtpg.envs.virtualhome.behavior_lib.Action.Grab import Grab
from mabtpg.envs.gridenv.minigrid.planning_action import PlanningAction

class LeftGrab(Grab):
    can_be_expanded = True
    num_args = 1

    def __init__(self, *args):
        super().__init__(*args)
        self.agent_id = self.args[0]
        self.target_obj = self.args[1]

        self.act_max_step = 2
        self.act_cur_step = 0

    def get_action_model(self):
        self.pre = {f"IsLeftHandEmpty({self.agent_id})", f"IsNear({self.agent_id},{self.target_obj})"}
        self.add = {f"IsLeftHolding({self.agent_id},{self.target_obj})", "IsLeftHandFull({self.agent_id})"}
        self.del_set = {f"IsLeftHandEmpty({self.agent_id})"}
        self.del_set |= {f'IsOn({self.target_obj},{place})' for place in self.env.category_to_objects["SURFACES"]}
        self.del_set |= {f'IsIn({self.target_obj},{place})' for place in self.env.category_to_objects["CAN_OPEN"]}



    # @property
    # def action_class_name(self):
    #     return Grab.__name__

    @classmethod
    def get_planning_action_list(cls, agent, env):
        planning_action_list = []

        obj_ls = env.category_to_objects["GRABBABLE"]
        for obj in obj_ls:
            action_model = {}

            action_model["pre"] = {f"IsLeftHandEmpty(agent-{agent.id})", f"IsNear(agent-{agent.id},{obj})"}
            action_model["add"] = {f"IsLeftHolding(agent-{agent.id},{obj})", f"IsLeftHandFull(agent-{agent.id})"}
            action_model["del_set"] = {f"IsLeftHandEmpty(agent-{agent.id})"}
            action_model["del_set"] |= {f'IsOn({obj},{place})' for place in env.category_to_objects["SURFACES"]}
            action_model["del_set"] |= {f'IsIn({obj},{place})' for place in env.category_to_objects["CAN_OPEN"]}
            action_model["cost"] = 3
            planning_action_list.append(PlanningAction(f"LeftGrab(agent-{agent.id},{obj})", **action_model))
        return planning_action_list