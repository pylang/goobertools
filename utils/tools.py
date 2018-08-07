"""Handy tools."""


def assertFrameEqual(df1, df2, **kwds):
    """Return True if two DataFrames are equal, ignoring order of columns.

    Parameters
    ----------
    {df1, df2} : DataFrame
        Compare two objects using pandas testing tools.
    **kwds : dict-like
        Keywords for `pandas.util.testing.assert_frame_equal()`.

    References
    ----------
    .. [1] A. Hayden,  "Equality in Pandas DataFrames - Column Order Matters?"
       https://stackoverflow.com/a/14224489/4531270
       
    """
    from pandas.util.testing import assert_frame_equal
    # `sort` is deprecated; works in pandas 0.16.2; last worked in lamana 0.4.9
    # replaced `sort` with `sort_index` for pandas 0.17.1; backwards compatible
    return assert_frame_equal(
        df1.sort_index(axis=1), df2.sort_index(axis=1), check_names=True, **kwds
    )

