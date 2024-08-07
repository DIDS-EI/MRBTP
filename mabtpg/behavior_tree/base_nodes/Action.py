from mabtpg.behavior_tree.base_nodes.BehaviorNode import BahaviorNode
from mabtpg.utils.tools import print_colored
from mabtpg.behavior_tree import Status
class Action(BahaviorNode):
    print_name_prefix = "action "
    type = 'Action'

    def __init__(self,*args):
        super().__init__(*args)
        self.info = self.get_info(*args)

        self.action=None
        self.act_cur_step=None
        self.act_max_step=None


    # def update(self):
    #     self.agent =

    @classmethod
    def get_info(self,*arg):
        return None


    def update(self):
        if self.env.simulation_mode == self.env.SimulationMode.computing:
            self.computing_update()
        if self.env.simulation_mode == self.env.SimulationMode.simulator:
            self.simulator_update()


    def computing_update(self)-> Status:
        if self.check_if_pre_in_predict_condition():
            return Status.RUNNING

        if self.agent.last_action==self.action:
            self.act_cur_step += 1
            if self.act_cur_step>=self.act_max_step:
                self.action.is_finish = True

        self.agent.action = self.action
        self.agent.last_action = self.action

        pass

    def simulator_update(self):
        pass


    def check_if_pre_in_predict_condition(self):

        act_pre = self.env.blackboard["action_pre"][self.name]

        if act_pre & self.agent.predict_condition['success'] !=set():
            if self.env.verbose: print_colored(f"{self.name}  Total Wait:{act_pre & self.agent.predict_condition['success']}",color="purple")
            return True

