"""
"""
import os
import numpy as np


__all__ = ('memmap_ndarray', 'memmap_structured_array')


def memmap_ndarray(arr, output_fname, store_shape_dtype=True):
    """ Create a Numpy memmap of the input array,
    optionally storing the array shape and dtype.

    Parameters
    ----------
    arr : ndarray
        Numpy array

    output_fname : string
        Filename of the memmap binary, including absolute path.

    store_shape_dtype : bool, optional
        If True, two additional Numpy binaries will be stored in the same parent
        directory as the output memmap file, `shape.npy` and `dtype.npy`.
        The purpose of these binaries is to facilitate calculating binary offsets.
        Default is True.
    """
    mmp = np.memmap(output_fname, mode='w+',
        dtype=arr.dtype, shape=arr.shape)
    mmp[:] = arr[:]
    del mmp

    output_dirname = os.path.dirname(output_fname)
    np.save(os.path.join(output_dirname, 'shape'), arr.shape)
    np.save(os.path.join(output_dirname, 'dtype'), arr.dtype)


def memmap_structured_array(arr, parent_dirname, *columns_to_save):
    """ Function saves a memory map of the desired columns of a structured array
    according to the standard directory tree layout.

    For each memory-mapped column, two additional Numpy binaries will be stored
    in the same directory: 1. shape.npy, 2. dtype.npy. These two binaries
    facilitate calculating binary offsets into the memory mapped array.

    Parameters
    ----------
    arr : array
        Numpy structured array

    parent_dirname : string
        Root directory where the data will be stored.

        Typically this is of the form 'some/path/subvol_0_1_2'.

    columns_to_save : sequence of strings, optional
        List of column names that will be memory-mapped to disk.
        If a single string argument ``all`` is passed, all columns will be stored.
        If no argument is passed, default behavior is to store all columns.
    """
    dt = arr.dtype

    if len(columns_to_save) == 0:
        columns_to_save = ['all']

    if columns_to_save[0] is 'all':
        columns_to_save = dt.names

    for colname in columns_to_save:
        msg = "Column name ``{0}`` does not appear in input array".format(colname)
        assert colname in dt.names, msg

        output_dirname = os.path.join(parent_dirname, colname)
        try:
            os.makedirs(output_dirname)
        except OSError:
            pass

        output_fname = os.path.join(output_dirname, colname + '.memmap')
        memmap_ndarray(arr, output_fname, store_shape_dtype=True)
