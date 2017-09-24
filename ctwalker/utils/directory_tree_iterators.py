import os
import fnmatch


__all__ = ('fname_generator', 'subdirname_generator')


def fname_generator(root_dirname, basename_filepat, recursive=True):
    """ Yield the absolute path of all files in the directory
    with a basename matching the input pattern.  If ``recursive`` is True,
    the entire directory tree will be searched for matching files.

    Parameters
    ----------
    root_dirname : string

    basename_filepat : string
        String pattern used to filter the filenames,
        e.g., '*.dat' or '*mid_string_filter*'

    recursive : bool, optional
        Default is True, in which case all subdirectories of ``root_dirname``
        will be searched.

    Returns
    -------
    fname : string
        Sequence of filenames (including absolute path)
    """
    for path, dirlist, filelist in os.walk(root_dirname):
        for filename in fnmatch.filter(filelist, basename_filepat):
            yield os.path.join(path, filename)
        if not recursive:
            break


def subdirname_generator(root_dirname, subdirname_filepat, recursive=True):
    """ Yield the absolute path of all subdirectories of ``root_dirname``
    with dirnames matching the input pattern.
    If ``recursive`` is True, the entire subdirectory tree will be returned.

    Parameters
    ----------
    root_dirname : string

    subdirname_filepat : string
        String pattern used to filter the subdirectory names,
        e.g., '*.dat' or '*mid_string_filter*'

    recursive : bool, optional
        Default is True, in which case all subdirectories of ``root_dirname``
        will be returned. If False, only top-level subdirectories will be returned.

    Returns
    -------
    dirname : string
        Sequence of directory names (including absolute path)
    """

    for path, dirlist, filelist in os.walk(root_dirname):
        for dirname in fnmatch.filter(dirlist, subdirname_filepat):
            yield os.path.join(root_dirname, dirname)
        if not recursive:
            break
