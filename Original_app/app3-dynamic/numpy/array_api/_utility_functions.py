from __future__ import annotations
from ._array_object import Array
from typing import Optional, Tuple, Union
import numpy as np

def all(x: Array, /, *, axis: Optional[Union[(int, Tuple[(int, ...)])]] = None, keepdims: bool = False) -> Array:
    """
    Array API compatible wrapper for :py:func:`np.all <numpy.all>`.

    See its docstring for more information.
    """
    print('/home/jiangt/FaaSLight-Re/Original_app/app3-dynamic/numpy/array_api/_utility_functions.py=all=10')
    return Array._new(np.asarray(np.all(x._array, axis=axis, keepdims=keepdims)))

def any(x: Array, /, *, axis: Optional[Union[(int, Tuple[(int, ...)])]] = None, keepdims: bool = False) -> Array:
    """
    Array API compatible wrapper for :py:func:`np.any <numpy.any>`.

    See its docstring for more information.
    """
    print('/home/jiangt/FaaSLight-Re/Original_app/app3-dynamic/numpy/array_api/_utility_functions.py=any=25')
    return Array._new(np.asarray(np.any(x._array, axis=axis, keepdims=keepdims)))

