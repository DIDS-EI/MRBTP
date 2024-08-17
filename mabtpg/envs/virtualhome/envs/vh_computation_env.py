# from mabtpg.envs.virtualhome.base.vh_env import VHEnv
from mabtpg.envs.virtualhome.base.vh_env import VHEnv
from mabtpg.envs.base.env import Env
from mabtpg.envs.gridenv.minigrid_computation_env.mini_comp_env import MiniCompEnv
from mabtpg.envs.virtualhome.tools import get_classify_objects_dic
import re
from mabtpg.envs.virtualhome.agent import Agent


class VHCompEnv(MiniCompEnv):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.use_atom_subtask_chain = False

        self.all_category_to_objects = None
        self.all_object_to_category = None
        self.get_all_classify_objects_dic()

        self.category_to_objects = None
        self.object_to_category =None

        self.agents = [Agent(self, i) for i in range(self.num_agent)]
        self.communication_times = 0

    def get_all_classify_objects_dic(self):
        self.all_category_to_objects, self.all_object_to_category = get_classify_objects_dic()

    def filter_objects_to_get_category(self, objects, add_obj=False):
        if add_obj:
            # self.objects = list(set(self.objects) | {
                # surface
            #     "bench", "kitchencabinet", "desk", "coffeetable", "fryingpan", \
            #
            #     # GRABBABLE
            #     "sundae", "toothpaste", "clothesshirt", "crackers", "pudding", "alcohol", "boardgame", "wallphone",
            #     "remotecontrol", \
            #     "clock", "hanger", "cutlets", "candybar", "wine", "toiletpaper", "slippers", "cereal", "apple",
            #     "magazine", \
            #     "wineglass", "milk", "cupcake", "folder", "wallpictureframe", "cellphone", "coffeepot", "crayons",
            #     "box", \
            #     "fryingpan", "radio", "chips",
            #
            #     # CONTAINERS
            #     "kitchencabinet", "washingmachine", "printer", "toaster", "closet", "box", "microwave", \
            #     "dishwasher", "fridge",
            #
            #     # can_open
            #     "coffeemaker", "cookingpot", "toothpaste", "coffeepot", "kitchencabinet",
            #
            #     # HAS_SWITCH
            #      "coffeemaker", "cellphone", "candle", "faucet", "washingmachine",
            # })

            self.objects = list( set(self.objects) | {
                # surface
                "towelrack", "bench", "kitchencabinet", "mousemat", "boardgame", "coffeetable", "fryingpan", \
                "radio", "cuttingboard", "floor", "tvstand","desk", "stove", "bed", "sofa", "plate", "bathroomcabinet","table"

                # GRABBABLE
"sundae", "toothpaste", "clothesshirt", "crackers", "pudding", "alcohol", "boardgame", "wallphone","remotecontrol", \
                 "whippedcream", "hanger", "cutlets", "candybar", "wine", "toiletpaper", "slippers", "cereal", "apple","magazine", \
                 "wineglass", "milk", "cupcake", "folder", "wallpictureframe", "cellphone", "coffeepot", "crayons","box", \
                 "fryingpan", "radio", "chips", "cuttingboard", "lime", "mug", "rug", "carrot", "cutleryfork","clothespile", \
                 "notes", "plum", "cookingpot", "toy", "salmon", "peach", "condimentbottle", "hairproduct", "salad","mouse", \

                # CONTAINERS
                "kitchencabinet", "washingmachine", "printer", "toaster", "closet", "box", "microwave", \
                "dishwasher", "fryingpan", "fridge", "toilet",

                # can_open
                "coffeemaker", "cookingpot", "toothpaste", "coffeepot", "kitchencabinet", "washingmachine", "window",
                "printer", \
                "curtains", "closet", "box"

                # HAS_SWITCH
                 "coffeemaker", "cellphone", "candle", "faucet", "washingmachine", "printer",
                "wallphone", "remotecontrol", \
                "computer", "toaster", "microwave", "dishwasher", "clock", "radio", "lightswitch", "fridge",
                "tablelamp", "stove", "tv", "oven"
            })
        objects = self.objects



        self.category_to_objects = {category: set() for category in self.all_category_to_objects.keys()}
        self.object_to_category = {}

        for obj in objects:
            if obj in self.all_object_to_category:
                categories = self.all_object_to_category[obj]
                self.object_to_category[obj] = categories
                for category in categories:
                    self.category_to_objects[category].add(obj)
        return self.category_to_objects,self.object_to_category

    def check_conflict(self,conds):
        # self状态:互斥状态映射
        mutually_exclusive_states = {
            'IsLeftHandEmpty': 'IsLeftHolding',
            'IsLeftHolding': 'IsLeftHandEmpty',
            'IsRightHandEmpty': 'IsRightHolding',
            'IsRightHolding': 'IsRightHandEmpty',

            'IsSitting': 'IsStanding',
            'IsStanding': 'IsSitting',

        }
        # 物体状态: Mapping from state to anti-state
        state_to_opposite = {
            'IsOpen': 'IsClose',
            'IsClose': 'IsOpen',
            'IsSwitchedOff': 'IsSwitchedOn',
            'IsSwitchedOn': 'IsSwitchedOff',
            'IsPlugged': 'IsUnplugged',
            'IsUnplugged': 'IsPlugged',
        }

        def update_state(c, state_dic):
            def extract_argument(state):
                match = re.search(r'\((.*?)\)', state)
                if match:
                    return match.group(1)
                return None

            for state, opposite in state_to_opposite.items():
                if state in c:
                    obj = extract_argument(c)
                    if obj in state_dic and opposite in state_dic[obj]:
                        return False
                    # 更新状态字典
                    elif obj in state_dic:
                        state_dic[obj].add(state)
                    else:
                        state_dic[obj] = set()
                        state_dic[obj].add(state)
                    break
            return True

        obj_state_dic = {}
        agent_state_dic = {}

        for agent_id in range(self.num_agent):
            agent_state_dic[f'agent-{agent_id}'] = set()

        is_near = False
        for c in conds:
            agent_id_str = None
            if "agent" in c:
                pattern = r'agent-\d'
                if re.search(pattern, c):
                    agent_id_str = re.search(pattern, c).group()  #'agent-0'

            if "IsNear" in c and is_near:
                return True
            elif "IsNear" in c:
                is_near = True
                continue
            # Cannot be updated, the value already exists in the past
            if not update_state(c, obj_state_dic):
                return True

            # Check for mutually exclusive states without obj
            if agent_id_str!=None:
                for state, opposite in mutually_exclusive_states.items():
                    if state in c and opposite in agent_state_dic[agent_id_str]:
                        return True
                    elif state in c:
                        agent_state_dic[agent_id_str].add(state)
                        break

        # for agent_id in range(self.num_agent):
        #     agent_id_str = f'agent-{agent_id}'
        #
        #     # 检查是否同时具有 'IsHoldingCleaningTool(self)', 'IsLeftHandEmpty(self)', 'IsRightHandEmpty(self)'
        #     required_states = {f'IsHoldingCleaningTool({agent_id_str})', f'IsLeftHandEmpty({agent_id_str})', f'IsRightHandEmpty({agent_id_str})'}
        #     if all(state in conds for state in required_states):
        #         return True
        #     required_states = {f'IsHoldingKnife({agent_id_str})', f'IsLeftHandEmpty({agent_id_str})', f'IsRightHandEmpty({agent_id_str})'}
        #     if all(state in conds for state in required_states):
        #         return True

        return False
