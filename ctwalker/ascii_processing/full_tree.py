"""
"""
import numpy as np

from ..utils import _compression_safe_opener

__all__ = ('full_tree_generator', )


def full_tree_generator(ascii_tree_fname, *colnums_to_yield):
    """ Iterate over an input ASCII Consistent Trees file yielding
    all rows of the desired columns.

    Each yielded row will contain a list of strings
    with length equal to len(colnums_to_yield).
    The final two elements yielded by the iterator are
    `tree_root_ids` and `tree_root_indices`.

    Parameters
    ----------
    ascii_tree_fname : string
        Absolute path to ascii output of Consistent Trees

    *colnums_to_yield : sequence of integers
        Sequence determines which columns the iterator will yield

    Returns
    -------
    string_data : tuple
        Tuple storing a row of requested column data.
        Each column of the yielded row has its data stored as a string.

    tree_root_ids : ndarray
        Integer array of shape (num_roots, ) storing the tree_root_ID of
        each independent root

    tree_root_indices : ndarray
        Integer array of shape (num_roots, ) storing the indices of
        the output `string_data` where each new tree starts.

    Examples
    --------
    The following toy example illustrates
    how the bookkeeping works for the returned quantities.

    >>> result = list(full_tree_generator(ascii_tree_fname, 0, 1, 2, 10))  # doctest: +SKIP
    >>> tree_root_indices = result.pop()  # doctest: +SKIP
    >>> tree_root_ids = result.pop()  # doctest: +SKIP

    The first element of ``result`` stores the first row of data in the tree file.
    This element is a tuple of strings, which in this case will have four elements
    corresponding to the data stored in columns 0, 1, 2, and 10 of the tree file.

    >>> first_row_first_tree = result[0]  # doctest: +SKIP

    In standard Consistent Trees outputs, Column 0 usually stores the scale factor,
    in which case the value of the first element of ``first_row_first_tree``
    will be the scale factor of the root snapshot (typically near unity).

    In standard Consistent Trees outputs, Column 1 usually stores the ID of the halo,
    in which case our returned ``tree_root_ids`` array will exhibit the following equality:

    >>> assert tree_root_ids[0] == int(first_row_first_tree[1])  # doctest: +SKIP

    To access the first row of the *second* full tree:

    >>> first_row_second_tree = result[tree_root_indices[1]]  # doctest: +SKIP

    Again we will see that ``first_row_second_tree[0]`` stores the scale factor of the
    root snapshot, and the following equality will hold:

    >>> assert tree_root_ids[1] == int(first_row_second_tree[1])  # doctest: +SKIP
    """
    opener = _compression_safe_opener(ascii_tree_fname)
    with opener(ascii_tree_fname, 'r') as f:

        # Skip the header, extracting num_trees
        while True:
            raw_header_line = next(f)
            if raw_header_line[0] != '#':
                break

        num_trees = int(raw_header_line)
        tree_root_indices = np.zeros(num_trees, dtype='i8')
        tree_root_ids = np.zeros(num_trees, dtype='i8')
        current_index = 0
        trunk_counter = 0
        # Iterate over remaining ascii lines
        while True:
            try:
                raw_line = next(f)
                current_index += 1

                if raw_line[0] == '#':
                    trunk_counter += 1
                    current_trunk_id = raw_line.strip().split()[-1]
                    tree_root_ids[trunk_counter-1] = current_trunk_id
                    tree_root_indices[trunk_counter-1] = current_index - trunk_counter
                else:
                    list_of_strings = raw_line.strip().split()
                    string_data = tuple(list_of_strings[idx] for idx in colnums_to_yield)
                    yield string_data

            except StopIteration:
                break

    yield tree_root_ids
    yield tree_root_indices
