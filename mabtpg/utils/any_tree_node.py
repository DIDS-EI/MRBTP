"""Generic n-ary tree node used by :mod:`mabtpg.behavior_tree.btml`."""

from __future__ import annotations

import copy
from typing import Callable, Iterable, List, Optional


class AnyTreeNode:
    """Lightweight n-ary tree node.

    Attributes:
        node_type: A label identifying the node's role (e.g. a value from
            :class:`mabtpg.behavior_tree.constants.NODE_TYPE`).
        cls_name: The class name represented by this node, if any.
        args:     Positional arguments associated with the node.
        children: Child nodes (mutable).
        info:     Free-form metadata dictionary.
        has_args: Whether ``args`` should be rendered alongside the name.
    """

    def __init__(
        self,
        node_type,
        cls_name: Optional[str] = None,
        args: Iterable = (),
        children: Iterable["AnyTreeNode"] = (),
        info: Optional[dict] = None,
        has_args: bool = True,
    ):
        self.node_type = node_type
        self.cls_name = cls_name
        self.args = args
        self.children: List["AnyTreeNode"] = list(children)
        # Default to a fresh dict per instance to avoid shared-mutable-default bugs.
        self.info: dict = dict(info) if info is not None else {}
        self.has_args = has_args

    @property
    def print_name(self) -> str:
        if not self.has_args:
            return f"{self.node_type} {self.cls_name}"
        return f"{self.node_type} {self.cls_name}({','.join(self.args)})"

    def print(self) -> None:
        print_tree_from_root(self)

    def clone_self(self) -> "AnyTreeNode":
        return copy.deepcopy(self)

    def add_child(self, child: "AnyTreeNode") -> None:
        self.children.append(child)

    def add_children(self, children: Iterable["AnyTreeNode"]) -> None:
        self.children += list(children)

    def __repr__(self) -> str:
        if not self.has_args:
            return f"{self.node_type} {self.cls_name}"
        return f"{self.node_type} {self.cls_name} {self.args}"


# --------------------------------------------------------------------------- #
# Generic tree algorithms
# --------------------------------------------------------------------------- #

def new_tree_like(root: Optional[AnyTreeNode], new_func: Callable[[AnyTreeNode], AnyTreeNode]):
    """Build a new tree by mapping ``new_func`` over each node of ``root``."""
    if not root:
        return None

    new_root = new_func(root)
    stack = [(root, new_root)]
    while stack:
        node, new_node = stack.pop()
        for child in node.children:
            new_child = new_func(child)
            new_node.children.append(new_child)
            stack.append((child, new_child))
    return new_root


def traverse_and_modify_tree(root: Optional[AnyTreeNode], func: Callable[[AnyTreeNode], None]) -> None:
    """Pre-order traverse the tree, applying ``func`` in place to each node."""
    if not root:
        return
    stack = [root]
    while stack:
        node = stack.pop()
        func(node)
        stack.extend(node.children)


def print_tree_from_root(node: AnyTreeNode, indent: int = 0) -> None:
    """Recursively print the tree, indented by depth."""
    print(f"{'    ' * indent}{node.print_name}")
    if hasattr(node, "children"):
        for child in node.children:
            print_tree_from_root(child, indent + 1)


def print_tree(root: Optional[AnyTreeNode]) -> None:
    """Pre-order print of the tree using each node's ``__repr__``."""
    if root is None:
        return
    print(root)
    for child in root.children:
        print_tree(child)


if __name__ == "__main__":
    # Tiny self-test.
    def _new(node: AnyTreeNode) -> AnyTreeNode:
        return AnyTreeNode(node.node_type, node.cls_name, node.args)

    root = AnyTreeNode("Type", "ClassA", ("InstanceA",))
    a = AnyTreeNode("Type", "ClassB", ("InstanceB",))
    b = AnyTreeNode("Type", "ClassC", ("InstanceC",))
    root.children.extend([a, b])
    a.children.append(AnyTreeNode("Type", "ClassD", ("InstanceD",)))
    a.children.append(AnyTreeNode("Type", "ClassE", ("InstanceE",)))
    b.children.append(AnyTreeNode("Type", "ClassF", ("InstanceF",)))

    print("old")
    print_tree(root)
    print("new")
    print_tree(new_tree_like(root, _new))
