from mabtpg.behavior_tree.base_nodes import Action
from mabtpg.behavior_tree import Status
from mabtpg.envs.numerical_env.numsim_tools import str_to_frozenset,get_action_name,NumAction
from mabtpg.envs.gridenv.minigrid.planning_action import PlanningAction

class MoveHeavyInRoom(Action):
    can_be_expanded = True
    num_args = 4

    def __init__(self,*args):
        self.name = get_action_name(args[0])

        self.agent_id = args[0]
        self.to_room_id = args[2]

        self.pre = set()
        self.add = set()
        self.del_set = set()

        self.act_max_step = -1

        self.action = NumAction(name=self.name, pre=self.pre, add=self.add, del_set=self.del_set,act_step = self.act_max_step)


    def get_planning_action_list(cls, agent, env):
        planning_action_list = []
        action_model = {
            "pre": {f"IsOpen(door)", f"IsInRoom(agent-{agent.id},room-0)",f"IsInRoom(ball-heavy,room-0)"},
            "add": {f"IsInRoom(agent-{agent.id},room-1)"},
            "del_set": {f"IsInRoom(agent-{agent.id},room-0)"},
            "cost": 1
        }
        planning_action_list.append(PlanningAction(f"GoBtwRoom(agent-{agent.id},room-0,room-1)",**action_model))

        action_model = {
            "pre": {f"IsOpen(door)", f"IsInRoom(agent-{agent.id},room-1)"},
            "add": {f"IsInRoom(agent-{agent.id},room-0)"},
            "del_set": {f"IsInRoom(agent-{agent.id},room-1)"},
            "cost": 1
        }
        planning_action_list.append(PlanningAction(f"GoBtwRoom(agent-{agent.id},room-1,room-0)",**action_model))

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


