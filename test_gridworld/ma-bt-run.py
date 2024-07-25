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
        print(self.pre)
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

class Leaf:
    def __init__(self,type,content):
        self.type=type
        self.content=content #conditionset or action
        self.parent=None
        self.parent_index=0

    def tick(self,state):
        if self.type=='cond':
            if self.content <= state:
                return 'success',self.content
            else:
                return 'failure',self.content
        if self.type=='act':
            if self.content.pre<=state:
                return 'running',self.content #action
            else:
                return 'failure',self.content

    def __str__(self):
        print( self.content)
        return ''

    def print_nodes(self):
        print(self.content)

    def count_size(self):
        return 1

class ControlBT:
    def __init__(self,type):
        self.type=type
        self.children=[]
        self.parent=None
        self.parent_index=0
        #self.fifo_cond_node_list=[]

    def add_child(self,subtree_list):
        for subtree in subtree_list:
            self.children.append(subtree)
            subtree.parent=self
            subtree.parent_index=len(self.children)-1
            # if isinstance(subtree,Leaf):
            #     if subtree.type =='cond':
            #         self.fifo_cond_node_list.append(subtree)
            # else:
            #         self.fifo_cond_node_list.append(subtree.fifo_cond_node_list)

    def tick(self,state):
        if len(self.children) < 1:
            print("error,no child")
        if self.type =='?':
            for child in self.children:
                val,obj=child.tick(state)
                if val=='success':
                    return val,obj
                if val=='running':
                    return val,obj
            return 'failure','?fails'
        if self.type =='>':
            for child in self.children:
                val,obj=child.tick(state)
                if val=='failure':
                    return val,obj
                if val=='running':
                    return val,obj
            return 'success', '>success'
        if self.type =='act':
            return self.children[0].tick(state)
        if self.type =='cond':
            return self.children[0].tick(state)

    def getFirstChild(self):
        return self.children[0]

    def __str__(self):
        print(self.type+'\n')
        for child in self.children:
            print (child)
        return ''

    def print_nodes(self):
        print(self.type)
        for child in self.children:
            child.print_nodes()
    def count_size(self):
        result=1
        for child in self.children:
            result+= child.count_size()
        return result

class CommCenter:
    def __init__(self):
        self.condition_queue=[]
        self.comm_count=0
        self.condition_count=0
        self.index=0
        self.group_size=1

    def add_goal(self,goal):
        self.condition_queue.append(goal)

    def add_conditions(self,conditions):
        for cond in conditions:
            if cond not in self.condition_queue:
                self.condition_queue.append(cond)
            self.condition_count+=1
        self.comm_count+=1

    def get_condition(self):
        self.comm_count+=self.group_size
        self.condition_count += self.group_size
        c = self.condition_queue[self.index]
        self.index+=1
        return c

    def clear(self):
        self.condition_queue = []
        self.comm_count = 0
        self.condition_count = 0
        self.index = 0


global comm_center
comm_center = CommCenter()


