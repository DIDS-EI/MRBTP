import gym
from tabulate import tabulate
from mabtpg.envs.base.env import Env
from mabtpg.utils.tools import print_colored
from mabtpg import BehaviorLibrary
from mabtpg.envs.numericenv.agent import Agent

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

        self.agents = [Agent(self, i) for i in range(num_agent)]
        self.create_behavior_libs()

        self.step_count=0

        self.blackboard = {
            # other subgoal: the agent's subgoal
            # if some subgoal's dependency is the agent's subgoal, [other subgoal] cannot to regard success
            # task: task_id,subgoal
            # "task_num": 0,  # 给所有任务编个号
            # "running_tasks":[],# [(1,x),(2,x)]
            # Each key is the task name, and the value is a list containing all tasks that depend on it as successors.
            # 每个键是任务名，值是一个包含所有受其依赖的后续任务的列表
            # (1,x) : [(2,x),(3,x),(4,x)]
            # (2,x) : [(3,x),(4,x),..]
            # ...
            # (8,x) : []
            # "dependent_tasks_dic": {},

            # 记录每个任务的 dependency
            # (1,x): set
            # (2,x): set

            "task_agents_queue":[], # 在执行任务的智能体的列表，里面存正在做任务的 agent 的列表
            # "predict_condition": set(),  # 总的假设空间
            "action_pre": {}
        }

    def set_agent_actions(self,agent_actions):
        self.actions_lists = agent_actions
        for act_ls in agent_actions:
            for act in act_ls:
                self.blackboard["action_pre"][act.name] = frozenset(act.pre)


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
                if self.state >= action.pre:
                    self.state = (self.state | action.add) - action.del_set
                else:
                    print_colored(f"AGENT-{i} cannot do it!", color="red")

            if not self.agents[i].bt_success:
                done = False

        # execute
        # for agent_id,action in cur_agent_actions.items():
        #     if self.state >= action.pre:
        #         self.state = (self.state | action.add) - action.del_set
        #     else:
        #         print_colored(f"AGENT-{agent_id} cannot do it!", color="red")


        if self.render_mode == "human":
            self.render()

        return self.state, done, None, {}

    def create_behavior_libs(self):
        from mabtpg.utils import get_root_path
        root_path = get_root_path()


        behavior_lib_path = f"{root_path}/envs/numericenv/behavior_lib"
        behavior_lib = BehaviorLibrary(behavior_lib_path)
        for agent in self.agents:
            agent.behavior_lib = behavior_lib