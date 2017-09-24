"""
"""
import os
import numpy as np
import pytest

from .. import write_full_tree_memmaps
from ...utils.directory_tree_iterators import fname_generator


fake_tree_dirname = "/Users/aphearin/work/sims/bolplanck/fake_small_trees"
if os.path.isdir(fake_tree_dirname):
    HAS_FAKE_TREES = True
else:
    HAS_FAKE_TREES = False


__all__ = ('test1', )


@pytest.mark.xfail
def test1():
    filepat = "tree_*.dat*"
    fname_list = list(fname_generator(fake_tree_dirname, filepat))

    output_dirname = os.path.join(os.path.dirname(fake_tree_dirname),
            "test_fake_small_trees")

    desired_columns_dtype = np.dtype([])

    write_indexing_arrays_to_disk = True

    colnums_to_yield = (0, 1, 2, 3, 10)

    msg = "Need to implement unit-tests on ``{0}``"
    raise NotImplementedError(msg.format(fake_tree_dirname))

    write_full_tree_memmaps(fname_list, output_dirname,
        desired_columns_dtype, write_indexing_arrays_to_disk, *colnums_to_yield)
