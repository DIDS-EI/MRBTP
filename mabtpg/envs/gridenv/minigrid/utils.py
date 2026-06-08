
import numpy as np
from minigrid.core.constants import DIR_TO_VEC

def obj_to_planning_name(obj):
    name = f"{obj.color}_{obj.type}"
    if obj.cur_pos == None:
        x="None"
        y="None"
    else:
        x, y = obj.cur_pos
    return f"{name}-{x}_{y}"


def get_direction_index(vec):
    for index, direction in enumerate(DIR_TO_VEC):
        if np.array_equal(vec, direction):
            return index
    raise ValueError(f"Vector {vec} not found in DIR_TO_VEC")

