from mabtpg.utils.path import get_root_path
root_path = get_root_path()
icon_folder_path = f"{root_path}\envs\gridenv\\vhgrid\objects\icons"

from mabtpg.envs.gridenv.base.object import Object

class VHGridObject(Object):
    icon_folder_path = icon_folder_path