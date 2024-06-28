
from mabtpg.envs.gridenv.base.magrid_env import MAGridEnv

class VHGridEnv(MAGridEnv):
    def __init__(self,**kwargs):
        super().__init__(**kwargs)