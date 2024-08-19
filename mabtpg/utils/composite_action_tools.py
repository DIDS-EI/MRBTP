import time

from mabtpg.btp.base.planning_agent import PlanningAgent
from mabtpg.btp.cabtp import CABTP
from mabtpg.envs.gridenv.minigrid.planning_action import PlanningAction
from mabtpg.utils.tools import extract_parameters_from_action_name,extract_predicate_from_action_name,extract_agent_id_from_action_name
from mabtpg.behavior_tree.btml.BTML import BTML
from mabtpg.utils import parse_predicate_logic
from mabtpg.utils.any_tree_node import AnyTreeNode
from mabtpg.behavior_tree.constants import NODE_TYPE
from mabtpg.btp.base.planning_condition import PlanningCondition

class CompositeActionPlanner:
    def __init__(self, action_model, composition_action,env=None):
        self.env = env
        self.action_model = action_model
        self.action_sequences = composition_action

        self.planning_ls = []
        self.btml_ls = []

        self.btml_dic={}
        self.expanded_num = 0
        self.expanded_time = 0
        # 获取每个 comp_act_name 对应的 agent_id 列表
        # self.comp_agents_ls_dic = {}

    def plan_sub_bt_from_filtered_actions(self,agent_comp_sequence,comp_act_name):
        """
        Plan sub-behavior trees based on filtered actions and given sequence.

        Args:
            filtered_actions (list): List of actions that match the sequence predicates.
            sequence (list): List of action predicates that define the sequence.
            composite_action_name (str): Name of the composite action.

        Returns:
            list: List of planned composite actions.
        """

        # cond = agent_comp_sequence[0].pre
        # for planning_action in agent_comp_sequence:
        #     sequence_node = AnyTreeNode(NODE_TYPE.sequence)
        #
        #     planning_condition = PlanningCondition(cond,planning_action)
        #     PlanningAgent.add_conditions(planning_condition,sequence_node)
        #
        #     cond = planning_action.pre | cond - planning_action.del_set

        # sub_goal = (agent_comp_sequence[-1].pre | agent_comp_sequence[-1].add) - agent_comp_sequence[-1].del_set
        sub_goal =  agent_comp_sequence[-1].add
        planning_algorithm = CABTP(env=self.env, verbose=False, goal=frozenset(sub_goal), action_list=agent_comp_sequence)
        result = planning_algorithm.planning()

        if result is None: return [],[]


        composite_action_model = {
            "pre": set(), # 原来那样会出现 有些pre 就没了cangoto door & cangoto key ???
            "add": set(),
            "del_set": set(),
            "cost": 0
        }
        sum_add = set()
        for i, a in enumerate(agent_comp_sequence):
            composite_action_model["pre"] |= a.pre - sum_add

            composite_action_model["add"] |= a.add
            composite_action_model["add"] -= a.del_set

            composite_action_model["del_set"] |= a.del_set
            composite_action_model["del_set"] -= a.add

            sum_add |= a.add

        # add里总是有 IsHandEmpty
        composite_action_model["del_set"] = composite_action_model["del_set"] - composite_action_model["add"]
        composite_action_model["add"] = composite_action_model["add"]-composite_action_model["pre"]

        planning_action = PlanningAction(f"{comp_act_name}()", **composite_action_model)


        # get btml
        planning_algorithm.create_anytree()
        sub_btml = BTML()
        sub_btml.cls_name = comp_act_name
        sub_btml.anytree_root = planning_algorithm.anytree_root


        return planning_action,sub_btml

    def no_agent_plan_sub_bt_from_filtered_actions(self,agent_comp_sequence,comp_act_name):
        """
        Plan sub-behavior trees based on filtered actions and given sequence.

        Args:
            filtered_actions (list): List of actions that match the sequence predicates.
            sequence (list): List of action predicates that define the sequence.
            composite_action_name (str): Name of the composite action.

        Returns:
            list: List of planned composite actions.
        """

        #
        # sub_goal =  agent_comp_sequence[-1].add
        # planning_algorithm = CABTP(env=self.env, verbose=False, goal=frozenset(sub_goal), action_list=agent_comp_sequence)
        # result = planning_algorithm.planning()

        return True,""


    def get_single_agent_composite_action(self,comp_act_name,comp_sequence,agent_id,action_model):

        if agent_id!=-1:
            agent_name = f"agent-{agent_id}"

            agent_comp_name_sequence = []
            for action_name in comp_sequence:
                cls_name, args = parse_predicate_logic(action_name)
                new_args = [agent_name if arg=="self" else arg for arg in args]
                new_name = f'{cls_name}({",".join(new_args)})'
                agent_comp_name_sequence.append(new_name)

            action_model_dic={}
            for action in action_model:
                action_model_dic[action.name] = action

            # get planning action
            agent_comp_sequence = []
            for action_name in agent_comp_name_sequence:
                if action_name in action_model_dic:
                    agent_comp_sequence.append(action_model_dic[action_name])
                else:
                    return [],[]

            planning_action, sub_btml = self.plan_sub_bt_from_filtered_actions(agent_comp_sequence,comp_act_name)
            return planning_action,sub_btml

        else:
            action_model_dic={}
            for action in action_model:
                action_model_dic[action.name] = action

            # get planning action
            success, msg = self.plan_sub_bt_from_filtered_actions(comp_sequence,comp_act_name)
            return success, msg



    def get_composite_action(self):
        """
        Generate composite actions based on action sequences for each agent.
        Args:
            None
        Returns:
            tuple: A tuple containing two dictionaries:
                - planning_ls: Dictionary with agent IDs as keys and lists of composite PlanningActions as values.
                - comp_btml_dic: Dictionary with comp_actions_name as keys and  BTMLs as values.
        """

        for agent_id, agent_composition_action_dic in enumerate(self.action_sequences):

            btml = BTML()
            planning_action_ls = []

            # Iterate through each action list for each agent
            for comp_act_name,comp_sequence in agent_composition_action_dic.items():

                start_time = time.time()
                planning_action,sub_btml = self.get_single_agent_composite_action(comp_act_name,comp_sequence,agent_id,self.action_model[agent_id])
                end_time = time.time()

                planning_action_ls.append(planning_action)
                btml.sub_btml_dict[comp_act_name] = sub_btml

                # record expanded num
                if comp_act_name not in self.btml_dic:
                    self.btml_dic[comp_act_name] = sub_btml
                    self.expanded_num += len(comp_sequence)
                    self.expanded_time += (end_time - start_time)

            self.planning_ls.append(planning_action_ls)
            self.btml_ls.append(btml)

        return self.planning_ls,self.btml_ls
