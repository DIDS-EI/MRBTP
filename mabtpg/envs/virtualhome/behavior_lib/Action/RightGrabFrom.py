from mabtpg.envs.virtualhome.behavior_lib._base.VHAction import VHAction
import itertools
from mabtpg.envs.virtualhome.behavior_lib.Action.Grab import Grab
from mabtpg.envs.gridenv.minigrid.planning_action import PlanningAction
class RightGrabFrom(Grab):
    can_be_expanded = False
    num_args = 2
    # obj1 is reachable (not inside some closed container)
    valid_args = list(itertools.product(VHAction.Objects, VHAction.CanOpenPlaces))

    def __init__(self, *args):
        super().__init__(*args)
        self.agent_id = args[0]
        self.obj = args[1]
        self.container = args[2]

        self.act_max_step = 2
        self.act_cur_step = 0

    def get_action_model(self):
        self.pre = {f"IsRightHandEmpty({self.agent_id})", f"IsIn({self.obj},{self.container})", f"IsNear({self.agent_id},{self.container})", f"IsOpen({self.container})"}
        self.add = {f"IsRightHolding({self.agent_id},{self.obj})", f"IsRightHandFull({self.agent_id})"}
        self.del_set = {f"IsRightHandEmpty({self.agent_id})"}
        self.del_set |= {f'IsIn({self.obj},{place})' for place in self.env.category_to_objects["CONTAINERS"]}

    # @property
    # def action_class_name(self):
    #     return Grab.__name__

    @classmethod
    def get_planning_action_list(cls, agent, env):
        planning_action_list = []

        obj_ls = env.category_to_objects["GRABBABLE"]
        container_ls = env.category_to_objects["CONTAINERS"]
        for obj in obj_ls:
            for container in container_ls:
                action_model = {}

                action_model["pre"] = {f"IsRightHandEmpty(agent-{agent.id})", f"IsIn({obj},{container})", f"IsNear(agent-{agent.id},{container})", f"IsOpen({container})"}
                action_model["add"] = {f"IsRightHolding(agent-{agent.id},{obj})", f"IsRightHandFull(agent-{agent.id})"}
                action_model["del_set"] = {f"IsRightHandEmpty(agent-{agent.id})"}
                action_model["del_set"] |= {f'IsIn({obj},{place})' for place in env.category_to_objects["CONTAINERS"]}
                action_model["cost"] = 4
                planning_action_list.append(PlanningAction(f"{cls.__name__}(agent-{agent.id},{obj},{container})", **action_model))
        return planning_action_list