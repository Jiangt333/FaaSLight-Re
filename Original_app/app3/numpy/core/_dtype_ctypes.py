"""
Conversion from ctypes to dtype.

In an ideal world, we could achieve this through the PEP3118 buffer protocol,
something like::

    def dtype_from_ctypes_type(t):
        # needed to ensure that the shape of `t` is within memoryview.format
        class DummyStruct(ctypes.Structure):
            _fields_ = [('a', t)]

        # empty to avoid memory allocation
        ctype_0 = (DummyStruct * 0)()
        mv = memoryview(ctype_0)

        # convert the struct, and slice back out the field
        return _dtype_from_pep3118(mv.format)['a']

Unfortunately, this fails because:

* ctypes cannot handle length-0 arrays with PEP3118 (bpo-32782)
* PEP3118 cannot represent unions, but both numpy and ctypes can
* ctypes cannot handle big-endian structs with PEP3118 (bpo-32780)
"""

import numpy as np

def _from_ctypes_array(t):
    return np.dtype((dtype_from_ctypes_type(t._type_), (t._length_, )))

def _from_ctypes_structure(t):
    import custom_funtemplate
    return custom_funtemplate.rewrite_template('numpy.core._dtype_ctypes._from_ctypes_structure', '_from_ctypes_structure(t)', {'dtype_from_ctypes_type': dtype_from_ctypes_type, 'np': np, 't': t}, 1)

def _from_ctypes_scalar(t):
    """
    Return the dtype type with endianness included if it's the case
    """
    import custom_funtemplate
    return custom_funtemplate.rewrite_template('numpy.core._dtype_ctypes._from_ctypes_scalar', '_from_ctypes_scalar(t)', {'np': np, 't': t}, 1)

def _from_ctypes_union(t):
    import custom_funtemplate
    return custom_funtemplate.rewrite_template('numpy.core._dtype_ctypes._from_ctypes_union', '_from_ctypes_union(t)', {'dtype_from_ctypes_type': dtype_from_ctypes_type, 'np': np, 't': t}, 1)

def dtype_from_ctypes_type(t):
    """
    Construct a dtype object from a ctypes type
    """
    import custom_funtemplate
    return custom_funtemplate.rewrite_template('numpy.core._dtype_ctypes.dtype_from_ctypes_type', 'dtype_from_ctypes_type(t)', {'_from_ctypes_array': _from_ctypes_array, '_from_ctypes_structure': _from_ctypes_structure, '_from_ctypes_union': _from_ctypes_union, '_from_ctypes_scalar': _from_ctypes_scalar, 't': t}, 1)

