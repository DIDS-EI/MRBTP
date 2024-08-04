from tabulate import tabulate
from mabtpg.envs.base.env import Env
from mabtpg.utils.tools import print_colored
from mabtpg import BehaviorLibrary
from mabtpg.envs.computation_env.agent import Agent
from mabtpg.envs.computation_env.numerical_env.numsim_tools import get_action_name
class ComputationEnv(Env):
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

        self.agents = [Agent(self, i) for i in range(num_agent)]
        self.create_behavior_libs()

    def set_agent_actions(self,total_actions,agent_actions):
        self.total_actions = total_actions
        self.agents_actions = agent_actions
        for act in total_actions:
            self.blackboard["action_pre"][get_action_name(act.name)] = frozenset(act.pre)


    def print_agent_action_tabulate(self,agent_id,action):
        YELLOW = "\033[93m"
        RESET = "\033[0m"
        def colorize(items):
            return ', '.join(f"{YELLOW}{str(x)}{RESET}" for x in sorted(set(items)))
        data = [[
            f"agent {agent_id}",
            action.name,
            f"pre:{colorize(action.pre)}",
            f"add:{colorize(action.add)}",
            f"del:{colorize(action.del_set)}",
        ]]
        # 设置表头
        headers = ["Agent", "Action Name", "Preconditions", "Additions", "Deletions"]
        print(tabulate(data, tablefmt="grid")) #fancy_grid

    def step(self,action=None,num_agent = None):
        if num_agent is None:
            num_agent = self.num_agent
        self.step_count += 1
        done = True
        agents_step = 0
        # cur_agent_actions = {}

        for i in range(num_agent):
            print_colored(f"---AGENT - {i}---",color="yellow")
            action = self.agents[i].step()
            # print(f"agent {i}, {action.name}")
            if action is None:
                print(f"Agent {i} has no action")
            else:
                # cur_agent_actions[i] = action
                self.print_agent_action_tabulate(i,action)

                # execute
                if self.state >= action.pre and action.is_finish:
                    self.state = (self.state | action.add) - action.del_set
                    agents_step += 1
                elif self.state < action.pre and action.is_finish:
                    print_colored(f"AGENT-{i} cannot do it!", color="red")
                else:
                    print_colored(f"AGENT-{i} is doing {action.name}", color="green")


            if not self.agents[i].bt_success:
                done = False

        # execute
        # for agent_id,action in cur_agent_actions.items():
        #     if self.state >= action.pre:
        #         agents_step += 1
        #         self.state = (self.state | action.add) - action.del_set
        #     else:
        #         print_colored(f"AGENT-{agent_id} cannot do it!", color="red")


        if self.render_mode == "human":
            self.render()

        return self.state, done, None, {},agents_step

    def create_behavior_libs(self):
        from mabtpg.utils import get_root_path
        root_path = get_root_path()


        behavior_lib_path = f"{root_path}/envs/numericenv/behavior_lib"
        behavior_lib = BehaviorLibrary(behavior_lib_path)
        for agent in self.agents:
            agent.behavior_lib = behavior_lib