class Robot:
    def __init__(self):
        self.bt = ControlBT(type='?')
        self.actions=[]
        self.nodes =[] #condition nodes
        self.traversed = [] #expanded

    def isEmptyTree(self):
        if len(self.bt.children)==0:
            return True
        return False

    def tick(self,state):
        if self.isEmptyTree():
            return 'failure',{}
        return self.bt.tick(state)

    def expand_with_prune(self,c):
        find_condition=False
        for i in range(0, len(self.nodes)):
            if self.nodes[i].content ==c:
                find_condition=True
        if find_condition:
            self.insideExpand(c)
        else:
            self.outsideExpand(c)

    def insideExpand(self,c):
        actions = self.actions
        index = -1
        for i in range(0, len(self.nodes)):
            if self.nodes[i].content ==c:
                c_node = self.nodes[i]
                index = i
                break
        if index == -1:
            print('Failure')
            return False
        subtree = ControlBT(type='?')
        subtree.add_child([copy.deepcopy(c_node)])
        c = c_node.content
        new_conditions=[]
        expanded = False
        for i in range(0, len(actions)):
            # print("have action")
            if not c & ((actions[i].pre | actions[i].add) - actions[i].del_set) <= set():
                # print ("pass add")
                if (c - actions[i].del_set) == c:
                    # print("pass delete")
                    c_attr = (actions[i].pre | c) - actions[i].add
                    valid = True
                    for j in self.traversed:
                        if j <= c_attr:
                            valid = False
                            break
                    if valid:
                        # print("pass prune")
                        sequence_structure = ControlBT(type='>')
                        c_attr_node = Leaf(type='cond', content=c_attr)
                        a_node = Leaf(type='act', content=actions[i])
                        sequence_structure.add_child([c_attr_node, a_node])
                        subtree.add_child([sequence_structure])

                        self.nodes.append(c_attr_node)
                        new_conditions.append(c_attr)
                        expanded = True
        if not expanded:
            return True
        parent_of_c = c_node.parent
        parent_of_c.children[0] = subtree
        self.traversed.append(c)
        comm_center.add_conditions(new_conditions)

    def outsideExpand(self,c):
        actions = self.actions
        c_node = Leaf(type='cond', content=c)
        subtree = ControlBT(type='?')
        subtree.add_child([c_node])
        c = c_node.content
        expanded = False
        new_conditions=[]
        for i in range(0, len(actions)):
            # print("have action")
            if not c & ((actions[i].pre | actions[i].add) - actions[i].del_set) <= set():
                # print ("pass add")
                if (c - actions[i].del_set) == c:
                    # print("pass delete")
                    c_attr = (actions[i].pre | c) - actions[i].add
                    valid = True
                    for j in self.traversed:
                        if j <= c_attr:
                            valid = False
                            break
                    if valid:
                        # print("pass prune")
                        sequence_structure = ControlBT(type='>')
                        c_attr_node = Leaf(type='cond', content=c_attr)
                        a_node = Leaf(type='act', content=actions[i])
                        sequence_structure.add_child([c_attr_node, a_node])
                        subtree.add_child([sequence_structure])

                        self.nodes.append(c_attr_node)
                        new_conditions.append(c_attr)
                        expanded = True
        if not expanded:
            return True
        self.bt.add_child([subtree])
        self.traversed.append(c)
        comm_center.add_conditions(new_conditions)



class BTalgorithm:
    def __init__(self):
        self.bt = None
        self.nodes=[]
        self.traversed=[]
        self.conditions=[]
        self.conditions_index=[]
        #print (self.conditions_list[0])

    def clear(self):
        self.bt = None
        self.nodes = []
        self.traversed = []
        self.conditions = []
        self.conditions_index = []

    def run_algorithm(self,start,goal,actions):
        self.bt = ControlBT(type='cond')
        g_node = Leaf(type='cond', content=goal)
        self.bt.add_child([g_node])

        # self.nodes.append(goal)
        self.conditions.append(goal)
        self.nodes.append(g_node) #condition node list
        #nodes_start_index=0
        # self.conditions_index.append(0)
        val, obj = self.bt.tick(start)
        canrun = False
        if val == 'success' or val == 'running':
            canrun = True
        while not canrun:
            index = -1
            for i in range(0,len(self.nodes)):
                if self.nodes[i].content in self.traversed:
                    #nodes_start_index +=1
                    continue
                else:
                    c_node = self.nodes[i]
                    #nodes_start_index += 1
                    index = i
                    break
            if index == -1:
                print('Failure')
                return False
            #node_index = self.conditions_index[index]
            #print ('selecting'+str(c)+' with index'+str(index)+' and node index '+str(node_index))
            subtree = ControlBT(type='?')
            subtree.add_child([copy.deepcopy(c_node)])
            c = c_node.content
            for i in range(0,len(actions)):
                #print("have action")
                if not c & ( (actions[i].pre | actions[i].add)-actions[i].del_set) <=set():
                    #print ("pass add")
                    if (c - actions[i].del_set) == c:
                        #print("pass delete")
                        c_attr = (actions[i].pre | c )-actions[i].add
                        valid = True
                        for j in self.traversed:
                            if j<=c_attr:
                                valid = False
                                break
                        if valid:
                            #print("pass prune")
                            sequence_structure=ControlBT(type='>')
                            c_attr_node = Leaf(type='cond', content=c_attr)
                            #c_attr_node_tree = ControlBT(type='cond')
                            #c_attr_node_tree.add_child([c_attr_node])
                            a_node = Leaf(type='act', content=actions[i])
                            sequence_structure.add_child([c_attr_node,a_node])
                            subtree.add_child([sequence_structure])

                            self.nodes.append(c_attr_node)
                            # val, obj = subtree.tick(start)
                            # print ("subtreetick",val,obj)
                            # if c_attr <=start:
                            #     canrun=True
                            # self.nodes.append(Node(type='->',content='->'))
                            # self.nodes[node_index].add_child(self.nodes[-1])
                            # self.nodes.append(c_attr)
                            # self.nodes[-2].add_child(self.nodes[-1])
                            # self.conditions.append(c_attr)
                            # self.conditions_index.append( len(self.nodes)-1)
                            #
                            # self.nodes.append(Node(type='a',content='action'+str(i)))
                            # self.nodes[-3].add_child(self.nodes[-1])

            parent_of_c = c_node.parent
            parent_of_c.children[0] = subtree
            #c_node_tree.children[0] = subtree
            #self.bt.children[0]=subtree
            #self.print_solution()
            self.traversed.append(c)
            val, obj = self.bt.tick(start)
            canrun = False
            if val == 'success' or val == 'running':
                canrun = True
        return True

    def print_solution(self):
        print(len(self.nodes))
        # for i in self.nodes:
        #     if isinstance(i,Node):
        #         print (i.content)
        #     else:
        #         print (i)

