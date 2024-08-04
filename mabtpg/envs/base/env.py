import time

from mabtpg.envs.virtualhome.simulation.unity_simulator import UnityCommunication

import gymnasium as gym

from mabtpg.utils import ROOT_PATH

from mabtpg.envs.base.agent import Agent
import subprocess

from mabtpg.behavior_tree.behavior_library import BehaviorLibrary


class Env(gym.Env):
    agent_num = 1
    behavior_lib_path = None
    print_ticks = False
    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)

        self.time = 0
        self.start_time = time.time()

        self.create_behavior_lib()
        self.create_agents()

        self.simulation_mode = "simulation" # "computation"

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





