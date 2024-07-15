from mabtpg.behavior_tree.base_nodes.Action import Action
from mabtpg.behavior_tree.base_nodes.Condition import Condition
from mabtpg.behavior_tree.base_nodes.Inverter import Inverter
from mabtpg.behavior_tree.base_nodes.Fallback import Fallback
from mabtpg.behavior_tree.base_nodes.Sequence import Sequence
from mabtpg.behavior_tree.base_nodes.Subtree import Subtree
from mabtpg.behavior_tree.base_nodes.CompositeAction import CompositeAction
from mabtpg.behavior_tree.base_nodes.CompositeCondition import CompositeCondition


base_node_map = {
    "act": Action,
    "action": Action,

    "cond": Condition,
    "condition": Condition,

    "sub": Subtree,
    "subtree": Subtree
}

base_node_type_map={
    "act": 'Action',
    "action": 'Action',

    "cond": "Condition",
    "condition": "Condition",

    "sub": 'Subtree',
    "subtree": 'Subtree'
}

control_node_map = {
    "not": Inverter,
    "selector": Fallback,
    "fallback": Fallback,
    "sequence": Sequence
}


composite_node_map = {
    "act": CompositeAction,
    "action": CompositeAction,
    "composite_action": CompositeAction,

    "cond" : CompositeCondition,
    "condition" : CompositeCondition,
    "composite_condition" : CompositeCondition,
}