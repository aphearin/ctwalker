"""
"""
import os
import shutil
import numpy as np

from .. import write_full_tree_memmaps
from ...utils.directory_tree_iterators import fname_generator


fake_tree_dirname = "/Users/aphearin/work/sims/bolplanck/fake_small_trees"
if os.path.isdir(fake_tree_dirname):
    HAS_FAKE_TREES = True
else:
    HAS_FAKE_TREES = False


__all__ = ('test1', )


def test1():
    if HAS_FAKE_TREES:
        filepat = "tree_*.dat*"
        fname_list = list(fname_generator(fake_tree_dirname, filepat))

        output_dirname = os.path.join(os.path.dirname(fake_tree_dirname),
                "test_fake_small_trees")
        try:
            shutil.rmtree(output_dirname)
        except OSError:
            pass
        os.makedirs(output_dirname)

        desired_columns_dtype = np.dtype([('scale_factor', 'f4'), ('halo_id', 'i8')])
        colnums_to_yield = (0, 1)

        write_full_tree_memmaps(fname_list, output_dirname,
                desired_columns_dtype, *colnums_to_yield)
