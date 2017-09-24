"""
"""
import os
from .. import write_full_tree_memmaps


fake_tree_dirname = "/Users/aphearin/work/sims/bolplanck/fake_small_trees"
if os.path.isdir(fake_tree_dirname):
    HAS_FAKE_TREES = True
else:
    HAS_FAKE_TREES = False


__all__ = ('test1', )


def test1():
    pass
