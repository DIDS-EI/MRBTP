from mabtpg.envs.virtualhome.behavior_lib._base.VHAction import VHAction
from mabtpg.envs.virtualhome.behavior_lib.Action.PutIn import PutIn
from mabtpg.envs.gridenv.minigrid.planning_action import PlanningAction
class LeftPutIn(PutIn):
    can_be_expanded = True
    num_args = 2


    def __init__(self, *args):
        super().__init__(*args)
        self.agent_id = args[0]
        self.target_obj = args[1]
        self.target_place = args[2]

        self.pre = {f'IsLeftHolding(agent-{self.agent_id},{self.target_obj})', f'IsNear(agent-{self.agent_id},{self.target_place})', f'IsOpen({self.target_place})'}
        self.add = {f'IsLeftHandEmpty(agent-{self.agent_id})', f'IsIn({self.target_obj},{self.target_place})'}
        self.del_set = {f'IsLeftHolding(agent-{self.agent_id},{self.target_obj})'}

        self.act_max_step = 4
        self.act_cur_step = 0


    @classmethod
    def get_planning_action_list(cls, agent, env):
        planning_action_list = []

        obj_ls = env.category_to_objects["GRABBABLE"]
        place_ls = env.category_to_objects["CONTAINERS"]
        for obj in obj_ls:
            for place in place_ls:
                action_model = {}

                action_model["pre"] = {f'IsLeftHolding(agent-{agent.id},{obj})', f'IsNear(agent-{agent.id},{place})', f'IsOpen({place})'}
                action_model["add"] = {f'IsLeftHandEmpty(agent-{agent.id})', f'IsIn({obj},{place})'}
                action_model["del_set"] = {f'IsLeftHolding(agent-{agent.id},{obj})'}
                action_model["cost"] = 4
                planning_action_list.append(PlanningAction(f"LeftPutIn(agent-{agent.id},{obj},{place})", **action_model))
        return planning_action_list

    # @property
    # def action_class_name(self):
    #     return PutIn.__name__