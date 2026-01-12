from __future__ import annotations
from ._array_object import Array
from ._dtypes import _result_type
from typing import Optional, Tuple
import numpy as np

def argmax(x: Array, /, *, axis: Optional[int] = None, keepdims: bool = False) -> Array:
    """
    Array API compatible wrapper for :py:func:`np.argmax <numpy.argmax>`.

    See its docstring for more information.
    """
    print('/home/jiangt/FaaSLight-Re/Original_app/app3-dynamic/numpy/array_api/_searching_functions.py=argmax=11')
    return Array._new(np.asarray(np.argmax(x._array, axis=axis, keepdims=keepdims)))

def argmin(x: Array, /, *, axis: Optional[int] = None, keepdims: bool = False) -> Array:
    """
    Array API compatible wrapper for :py:func:`np.argmin <numpy.argmin>`.

    See its docstring for more information.
    """
    print('/home/jiangt/FaaSLight-Re/Original_app/app3-dynamic/numpy/array_api/_searching_functions.py=argmin=20')
    return Array._new(np.asarray(np.argmin(x._array, axis=axis, keepdims=keepdims)))

def nonzero(x: Array, /) -> Tuple[(Array, ...)]:
    """
    Array API compatible wrapper for :py:func:`np.nonzero <numpy.nonzero>`.

    See its docstring for more information.
    """
    print('/home/jiangt/FaaSLight-Re/Original_app/app3-dynamic/numpy/array_api/_searching_functions.py=nonzero=29')
    return tuple((Array._new(i) for i in np.nonzero(x._array)))

def where(condition: Array, x1: Array, x2: Array, /) -> Array:
    """
    Array API compatible wrapper for :py:func:`np.where <numpy.where>`.

    See its docstring for more information.
    """
    print('/home/jiangt/FaaSLight-Re/Original_app/app3-dynamic/numpy/array_api/_searching_functions.py=where=38')
    _result_type(x1.dtype, x2.dtype)
    (x1, x2) = Array._normalize_two_args(x1, x2)
    return Array._new(np.where(condition._array, x1._array, x2._array))

