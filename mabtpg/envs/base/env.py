import time

from mabtpg.envs.virtualhome.simulation.unity_simulator import UnityCommunication

import gymnasium as gym

from mabtpg.utils import ROOT_PATH

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

            "predict_condition": {
                "success": set(),
                "fail": set(),
            },
            "task_agents_queue":[], # 在执行任务的智能体的列表，里面存正在做任务的 agent 的列表
            # "predict_condition": set(),  # 总的假设空间
            "action_pre": {}
        }

    def load(self,json):
        self.num_agent = None
        self.action_lists = []
        self.goal = None
        self.init_state = None

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
        action_list = []
        for i in range(self.num_agent):
            if verbose: print("\n" + "-"*10 + f" getting action list for agent_{i} " + "-"*10)
            action_list.append([])
            for cls in self.agents[i].behavior_lib["Action"].values():
                if cls.can_be_expanded:
                    agent_action_list = cls.get_planning_action_list(self.agents[i], self)
                    action_list[i] += agent_action_list
                    if verbose:print(f"action: {cls.__name__}, got {len(agent_action_list)} instances.")

            if verbose:
                print(f"full action list ({len(action_list[i])} in total):")
                for a in action_list[i]:
                    print(a.name)
                # print(a.name,"pre:",a.pre)

        # if centralize:
        #     self.action_list = list(itertools.chain(*action_list)) #flattened_list
        # else:
        #     self.action_list = action_list

        # write it into blackboard
        # for act_ls in action_list:
        #     for act in act_ls:
        #         self.blackboard["action_pre"][act.name] = frozenset(act.pre)

        return action_list


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





