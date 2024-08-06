from mabtpg.envs.virtualhome.behavior_lib._base.VHAction import VHAction
from mabtpg.envs.gridenv.minigrid.planning_action import PlanningAction

class Open(VHAction):
    can_be_expanded = True
    num_args = 1
    valid_args = VHAction.CanOpenPlaces

    def __init__(self, *args):
        super().__init__(*args)
        self.agent_id = args[0]
        self.target_obj = args[1]

        self.pre = {f"IsClose({self.target_obj})", f"IsNear({self.agent_id},{self.target_obj})", f"IsLeftHandEmpty({self.agent_id})"}
        self.add = {f"IsOpen({self.target_obj})"}
        self.del_set = {f"IsClose({self.target_obj})"}

        self.act_max_step = 2
        self.act_cur_step = 0

    @classmethod
    def get_planning_action_list(cls, agent, env):
        planning_action_list = []

        obj_ls = env.category_to_objects["CAN_OPEN"]
        for obj in obj_ls:
            action_model = {}

            action_model["pre"] = {f"IsClose(agent-{agent.id},{obj})", f"IsNear(agent-{agent.id},{obj})", f"IsLeftHandEmpty(agent-{agent.id})"}
            action_model["add"] = {f"IsOpen({obj})"}
            action_model["del_set"] = {f"IsClose({obj})"}
            action_model["cost"] = 2
            planning_action_list.append(PlanningAction(f"Open(agent-{agent.id},{obj})", **action_model))
        return planning_action_list