if __name__ == '__main__':
    random.seed(1)

    # literals_num =10
    # start = generate_random_state(literals_num)
    # a = Action()
    # a.generate_from_state(start, literals_num)
    # state = state_transition(start, a)
    # algo = BTalgorithm()
    # algo.clear()
    # actions = [a]
    # goal = state
    #
    # if algo.run_algorithm(start, goal, list(actions)):
    #     val, obj = algo.bt.tick(start)
    #     print (val)
    #     print (obj)
    #     print (start,goal)
    # else:
    #     print ("No solution")
    #     print(start, goal)
    # #print (algo.bt)
    # val, obj = algo.bt.tick(start)
    # print(val)
    # print(obj)


    # literals_num=10
    # depth = 50
    # iters= 1000
    # total_tree_size = []
    # total_action_num = []
    # total_state_num = []
    # total_steps_num=[]
    # success_count =0
    # failure_count = 0
    # for count in range (0,1000):
    #     states = []
    #     actions = []
    #     start = generate_random_state(literals_num)
    #     state = start
    #     states.append(state)
    #     for i in range (0,depth):
    #         a = Action()
    #         a.generate_from_state(state,literals_num)
    #         if not a in actions:
    #             actions.append(a)
    #         state = state_transition(state,a)
    #         if state in states:
    #             pass
    #         else:
    #             states.append(state)
    #
    #     goal = states[-1]
    #     state = start
    #     for i in range (0,iters):
    #         a = Action()
    #         a.generate_from_state(state,literals_num)
    #         if not a in actions:
    #             actions.append(a)
    #         state = state_transition(state,a)
    #         if state in states:
    #             pass
    #         else:
    #             states.append(state)
    #         state = random.sample(states,1)[0]
    #
    #     algo = BTalgorithm()
    #     if algo.run_algorithm(start, goal, list(actions)):
    #         total_tree_size.append( algo.bt.count_size()-1)
    #     else:
    #         print ("error")
    #     #test code
    #     state=start
    #     steps=0
    #     val, obj = algo.bt.tick(state)
    #     while val !='success' and val !='failure':
    #         state = state_transition(state,obj)
    #         val, obj = algo.bt.tick(state)
    #         if(val == 'failure'):
    #             print("bt fails at step",steps)
    #         steps+=1
    #         if(steps>=500):
    #             break
    #     if not goal <= state:
    #         #print ("wrong solution",steps)
    #         failure_count+=1
    #
    #     else:
    #         #print ("right solution",steps)
    #         success_count+=1
    #         total_steps_num.append(steps)
    #     algo.clear()
    #     total_action_num.append(len(actions))
    #     total_state_num.append(len(states))
    # print (success_count,failure_count)
    #
    # print(np.mean(total_tree_size), np.std(total_tree_size, ddof=1))
    # print (np.mean(total_steps_num),np.std(total_steps_num,ddof=1))
    # print (np.mean(total_state_num))
    # print (np.mean(total_action_num))


