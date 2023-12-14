# deprecated
import numpy as np

def np_custom_arange(
        *args, rtol: float=1e-05, atol: float=1e-08, include_start: bool=True, include_stop: bool = False, **kwargs
):
    """
    Combines numpy.arange and numpy.isclose to mimic open, half-open and closed intervals.

    Avoids also floating point rounding errors as with
    >>> np.arange(1, 1.3, 0.1)
    array([1., 1.1, 1.2, 1.3])

    Parameters
    ----------
    *args : float
        passed to np.arange
    rtol : float
        if last element of array is within this relative tolerance to stop and include[0]==False, it is skipped
    atol : float
        if last element of array is within this relative tolerance to stop and include[1]==False, it is skipped
    include_start: bool
        if first element is included in the returned array
    include_stop: bool
        if last elements are included in the returned array if stop equals last element
    kwargs :
        passed to np.arange

    Returns
    -------
    np.ndarray :
        as np.arange but eventually with first and last element stripped/added
    """
    # process arguments
    if len(args) == 1:
        start = 0
        stop = args[0]
        step = 1
    elif len(args) == 2:
        start, stop = args
        step = 1
    else:
        assert len(args) == 3
        start, stop, step = tuple(args)

    arr = np.arange(start, stop, step, **kwargs)
    if not include_start:
        arr = np.delete(arr, 0)

    if include_stop:
        if np.isclose(arr[-1] + step, stop, rtol=rtol, atol=atol):
            arr = np.c_[arr, arr[-1] + step]
    else:
        if np.isclose(arr[-1], stop, rtol=rtol, atol=atol):
            arr = np.delete(arr, -1)
    return arr

def np_arange_inclusive(*args, **kwargs):
    return np_custom_arange(*args, **kwargs, include_start=True, include_stop=True)

def np_arange_exclusive(*args, **kwargs):
    return np_custom_arange(*args, **kwargs, include_start=True, include_stop=False)