"""
"""
import os
import gzip
from itertools import product


__all__ = ('get_subvolID_from_fname', )


def get_subvolID_from_fname(fname):

    subvolID = _extract_three_consecutive_integers(
        _parse_fname_into_substrings(fname))
    if subvolID == -1:
        msg = ("The filename {0} does not have \na unique triplet of integers "
            "separated by underscores".format(fname))
        raise ValueError(msg)
    else:
        return subvolID


def subvol_substring_generator(x_seq, y_seq, z_seq):
    try:
        __ = iter(x_seq)
    except TypeError:
        raise TypeError("Input ``x_seq`` must be an iterable sequence such as a list or generator")
    assert str(x_seq) != x_seq, "Input ``x_seq`` should be a list, not a single string"

    try:
        __ = iter(y_seq)
    except TypeError:
        raise TypeError("Input ``y_seq`` must be an iterable sequence such as a list or generator")
    assert str(y_seq) != y_seq, "Input ``y_seq`` should be a list, not a single string"

    try:
        __ = iter(z_seq)
    except TypeError:
        raise TypeError("Input ``z_seq`` must be an iterable sequence such as a list or generator")
    assert str(z_seq) != z_seq, "Input ``z_seq`` should be a list, not a single string"

    for x, y, z in product(x_seq, y_seq, z_seq):
        yield '_'.join((str(x), str(y), str(z)))


def count_num_trees_in_hlist_file(fname):
    """ In the header of a typical Consistent Trees ASCII file,
    there are a sequence of lines beginning with '#'. The first line that does not
    begin with '#' is a single integer providing the total number of tree roots
    in the file. The `count_num_trees_in_hlist_file` function scans the hlist file
    for this integer and returns it.

    Notes
    -----
    The algorithm used here will fail if the Consistent Trees
    header is formatted differently.
    """
    opener = _compression_safe_opener(fname)
    with opener(fname, 'r') as f:
        current_char = '#'
        while current_char == '#':
            current_char = next(f)[0]
    return int(current_char)


def _compression_safe_opener(fname):
    """ Determine whether to use *open* or *gzip.open* to read
    the input file, depending on whether or not the file is compressed.
    """
    f = gzip.open(fname, 'r')
    try:
        f.read(1)
        opener = gzip.open
    except IOError:
        opener = open
    finally:
        f.close()
    return opener


def _parse_fname_into_substrings(fname):
    basename = os.path.basename(fname)
    _tmp_fname = basename.replace('.', '_')
    return _tmp_fname.split('_')


def _is_integer(s):
    try:
        assert float(s) == round(float(s))
        assert type(s) is not bool
        return True
    except:
        return False


def _extract_three_consecutive_integers(seq):
    """ Given an input sequence, either return a three-element tuple of integers,
    or return -1, depending on whether there exists a unique appearance
    of exactly three consecutive integers in the sequence.

    The purpose of this function is to help identify whether there is a well-defined
    subvolumeID that can be determined from a filename potentially storing an hlist file.
    """
    running_triplet = [False, False, False]

    triplet_list = []
    for element in seq:
        running_triplet.append(element)
        running_triplet.pop(0)

        if list(_is_integer(e) for e in running_triplet) == [True, True, True]:
            triplet_list.append(tuple(int(r) for r in running_triplet))

    if len(triplet_list) == 1:
        return triplet_list[0]
    else:
        return -1