#casestudy begin

    actions=[]
    a = Action(name='movebtob')
    a.pre={1,2}
    a.add={3}
    a.del_set={1,4}
    actions.append(a)
    a=Action(name='moveatob')
    a.pre={1}
    a.add={5,2}
    a.del_set={1,6}
    actions.append(a)
    a=Action(name='moveatoa')
    a.pre={7}
    a.add={8,2}
    a.del_set={7,6}
    actions.append(a)

    start = {1,7,4,6}
    goal={3}

    robot1 = Robot()
    robot1.actions=[actions[0],actions[1]]
    robot2 = Robot()
    robot2.actions=[actions[2]]
    robot_list = [robot1,robot2]
    for i in range(0,3):
        t=Robot()
        t.actions = actions
        robot_list.append(t)
    #planning begin
    canrun= False
    for rob in robot_list:
        val, obj = rob.tick(start)
        if val == 'success' or val == 'running':
            canrun = True
    comm_center.add_goal(goal)
    comm_center.group_size=len(robot_list)
    while not canrun:
        c = comm_center.get_condition()
        for rob in robot_list:
            rob.expand_with_prune(c)

            val, obj = rob.tick(start)
            if val == 'success' or val == 'running':
                canrun = True
    #test begin
    state = start
    steps = 0
    canrun,have_success,have_running,all_fail = False,False,False,True
    running_actions=[]
    for rob in robot_list:
        val, obj = rob.tick(state)
        if val == 'success' or val == 'running':
            canrun = True
            all_fail = False
        if val == 'success':
            have_success = True
        if val == 'running':
            have_running = True
            running_actions.append(obj)
            #print (obj.name)
    group_success = (not have_running) and have_success
    while (not group_success) and (not all_fail):
        state = ma_state_transition(state, running_actions)
        #next tick
        canrun, have_success, have_running, all_fail = False, False, False, True
        running_actions = []
        for rob in robot_list:
            val, obj = rob.tick(state)
            if val == 'success' or val == 'running':
                canrun = True
                all_fail = False
            if val == 'success':
                have_success = True
            if val == 'running':
                have_running = True
                running_actions.append(obj)
        group_success = (not have_running) and have_success
        #tick end
        if all_fail:
            print("all bts fail at step", steps)
        steps += 1
        if steps>=10:
            break
    if not goal <= state:
        print ("wrong solution",steps)
    else:
        print ("right solution",steps)
    if group_success:
        print ("group success")
    print('conditions transmitted:',comm_center.condition_count,'communication times:',comm_center.comm_count,'expanded conditions',comm_center.index)
    #print bt
    # for i in range(0,len(robot_list)):
    #      print("bt of robot",i+1)
    #      robot_list[i].bt.print_nodes()


    # algo = BTalgorithm()
    # algo.clear()
    # algo.run_algorithm(start, goal, list(actions))
    # state = start
    # steps = 0
    # val, obj = algo.bt.tick(state)
    # while val != 'success' and val != 'failure':
    #     state = state_transition(state, obj)
    #     print (obj.name)
    #     val, obj = algo.bt.tick(state)
    #     if (val == 'failure'):
    #         print("bt fails at step", steps)
    #     steps += 1
    # if not goal <= state:
    #     print ("wrong solution",steps)
    # else:
    #     print ("right solution",steps)
    # algo.bt.print_nodes()
    # print (algo.bt.count_size()-1)
    # algo.clear()

#case study end


    #     total_action_num.append(len(actions))
    #     total_state_num.append(len(states))
    #
    # print (np.mean(total_tree_size),np.std(total_tree_size,ddof=1))
    # print (np.mean(total_state_num))
    # print (np.mean(total_action_num))
    # #print (fail_count,danger_count)




    # algo = Weakalgorithm()
    # Init = {1, 2, 3, 5}
    # Goal = {4}
    # actions = []
    # a0 = Action()
    # a0.pre,a0.add,a0.del_set={1,0},{4},{1,3}
    # a1 = Action()
    # a1.pre, a1.add, a1.del_set = {1}, {6,0}, {1, 5}
    # a2 = Action()
    # a2.pre, a2.add, a2.del_set = {2}, {7, 0}, {2, 5}
    # actions.append(a0)
    # actions.append(a1)
    # actions.append(a2)
    #
    # algo.run_algorithm(Init,Goal,actions)
    # algo.print_solution()
