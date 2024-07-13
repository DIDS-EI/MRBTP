from mabtpg.behavior_tree.base_nodes import Action
from mabtpg.behavior_tree import Status
from minigrid.core.actions import Actions
from mabtpg.envs.gridenv.minigrid.objects import CAN_PICKUP
from mabtpg.envs.gridenv.minigrid.planning_action import PlanningAction
from mabtpg.envs.gridenv.minigrid.utils import obj_to_planning_name, get_direction_index
import numpy as np



class GetKeyAndOpenDoor(Action):
    can_be_expanded = True
    num_args = 2
    # sub_actions_ls = ['GoToInRoom(agent,key,room)','PickUp(agent,key)','GoToInRoom(agent,door,room)','Toggle(agent,door)']
    sub_act_ls = ['GoToInRoom','PickUp','GoToInRoom','Toggle']

    def __init__(self, *args):
        super().__init__(*args)
        self.path = None

    @classmethod
    def get_planning_action_list(cls, agent, env):
        planning_action_list = []

        # 在底层的动作中，根据 agent、key room 找到对应的所有 sub_actions_ls 中的具体动作，比如
        # sub_act_ls = ['GoToInRoom(agent,key,room)','PickUp(agent,key)','GoToInRoom(agent,door,room)','Toggle(agent,door)']


        return planning_action_list


    def update(self) -> Status:
        return Status.RUNNING