from mabtpg.utils.tools import print_colored

class DMRCA:
    def __init__(self, goal, start, action_lists, num_agent=None):
        self.goal = goal
        self.start = start
        self.action_lists = action_lists
        self.num_agent = num_agent
        if num_agent != len(self.action_lists):
            print_colored(f"Error num_agent {num_agent} != len(self.action_lists) {len(self.action_lists)}!",color="red")

