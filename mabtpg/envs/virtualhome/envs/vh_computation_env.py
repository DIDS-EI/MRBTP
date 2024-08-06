# from mabtpg.envs.virtualhome.base.vh_env import VHEnv
from mabtpg.envs.virtualhome.base.vh_env import VHEnv
from mabtpg.envs.base.env import Env
from mabtpg.envs.gridenv.minigrid_computation_env.mini_comp_env import MiniCompEnv
from mabtpg.envs.virtualhome.tools import get_classify_objects_dic


class VHCompEnv(MiniCompEnv):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.use_subtask_chain = False

        self.all_category_to_objects = None
        self.all_object_to_category = None
        self.get_all_classify_objects_dic()

        self.category_to_objects = None
        self.object_to_category =None

    def get_all_classify_objects_dic(self):
        self.all_category_to_objects, self.all_object_to_category = get_classify_objects_dic()

    def filter_objects_to_get_category(self, objects):
        self.category_to_objects = {category: set() for category in self.all_category_to_objects.keys()}
        self.object_to_category = {}

        for obj in objects:
            if obj in self.all_object_to_category:
                categories = self.all_object_to_category[obj]
                self.object_to_category[obj] = categories
                for category in categories:
                    self.category_to_objects[category].add(obj)
        return self.category_to_objects,self.object_to_category