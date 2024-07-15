import os

def get_root_path():
    return os.path.abspath(
        os.path.join(__file__, "../..")
    )

ROOT_PATH = get_root_path()