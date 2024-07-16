from minigrid.core.actions import Actions
from mabtpg.behavior_tree.utils import Status

class Agent(object):
    def __init__(self,env=None,id=0):
        self.env = env
        self.id = id
        self.subgoal = None
        self.subtree = None

        self.behavior_lib = None

        self.action = Actions.done
        self.bt_success = None

        self.position = (-1, -1)
        self.direction = -1
        self.carrying = None

        self.last_tick_output = None


    def planning_for_subgoal(self,subgoal):
        from mabtpg.btp.pbtp import PBTP

        if self.env.action_lists is None:
            self.env.action_lists = self.env.get_action_lists()

        subgoal_set = self.env.comm['subgoal_map'][subgoal]
        precondition = frozenset(self.env.comm['precondition'])

        action_list = self.env.action_lists[self.id]

        planning_algorithm = PBTP(action_list,subgoal_set,verbose=False,precondition=precondition)
        planning_algorithm.planning()
        bt = planning_algorithm.output_bt(self.behavior_lib)

        bt.bind_agent(self)
        self.subtree = bt

        print('-----------------')
        print(f'{self.agent_id} planning for {subgoal}: {subgoal_set}, output bt:')
        bt.print()
        bt.draw(f'{self.agent_id} {subgoal}')



    @property
    def agent_id(self):
        return f'agent-{self.id}'

    def bind_bt(self,bt):
        self.bt = bt
        bt.bind_agent(self)

    def step(self):
        self.action = Actions.done

        self.bt.tick(verbose=True,bt_name=f'{self.agent_id} bt')

        self.bt_success = self.bt.root.status == Status.SUCCESS
        return self.action
