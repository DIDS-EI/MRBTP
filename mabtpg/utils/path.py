"""Path helpers for locating the :mod:`mabtpg` project root."""

import os


def get_root_path() -> str:
    """Return the absolute path of the ``mabtpg`` package directory."""
    return os.path.abspath(os.path.join(__file__, "../.."))


ROOT_PATH = get_root_path()
