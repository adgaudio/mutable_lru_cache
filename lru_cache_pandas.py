import pandas as pd


def _pd_hash_on_indexes(arg):
    """
    hash pandas objects to immutable (index, columns) without modifying the
    objects

    This hash function uniquely identifies pandas.Series and pandas.DataFrame
    by (index, columns).

    This means if values of a column have been overwritten (due to a mutable or
    "inplace" operation), this cache funtion will ignore the changes and not
    update the cache.
    """
    if isinstance(arg, (pd.DataFrame, pd.Series)):
        return (tuple(arg.index), tuple(arg.columns))
    else:
        return arg


pd_lru_cache = lru_cache_factory(_pd_hash_on_indexes)
