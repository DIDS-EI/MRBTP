class PlanningCondition:
    def __init__(self,condition,action=None):
        self.condition_set = condition
        self.action = action
        self.children = []
        # for generate bt
        self.parent_node = None
