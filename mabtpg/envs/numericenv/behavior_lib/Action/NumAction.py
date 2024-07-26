from mabtpg.behavior_tree.base_nodes import Action
from mabtpg.utils.tools import print_colored
from mabtpg.behavior_tree import Status


class NumAction(Action):
    can_be_expanded = True
    num_args = 4

    def __init__(self,args):
        super().__init__(args)
        self.action = args[0]
        self.act_name = self.action.name
        self.pre = self.action.pre
        self.add = self.action.add
        self.del_set = self.action.del_set

        self.get_name()

    def get_name(self):
        # Convert frozensets to sorted lists, then join elements with ', '
        pre_str = ', '.join(str(x) for x in sorted(set(self.pre)))
        add_str = ', '.join(str(x) for x in sorted(set(self.add)))
        del_set_str = ', '.join(str(x) for x in sorted(set(self.del_set)))

        # Build the name string with formatted attributes
        self.name = (f"{self.act_name}  \n  pre: ({pre_str}) \n "
                     f"add: ({add_str})   \n del: ({del_set_str})")

    @classmethod
    def get_info(self,*arg):
        return None

    def update(self) -> Status:
        self.agent.action = self.action
        # self.env.state = (self.env.state | self.add) - self.del_set
        return Status.RUNNING


