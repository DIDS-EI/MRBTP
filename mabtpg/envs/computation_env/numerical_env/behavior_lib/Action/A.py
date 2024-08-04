from mabtpg.behavior_tree.base_nodes import Action
from mabtpg.behavior_tree import Status
from mabtpg.envs.computation_env.numerical_env.numsim_tools import str_to_frozenset,get_action_name,NumAction


class A(Action):
    can_be_expanded = True
    num_args = 4

    def __init__(self,*args):
        self.name = get_action_name(args[0])

        self.pre_str = args[1]
        self.add_str = args[2]
        self.del_set_str = args[3]

        self.act_max_step = int(args[4])
        self.act_cur_step = 0

        self.pre = str_to_frozenset(self.pre_str)
        self.add = str_to_frozenset(self.add_str)
        self.del_set = str_to_frozenset(self.del_set_str)

        self.get_info_name()
        self.ins_name = self.get_info_name()
        super().__init__(args)
        self.name = get_action_name(args[0])

        self.action = NumAction(name=self.name, pre=self.pre, add=self.add, del_set=self.del_set,act_step = self.act_max_step)


    def get_info_name(self):
        # Convert frozensets to sorted lists, then join elements with ', '
        self.pre_str = self.pre_str.replace('_', ', ')
        self.add_str = self.add_str.replace('_', ', ')
        self.del_set_str = self.del_set_str.replace('_', ', ')

        # Build the name string with formatted attributes
        self.info_name = (f"{self.name}  \n  pre: ({self.pre_str}) \n "
                     f"add: ({self.add_str})   \n del: ({self.del_set_str})")

    @property
    def draw_name(self):
        return f"{self.info_name}"


    @classmethod
    def get_info(self,*arg):
        return None


    @property
    def print_name(self):
        return f'{self.print_name_prefix}{self.name} pre: ({self.pre_str}) add: ({self.add_str})  del: ({self.del_set_str})'

    def update(self) -> Status:

        if self.check_if_pre_in_predict_condition():
            return Status.RUNNING

        if self.agent.last_action==self.action:
            self.act_cur_step += 1
            if self.act_cur_step>=self.act_max_step:
                self.action.is_finish = True

        self.agent.action = self.action
        self.agent.last_action = self.action

        return Status.RUNNING


