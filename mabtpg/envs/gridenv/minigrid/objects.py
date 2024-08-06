
# from minigrid.core.constants import OBJECT_TO_IDX
# from minigrid.core.world_object import *

# attr_list = ["can_overlap", "can_pickup", "can_contain"]
#
# attr_obj_dict = {}
#
# obj_instance_list = []
# # generate object instance list
# for obj_type in list(OBJECT_TO_IDX.keys())[2:-1]:
#     exec(f"obj_instance = {obj_type.title()}()")
#     obj_instance_list.append(obj_instance)
#
# print(obj_instance_list)

ALL = ["wall","floor","ball","key","box","door","goal","lava"]

CAN_GOTO = ["ball","key","box","door","goal"]

CAN_PICKUP = ["ball","key","box"]

CAN_TOGGLE = ["door"]


# for attr in attr_list:
#     for obj_type in OBJECT_TO_IDX.keys()[2:-1]:
#         pass

