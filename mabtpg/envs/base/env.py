import time

from mabtpg.envs.virtualhome.simulation.unity_simulator import UnityCommunication

import gymnasium as gym

from mabtpg.utils import ROOT_PATH
import json
from mabtpg.envs.base.agent import Agent
import subprocess

from mabtpg.behavior_tree.behavior_library import BehaviorLibrary

from enum import Enum, auto

class SimulationMode(Enum):
    computing = auto()
    grid = auto()
    simulator = auto()


class Env(gym.Env):
    num_agent = 1
    behavior_lib_path = None
    print_ticks = False
    SimulationMode = SimulationMode

    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)

        self.time = 0
        self.start_time = time.time()

        self.create_behavior_lib()
        self.create_agents()

        self.simulation_mode = SimulationMode.computing
        self.action_model = None
        self.goal = None
        self.init_state =None
        self.objects = None
        self.action_space = None
        self.num_agent =None

        self.step_count=0
        self.blackboard = {
            # other subgoal: the agent's subgoal
            # if some subgoal's dependency is the agent's subgoal, [other subgoal] cannot to regard success
            # task: task_id,subgoal
            # "task_num": 0,
            # "running_tasks":[],# [(1,x),(2,x)]
            # Each key is the task name, and the value is a list containing all tasks that depend on it as successors.
            # Each key is a task name, and the value is a list of all subsequent tasks that it depends on
            # (1,x) : [(2,x),(3,x),(4,x)]
            # (2,x) : [(3,x),(4,x),..]
            # ...
            # (8,x) : []
            # "dependent_tasks_dic": {},

            # Record the dependency of each task
            # (1,x): set
            # (2,x): set

            "predict_condition": {
                "success": set(),
                "fail": set(),
            },
            "task_agents_queue":[], # The list of agents that are performing tasks, there is a list of agents that are doing tasks
            # "predict_condition": set(),  # The total hypothesis space
            "action_pre": {}
        }

    def load(self,json_path):
        with open(json_path, 'r') as json_file:
            env_info = json.load(json_file)

        self.goal = env_info["goal"]
        self.init_state = env_info["init_state"]
        self.objects = env_info["objects"]
        self.action_space = env_info["action_space"]
        self.num_agent = len(env_info["action_space"])

        pass

    def get_objects_lists(self):
        pass

    def create_action_model(self,verbose=False,centralize=False):

        # def collect_action_nodes(behavior_lib):
        #     action_list = []
        #     can_expand_ored = 0
        #     for cls in behavior_lib["Action"].values():
        #         if cls.can_be_expanded:
        #             can_expand_ored += 1
        #             # print(f"Expandable action: {cls.__name__}, with {len(cls.valid_args)} valid argument combinations")
        #             # print({cls.__name__})
        #             if cls.num_args == 0:
        #                 action_list.append(Action(name=cls.get_ins_name(), **cls.get_info()))
        #             if cls.num_args == 1:
        #                 for arg in cls.valid_args:
        #                     action_list.append(Action(name=cls.get_ins_name(arg), **cls.get_info(arg)))
        #             if cls.num_args > 1:
        #                 for args in cls.valid_args:
        #                     action_list.append(Action(name=cls.get_ins_name(*args), **cls.get_info(*args)))

        self.get_objects_lists()

        # generate action list for all Agents
        action_model = []
        for i in range(self.num_agent):
            if verbose: print("\n" + "-"*10 + f" getting action list for agent_{i} " + "-"*10)
            action_model.append([])
            for cls in self.agents[i].behavior_lib["Action"].values():
                if cls.can_be_expanded:
                    agent_action_list = cls.get_planning_action_list(self.agents[i], self)
                    action_model[i] += agent_action_list
                    if verbose:print(f"action: {cls.__name__}, got {len(agent_action_list)} instances.")

            if verbose:
                print(f"full action list ({len(action_model[i])} in total):")
                for a in action_model[i]:
                    print(a.name)
                # print(a.name,"pre:",a.pre)

        # if centralize:
        #     self.action_list = list(itertools.chain(*action_list)) #flattened_list
        # else:
        #     self.action_list = action_list

        # write it into blackboard
        for act_ls in action_model:
            for act in act_ls:
                self.blackboard["action_pre"][act.name] = frozenset(act.pre)

        self.action_model = action_model
        return action_model


    def step(self):
        self.time = time.time() - self.start_time

        for agent in self.agents:
            agent.step()

        self.env_step()

        self.last_step_time = self.time

        return self.task_finished()

    def task_finished(self):
        if {"IsIn(milk,fridge)","IsClosed(fridge)"} <= self.agents[0].condition_set:
            return True
        else:
            return False


    def create_agents(self):
        agent = Agent()
        agent.env = self
        self.agents = [agent]


    def create_behavior_lib(self):

        self.behavior_lib = BehaviorLibrary(self.behavior_lib_path)



    def env_step(self):
        pass


    def reset(self):
        raise NotImplementedError

    def close(self):
        raise NotImplementedError





