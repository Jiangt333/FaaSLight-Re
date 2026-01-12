"""
Standard container-class for easy multiple-inheritance.

Try to inherit from the ndarray instead of using this class as this is not
complete.

"""

from numpy.core import array, asarray, absolute, add, subtract, multiply, divide, remainder, power, left_shift, right_shift, bitwise_and, bitwise_or, bitwise_xor, invert, less, less_equal, not_equal, equal, greater, greater_equal, shape, reshape, arange, sin, sqrt, transpose


class container:
    """
    container(data, dtype=None, copy=True)

    Standard container-class for easy multiple-inheritance.

    Methods
    -------
    copy
    tostring
    byteswap
    astype

    """
    
    def __init__(self, data, dtype=None, copy=True):
        print('/home/jiangt/FaaSLight-Re/Original_app/app3-dynamic/numpy/lib/user_array.py=container=__init__=30')
        self.array = array(data, dtype, copy=copy)
    
    def __repr__(self):
        print('/home/jiangt/FaaSLight-Re/Original_app/app3-dynamic/numpy/lib/user_array.py=container=__repr__=33')
        if self.ndim > 0:
            return self.__class__.__name__ + repr(self.array)[len('array'):]
        else:
            return self.__class__.__name__ + '(' + repr(self.array) + ')'
    
    def __array__(self, t=None):
        print('/home/jiangt/FaaSLight-Re/Original_app/app3-dynamic/numpy/lib/user_array.py=container=__array__=39')
        if t:
            return self.array.astype(t)
        return self.array
    
    def __len__(self):
        print('/home/jiangt/FaaSLight-Re/Original_app/app3-dynamic/numpy/lib/user_array.py=container=__len__=45')
        return len(self.array)
    
    def __getitem__(self, index):
        print('/home/jiangt/FaaSLight-Re/Original_app/app3-dynamic/numpy/lib/user_array.py=container=__getitem__=48')
        return self._rc(self.array[index])
    
    def __setitem__(self, index, value):
        print('/home/jiangt/FaaSLight-Re/Original_app/app3-dynamic/numpy/lib/user_array.py=container=__setitem__=51')
        self.array[index] = asarray(value, self.dtype)
    
    def __abs__(self):
        print('/home/jiangt/FaaSLight-Re/Original_app/app3-dynamic/numpy/lib/user_array.py=container=__abs__=54')
        return self._rc(absolute(self.array))
    
    def __neg__(self):
        print('/home/jiangt/FaaSLight-Re/Original_app/app3-dynamic/numpy/lib/user_array.py=container=__neg__=57')
        return self._rc(-self.array)
    
    def __add__(self, other):
        print('/home/jiangt/FaaSLight-Re/Original_app/app3-dynamic/numpy/lib/user_array.py=container=__add__=60')
        return self._rc(self.array + asarray(other))
    __radd__ = __add__
    
    def __iadd__(self, other):
        print('/home/jiangt/FaaSLight-Re/Original_app/app3-dynamic/numpy/lib/user_array.py=container=__iadd__=65')
        add(self.array, other, self.array)
        return self
    
    def __sub__(self, other):
        print('/home/jiangt/FaaSLight-Re/Original_app/app3-dynamic/numpy/lib/user_array.py=container=__sub__=69')
        return self._rc(self.array - asarray(other))
    
    def __rsub__(self, other):
        print('/home/jiangt/FaaSLight-Re/Original_app/app3-dynamic/numpy/lib/user_array.py=container=__rsub__=72')
        return self._rc(asarray(other) - self.array)
    
    def __isub__(self, other):
        print('/home/jiangt/FaaSLight-Re/Original_app/app3-dynamic/numpy/lib/user_array.py=container=__isub__=75')
        subtract(self.array, other, self.array)
        return self
    
    def __mul__(self, other):
        print('/home/jiangt/FaaSLight-Re/Original_app/app3-dynamic/numpy/lib/user_array.py=container=__mul__=79')
        return self._rc(multiply(self.array, asarray(other)))
    __rmul__ = __mul__
    
    def __imul__(self, other):
        print('/home/jiangt/FaaSLight-Re/Original_app/app3-dynamic/numpy/lib/user_array.py=container=__imul__=84')
        multiply(self.array, other, self.array)
        return self
    
    def __div__(self, other):
        print('/home/jiangt/FaaSLight-Re/Original_app/app3-dynamic/numpy/lib/user_array.py=container=__div__=88')
        return self._rc(divide(self.array, asarray(other)))
    
    def __rdiv__(self, other):
        print('/home/jiangt/FaaSLight-Re/Original_app/app3-dynamic/numpy/lib/user_array.py=container=__rdiv__=91')
        return self._rc(divide(asarray(other), self.array))
    
    def __idiv__(self, other):
        print('/home/jiangt/FaaSLight-Re/Original_app/app3-dynamic/numpy/lib/user_array.py=container=__idiv__=94')
        divide(self.array, other, self.array)
        return self
    
    def __mod__(self, other):
        print('/home/jiangt/FaaSLight-Re/Original_app/app3-dynamic/numpy/lib/user_array.py=container=__mod__=98')
        return self._rc(remainder(self.array, other))
    
    def __rmod__(self, other):
        print('/home/jiangt/FaaSLight-Re/Original_app/app3-dynamic/numpy/lib/user_array.py=container=__rmod__=101')
        return self._rc(remainder(other, self.array))
    
    def __imod__(self, other):
        print('/home/jiangt/FaaSLight-Re/Original_app/app3-dynamic/numpy/lib/user_array.py=container=__imod__=104')
        remainder(self.array, other, self.array)
        return self
    
    def __divmod__(self, other):
        print('/home/jiangt/FaaSLight-Re/Original_app/app3-dynamic/numpy/lib/user_array.py=container=__divmod__=108')
        return (self._rc(divide(self.array, other)), self._rc(remainder(self.array, other)))
    
    def __rdivmod__(self, other):
        print('/home/jiangt/FaaSLight-Re/Original_app/app3-dynamic/numpy/lib/user_array.py=container=__rdivmod__=112')
        return (self._rc(divide(other, self.array)), self._rc(remainder(other, self.array)))
    
    def __pow__(self, other):
        print('/home/jiangt/FaaSLight-Re/Original_app/app3-dynamic/numpy/lib/user_array.py=container=__pow__=116')
        return self._rc(power(self.array, asarray(other)))
    
    def __rpow__(self, other):
        print('/home/jiangt/FaaSLight-Re/Original_app/app3-dynamic/numpy/lib/user_array.py=container=__rpow__=119')
        return self._rc(power(asarray(other), self.array))
    
    def __ipow__(self, other):
        print('/home/jiangt/FaaSLight-Re/Original_app/app3-dynamic/numpy/lib/user_array.py=container=__ipow__=122')
        power(self.array, other, self.array)
        return self
    
    def __lshift__(self, other):
        print('/home/jiangt/FaaSLight-Re/Original_app/app3-dynamic/numpy/lib/user_array.py=container=__lshift__=126')
        return self._rc(left_shift(self.array, other))
    
    def __rshift__(self, other):
        print('/home/jiangt/FaaSLight-Re/Original_app/app3-dynamic/numpy/lib/user_array.py=container=__rshift__=129')
        return self._rc(right_shift(self.array, other))
    
    def __rlshift__(self, other):
        print('/home/jiangt/FaaSLight-Re/Original_app/app3-dynamic/numpy/lib/user_array.py=container=__rlshift__=132')
        return self._rc(left_shift(other, self.array))
    
    def __rrshift__(self, other):
        print('/home/jiangt/FaaSLight-Re/Original_app/app3-dynamic/numpy/lib/user_array.py=container=__rrshift__=135')
        return self._rc(right_shift(other, self.array))
    
    def __ilshift__(self, other):
        print('/home/jiangt/FaaSLight-Re/Original_app/app3-dynamic/numpy/lib/user_array.py=container=__ilshift__=138')
        left_shift(self.array, other, self.array)
        return self
    
    def __irshift__(self, other):
        print('/home/jiangt/FaaSLight-Re/Original_app/app3-dynamic/numpy/lib/user_array.py=container=__irshift__=142')
        right_shift(self.array, other, self.array)
        return self
    
    def __and__(self, other):
        print('/home/jiangt/FaaSLight-Re/Original_app/app3-dynamic/numpy/lib/user_array.py=container=__and__=146')
        return self._rc(bitwise_and(self.array, other))
    
    def __rand__(self, other):
        print('/home/jiangt/FaaSLight-Re/Original_app/app3-dynamic/numpy/lib/user_array.py=container=__rand__=149')
        return self._rc(bitwise_and(other, self.array))
    
    def __iand__(self, other):
        print('/home/jiangt/FaaSLight-Re/Original_app/app3-dynamic/numpy/lib/user_array.py=container=__iand__=152')
        bitwise_and(self.array, other, self.array)
        return self
    
    def __xor__(self, other):
        print('/home/jiangt/FaaSLight-Re/Original_app/app3-dynamic/numpy/lib/user_array.py=container=__xor__=156')
        return self._rc(bitwise_xor(self.array, other))
    
    def __rxor__(self, other):
        print('/home/jiangt/FaaSLight-Re/Original_app/app3-dynamic/numpy/lib/user_array.py=container=__rxor__=159')
        return self._rc(bitwise_xor(other, self.array))
    
    def __ixor__(self, other):
        print('/home/jiangt/FaaSLight-Re/Original_app/app3-dynamic/numpy/lib/user_array.py=container=__ixor__=162')
        bitwise_xor(self.array, other, self.array)
        return self
    
    def __or__(self, other):
        print('/home/jiangt/FaaSLight-Re/Original_app/app3-dynamic/numpy/lib/user_array.py=container=__or__=166')
        return self._rc(bitwise_or(self.array, other))
    
    def __ror__(self, other):
        print('/home/jiangt/FaaSLight-Re/Original_app/app3-dynamic/numpy/lib/user_array.py=container=__ror__=169')
        return self._rc(bitwise_or(other, self.array))
    
    def __ior__(self, other):
        print('/home/jiangt/FaaSLight-Re/Original_app/app3-dynamic/numpy/lib/user_array.py=container=__ior__=172')
        bitwise_or(self.array, other, self.array)
        return self
    
    def __pos__(self):
        print('/home/jiangt/FaaSLight-Re/Original_app/app3-dynamic/numpy/lib/user_array.py=container=__pos__=176')
        return self._rc(self.array)
    
    def __invert__(self):
        print('/home/jiangt/FaaSLight-Re/Original_app/app3-dynamic/numpy/lib/user_array.py=container=__invert__=179')
        return self._rc(invert(self.array))
    
    def _scalarfunc(self, func):
        print('/home/jiangt/FaaSLight-Re/Original_app/app3-dynamic/numpy/lib/user_array.py=container=_scalarfunc=182')
        if self.ndim == 0:
            return func(self[0])
        else:
            raise TypeError('only rank-0 arrays can be converted to Python scalars.')
    
    def __complex__(self):
        print('/home/jiangt/FaaSLight-Re/Original_app/app3-dynamic/numpy/lib/user_array.py=container=__complex__=189')
        return self._scalarfunc(complex)
    
    def __float__(self):
        print('/home/jiangt/FaaSLight-Re/Original_app/app3-dynamic/numpy/lib/user_array.py=container=__float__=192')
        return self._scalarfunc(float)
    
    def __int__(self):
        print('/home/jiangt/FaaSLight-Re/Original_app/app3-dynamic/numpy/lib/user_array.py=container=__int__=195')
        return self._scalarfunc(int)
    
    def __hex__(self):
        print('/home/jiangt/FaaSLight-Re/Original_app/app3-dynamic/numpy/lib/user_array.py=container=__hex__=198')
        return self._scalarfunc(hex)
    
    def __oct__(self):
        print('/home/jiangt/FaaSLight-Re/Original_app/app3-dynamic/numpy/lib/user_array.py=container=__oct__=201')
        return self._scalarfunc(oct)
    
    def __lt__(self, other):
        print('/home/jiangt/FaaSLight-Re/Original_app/app3-dynamic/numpy/lib/user_array.py=container=__lt__=204')
        return self._rc(less(self.array, other))
    
    def __le__(self, other):
        print('/home/jiangt/FaaSLight-Re/Original_app/app3-dynamic/numpy/lib/user_array.py=container=__le__=207')
        return self._rc(less_equal(self.array, other))
    
    def __eq__(self, other):
        print('/home/jiangt/FaaSLight-Re/Original_app/app3-dynamic/numpy/lib/user_array.py=container=__eq__=210')
        return self._rc(equal(self.array, other))
    
    def __ne__(self, other):
        print('/home/jiangt/FaaSLight-Re/Original_app/app3-dynamic/numpy/lib/user_array.py=container=__ne__=213')
        return self._rc(not_equal(self.array, other))
    
    def __gt__(self, other):
        print('/home/jiangt/FaaSLight-Re/Original_app/app3-dynamic/numpy/lib/user_array.py=container=__gt__=216')
        return self._rc(greater(self.array, other))
    
    def __ge__(self, other):
        print('/home/jiangt/FaaSLight-Re/Original_app/app3-dynamic/numpy/lib/user_array.py=container=__ge__=219')
        return self._rc(greater_equal(self.array, other))
    
    def copy(self):
        print('/home/jiangt/FaaSLight-Re/Original_app/app3-dynamic/numpy/lib/user_array.py=container=copy=222')
        return self._rc(self.array.copy())
    
    def tostring(self):
        print('/home/jiangt/FaaSLight-Re/Original_app/app3-dynamic/numpy/lib/user_array.py=container=tostring=226')
        return self.array.tostring()
    
    def tobytes(self):
        print('/home/jiangt/FaaSLight-Re/Original_app/app3-dynamic/numpy/lib/user_array.py=container=tobytes=230')
        return self.array.tobytes()
    
    def byteswap(self):
        print('/home/jiangt/FaaSLight-Re/Original_app/app3-dynamic/numpy/lib/user_array.py=container=byteswap=234')
        return self._rc(self.array.byteswap())
    
    def astype(self, typecode):
        print('/home/jiangt/FaaSLight-Re/Original_app/app3-dynamic/numpy/lib/user_array.py=container=astype=238')
        return self._rc(self.array.astype(typecode))
    
    def _rc(self, a):
        print('/home/jiangt/FaaSLight-Re/Original_app/app3-dynamic/numpy/lib/user_array.py=container=_rc=242')
        if len(shape(a)) == 0:
            return a
        else:
            return self.__class__(a)
    
    def __array_wrap__(self, *args):
        print('/home/jiangt/FaaSLight-Re/Original_app/app3-dynamic/numpy/lib/user_array.py=container=__array_wrap__=248')
        return self.__class__(args[0])
    
    def __setattr__(self, attr, value):
        print('/home/jiangt/FaaSLight-Re/Original_app/app3-dynamic/numpy/lib/user_array.py=container=__setattr__=251')
        if attr == 'array':
            object.__setattr__(self, attr, value)
            return
        try:
            self.array.__setattr__(attr, value)
        except AttributeError:
            object.__setattr__(self, attr, value)
    
    def __getattr__(self, attr):
        print('/home/jiangt/FaaSLight-Re/Original_app/app3-dynamic/numpy/lib/user_array.py=container=__getattr__=261')
        if attr == 'array':
            return object.__getattribute__(self, attr)
        return self.array.__getattribute__(attr)

if __name__ == '__main__':
    temp = reshape(arange(10000), (100, 100))
    ua = container(temp)
    print(dir(ua))
    print(shape(ua), ua.shape)
    ua_small = ua[:3, :5]
    print(ua_small)
    ua_small[(0, 0)] = 10
    print(ua_small[(0, 0)], ua[(0, 0)])
    print(sin(ua_small) / 3.0 * 6.0 + sqrt(ua_small**2))
    print(less(ua_small, 103), type(less(ua_small, 103)))
    print(type(ua_small * reshape(arange(15), shape(ua_small))))
    print(reshape(ua_small, (5, 3)))
    print(transpose(ua_small))

