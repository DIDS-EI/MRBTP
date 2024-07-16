from mabtpg.behavior_tree.base_nodes.BehaviorNode import BahaviorNode, Status
from mabtpg.behavior_tree.base_nodes.Action import Action

class CompositeAction(Action):
    print_name_prefix = "action "
    type = 'Action'

    def __init__(self,*args):
        self.args = args
        super().__init__(*args)
        self.subtree = None


    def bind_agent(self,agent):
        self.agent = agent
        self.env = agent.env
        self.subtree.bind_agent(agent)


    def update(self) -> Status:
        self.subtree.tick(verbose=True)

        return self.subtree.root.status

