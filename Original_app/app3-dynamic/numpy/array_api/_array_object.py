"""
Wrapper class around the ndarray object for the array API standard.

The array API standard defines some behaviors differently than ndarray, in
particular, type promotion rules are different (the standard has no
value-based casting). The standard also specifies a more limited subset of
array methods and functionalities than are implemented on ndarray. Since the
goal of the array_api namespace is to be a minimal implementation of the array
API standard, we need to define a separate wrapper class for the array_api
namespace.

The standard compliant class is only a wrapper class. It is *not* a subclass
of ndarray.
"""

from __future__ import annotations
import operator
from enum import IntEnum
from ._creation_functions import asarray
from ._dtypes import _all_dtypes, _boolean_dtypes, _integer_dtypes, _integer_or_boolean_dtypes, _floating_dtypes, _numeric_dtypes, _result_type, _dtype_categories
from typing import TYPE_CHECKING, Optional, Tuple, Union, Any, SupportsIndex
import types
if TYPE_CHECKING:
    from ._typing import Any, PyCapsule, Device, Dtype
    import numpy.typing as npt
import numpy as np
from numpy import array_api


class Array:
    """
    n-d array object for the array API namespace.

    See the docstring of :py:obj:`np.ndarray <numpy.ndarray>` for more
    information.

    This is a wrapper around numpy.ndarray that restricts the usage to only
    those things that are required by the array API namespace. Note,
    attributes on this object that start with a single underscore are not part
    of the API specification and should only be used internally. This object
    should not be constructed directly. Rather, use one of the creation
    functions, such as asarray().

    """
    _array: np.ndarray
    
    @classmethod
    def _new(cls, x, /):
        """
        This is a private method for initializing the array API Array
        object.

        Functions outside of the array_api submodule should not use this
        method. Use one of the creation functions instead, such as
        ``asarray``.

        """
        print('/home/jiangt/FaaSLight-Re/Original_app/app3-dynamic/numpy/array_api/_array_object.py=Array=_new=63')
        obj = super().__new__(cls)
        if isinstance(x, np.generic):
            x = np.asarray(x)
        if x.dtype not in _all_dtypes:
            raise TypeError(f"The array_api namespace does not support the dtype '{x.dtype}'")
        obj._array = x
        return obj
    
    def __new__(cls, *args, **kwargs):
        print('/home/jiangt/FaaSLight-Re/Original_app/app3-dynamic/numpy/array_api/_array_object.py=Array=__new__=87')
        raise TypeError('The array_api Array object should not be instantiated directly. Use an array creation function, such as asarray(), instead.')
    
    def __str__(self: Array, /) -> str:
        """
        Performs the operation __str__.
        """
        print('/home/jiangt/FaaSLight-Re/Original_app/app3-dynamic/numpy/array_api/_array_object.py=Array=__str__=95')
        return self._array.__str__().replace('array', 'Array')
    
    def __repr__(self: Array, /) -> str:
        """
        Performs the operation __repr__.
        """
        print('/home/jiangt/FaaSLight-Re/Original_app/app3-dynamic/numpy/array_api/_array_object.py=Array=__repr__=101')
        suffix = f', dtype={self.dtype.name})'
        if 0 in self.shape:
            prefix = 'empty('
            mid = str(self.shape)
        else:
            prefix = 'Array('
            mid = np.array2string(self._array, separator=', ', prefix=prefix, suffix=suffix)
        return prefix + mid + suffix
    
    def __array__(self, dtype: None | np.dtype[Any] = None) -> npt.NDArray[Any]:
        """
        Warning: this method is NOT part of the array API spec. Implementers
        of other libraries need not include it, and users should not assume it
        will be present in other implementations.

        """
        print('/home/jiangt/FaaSLight-Re/Original_app/app3-dynamic/numpy/array_api/_array_object.py=Array=__array__=116')
        return np.asarray(self._array, dtype=dtype)
    
    def _check_allowed_dtypes(self, other: bool | int | float | Array, dtype_category: str, op: str) -> Array:
        """
        Helper function for operators to only allow specific input dtypes

        Use like

            other = self._check_allowed_dtypes(other, 'numeric', '__add__')
            if other is NotImplemented:
                return other
        """
        print('/home/jiangt/FaaSLight-Re/Original_app/app3-dynamic/numpy/array_api/_array_object.py=Array=_check_allowed_dtypes=129')
        if self.dtype not in _dtype_categories[dtype_category]:
            raise TypeError(f'Only {dtype_category} dtypes are allowed in {op}')
        if isinstance(other, (int, float, bool)):
            other = self._promote_scalar(other)
        elif isinstance(other, Array):
            if other.dtype not in _dtype_categories[dtype_category]:
                raise TypeError(f'Only {dtype_category} dtypes are allowed in {op}')
        else:
            return NotImplemented
        res_dtype = _result_type(self.dtype, other.dtype)
        if op.startswith('__i'):
            if res_dtype != self.dtype:
                raise TypeError(f'Cannot perform {op} with dtypes {self.dtype} and {other.dtype}')
        return other
    
    def _promote_scalar(self, scalar):
        """
        Returns a promoted version of a Python scalar appropriate for use with
        operations on self.

        This may raise an OverflowError in cases where the scalar is an
        integer that is too large to fit in a NumPy integer dtype, or
        TypeError when the scalar type is incompatible with the dtype of self.
        """
        print('/home/jiangt/FaaSLight-Re/Original_app/app3-dynamic/numpy/array_api/_array_object.py=Array=_promote_scalar=171')
        if isinstance(scalar, bool):
            if self.dtype not in _boolean_dtypes:
                raise TypeError('Python bool scalars can only be promoted with bool arrays')
        elif isinstance(scalar, int):
            if self.dtype in _boolean_dtypes:
                raise TypeError('Python int scalars cannot be promoted with bool arrays')
        elif isinstance(scalar, float):
            if self.dtype not in _floating_dtypes:
                raise TypeError('Python float scalars can only be promoted with floating-point arrays.')
        else:
            raise TypeError("'scalar' must be a Python scalar")
        return Array._new(np.array(scalar, self.dtype))
    
    @staticmethod
    def _normalize_two_args(x1, x2) -> Tuple[(Array, Array)]:
        """
        Normalize inputs to two arg functions to fix type promotion rules

        NumPy deviates from the spec type promotion rules in cases where one
        argument is 0-dimensional and the other is not. For example:

        >>> import numpy as np
        >>> a = np.array([1.0], dtype=np.float32)
        >>> b = np.array(1.0, dtype=np.float64)
        >>> np.add(a, b) # The spec says this should be float64
        array([2.], dtype=float32)

        To fix this, we add a dimension to the 0-dimension array before passing it
        through. This works because a dimension would be added anyway from
        broadcasting, so the resulting shape is the same, but this prevents NumPy
        from not promoting the dtype.
        """
        print('/home/jiangt/FaaSLight-Re/Original_app/app3-dynamic/numpy/array_api/_array_object.py=Array=_normalize_two_args=209')
        if (x1.ndim == 0 and x2.ndim != 0):
            x1 = Array._new(x1._array[None])
        elif (x2.ndim == 0 and x1.ndim != 0):
            x2 = Array._new(x2._array[None])
        return (x1, x2)
    
    def _validate_index(self, key):
        """
        Validate an index according to the array API.

        The array API specification only requires a subset of indices that are
        supported by NumPy. This function will reject any index that is
        allowed by NumPy but not required by the array API specification. We
        always raise ``IndexError`` on such indices (the spec does not require
        any specific behavior on them, but this makes the NumPy array API
        namespace a minimal implementation of the spec). See
        https://data-apis.org/array-api/latest/API_specification/indexing.html
        for the full list of required indexing behavior

        This function raises IndexError if the index ``key`` is invalid. It
        only raises ``IndexError`` on indices that are not already rejected by
        NumPy, as NumPy will already raise the appropriate error on such
        indices. ``shape`` may be None, in which case, only cases that are
        independent of the array shape are checked.

        The following cases are allowed by NumPy, but not specified by the array
        API specification:

        - Indices to not include an implicit ellipsis at the end. That is,
          every axis of an array must be explicitly indexed or an ellipsis
          included. This behaviour is sometimes referred to as flat indexing.

        - The start and stop of a slice may not be out of bounds. In
          particular, for a slice ``i:j:k`` on an axis of size ``n``, only the
          following are allowed:

          - ``i`` or ``j`` omitted (``None``).
          - ``-n <= i <= max(0, n - 1)``.
          - For ``k > 0`` or ``k`` omitted (``None``), ``-n <= j <= n``.
          - For ``k < 0``, ``-n - 1 <= j <= max(0, n - 1)``.

        - Boolean array indices are not allowed as part of a larger tuple
          index.

        - Integer array indices are not allowed (with the exception of 0-D
          arrays, which are treated the same as scalars).

        Additionally, it should be noted that indices that would return a
        scalar in NumPy will return a 0-D array. Array scalars are not allowed
        in the specification, only 0-D arrays. This is done in the
        ``Array._new`` constructor, not this function.

        """
        print('/home/jiangt/FaaSLight-Re/Original_app/app3-dynamic/numpy/array_api/_array_object.py=Array=_validate_index=246')
        _key = (key if isinstance(key, tuple) else (key, ))
        for i in _key:
            if (isinstance(i, bool) or not ((isinstance(i, SupportsIndex) or isinstance(i, slice) or i == Ellipsis or i is None or isinstance(i, Array) or isinstance(i, np.ndarray)))):
                raise IndexError(f'Single-axes index {i} has type(i)={type(i)!r}, but only integers, slices (:), ellipsis (...), newaxis (None), zero-dimensional integer arrays and boolean arrays are specified in the Array API.')
        nonexpanding_key = []
        single_axes = []
        n_ellipsis = 0
        key_has_mask = False
        for i in _key:
            if i is not None:
                nonexpanding_key.append(i)
                if (isinstance(i, Array) or isinstance(i, np.ndarray)):
                    if i.dtype in _boolean_dtypes:
                        key_has_mask = True
                    single_axes.append(i)
                elif i == Ellipsis:
                    n_ellipsis += 1
                else:
                    single_axes.append(i)
        n_single_axes = len(single_axes)
        if n_ellipsis > 1:
            return
        elif n_ellipsis == 0:
            if (not key_has_mask and n_single_axes < self.ndim):
                raise IndexError(f'self.ndim={self.ndim!r}, but the multi-axes index only specifies {n_single_axes} dimensions. If this was intentional, add a trailing ellipsis (...) which expands into as many slices (:) as necessary - this is what np.ndarray arrays implicitly do, but such flat indexing behaviour is not specified in the Array API.')
        if n_ellipsis == 0:
            indexed_shape = self.shape
        else:
            ellipsis_start = None
            for (pos, i) in enumerate(nonexpanding_key):
                if not ((isinstance(i, Array) or isinstance(i, np.ndarray))):
                    if i == Ellipsis:
                        ellipsis_start = pos
                        break
            assert ellipsis_start is not None
            ellipsis_end = self.ndim - (n_single_axes - ellipsis_start)
            indexed_shape = self.shape[:ellipsis_start] + self.shape[ellipsis_end:]
        for (i, side) in zip(single_axes, indexed_shape):
            if isinstance(i, slice):
                if side == 0:
                    f_range = '0 (or None)'
                else:
                    f_range = f'between -{side} and {side - 1} (or None)'
                if i.start is not None:
                    try:
                        start = operator.index(i.start)
                    except TypeError:
                        pass
                    else:
                        if not -side <= start <= side:
                            raise IndexError(f'Slice {i} contains start={start!r}, but should be {f_range} for an axis of size {side} (out-of-bounds starts are not specified in the Array API)')
                if i.stop is not None:
                    try:
                        stop = operator.index(i.stop)
                    except TypeError:
                        pass
                    else:
                        if not -side <= stop <= side:
                            raise IndexError(f'Slice {i} contains stop={stop!r}, but should be {f_range} for an axis of size {side} (out-of-bounds stops are not specified in the Array API)')
            elif isinstance(i, Array):
                if (i.dtype in _boolean_dtypes and len(_key) != 1):
                    assert isinstance(key, tuple)
                    raise IndexError(f'Single-axes index {i} is a boolean array and len(key)={len(key)!r}, but masking is only specified in the Array API when the array is the sole index.')
                elif (i.dtype in _integer_dtypes and i.ndim != 0):
                    raise IndexError(f'Single-axes index {i} is a non-zero-dimensional integer array, but advanced integer indexing is not specified in the Array API.')
            elif isinstance(i, tuple):
                raise IndexError(f'Single-axes index {i} is a tuple, but nested tuple indices are not specified in the Array API.')
    
    def __abs__(self: Array, /) -> Array:
        """
        Performs the operation __abs__.
        """
        print('/home/jiangt/FaaSLight-Re/Original_app/app3-dynamic/numpy/array_api/_array_object.py=Array=__abs__=412')
        if self.dtype not in _numeric_dtypes:
            raise TypeError('Only numeric dtypes are allowed in __abs__')
        res = self._array.__abs__()
        return self.__class__._new(res)
    
    def __add__(self: Array, other: Union[(int, float, Array)], /) -> Array:
        """
        Performs the operation __add__.
        """
        print('/home/jiangt/FaaSLight-Re/Original_app/app3-dynamic/numpy/array_api/_array_object.py=Array=__add__=421')
        other = self._check_allowed_dtypes(other, 'numeric', '__add__')
        if other is NotImplemented:
            return other
        (self, other) = self._normalize_two_args(self, other)
        res = self._array.__add__(other._array)
        return self.__class__._new(res)
    
    def __and__(self: Array, other: Union[(int, bool, Array)], /) -> Array:
        """
        Performs the operation __and__.
        """
        print('/home/jiangt/FaaSLight-Re/Original_app/app3-dynamic/numpy/array_api/_array_object.py=Array=__and__=432')
        other = self._check_allowed_dtypes(other, 'integer or boolean', '__and__')
        if other is NotImplemented:
            return other
        (self, other) = self._normalize_two_args(self, other)
        res = self._array.__and__(other._array)
        return self.__class__._new(res)
    
    def __array_namespace__(self: Array, /, *, api_version: Optional[str] = None) -> types.ModuleType:
        print('/home/jiangt/FaaSLight-Re/Original_app/app3-dynamic/numpy/array_api/_array_object.py=Array=__array_namespace__=443')
        if (api_version is not None and not api_version.startswith('2021.')):
            raise ValueError(f'Unrecognized array API version: {api_version!r}')
        return array_api
    
    def __bool__(self: Array, /) -> bool:
        """
        Performs the operation __bool__.
        """
        print('/home/jiangt/FaaSLight-Re/Original_app/app3-dynamic/numpy/array_api/_array_object.py=Array=__bool__=450')
        if self._array.ndim != 0:
            raise TypeError('bool is only allowed on arrays with 0 dimensions')
        if self.dtype not in _boolean_dtypes:
            raise ValueError('bool is only allowed on boolean arrays')
        res = self._array.__bool__()
        return res
    
    def __dlpack__(self: Array, /, *, stream: None = None) -> PyCapsule:
        """
        Performs the operation __dlpack__.
        """
        print('/home/jiangt/FaaSLight-Re/Original_app/app3-dynamic/numpy/array_api/_array_object.py=Array=__dlpack__=462')
        return self._array.__dlpack__(stream=stream)
    
    def __dlpack_device__(self: Array, /) -> Tuple[(IntEnum, int)]:
        """
        Performs the operation __dlpack_device__.
        """
        print('/home/jiangt/FaaSLight-Re/Original_app/app3-dynamic/numpy/array_api/_array_object.py=Array=__dlpack_device__=468')
        return self._array.__dlpack_device__()
    
    def __eq__(self: Array, other: Union[(int, float, bool, Array)], /) -> Array:
        """
        Performs the operation __eq__.
        """
        print('/home/jiangt/FaaSLight-Re/Original_app/app3-dynamic/numpy/array_api/_array_object.py=Array=__eq__=475')
        other = self._check_allowed_dtypes(other, 'all', '__eq__')
        if other is NotImplemented:
            return other
        (self, other) = self._normalize_two_args(self, other)
        res = self._array.__eq__(other._array)
        return self.__class__._new(res)
    
    def __float__(self: Array, /) -> float:
        """
        Performs the operation __float__.
        """
        print('/home/jiangt/FaaSLight-Re/Original_app/app3-dynamic/numpy/array_api/_array_object.py=Array=__float__=488')
        if self._array.ndim != 0:
            raise TypeError('float is only allowed on arrays with 0 dimensions')
        if self.dtype not in _floating_dtypes:
            raise ValueError('float is only allowed on floating-point arrays')
        res = self._array.__float__()
        return res
    
    def __floordiv__(self: Array, other: Union[(int, float, Array)], /) -> Array:
        """
        Performs the operation __floordiv__.
        """
        print('/home/jiangt/FaaSLight-Re/Original_app/app3-dynamic/numpy/array_api/_array_object.py=Array=__floordiv__=500')
        other = self._check_allowed_dtypes(other, 'numeric', '__floordiv__')
        if other is NotImplemented:
            return other
        (self, other) = self._normalize_two_args(self, other)
        res = self._array.__floordiv__(other._array)
        return self.__class__._new(res)
    
    def __ge__(self: Array, other: Union[(int, float, Array)], /) -> Array:
        """
        Performs the operation __ge__.
        """
        print('/home/jiangt/FaaSLight-Re/Original_app/app3-dynamic/numpy/array_api/_array_object.py=Array=__ge__=511')
        other = self._check_allowed_dtypes(other, 'numeric', '__ge__')
        if other is NotImplemented:
            return other
        (self, other) = self._normalize_two_args(self, other)
        res = self._array.__ge__(other._array)
        return self.__class__._new(res)
    
    def __getitem__(self: Array, key: Union[(int, slice, ellipsis, Tuple[(Union[(int, slice, ellipsis)], ...)], Array)], /) -> Array:
        """
        Performs the operation __getitem__.
        """
        print('/home/jiangt/FaaSLight-Re/Original_app/app3-dynamic/numpy/array_api/_array_object.py=Array=__getitem__=522')
        self._validate_index(key)
        if isinstance(key, Array):
            key = key._array
        res = self._array.__getitem__(key)
        return self._new(res)
    
    def __gt__(self: Array, other: Union[(int, float, Array)], /) -> Array:
        """
        Performs the operation __gt__.
        """
        print('/home/jiangt/FaaSLight-Re/Original_app/app3-dynamic/numpy/array_api/_array_object.py=Array=__gt__=541')
        other = self._check_allowed_dtypes(other, 'numeric', '__gt__')
        if other is NotImplemented:
            return other
        (self, other) = self._normalize_two_args(self, other)
        res = self._array.__gt__(other._array)
        return self.__class__._new(res)
    
    def __int__(self: Array, /) -> int:
        """
        Performs the operation __int__.
        """
        print('/home/jiangt/FaaSLight-Re/Original_app/app3-dynamic/numpy/array_api/_array_object.py=Array=__int__=552')
        if self._array.ndim != 0:
            raise TypeError('int is only allowed on arrays with 0 dimensions')
        if self.dtype not in _integer_dtypes:
            raise ValueError('int is only allowed on integer arrays')
        res = self._array.__int__()
        return res
    
    def __index__(self: Array, /) -> int:
        """
        Performs the operation __index__.
        """
        print('/home/jiangt/FaaSLight-Re/Original_app/app3-dynamic/numpy/array_api/_array_object.py=Array=__index__=564')
        res = self._array.__index__()
        return res
    
    def __invert__(self: Array, /) -> Array:
        """
        Performs the operation __invert__.
        """
        print('/home/jiangt/FaaSLight-Re/Original_app/app3-dynamic/numpy/array_api/_array_object.py=Array=__invert__=571')
        if self.dtype not in _integer_or_boolean_dtypes:
            raise TypeError('Only integer or boolean dtypes are allowed in __invert__')
        res = self._array.__invert__()
        return self.__class__._new(res)
    
    def __le__(self: Array, other: Union[(int, float, Array)], /) -> Array:
        """
        Performs the operation __le__.
        """
        print('/home/jiangt/FaaSLight-Re/Original_app/app3-dynamic/numpy/array_api/_array_object.py=Array=__le__=580')
        other = self._check_allowed_dtypes(other, 'numeric', '__le__')
        if other is NotImplemented:
            return other
        (self, other) = self._normalize_two_args(self, other)
        res = self._array.__le__(other._array)
        return self.__class__._new(res)
    
    def __lshift__(self: Array, other: Union[(int, Array)], /) -> Array:
        """
        Performs the operation __lshift__.
        """
        print('/home/jiangt/FaaSLight-Re/Original_app/app3-dynamic/numpy/array_api/_array_object.py=Array=__lshift__=591')
        other = self._check_allowed_dtypes(other, 'integer', '__lshift__')
        if other is NotImplemented:
            return other
        (self, other) = self._normalize_two_args(self, other)
        res = self._array.__lshift__(other._array)
        return self.__class__._new(res)
    
    def __lt__(self: Array, other: Union[(int, float, Array)], /) -> Array:
        """
        Performs the operation __lt__.
        """
        print('/home/jiangt/FaaSLight-Re/Original_app/app3-dynamic/numpy/array_api/_array_object.py=Array=__lt__=602')
        other = self._check_allowed_dtypes(other, 'numeric', '__lt__')
        if other is NotImplemented:
            return other
        (self, other) = self._normalize_two_args(self, other)
        res = self._array.__lt__(other._array)
        return self.__class__._new(res)
    
    def __matmul__(self: Array, other: Array, /) -> Array:
        """
        Performs the operation __matmul__.
        """
        print('/home/jiangt/FaaSLight-Re/Original_app/app3-dynamic/numpy/array_api/_array_object.py=Array=__matmul__=613')
        other = self._check_allowed_dtypes(other, 'numeric', '__matmul__')
        if other is NotImplemented:
            return other
        res = self._array.__matmul__(other._array)
        return self.__class__._new(res)
    
    def __mod__(self: Array, other: Union[(int, float, Array)], /) -> Array:
        """
        Performs the operation __mod__.
        """
        print('/home/jiangt/FaaSLight-Re/Original_app/app3-dynamic/numpy/array_api/_array_object.py=Array=__mod__=625')
        other = self._check_allowed_dtypes(other, 'numeric', '__mod__')
        if other is NotImplemented:
            return other
        (self, other) = self._normalize_two_args(self, other)
        res = self._array.__mod__(other._array)
        return self.__class__._new(res)
    
    def __mul__(self: Array, other: Union[(int, float, Array)], /) -> Array:
        """
        Performs the operation __mul__.
        """
        print('/home/jiangt/FaaSLight-Re/Original_app/app3-dynamic/numpy/array_api/_array_object.py=Array=__mul__=636')
        other = self._check_allowed_dtypes(other, 'numeric', '__mul__')
        if other is NotImplemented:
            return other
        (self, other) = self._normalize_two_args(self, other)
        res = self._array.__mul__(other._array)
        return self.__class__._new(res)
    
    def __ne__(self: Array, other: Union[(int, float, bool, Array)], /) -> Array:
        """
        Performs the operation __ne__.
        """
        print('/home/jiangt/FaaSLight-Re/Original_app/app3-dynamic/numpy/array_api/_array_object.py=Array=__ne__=647')
        other = self._check_allowed_dtypes(other, 'all', '__ne__')
        if other is NotImplemented:
            return other
        (self, other) = self._normalize_two_args(self, other)
        res = self._array.__ne__(other._array)
        return self.__class__._new(res)
    
    def __neg__(self: Array, /) -> Array:
        """
        Performs the operation __neg__.
        """
        print('/home/jiangt/FaaSLight-Re/Original_app/app3-dynamic/numpy/array_api/_array_object.py=Array=__neg__=658')
        if self.dtype not in _numeric_dtypes:
            raise TypeError('Only numeric dtypes are allowed in __neg__')
        res = self._array.__neg__()
        return self.__class__._new(res)
    
    def __or__(self: Array, other: Union[(int, bool, Array)], /) -> Array:
        """
        Performs the operation __or__.
        """
        print('/home/jiangt/FaaSLight-Re/Original_app/app3-dynamic/numpy/array_api/_array_object.py=Array=__or__=667')
        other = self._check_allowed_dtypes(other, 'integer or boolean', '__or__')
        if other is NotImplemented:
            return other
        (self, other) = self._normalize_two_args(self, other)
        res = self._array.__or__(other._array)
        return self.__class__._new(res)
    
    def __pos__(self: Array, /) -> Array:
        """
        Performs the operation __pos__.
        """
        print('/home/jiangt/FaaSLight-Re/Original_app/app3-dynamic/numpy/array_api/_array_object.py=Array=__pos__=678')
        if self.dtype not in _numeric_dtypes:
            raise TypeError('Only numeric dtypes are allowed in __pos__')
        res = self._array.__pos__()
        return self.__class__._new(res)
    
    def __pow__(self: Array, other: Union[(int, float, Array)], /) -> Array:
        """
        Performs the operation __pow__.
        """
        print('/home/jiangt/FaaSLight-Re/Original_app/app3-dynamic/numpy/array_api/_array_object.py=Array=__pow__=687')
        from ._elementwise_functions import pow
        other = self._check_allowed_dtypes(other, 'numeric', '__pow__')
        if other is NotImplemented:
            return other
        return pow(self, other)
    
    def __rshift__(self: Array, other: Union[(int, Array)], /) -> Array:
        """
        Performs the operation __rshift__.
        """
        print('/home/jiangt/FaaSLight-Re/Original_app/app3-dynamic/numpy/array_api/_array_object.py=Array=__rshift__=700')
        other = self._check_allowed_dtypes(other, 'integer', '__rshift__')
        if other is NotImplemented:
            return other
        (self, other) = self._normalize_two_args(self, other)
        res = self._array.__rshift__(other._array)
        return self.__class__._new(res)
    
    def __setitem__(self, key: Union[(int, slice, ellipsis, Tuple[(Union[(int, slice, ellipsis)], ...)], Array)], value: Union[(int, float, bool, Array)], /) -> None:
        """
        Performs the operation __setitem__.
        """
        print('/home/jiangt/FaaSLight-Re/Original_app/app3-dynamic/numpy/array_api/_array_object.py=Array=__setitem__=711')
        self._validate_index(key)
        if isinstance(key, Array):
            key = key._array
        self._array.__setitem__(key, asarray(value)._array)
    
    def __sub__(self: Array, other: Union[(int, float, Array)], /) -> Array:
        """
        Performs the operation __sub__.
        """
        print('/home/jiangt/FaaSLight-Re/Original_app/app3-dynamic/numpy/array_api/_array_object.py=Array=__sub__=730')
        other = self._check_allowed_dtypes(other, 'numeric', '__sub__')
        if other is NotImplemented:
            return other
        (self, other) = self._normalize_two_args(self, other)
        res = self._array.__sub__(other._array)
        return self.__class__._new(res)
    
    def __truediv__(self: Array, other: Union[(float, Array)], /) -> Array:
        """
        Performs the operation __truediv__.
        """
        print('/home/jiangt/FaaSLight-Re/Original_app/app3-dynamic/numpy/array_api/_array_object.py=Array=__truediv__=743')
        other = self._check_allowed_dtypes(other, 'floating-point', '__truediv__')
        if other is NotImplemented:
            return other
        (self, other) = self._normalize_two_args(self, other)
        res = self._array.__truediv__(other._array)
        return self.__class__._new(res)
    
    def __xor__(self: Array, other: Union[(int, bool, Array)], /) -> Array:
        """
        Performs the operation __xor__.
        """
        print('/home/jiangt/FaaSLight-Re/Original_app/app3-dynamic/numpy/array_api/_array_object.py=Array=__xor__=754')
        other = self._check_allowed_dtypes(other, 'integer or boolean', '__xor__')
        if other is NotImplemented:
            return other
        (self, other) = self._normalize_two_args(self, other)
        res = self._array.__xor__(other._array)
        return self.__class__._new(res)
    
    def __iadd__(self: Array, other: Union[(int, float, Array)], /) -> Array:
        """
        Performs the operation __iadd__.
        """
        print('/home/jiangt/FaaSLight-Re/Original_app/app3-dynamic/numpy/array_api/_array_object.py=Array=__iadd__=765')
        other = self._check_allowed_dtypes(other, 'numeric', '__iadd__')
        if other is NotImplemented:
            return other
        self._array.__iadd__(other._array)
        return self
    
    def __radd__(self: Array, other: Union[(int, float, Array)], /) -> Array:
        """
        Performs the operation __radd__.
        """
        print('/home/jiangt/FaaSLight-Re/Original_app/app3-dynamic/numpy/array_api/_array_object.py=Array=__radd__=775')
        other = self._check_allowed_dtypes(other, 'numeric', '__radd__')
        if other is NotImplemented:
            return other
        (self, other) = self._normalize_two_args(self, other)
        res = self._array.__radd__(other._array)
        return self.__class__._new(res)
    
    def __iand__(self: Array, other: Union[(int, bool, Array)], /) -> Array:
        """
        Performs the operation __iand__.
        """
        print('/home/jiangt/FaaSLight-Re/Original_app/app3-dynamic/numpy/array_api/_array_object.py=Array=__iand__=786')
        other = self._check_allowed_dtypes(other, 'integer or boolean', '__iand__')
        if other is NotImplemented:
            return other
        self._array.__iand__(other._array)
        return self
    
    def __rand__(self: Array, other: Union[(int, bool, Array)], /) -> Array:
        """
        Performs the operation __rand__.
        """
        print('/home/jiangt/FaaSLight-Re/Original_app/app3-dynamic/numpy/array_api/_array_object.py=Array=__rand__=796')
        other = self._check_allowed_dtypes(other, 'integer or boolean', '__rand__')
        if other is NotImplemented:
            return other
        (self, other) = self._normalize_two_args(self, other)
        res = self._array.__rand__(other._array)
        return self.__class__._new(res)
    
    def __ifloordiv__(self: Array, other: Union[(int, float, Array)], /) -> Array:
        """
        Performs the operation __ifloordiv__.
        """
        print('/home/jiangt/FaaSLight-Re/Original_app/app3-dynamic/numpy/array_api/_array_object.py=Array=__ifloordiv__=807')
        other = self._check_allowed_dtypes(other, 'numeric', '__ifloordiv__')
        if other is NotImplemented:
            return other
        self._array.__ifloordiv__(other._array)
        return self
    
    def __rfloordiv__(self: Array, other: Union[(int, float, Array)], /) -> Array:
        """
        Performs the operation __rfloordiv__.
        """
        print('/home/jiangt/FaaSLight-Re/Original_app/app3-dynamic/numpy/array_api/_array_object.py=Array=__rfloordiv__=817')
        other = self._check_allowed_dtypes(other, 'numeric', '__rfloordiv__')
        if other is NotImplemented:
            return other
        (self, other) = self._normalize_two_args(self, other)
        res = self._array.__rfloordiv__(other._array)
        return self.__class__._new(res)
    
    def __ilshift__(self: Array, other: Union[(int, Array)], /) -> Array:
        """
        Performs the operation __ilshift__.
        """
        print('/home/jiangt/FaaSLight-Re/Original_app/app3-dynamic/numpy/array_api/_array_object.py=Array=__ilshift__=828')
        other = self._check_allowed_dtypes(other, 'integer', '__ilshift__')
        if other is NotImplemented:
            return other
        self._array.__ilshift__(other._array)
        return self
    
    def __rlshift__(self: Array, other: Union[(int, Array)], /) -> Array:
        """
        Performs the operation __rlshift__.
        """
        print('/home/jiangt/FaaSLight-Re/Original_app/app3-dynamic/numpy/array_api/_array_object.py=Array=__rlshift__=838')
        other = self._check_allowed_dtypes(other, 'integer', '__rlshift__')
        if other is NotImplemented:
            return other
        (self, other) = self._normalize_two_args(self, other)
        res = self._array.__rlshift__(other._array)
        return self.__class__._new(res)
    
    def __imatmul__(self: Array, other: Array, /) -> Array:
        """
        Performs the operation __imatmul__.
        """
        print('/home/jiangt/FaaSLight-Re/Original_app/app3-dynamic/numpy/array_api/_array_object.py=Array=__imatmul__=849')
        other = self._check_allowed_dtypes(other, 'numeric', '__imatmul__')
        if other is NotImplemented:
            return other
        other_shape = other.shape
        if (self.shape == () or other_shape == ()):
            raise ValueError('@= requires at least one dimension')
        if (len(other_shape) == 1 or other_shape[-1] != other_shape[-2]):
            raise ValueError('@= cannot change the shape of the input array')
        self._array[:] = self._array.__matmul__(other._array)
        return self
    
    def __rmatmul__(self: Array, other: Array, /) -> Array:
        """
        Performs the operation __rmatmul__.
        """
        print('/home/jiangt/FaaSLight-Re/Original_app/app3-dynamic/numpy/array_api/_array_object.py=Array=__rmatmul__=871')
        other = self._check_allowed_dtypes(other, 'numeric', '__rmatmul__')
        if other is NotImplemented:
            return other
        res = self._array.__rmatmul__(other._array)
        return self.__class__._new(res)
    
    def __imod__(self: Array, other: Union[(int, float, Array)], /) -> Array:
        """
        Performs the operation __imod__.
        """
        print('/home/jiangt/FaaSLight-Re/Original_app/app3-dynamic/numpy/array_api/_array_object.py=Array=__imod__=883')
        other = self._check_allowed_dtypes(other, 'numeric', '__imod__')
        if other is NotImplemented:
            return other
        self._array.__imod__(other._array)
        return self
    
    def __rmod__(self: Array, other: Union[(int, float, Array)], /) -> Array:
        """
        Performs the operation __rmod__.
        """
        print('/home/jiangt/FaaSLight-Re/Original_app/app3-dynamic/numpy/array_api/_array_object.py=Array=__rmod__=893')
        other = self._check_allowed_dtypes(other, 'numeric', '__rmod__')
        if other is NotImplemented:
            return other
        (self, other) = self._normalize_two_args(self, other)
        res = self._array.__rmod__(other._array)
        return self.__class__._new(res)
    
    def __imul__(self: Array, other: Union[(int, float, Array)], /) -> Array:
        """
        Performs the operation __imul__.
        """
        print('/home/jiangt/FaaSLight-Re/Original_app/app3-dynamic/numpy/array_api/_array_object.py=Array=__imul__=904')
        other = self._check_allowed_dtypes(other, 'numeric', '__imul__')
        if other is NotImplemented:
            return other
        self._array.__imul__(other._array)
        return self
    
    def __rmul__(self: Array, other: Union[(int, float, Array)], /) -> Array:
        """
        Performs the operation __rmul__.
        """
        print('/home/jiangt/FaaSLight-Re/Original_app/app3-dynamic/numpy/array_api/_array_object.py=Array=__rmul__=914')
        other = self._check_allowed_dtypes(other, 'numeric', '__rmul__')
        if other is NotImplemented:
            return other
        (self, other) = self._normalize_two_args(self, other)
        res = self._array.__rmul__(other._array)
        return self.__class__._new(res)
    
    def __ior__(self: Array, other: Union[(int, bool, Array)], /) -> Array:
        """
        Performs the operation __ior__.
        """
        print('/home/jiangt/FaaSLight-Re/Original_app/app3-dynamic/numpy/array_api/_array_object.py=Array=__ior__=925')
        other = self._check_allowed_dtypes(other, 'integer or boolean', '__ior__')
        if other is NotImplemented:
            return other
        self._array.__ior__(other._array)
        return self
    
    def __ror__(self: Array, other: Union[(int, bool, Array)], /) -> Array:
        """
        Performs the operation __ror__.
        """
        print('/home/jiangt/FaaSLight-Re/Original_app/app3-dynamic/numpy/array_api/_array_object.py=Array=__ror__=935')
        other = self._check_allowed_dtypes(other, 'integer or boolean', '__ror__')
        if other is NotImplemented:
            return other
        (self, other) = self._normalize_two_args(self, other)
        res = self._array.__ror__(other._array)
        return self.__class__._new(res)
    
    def __ipow__(self: Array, other: Union[(int, float, Array)], /) -> Array:
        """
        Performs the operation __ipow__.
        """
        print('/home/jiangt/FaaSLight-Re/Original_app/app3-dynamic/numpy/array_api/_array_object.py=Array=__ipow__=946')
        other = self._check_allowed_dtypes(other, 'numeric', '__ipow__')
        if other is NotImplemented:
            return other
        self._array.__ipow__(other._array)
        return self
    
    def __rpow__(self: Array, other: Union[(int, float, Array)], /) -> Array:
        """
        Performs the operation __rpow__.
        """
        print('/home/jiangt/FaaSLight-Re/Original_app/app3-dynamic/numpy/array_api/_array_object.py=Array=__rpow__=956')
        from ._elementwise_functions import pow
        other = self._check_allowed_dtypes(other, 'numeric', '__rpow__')
        if other is NotImplemented:
            return other
        return pow(other, self)
    
    def __irshift__(self: Array, other: Union[(int, Array)], /) -> Array:
        """
        Performs the operation __irshift__.
        """
        print('/home/jiangt/FaaSLight-Re/Original_app/app3-dynamic/numpy/array_api/_array_object.py=Array=__irshift__=969')
        other = self._check_allowed_dtypes(other, 'integer', '__irshift__')
        if other is NotImplemented:
            return other
        self._array.__irshift__(other._array)
        return self
    
    def __rrshift__(self: Array, other: Union[(int, Array)], /) -> Array:
        """
        Performs the operation __rrshift__.
        """
        print('/home/jiangt/FaaSLight-Re/Original_app/app3-dynamic/numpy/array_api/_array_object.py=Array=__rrshift__=979')
        other = self._check_allowed_dtypes(other, 'integer', '__rrshift__')
        if other is NotImplemented:
            return other
        (self, other) = self._normalize_two_args(self, other)
        res = self._array.__rrshift__(other._array)
        return self.__class__._new(res)
    
    def __isub__(self: Array, other: Union[(int, float, Array)], /) -> Array:
        """
        Performs the operation __isub__.
        """
        print('/home/jiangt/FaaSLight-Re/Original_app/app3-dynamic/numpy/array_api/_array_object.py=Array=__isub__=990')
        other = self._check_allowed_dtypes(other, 'numeric', '__isub__')
        if other is NotImplemented:
            return other
        self._array.__isub__(other._array)
        return self
    
    def __rsub__(self: Array, other: Union[(int, float, Array)], /) -> Array:
        """
        Performs the operation __rsub__.
        """
        print('/home/jiangt/FaaSLight-Re/Original_app/app3-dynamic/numpy/array_api/_array_object.py=Array=__rsub__=1000')
        other = self._check_allowed_dtypes(other, 'numeric', '__rsub__')
        if other is NotImplemented:
            return other
        (self, other) = self._normalize_two_args(self, other)
        res = self._array.__rsub__(other._array)
        return self.__class__._new(res)
    
    def __itruediv__(self: Array, other: Union[(float, Array)], /) -> Array:
        """
        Performs the operation __itruediv__.
        """
        print('/home/jiangt/FaaSLight-Re/Original_app/app3-dynamic/numpy/array_api/_array_object.py=Array=__itruediv__=1011')
        other = self._check_allowed_dtypes(other, 'floating-point', '__itruediv__')
        if other is NotImplemented:
            return other
        self._array.__itruediv__(other._array)
        return self
    
    def __rtruediv__(self: Array, other: Union[(float, Array)], /) -> Array:
        """
        Performs the operation __rtruediv__.
        """
        print('/home/jiangt/FaaSLight-Re/Original_app/app3-dynamic/numpy/array_api/_array_object.py=Array=__rtruediv__=1021')
        other = self._check_allowed_dtypes(other, 'floating-point', '__rtruediv__')
        if other is NotImplemented:
            return other
        (self, other) = self._normalize_two_args(self, other)
        res = self._array.__rtruediv__(other._array)
        return self.__class__._new(res)
    
    def __ixor__(self: Array, other: Union[(int, bool, Array)], /) -> Array:
        """
        Performs the operation __ixor__.
        """
        print('/home/jiangt/FaaSLight-Re/Original_app/app3-dynamic/numpy/array_api/_array_object.py=Array=__ixor__=1032')
        other = self._check_allowed_dtypes(other, 'integer or boolean', '__ixor__')
        if other is NotImplemented:
            return other
        self._array.__ixor__(other._array)
        return self
    
    def __rxor__(self: Array, other: Union[(int, bool, Array)], /) -> Array:
        """
        Performs the operation __rxor__.
        """
        print('/home/jiangt/FaaSLight-Re/Original_app/app3-dynamic/numpy/array_api/_array_object.py=Array=__rxor__=1042')
        other = self._check_allowed_dtypes(other, 'integer or boolean', '__rxor__')
        if other is NotImplemented:
            return other
        (self, other) = self._normalize_two_args(self, other)
        res = self._array.__rxor__(other._array)
        return self.__class__._new(res)
    
    def to_device(self: Array, device: Device, /, stream: None = None) -> Array:
        print('/home/jiangt/FaaSLight-Re/Original_app/app3-dynamic/numpy/array_api/_array_object.py=Array=to_device=1053')
        if stream is not None:
            raise ValueError('The stream argument to to_device() is not supported')
        if device == 'cpu':
            return self
        raise ValueError(f'Unsupported device {device!r}')
    
    @property
    def dtype(self) -> Dtype:
        """
        Array API compatible wrapper for :py:meth:`np.ndarray.dtype <numpy.ndarray.dtype>`.

        See its docstring for more information.
        """
        print('/home/jiangt/FaaSLight-Re/Original_app/app3-dynamic/numpy/array_api/_array_object.py=Array=dtype=1060')
        return self._array.dtype
    
    @property
    def device(self) -> Device:
        print('/home/jiangt/FaaSLight-Re/Original_app/app3-dynamic/numpy/array_api/_array_object.py=Array=device=1069')
        return 'cpu'
    
    @property
    def mT(self) -> Array:
        print('/home/jiangt/FaaSLight-Re/Original_app/app3-dynamic/numpy/array_api/_array_object.py=Array=mT=1074')
        from .linalg import matrix_transpose
        return matrix_transpose(self)
    
    @property
    def ndim(self) -> int:
        """
        Array API compatible wrapper for :py:meth:`np.ndarray.ndim <numpy.ndarray.ndim>`.

        See its docstring for more information.
        """
        print('/home/jiangt/FaaSLight-Re/Original_app/app3-dynamic/numpy/array_api/_array_object.py=Array=ndim=1079')
        return self._array.ndim
    
    @property
    def shape(self) -> Tuple[(int, ...)]:
        """
        Array API compatible wrapper for :py:meth:`np.ndarray.shape <numpy.ndarray.shape>`.

        See its docstring for more information.
        """
        print('/home/jiangt/FaaSLight-Re/Original_app/app3-dynamic/numpy/array_api/_array_object.py=Array=shape=1088')
        return self._array.shape
    
    @property
    def size(self) -> int:
        """
        Array API compatible wrapper for :py:meth:`np.ndarray.size <numpy.ndarray.size>`.

        See its docstring for more information.
        """
        print('/home/jiangt/FaaSLight-Re/Original_app/app3-dynamic/numpy/array_api/_array_object.py=Array=size=1097')
        return self._array.size
    
    @property
    def T(self) -> Array:
        """
        Array API compatible wrapper for :py:meth:`np.ndarray.T <numpy.ndarray.T>`.

        See its docstring for more information.
        """
        print('/home/jiangt/FaaSLight-Re/Original_app/app3-dynamic/numpy/array_api/_array_object.py=Array=T=1106')
        if self.ndim != 2:
            raise ValueError('x.T requires x to have 2 dimensions. Use x.mT to transpose stacks of matrices and permute_dims() to permute dimensions.')
        return self.__class__._new(self._array.T)


