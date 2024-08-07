from mabtpg.envs.virtualhome.behavior_lib._base.VHAction import VHAction
import itertools
from mabtpg.envs.virtualhome.behavior_lib.Action.Put import Put
from mabtpg.envs.gridenv.minigrid.planning_action import PlanningAction

class RightPut(Put):
    can_be_expanded = True
    num_args = 2
    valid_args = list(itertools.product(VHAction.Objects, VHAction.SurfacePlaces))

    def __init__(self, *args):
        super().__init__(*args)
        self.agent_id = args[0]
        self.target_obj = args[1]
        self.target_place = args[2]

        self.act_max_step = 2
        self.act_cur_step = 0

    def get_action_model(self):
        self.pre = {f'IsRightHolding({self.agent_id},{self.target_obj})', f'IsNear({self.agent_id},{self.target_place})'}
        self.add = {f'IsRightHandEmpty({self.agent_id})', f'IsOn({self.target_obj},{self.target_place})'}
        self.del_set = {f'IsRightHolding({self.agent_id},{self.target_obj})'}


    @classmethod
    def get_planning_action_list(cls, agent, env):
        planning_action_list = []

        obj_ls = env.category_to_objects["GRABBABLE"]
        place_ls = env.category_to_objects["SURFACES"]
        for obj in obj_ls:
            for place in place_ls:
                action_model = {}

                action_model["pre"] = {f'IsRightHolding(agent-{agent.id},{obj})', f'IsNear(agent-{agent.id},{place})'}
                action_model["add"] = {f'IsRightHandEmpty(agent-{agent.id})', f'IsOn({obj},{place})'}
                action_model["del_set"] = {f'IsRightHolding(agent-{agent.id},{obj})'}
                action_model["cost"] = 6
                planning_action_list.append(PlanningAction(f"RightPut(agent-{agent.id},{obj},{place})", **action_model))
        return planning_action_list


    def change_condition_set(self):
        self.agent.condition_set |= (self.info["add"])
        self.agent.condition_set -= self.info["del_set"]

    # @property
    # def action_class_name(self):
    #     return Put.__name__