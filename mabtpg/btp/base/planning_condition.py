class PlanningCondition:
    def __init__(self,condition,action=None,composition_action_flag=False,sub_goal=None,sub_del=None):
        self.condition_set = condition
        self.action = action
        self.children = []
        # for generate bt
        self.parent_node = None

        # for composition_action
        self.composition_action_flag = composition_action_flag
        self.sub_goal = sub_goal
        self.sub_del = sub_del