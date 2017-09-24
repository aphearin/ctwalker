""" Module storing function used to determine
the Numpy dtype of Consistent Trees ascii data.
"""
import numpy as np


__all__ = ('simulation_column_dtype', 'sub_dtype', 'get_colnums')


def simulation_column_dtype(fname):
    """ Function returning the Numpy dtype given user-created ascii data ``fname`` that
    places the Consistent Trees header information into a specific format described below.

    See ``ctwalker/data/bolplanck_columns.dat`` for a specific example
    of the required format of the ``fname`` file.

    The ascii data in ``fname`` should have one row for every column of data in the
    Consistent Trees file. Each row should have two space-separated strings.
    The first string stores the name of the column
    (e.g., 'halo_id' or 'mvir'); column names should only use alphanumeric
    characters, and may not contain spaces or special characters.
    The second string stores the type of data.
    Use 'f4' for float, 'f8' for double, 'i4' for int, and 'i8' for long.

    Parameters
    -----------
    fname : string
        Absolute path to the ascii file providing the formatting information

    Returns
    -------
    dt : `numpy.dtype`
        Numpy dtype object defining the formatting for the Consistent Trees file
    """
    data_types = []
    with open(fname, 'r') as f:
        for raw_line in f:
            line = tuple(s for s in raw_line.strip().split())
            data_types.append(line)

    return np.dtype(data_types)


def sub_dtype(full_dtype, *names):
    """
    """
    return np.dtype([(name, full_dtype[name]) for name in names])


def get_colnums(full_dtype, *names):
    return list(full_dtype.names.index(name) for name in names)
