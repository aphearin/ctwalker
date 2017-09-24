"""
"""
try:
    import gzip
    HAS_GZIP = True
except ImportError:
    HAS_GZIP = False


__all__ = ('_compression_safe_opener', )


def _compression_safe_opener(fname):
    """ Determine whether to use *open* or *gzip.open* to read
    the input file, depending on whether or not the file is compressed.
    """
    if not HAS_GZIP:
        msg = "Must have ``gzip`` installed to use _compression_safe_opener"
        raise ImportError(msg)

    f = gzip.open(fname, 'r')
    try:
        f.read(1)
        opener = gzip.open
    except IOError:
        opener = open
    finally:
        f.close()
    return opener
