from tabulate import tabulate
from mabtpg.envs.base.env import Env
from mabtpg.utils.tools import print_colored
from mabtpg import BehaviorLibrary
from mabtpg.envs.numerical_env.numsim_tools import get_action_name
from mabtpg.envs.numerical_env.numerical_env import NumEnv
from mabtpg.envs.gridenv.minigrid_computation_env.agent import Agent

class MiniCompEnv(NumEnv):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.num_rooms = None
        self.num_objs = None
        self.objects_rooms_dic = None
        self.target_room_ls = None

        self.use_atom_subtask_chain = False
        self.action_fail_p = None

        self.agents = [Agent(self, i) for i in range(self.num_agent)]
        self.verbose=True
        self.communication_times = 0

    def reset(self):
        for agent in self.agents:
            agent.is_fail = False
        self.communication_times = 0


    def create_behavior_libs(self):
        from mabtpg.utils import get_root_path
        root_path = get_root_path()


        behavior_lib_path = f"{root_path}/envs/gridenv/minigrid_computation_env/behavior_lib"
        behavior_lib = BehaviorLibrary(behavior_lib_path)
        for agent in self.agents:
            agent.behavior_lib = behavior_lib

    def step(self,action=None,num_agent = None):
        if num_agent is None:
            num_agent = self.num_agent
        self.step_count += 1
        done = True
        self.agents_step = 0

        # cur_agent_actions = {}

        agent_action_every_step = ["" for _ in range(num_agent)]
        finish_and_fail=False

        for i in range(num_agent):
            if self.verbose: print_colored(f"---AGENT - {i}---",color="yellow")

            if self.agents[i].is_fail:
                if self.verbose:print_colored(f"is_fail", color="yellow")
                continue

            action = self.agents[i].step()

            # print(f"agent {i}, {action.name}")
            if action is None:
                if self.verbose: print(f"Agent {i} has no action")
                agent_action_every_step[i] = None
            else:
                # cur_agent_actions[i] = action
                agent_action_every_step[i] = action.name
                if self.verbose:  self.print_agent_action_tabulate(i,action)

            if not self.agents[i].bt_success:
                done = False

        # if agent_action_every_step == [None for _ in range(num_agent)]:
        #     finish_and_fail = True

        # execute
        # for agent_id,action in cur_agent_actions.items():
        #     if self.state >= action.pre:
        #         agents_step += 1
        #         self.state = (self.state | action.add) - action.del_set
        #     else:
        #         print_colored(f"AGENT-{agent_id} cannot do it!", color="red")

        if self.render_mode == "human":
            self.render()

        return self.state, done, None, {}, self.agents_step,finish_and_fail

