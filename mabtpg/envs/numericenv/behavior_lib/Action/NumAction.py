from mabtpg.behavior_tree.base_nodes import Action
from mabtpg.utils.tools import print_colored
from mabtpg.behavior_tree import Status


class NumAction(Action):
    can_be_expanded = True
    num_args = 4

    def __init__(self,args):
        super().__init__(args)
        self.action = args[0]
        self.name = self.action.name
        self.pre = self.action.pre
        self.add = self.action.add
        self.del_set = self.action.del_set

        self.get_info_name()
        self.ins_name = self.modify_ins_name()

    def get_info_name(self):
        # Convert frozensets to sorted lists, then join elements with ', '
        self.pre_str = ', '.join(str(x) for x in sorted(set(self.pre)))
        self.add_str = ', '.join(str(x) for x in sorted(set(self.add)))
        self.del_set_str = ', '.join(str(x) for x in sorted(set(self.del_set)))

        # Build the name string with formatted attributes
        self.info_name = (f"{self.name}  \n  pre: ({self.pre_str}) \n "
                     f"add: ({self.add_str})   \n del: ({self.del_set_str})")

    def modify_ins_name(self):
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

        self.agent.action = self.action
        # self.env.state = (self.env.state | self.add) - self.del_set
        return Status.RUNNING


