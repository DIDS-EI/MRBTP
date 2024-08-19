from mabtpg.behavior_tree.base_nodes import Action
from mabtpg.behavior_tree import Status
from mabtpg.envs.numerical_env.numsim_tools import str_to_frozenset,get_action_name,NumAction
from mabtpg.envs.gridenv.minigrid.planning_action import PlanningAction

class ToggleDoorWithKey0(Action):
    can_be_expanded = True
    num_args = 4

    def __init__(self,*args):
        self.name = get_action_name(args[0])

        self.agent_id = args[0]

        self.pre = set()
        self.add = set()
        self.del_set = set()

        self.act_max_step = -1

        self.action = NumAction(name=self.name, pre=self.pre, add=self.add, del_set=self.del_set,act_step = self.act_max_step)


    def get_planning_action_list(cls, agent, env):
        planning_action_list = []
        action_model = {
            "pre": {f"CanGoTo(key-0)", f"IsInRoom(agent-{agent.id},room-0)", f"IsHandEmpty(agent-{agent.id})"},
            "add": {f"IsOpen(door)"},
            "del_set": {f"CanGoTo(key-0)"},
            "cost": 1
        }
        planning_action_list.append(PlanningAction(f"ToggleDoorWithKey0(agent-{agent.id})",**action_model))

        return planning_action_list


    def update(self) -> Status:

        if self.env.use_atom_subtask_chain:
            if self.check_if_pre_in_predict_condition():
                return Status.RUNNING

        if self.agent.last_action==self.action:
            self.act_cur_step += 1
            if self.act_cur_step>=self.act_max_step:
                self.action.is_finish = True

        self.agent.action = self.action
        self.agent.last_action = self.action

        return Status.RUNNING


