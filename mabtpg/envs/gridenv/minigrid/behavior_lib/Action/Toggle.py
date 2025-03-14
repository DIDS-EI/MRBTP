# from mabtpg.behavior_tree.base_nodes import Action
from mabtpg.envs.gridenv.minigrid.behavior_lib.base.Action import MinigridAction as Action
from mabtpg.behavior_tree import Status
from minigrid.core.actions import Actions
from mabtpg.envs.gridenv.minigrid.objects import CAN_TOGGLE
from mabtpg.envs.gridenv.minigrid.planning_action import PlanningAction


class Toggle(Action):
    can_be_expanded = True
    num_args = 2
    valid_args = [CAN_TOGGLE]

    def __init__(self, *args):
        super().__init__(*args)
        self.path = None


    @classmethod
    def get_planning_action_list(cls, agent, env):
        planning_action_list = []
        can_toggle = env.cache["can_toggle"]
        for obj_id in can_toggle:
            action_model = {}
            action_model["pre"] = {f"IsClose({obj_id})", f"IsNear(agent-{agent.id},{obj_id})"}

            if "door" in obj_id:
                action_model["pre"] |= {f"CanOpen(agent-{agent.id},{obj_id})"}

            action_model["add"]={f"IsOpen({obj_id})"}
            action_model["del_set"] = {f"IsClose({obj_id})"}
            action_model["cost"] = 1
            planning_action_list.append(PlanningAction(f"Toggle(agent-{agent.id},{obj_id})",**action_model))

        return planning_action_list


    def update(self) -> Status:

        if self.check_if_pre_in_predict_condition():
            return Status.RUNNING

        self.agent.action = Actions.toggle
        print("agent:", self.agent.id,"Toggle")
        return Status.RUNNING