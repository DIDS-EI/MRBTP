
from mabtpg.envs.gridenv.base.magrid_env import MAGridEnv
from mabtpg.envs.gridenv.vhgrid import Objects

class VHGridEnv(MAGridEnv):
    def __init__(self,**kwargs):
        super().__init__(**kwargs)

    def add_horz_objs(
        self,
        obj,
        x: int,
        y: int,
        length
    ):
        if length is None:
            length = self.width - x
        for i in range(0, length):
            self.add_obj(obj, x + i, y)

    def add_vert_objs(
        self,
        obj,
        x: int,
        y: int,
        length,
    ):
        if length is None:
            length = self.height - y
        for j in range(0, length):
            self.add_obj(obj, x, y + j)

    def add_rect_objs(self, obj, x: int, y: int, w: int, h: int):
        self.add_horz_objs(obj, x, y, w)
        self.add_horz_objs(obj, x, y + h - 1, w)
        self.add_vert_objs(obj, x, y, h)
        self.add_vert_objs(obj, x + w - 1, y, h)

    def _gen_grid(self, width, height):
        self.add_rect_objs(Objects.Wall(), 0, 0, width, height)
