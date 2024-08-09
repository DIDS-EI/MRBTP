from mabtpg.envs.virtualhome.behavior_lib._base.VHAction import VHAction
from mabtpg.envs.gridenv.minigrid.planning_action import PlanningAction


class Walk(VHAction):
    can_be_expanded = True
    num_args = 1
    # obj1 is reachable (not inside some closed container) or obj1 is a room.
    valid_args = VHAction.SurfacePlaces | VHAction.SittablePlaces | VHAction.Objects | \
                 VHAction.CanPutInPlaces | VHAction.HasSwitchObjects | VHAction.SittablePlaces
    # valid_args = VHAction.HasSwitchObjects


    def __init__(self, *args):
        super().__init__(*args)
        self.agent_id = args[0]
        self.target_obj = args[1]

        self.act_max_step = 2
        self.act_cur_step = 0


    def get_action_model(self):
        # obj_ls = self.env.category_to_objects["SURFACES"] | self.env.category_to_objects["GRABBABLE"] | self.env.category_to_objects["CONTAINERS"] | \
        #          self.env.category_to_objects["HAS_SWITCH"]

        self.pre = set()
        self.add = {f"IsNear({self.agent_id},{self.target_obj})"}
        self.del_set = {f'IsNear({self.agent_id},{place})' for place in self.env.objects if place != self.target_obj}
    @classmethod
    def get_planning_action_list(cls, agent, env):
        planning_action_list = []

        # obj_ls = env.category_to_objects["SURFACES"] | env.category_to_objects["GRABBABLE"] | env.category_to_objects["CONTAINERS"] | \
        #          env.category_to_objects["HAS_SWITCH"]
        obj_ls = env.objects

        for obj in obj_ls:
            action_model = {}

            action_model["pre"] = set()
            action_model["add"] = {f"IsNear(agent-{agent.id},{obj})"}
            action_model["del_set"] = {f'IsNear(agent-{agent.id},{place})' for place in obj_ls if place != obj}
            action_model["cost"] = 1
            planning_action_list.append(PlanningAction(f"Walk(agent-{agent.id},{obj})", **action_model))
        return planning_action_list
