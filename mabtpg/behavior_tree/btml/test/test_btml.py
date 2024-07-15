# from mabtpg.behavior_tree.scene.scene import Scene
# from mabtpg.behavior_tree.behavior_tree.btml.btmlCompiler import load

import os
from mabtpg.behavior_tree.behavior_tree import BehaviorTree,load_btml
from mabtpg.utils.path import ROOT_PATH

if __name__ == '__main__':

    btml_path = os.path.join(ROOT_PATH, 'behavior_tree\\btml\\test\\robot.bt')

    load_btml(btml_path,verbose=True)

    bt = BehaviorTree(btml_path)
    bt.print()
