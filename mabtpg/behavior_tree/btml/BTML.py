


class BTML:
    def __init__(self):
        self.anytree = None
        self.bt_root = None
        self.composite_btml_list = []

    def clone_with_new_root(self,root):
        new_btml = BTML()
        new_btml.bt_root = root
        new_btml.composite_btml_list = self.composite_btml_list[:]
        return new_btml