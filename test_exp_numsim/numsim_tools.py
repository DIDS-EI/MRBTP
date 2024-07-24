import random
import numpy as np
import copy

class Action:
    def __init__(self,name='anonymous action'):
        self.pre=set()
        self.add=set()
        self.del_set=set()
        self.name=name

    def __str__(self):
        return self.name

    def generate_from_state(self,state,num):
        for i in range(0,num):
            if i in state:
                if random.random() >0.5:
                    self.pre.add(i)
                    if random.random() >0.5:
                        self.del_set.add(i)
                    continue
            if random.random() > 0.5:
                self.add.add(i)
                continue
            if random.random() >0.5:
                self.del_set.add(i)

    def print_action(self):
        print (self.pre)
        print(self.add)
        print(self.del_set)


def generate_random_state(num):
    result = set()
    for i in range(0,num):
        if random.random()>0.5:
            result.add(i)
    return result

def state_transition(state,action):
    if not action.pre <= state:
        print ('error: action not applicable')
        return state
    new_state=(state | action.add) - action.del_set
    return new_state

def ma_state_transition(state,action_list):
    new_state = state
    for action in action_list:
        if not action.pre <= state:
            print('error: action not applicable')
            print (action.name,action.pre,state)
            return state
    for action in action_list:
        new_state = (new_state | action.add) - action.del_set
    return new_state
