from mabtpg.envs.virtualhome.behavior_lib._base.VHAction import VHAction
from mabtpg.envs.gridenv.minigrid.planning_action import PlanningAction

class SwitchOn(VHAction):
    can_be_expanded = True
    num_args = 1
    valid_args = VHAction.HasSwitchObjects


    def __init__(self, *args):
        super().__init__(*args)
        self.agent_id = args[0]
        self.target_obj = args[1]

        self.act_max_step = 2
        self.act_cur_step = 0

    def get_action_model(self):
        self.pre = {f"IsLeftHandEmpty({self.agent_id})", f"IsNear({self.agent_id},{self.target_obj})", f"IsSwitchedOff({self.target_obj})"}

        # if self.target_obj in self.env.category_to_objects["CAN_OPEN"]:
        #     self.pre |= {f'IsClose({self.target_obj})'}

        self.add = {f"IsSwitchedOn({self.target_obj})"}
        self.del_set = {f"IsSwitchedOff({self.target_obj})"}


    @classmethod
    def get_planning_action_list(cls, agent, env):
        planning_action_list = []

        obj_ls = env.category_to_objects["HAS_SWITCH"]
        for obj in obj_ls:
            action_model = {}

            action_model["pre"] = {f"IsLeftHandEmpty(agent-{agent.id})", f"IsNear(agent-{agent.id},{obj})", f"IsSwitchedOff({obj})"}

            # if obj in env.category_to_objects["CAN_OPEN"]:
            #     action_model["pre"] |= {f'IsClose({obj})'}

            action_model["add"] = {f"IsSwitchedOn({obj})"}
            action_model["del_set"] = {f"IsSwitchedOff({obj})"}

            # action_model["del_set"] |= {f'IsNear(agent-{agent.id},{place})' for place in obj_ls if place != obj}
            action_model["cost"] = 1
            planning_action_list.append(PlanningAction(f"SwitchOn(agent-{agent.id},{obj})", **action_model))
        return planning_action_list