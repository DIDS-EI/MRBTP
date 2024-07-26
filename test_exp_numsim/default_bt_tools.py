

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
