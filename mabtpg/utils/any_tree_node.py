import copy

class AnyTreeNode:
    def __init__(self, node_type, cls_name=None,args=(),children=(),info={},has_args = True):
        self.node_type = node_type
        self.cls_name = cls_name
        self.args = args
        self.children = list(children)
        self.info = info

        self.has_args = has_args


    @property
    def print_name(self):
        if not self.has_args:
            return f"{self.node_type} {self.cls_name}"
        else:
            return f"{self.node_type} {self.cls_name}({','.join(self.args)})"

    def print(self):
        print_tree_from_root(self)

    def clone_self(self):
        return copy.deepcopy(self)

    def add_child(self,child):
        self.children.append(child)

    def add_children(self,children):
        self.children += children

    def __repr__(self):
        if not self.has_args:
            return f"{self.node_type} {self.cls_name}"
        else:
            return f'{self.node_type} {self.cls_name} {self.args}'

def new_tree_like(root,new_func):
    if not root:
        return None

    stack = [(root, new_func(root))]
    new_root = None

    while stack:
        node, new_node = stack.pop()
        if not new_root:
            new_root = new_node

        for child in node.children:
            new_child = new_func(child)
            new_node.children.append(new_child)
            stack.append((child, new_child))

    return new_root

def traverse_and_modify_tree(root,func):
    if not root:
        return

    stack = [root]
    while stack:
        node = stack.pop()
        func(node)
        stack.extend(node.children)



def print_tree_from_root(node, indent=0):
    """
    Recursively prints the tree, each child with increased indentation.

    :param node: The current tree node to print.
    :param indent: The number of '\t' to prefix the line with.
    """
    # Print the current node, adding indentation to indicate the level
    print(f"{'    ' * indent}{node.print_name}")
    # If the node has child nodes, recursively print the child nodes
    if hasattr(node, "children"):
        for child in node.children:
            print_tree_from_root(child, indent + 1)


def print_tree(root):
    if root:
        print(root)
        for child in root.children:
            print_tree(child)


if __name__ == '__main__':
    #test_gridworld
    def new_func(node):
        return AnyTreeNode(node.node_type, node.cls_name, node.args)

    root = AnyTreeNode("Type", "ClassA", "InstanceA")
    child1 = AnyTreeNode("Type", "ClassB", "InstanceB")
    child2 = AnyTreeNode("Type", "ClassC", "InstanceC")
    root.children.extend([child1, child2])
    child1.children.append(AnyTreeNode("Type", "ClassD", "InstanceD"))
    child1.children.append(AnyTreeNode("Type", "ClassE", "InstanceE"))
    child2.children.append(AnyTreeNode("Type", "ClassF", "InstanceF"))

    print('old')
    print_tree(root)

    new_root = new_tree_like(root, new_func)

    print('new')
    print_tree(new_root)
