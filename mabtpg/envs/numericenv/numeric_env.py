import gym
from mabtpg.envs.base.env import Env
from mabtpg.utils.tools import print_colored
class NumericEnv(Env):
    def __init__(self,
        num_agent: int = 1,
        start: frozenset=(),
        goal: frozenset=(),
        **kwargs):
        super().__init__(**kwargs)

        self.num_agent = num_agent
        self.start = start
        self.goal = goal
        self.actions_lists = None

        self.state = set(self.start)

        self.step_count=0

    def step(self,action=None,num_agent = None):
        if num_agent is None:
            num_agent = self.num_agent
        self.step_count += 1
        done = True

        for i in range(num_agent):
            print_colored(f"---AGENT - {i}---",color="yellow")
            action = self.agents[i].step()
            print(f"agent {i}, {action.name}")

            if not self.agents[i].bt_success:
                done = False

        if self.render_mode == "human":
            self.render()

        return self.state, done, None, {}

    def create_behavior_lib(self):
        pass