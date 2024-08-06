from mabtpg.envs.virtualhome.behavior_lib._base.VHAction import VHAction
import itertools
from mabtpg.envs.virtualhome.behavior_lib.Action.Grab import Grab
from mabtpg.envs.gridenv.minigrid.planning_action import PlanningAction

class LeftGrabFrom(Grab):
    can_be_expanded = False
    num_args = 2
    valid_args = list(itertools.product(VHAction.Objects, VHAction.CanOpenPlaces))

    def __init__(self, *args):
        super().__init__(*args)
        self.agent_id = args[0]
        self.obj = args[1]
        self.container = args[2]

        self.pre = {f"IsLeftHandEmpty({self.agent_id})",f"IsIn({self.obj},{self.container})",f"IsNear({self.agent_id},{self.container})",f"IsOpen({self.container})"}
        self.add = {f"IsLeftHolding({self.agent_id},{self.obj})",f"IsLeftHandFull({self.agent_id})"}
        self.del_set = {f"IsLeftHandEmpty({self.agent_id})"}
        self.del_set |= {f'IsIn({self.obj},{place})' for place in self.env.category_to_objects["CONTAINERS"]}

        self.act_max_step = 4
        self.act_cur_step = 0

    @classmethod
    def get_planning_action_list(cls, agent, env):
        planning_action_list = []

        obj_ls = env.category_to_objects["GRABBABLE"]
        container_ls = env.category_to_objects["CONTAINERS"]
        for obj in obj_ls:
            for container in container_ls:
                action_model = {}

                action_model["pre"] =  {f"IsLeftHandEmpty(agent-{agent.id})", f"IsIn({obj},{container})", f"IsNear(agent-{agent.id},{container})", f"IsOpen({container})"}
                action_model["add"] = {f"IsLeftHolding(agent-{agent.id},{obj})", f"IsLeftHandFull(agent-{agent.id})"}
                action_model["del_set"] = {f"IsLeftHandEmpty(agent-{agent.id})"}
                action_model["del_set"] |= {f'IsIn({obj},{place})' for place in env.category_to_objects["CONTAINERS"]}
                action_model["cost"] = 4
                planning_action_list.append(PlanningAction(f"LeftGrabFrom(agent-{agent.id},{obj},{container})", **action_model))
        return planning_action_list

    # @property
    # def action_class_name(self):
    #     return Grab.__name__



