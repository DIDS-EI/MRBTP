
from mabtpg.btp.cabtp import CABTP
from mabtpg.envs.gridenv.minigrid.planning_action import PlanningAction
from mabtpg.utils.tools import extract_parameters_from_action_name,extract_predicate_from_action_name,extract_agent_id_from_action_name
from mabtpg.behavior_tree.btml.BTML import BTML

class CompositeActionPlanner:
    def __init__(self, action_lists, action_sequences):
        self.action_lists = action_lists
        self.action_sequences = action_sequences
        self.comp_actions_dic = {}
        self.comp_actions_BTML_dic = {}

    def plan_sub_bt_from_filtered_actions(self,filtered_actions,sequence,comp_actions_name):
        """
        Plan sub-behavior trees based on filtered actions and given sequence.

        Args:
            filtered_actions (list): List of actions that match the sequence predicates.
            sequence (list): List of action predicates that define the sequence.
            composite_action_name (str): Name of the composite action.

        Returns:
            list: List of planned composite actions.
        """
        composite_planning_action = []
        comp_actions_BTML = {}
        composite_BTML = None

        for act in filtered_actions:
            if sequence[-1] in act.name:
                sub_goal = (act.pre | act.add) - act.del_set

                planning_algorithm = CABTP(verbose=False, goal=frozenset(sub_goal), action_list=filtered_actions,
                                           sequence=sequence)
                planning_algorithm.planning()


                # Collect all parameters
                args_ls = []
                # cond_act_ls = planning_algorithm.collect_explored_cond_act
                seq_planning_cond = planning_algorithm.collect_explored_cond_act

                if len(seq_planning_cond) < len(sequence):
                    continue
                # 可选的组合动作
                opt_composition_act_ls = []
                cond_act_ls =[]
                for spc in seq_planning_cond:
                    seq_index,pla_cond,act = spc
                    if seq_index == len(sequence)-1: # find on path
                        cond_act_ls = [act]

                        tmp_seq = seq_index
                        # 把对应的几个拼在一起
                        while tmp_seq!=0:
                            for spc_j in seq_planning_cond:
                                seq_index_j,pla_cond_j,act_j = spc_j
                                if pla_cond_j.condition_set==pla_cond.parent_cond:
                                    cond_act_ls.append(act_j)
                                    tmp_seq = seq_index_j
                                    pla_cond = pla_cond_j
                        break
                if len(cond_act_ls) !=len(sequence):
                    print("No matching combination of actions found!!!")
                    continue


                # cond_act_ls = list(reversed(seq_planning_cond))
                # Calculate pre, add, and del for composite actions to construct PlanningAgent

                print("cond_act_ls",cond_act_ls)
                composite_action_model = {
                    "pre": set(), # 原来那样会出现 有些pre 就没了cangoto door & cangoto key ???
                    "add": set(),
                    "del_set": set(),
                    "cost": 0
                }
                sum_add = set()
                # sum_del = set()
                for i, a in enumerate(cond_act_ls):
                    # sum_add |= act.add
                    # composite_action_model["pre"] |= (act.pre - sum_add)
                    if i==0:
                        composite_action_model["pre"] = a.pre
                        composite_action_model["add"] = a.add
                        composite_action_model["del_set"] = a.del_set
                    composite_action_model["add"] = (composite_action_model["add"] | a.add) -a.del_set
                    composite_action_model["del_set"] = (composite_action_model["del_set"] | a.del_set) - a.add

                    if i>0:
                        # composite_action_model["pre"] = (act.pre-sum_add) | (composite_action_model["pre"]-act.del_set)
                        composite_action_model["pre"] |= (a.pre - sum_add)
                        # composite_action_model["pre"] = composite_action_model["pre"] - a.del_set
                    sum_add |= a.add

                    # add把pre减掉         ？
                    # composite_action_model["add"] -= composite_action_model["pre"]

                    args_ls.extend(extract_parameters_from_action_name(a.name))

                # # Preserve order and remove duplicates
                # gobetween(room-0,room-1), gobetween(room-01,room-0)
                args_ls = list(dict.fromkeys(args_ls))
                planning_action = PlanningAction(f"{comp_actions_name}({','.join(args_ls)})", **composite_action_model)

                composite_planning_action.append(planning_action)

                # get btml
                if composite_BTML==None:
                    planning_algorithm.create_anytree()


                    sub_btml = BTML()
                    sub_btml.cls_name = comp_actions_name
                    sub_btml.var_args = args_ls
                    sub_btml.anytree_root = planning_algorithm.anytree_root

                    self.comp_actions_BTML_dic[comp_actions_name] = sub_btml

                # planning_algorithm.create_anytree()
                # from mabtpg.behavior_tree.btml.BTML import BTML
                # sub_btml = BTML()
                # sub_btml.cls_name = comp_actions_name
                # sub_btml.var_args = args_ls
                # sub_btml.anytree_root = planning_algorithm.anytree_root
                #
                # comp_actions_BTML.update({comp_actions_name:sub_btml})

        return composite_planning_action,comp_actions_BTML

    def get_composite_action(self):
        """
        Generate composite actions based on action sequences for each agent.
        Args:
            None
        Returns:
            tuple: A tuple containing two dictionaries:
                - comp_actions_dic: Dictionary with agent IDs as keys and lists of composite PlanningActions as values.
                - comp_btml_dic: Dictionary with comp_actions_name as keys and  BTMLs as values.
        """

        for comp_actions_name,sequence in self.action_sequences.items():
            # last_agent_id = -1
            # planning_action = None

            # Iterate through each action list for each agent
            for i, action_list in enumerate(self.action_lists):
                agent_id = "agent-{}".format(i)

                # Filter out actions that match the sub-action list
                filtered_actions =[]
                filtered_actions_predicates = set()
                for plan_act in action_list:
                    predicates = extract_predicate_from_action_name(plan_act.name)
                    if predicates in sequence:
                        filtered_actions.append(plan_act)
                        filtered_actions_predicates.add(predicates)

                # Check if filtered_actions contains all the predicates from the sequence
                if filtered_actions_predicates != set(sequence):
                    continue

                # if planning_action != None:
                #     planning_action = modify_planning_agent(planning_action,last_agent_id,agent_id)
                #     last_agent_id = agent_id
                # else:

                # Plan sub-behavior tree from filtered actions
                agent_comp_pa_ls,agent_comp_btml_dic = self.plan_sub_bt_from_filtered_actions(filtered_actions,sequence,comp_actions_name)
                if agent_id not in self.comp_actions_dic:
                    self.comp_actions_dic[agent_id] = []
                self.comp_actions_dic[agent_id].extend(agent_comp_pa_ls)

                # new btml
                # if agent_id not in self.comp_actions_BTML_dic:
                #     self.comp_actions_BTML_dic[agent_id] = {}
                # self.comp_actions_BTML_dic[agent_id].update(agent_comp_btml_dic)

        return self.comp_actions_dic,self.comp_actions_BTML_dic
