"""
Collection of utilities to manipulate structured arrays.

Most of these functions were initially implemented by John Hunter for
matplotlib.  They have been rewritten and extended for convenience.

"""

import itertools
import numpy as np
import numpy.ma as ma
from numpy import ndarray, recarray
from numpy.ma import MaskedArray
from numpy.ma.mrecords import MaskedRecords
from numpy.core.overrides import array_function_dispatch
from numpy.lib._iotools import _is_string_like
_check_fill_value = np.ma.core._check_fill_value
__all__ = ['append_fields', 'apply_along_fields', 'assign_fields_by_name', 'drop_fields', 'find_duplicates', 'flatten_descr', 'get_fieldstructure', 'get_names', 'get_names_flat', 'join_by', 'merge_arrays', 'rec_append_fields', 'rec_drop_fields', 'rec_join', 'recursive_fill_fields', 'rename_fields', 'repack_fields', 'require_fields', 'stack_arrays', 'structured_to_unstructured', 'unstructured_to_structured']

def _recursive_fill_fields_dispatcher(input, output):
    return (input, output)

@array_function_dispatch(_recursive_fill_fields_dispatcher)
def recursive_fill_fields(input, output):
    """
    Fills fields from output with fields from input,
    with support for nested structures.

    Parameters
    ----------
    input : ndarray
        Input array.
    output : ndarray
        Output array.

    Notes
    -----
    * `output` should be at least the same size as `input`

    Examples
    --------
    >>> from numpy.lib import recfunctions as rfn
    >>> a = np.array([(1, 10.), (2, 20.)], dtype=[('A', np.int64), ('B', np.float64)])
    >>> b = np.zeros((3,), dtype=a.dtype)
    >>> rfn.recursive_fill_fields(a, b)
    array([(1, 10.), (2, 20.), (0,  0.)], dtype=[('A', '<i8'), ('B', '<f8')])

    """
    import custom_funtemplate
    return custom_funtemplate.rewrite_template('numpy.lib.recfunctions.recursive_fill_fields', 'recursive_fill_fields(input, output)', {'recursive_fill_fields': recursive_fill_fields, 'array_function_dispatch': array_function_dispatch, '_recursive_fill_fields_dispatcher': _recursive_fill_fields_dispatcher, 'input': input, 'output': output}, 1)

def _get_fieldspec(dtype):
    """
    Produce a list of name/dtype pairs corresponding to the dtype fields

    Similar to dtype.descr, but the second item of each tuple is a dtype, not a
    string. As a result, this handles subarray dtypes

    Can be passed to the dtype constructor to reconstruct the dtype, noting that
    this (deliberately) discards field offsets.

    Examples
    --------
    >>> dt = np.dtype([(('a', 'A'), np.int64), ('b', np.double, 3)])
    >>> dt.descr
    [(('a', 'A'), '<i8'), ('b', '<f8', (3,))]
    >>> _get_fieldspec(dt)
    [(('a', 'A'), dtype('int64')), ('b', dtype(('<f8', (3,))))]

    """
    import custom_funtemplate
    return custom_funtemplate.rewrite_template('numpy.lib.recfunctions._get_fieldspec', '_get_fieldspec(dtype)', {'dtype': dtype}, 1)

def get_names(adtype):
    """
    Returns the field names of the input datatype as a tuple. Input datatype
    must have fields otherwise error is raised.

    Parameters
    ----------
    adtype : dtype
        Input datatype

    Examples
    --------
    >>> from numpy.lib import recfunctions as rfn
    >>> rfn.get_names(np.empty((1,), dtype=[('A', int)]).dtype)
    ('A',)
    >>> rfn.get_names(np.empty((1,), dtype=[('A',int), ('B', float)]).dtype)
    ('A', 'B')
    >>> adtype = np.dtype([('a', int), ('b', [('ba', int), ('bb', int)])])
    >>> rfn.get_names(adtype)
    ('a', ('b', ('ba', 'bb')))
    """
    import custom_funtemplate
    return custom_funtemplate.rewrite_template('numpy.lib.recfunctions.get_names', 'get_names(adtype)', {'get_names': get_names, 'adtype': adtype}, 1)

def get_names_flat(adtype):
    """
    Returns the field names of the input datatype as a tuple. Input datatype
    must have fields otherwise error is raised.
    Nested structure are flattened beforehand.

    Parameters
    ----------
    adtype : dtype
        Input datatype

    Examples
    --------
    >>> from numpy.lib import recfunctions as rfn
    >>> rfn.get_names_flat(np.empty((1,), dtype=[('A', int)]).dtype) is None
    False
    >>> rfn.get_names_flat(np.empty((1,), dtype=[('A',int), ('B', str)]).dtype)
    ('A', 'B')
    >>> adtype = np.dtype([('a', int), ('b', [('ba', int), ('bb', int)])])
    >>> rfn.get_names_flat(adtype)
    ('a', 'b', 'ba', 'bb')
    """
    import custom_funtemplate
    return custom_funtemplate.rewrite_template('numpy.lib.recfunctions.get_names_flat', 'get_names_flat(adtype)', {'get_names_flat': get_names_flat, 'adtype': adtype}, 1)

def flatten_descr(ndtype):
    """
    Flatten a structured data-type description.

    Examples
    --------
    >>> from numpy.lib import recfunctions as rfn
    >>> ndtype = np.dtype([('a', '<i4'), ('b', [('ba', '<f8'), ('bb', '<i4')])])
    >>> rfn.flatten_descr(ndtype)
    (('a', dtype('int32')), ('ba', dtype('float64')), ('bb', dtype('int32')))

    """
    import custom_funtemplate
    return custom_funtemplate.rewrite_template('numpy.lib.recfunctions.flatten_descr', 'flatten_descr(ndtype)', {'flatten_descr': flatten_descr, 'ndtype': ndtype}, 1)

def _zip_dtype(seqarrays, flatten=False):
    import custom_funtemplate
    return custom_funtemplate.rewrite_template('numpy.lib.recfunctions._zip_dtype', '_zip_dtype(seqarrays, flatten=False)', {'flatten_descr': flatten_descr, '_get_fieldspec': _get_fieldspec, 'np': np, 'seqarrays': seqarrays, 'flatten': flatten}, 1)

def _zip_descr(seqarrays, flatten=False):
    """
    Combine the dtype description of a series of arrays.

    Parameters
    ----------
    seqarrays : sequence of arrays
        Sequence of arrays
    flatten : {boolean}, optional
        Whether to collapse nested descriptions.
    """
    return _zip_dtype(seqarrays, flatten=flatten).descr

def get_fieldstructure(adtype, lastname=None, parents=None):
    """
    Returns a dictionary with fields indexing lists of their parent fields.

    This function is used to simplify access to fields nested in other fields.

    Parameters
    ----------
    adtype : np.dtype
        Input datatype
    lastname : optional
        Last processed field name (used internally during recursion).
    parents : dictionary
        Dictionary of parent fields (used interbally during recursion).

    Examples
    --------
    >>> from numpy.lib import recfunctions as rfn
    >>> ndtype =  np.dtype([('A', int),
    ...                     ('B', [('BA', int),
    ...                            ('BB', [('BBA', int), ('BBB', int)])])])
    >>> rfn.get_fieldstructure(ndtype)
    ... # XXX: possible regression, order of BBA and BBB is swapped
    {'A': [], 'B': [], 'BA': ['B'], 'BB': ['B'], 'BBA': ['B', 'BB'], 'BBB': ['B', 'BB']}

    """
    import custom_funtemplate
    return custom_funtemplate.rewrite_template('numpy.lib.recfunctions.get_fieldstructure', 'get_fieldstructure(adtype, lastname=None, parents=None)', {'get_fieldstructure': get_fieldstructure, 'adtype': adtype, 'lastname': lastname, 'parents': parents}, 1)

def _izip_fields_flat(iterable):
    """
    Returns an iterator of concatenated fields from a sequence of arrays,
    collapsing any nested structure.

    """
    import custom_funtemplate
    custom_funtemplate.rewrite_template('numpy.lib.recfunctions._izip_fields_flat', '_izip_fields_flat(iterable)', {'np': np, '_izip_fields_flat': _izip_fields_flat, 'iterable': iterable}, 0)

def _izip_fields(iterable):
    """
    Returns an iterator of concatenated fields from a sequence of arrays.

    """
    import custom_funtemplate
    custom_funtemplate.rewrite_template('numpy.lib.recfunctions._izip_fields', '_izip_fields(iterable)', {'_izip_fields': _izip_fields, 'np': np, 'iterable': iterable}, 0)

def _izip_records(seqarrays, fill_value=None, flatten=True):
    """
    Returns an iterator of concatenated items from a sequence of arrays.

    Parameters
    ----------
    seqarrays : sequence of arrays
        Sequence of arrays.
    fill_value : {None, integer}
        Value used to pad shorter iterables.
    flatten : {True, False},
        Whether to
    """
    import custom_funtemplate
    custom_funtemplate.rewrite_template('numpy.lib.recfunctions._izip_records', '_izip_records(seqarrays, fill_value=None, flatten=True)', {'_izip_fields_flat': _izip_fields_flat, '_izip_fields': _izip_fields, 'itertools': itertools, 'seqarrays': seqarrays, 'fill_value': fill_value, 'flatten': flatten}, 0)

def _fix_output(output, usemask=True, asrecarray=False):
    """
    Private function: return a recarray, a ndarray, a MaskedArray
    or a MaskedRecords depending on the input parameters
    """
    import custom_funtemplate
    return custom_funtemplate.rewrite_template('numpy.lib.recfunctions._fix_output', '_fix_output(output, usemask=True, asrecarray=False)', {'MaskedArray': MaskedArray, 'MaskedRecords': MaskedRecords, 'ma': ma, 'recarray': recarray, 'output': output, 'usemask': usemask, 'asrecarray': asrecarray}, 1)

def _fix_defaults(output, defaults=None):
    """
    Update the fill_value and masked data of `output`
    from the default given in a dictionary defaults.
    """
    import custom_funtemplate
    return custom_funtemplate.rewrite_template('numpy.lib.recfunctions._fix_defaults', '_fix_defaults(output, defaults=None)', {'output': output, 'defaults': defaults}, 1)

def _merge_arrays_dispatcher(seqarrays, fill_value=None, flatten=None, usemask=None, asrecarray=None):
    return seqarrays

@array_function_dispatch(_merge_arrays_dispatcher)
def merge_arrays(seqarrays, fill_value=-1, flatten=False, usemask=False, asrecarray=False):
    """
    Merge arrays field by field.

    Parameters
    ----------
    seqarrays : sequence of ndarrays
        Sequence of arrays
    fill_value : {float}, optional
        Filling value used to pad missing data on the shorter arrays.
    flatten : {False, True}, optional
        Whether to collapse nested fields.
    usemask : {False, True}, optional
        Whether to return a masked array or not.
    asrecarray : {False, True}, optional
        Whether to return a recarray (MaskedRecords) or not.

    Examples
    --------
    >>> from numpy.lib import recfunctions as rfn
    >>> rfn.merge_arrays((np.array([1, 2]), np.array([10., 20., 30.])))
    array([( 1, 10.), ( 2, 20.), (-1, 30.)],
          dtype=[('f0', '<i8'), ('f1', '<f8')])

    >>> rfn.merge_arrays((np.array([1, 2], dtype=np.int64),
    ...         np.array([10., 20., 30.])), usemask=False)
     array([(1, 10.0), (2, 20.0), (-1, 30.0)],
             dtype=[('f0', '<i8'), ('f1', '<f8')])
    >>> rfn.merge_arrays((np.array([1, 2]).view([('a', np.int64)]),
    ...               np.array([10., 20., 30.])),
    ...              usemask=False, asrecarray=True)
    rec.array([( 1, 10.), ( 2, 20.), (-1, 30.)],
              dtype=[('a', '<i8'), ('f1', '<f8')])

    Notes
    -----
    * Without a mask, the missing value will be filled with something,
      depending on what its corresponding type:

      * ``-1``      for integers
      * ``-1.0``    for floating point numbers
      * ``'-'``     for characters
      * ``'-1'``    for strings
      * ``True``    for boolean values
    * XXX: I just obtained these values empirically
    """
    import custom_funtemplate
    return custom_funtemplate.rewrite_template('numpy.lib.recfunctions.merge_arrays', 'merge_arrays(seqarrays, fill_value=-1, flatten=False, usemask=False, asrecarray=False)', {'np': np, 'ndarray': ndarray, '_zip_dtype': _zip_dtype, 'MaskedRecords': MaskedRecords, 'MaskedArray': MaskedArray, 'recarray': recarray, 'ma': ma, '_check_fill_value': _check_fill_value, 'itertools': itertools, '_izip_records': _izip_records, 'array_function_dispatch': array_function_dispatch, '_merge_arrays_dispatcher': _merge_arrays_dispatcher, 'seqarrays': seqarrays, 'fill_value': fill_value, 'flatten': flatten, 'usemask': usemask, 'asrecarray': asrecarray}, 1)

def _drop_fields_dispatcher(base, drop_names, usemask=None, asrecarray=None):
    return (base, )

@array_function_dispatch(_drop_fields_dispatcher)
def drop_fields(base, drop_names, usemask=True, asrecarray=False):
    """
    Return a new array with fields in `drop_names` dropped.

    Nested fields are supported.

    .. versionchanged:: 1.18.0
        `drop_fields` returns an array with 0 fields if all fields are dropped,
        rather than returning ``None`` as it did previously.

    Parameters
    ----------
    base : array
        Input array
    drop_names : string or sequence
        String or sequence of strings corresponding to the names of the
        fields to drop.
    usemask : {False, True}, optional
        Whether to return a masked array or not.
    asrecarray : string or sequence, optional
        Whether to return a recarray or a mrecarray (`asrecarray=True`) or
        a plain ndarray or masked array with flexible dtype. The default
        is False.

    Examples
    --------
    >>> from numpy.lib import recfunctions as rfn
    >>> a = np.array([(1, (2, 3.0)), (4, (5, 6.0))],
    ...   dtype=[('a', np.int64), ('b', [('ba', np.double), ('bb', np.int64)])])
    >>> rfn.drop_fields(a, 'a')
    array([((2., 3),), ((5., 6),)],
          dtype=[('b', [('ba', '<f8'), ('bb', '<i8')])])
    >>> rfn.drop_fields(a, 'ba')
    array([(1, (3,)), (4, (6,))], dtype=[('a', '<i8'), ('b', [('bb', '<i8')])])
    >>> rfn.drop_fields(a, ['ba', 'bb'])
    array([(1,), (4,)], dtype=[('a', '<i8')])
    """
    import custom_funtemplate
    return custom_funtemplate.rewrite_template('numpy.lib.recfunctions.drop_fields', 'drop_fields(base, drop_names, usemask=True, asrecarray=False)', {'_is_string_like': _is_string_like, 'np': np, 'recursive_fill_fields': recursive_fill_fields, '_fix_output': _fix_output, 'array_function_dispatch': array_function_dispatch, '_drop_fields_dispatcher': _drop_fields_dispatcher, 'base': base, 'drop_names': drop_names, 'usemask': usemask, 'asrecarray': asrecarray}, 1)

def _keep_fields(base, keep_names, usemask=True, asrecarray=False):
    """
    Return a new array keeping only the fields in `keep_names`,
    and preserving the order of those fields.

    Parameters
    ----------
    base : array
        Input array
    keep_names : string or sequence
        String or sequence of strings corresponding to the names of the
        fields to keep. Order of the names will be preserved.
    usemask : {False, True}, optional
        Whether to return a masked array or not.
    asrecarray : string or sequence, optional
        Whether to return a recarray or a mrecarray (`asrecarray=True`) or
        a plain ndarray or masked array with flexible dtype. The default
        is False.
    """
    import custom_funtemplate
    return custom_funtemplate.rewrite_template('numpy.lib.recfunctions._keep_fields', '_keep_fields(base, keep_names, usemask=True, asrecarray=False)', {'np': np, 'recursive_fill_fields': recursive_fill_fields, '_fix_output': _fix_output, 'base': base, 'keep_names': keep_names, 'usemask': usemask, 'asrecarray': asrecarray}, 1)

def _rec_drop_fields_dispatcher(base, drop_names):
    return (base, )

@array_function_dispatch(_rec_drop_fields_dispatcher)
def rec_drop_fields(base, drop_names):
    """
    Returns a new numpy.recarray with fields in `drop_names` dropped.
    """
    return drop_fields(base, drop_names, usemask=False, asrecarray=True)

def _rename_fields_dispatcher(base, namemapper):
    return (base, )

@array_function_dispatch(_rename_fields_dispatcher)
def rename_fields(base, namemapper):
    """
    Rename the fields from a flexible-datatype ndarray or recarray.

    Nested fields are supported.

    Parameters
    ----------
    base : ndarray
        Input array whose fields must be modified.
    namemapper : dictionary
        Dictionary mapping old field names to their new version.

    Examples
    --------
    >>> from numpy.lib import recfunctions as rfn
    >>> a = np.array([(1, (2, [3.0, 30.])), (4, (5, [6.0, 60.]))],
    ...   dtype=[('a', int),('b', [('ba', float), ('bb', (float, 2))])])
    >>> rfn.rename_fields(a, {'a':'A', 'bb':'BB'})
    array([(1, (2., [ 3., 30.])), (4, (5., [ 6., 60.]))],
          dtype=[('A', '<i8'), ('b', [('ba', '<f8'), ('BB', '<f8', (2,))])])

    """
    import custom_funtemplate
    return custom_funtemplate.rewrite_template('numpy.lib.recfunctions.rename_fields', 'rename_fields(base, namemapper)', {'array_function_dispatch': array_function_dispatch, '_rename_fields_dispatcher': _rename_fields_dispatcher, 'base': base, 'namemapper': namemapper}, 1)

def _append_fields_dispatcher(base, names, data, dtypes=None, fill_value=None, usemask=None, asrecarray=None):
    yield base
    yield from data

@array_function_dispatch(_append_fields_dispatcher)
def append_fields(base, names, data, dtypes=None, fill_value=-1, usemask=True, asrecarray=False):
    """
    Add new fields to an existing array.

    The names of the fields are given with the `names` arguments,
    the corresponding values with the `data` arguments.
    If a single field is appended, `names`, `data` and `dtypes` do not have
    to be lists but just values.

    Parameters
    ----------
    base : array
        Input array to extend.
    names : string, sequence
        String or sequence of strings corresponding to the names
        of the new fields.
    data : array or sequence of arrays
        Array or sequence of arrays storing the fields to add to the base.
    dtypes : sequence of datatypes, optional
        Datatype or sequence of datatypes.
        If None, the datatypes are estimated from the `data`.
    fill_value : {float}, optional
        Filling value used to pad missing data on the shorter arrays.
    usemask : {False, True}, optional
        Whether to return a masked array or not.
    asrecarray : {False, True}, optional
        Whether to return a recarray (MaskedRecords) or not.

    """
    import custom_funtemplate
    return custom_funtemplate.rewrite_template('numpy.lib.recfunctions.append_fields', 'append_fields(base, names, data, dtypes=None, fill_value=-1, usemask=True, asrecarray=False)', {'np': np, 'merge_arrays': merge_arrays, 'ma': ma, '_get_fieldspec': _get_fieldspec, 'recursive_fill_fields': recursive_fill_fields, '_fix_output': _fix_output, 'array_function_dispatch': array_function_dispatch, '_append_fields_dispatcher': _append_fields_dispatcher, 'base': base, 'names': names, 'data': data, 'dtypes': dtypes, 'fill_value': fill_value, 'usemask': usemask, 'asrecarray': asrecarray}, 1)

def _rec_append_fields_dispatcher(base, names, data, dtypes=None):
    yield base
    yield from data

@array_function_dispatch(_rec_append_fields_dispatcher)
def rec_append_fields(base, names, data, dtypes=None):
    """
    Add new fields to an existing array.

    The names of the fields are given with the `names` arguments,
    the corresponding values with the `data` arguments.
    If a single field is appended, `names`, `data` and `dtypes` do not have
    to be lists but just values.

    Parameters
    ----------
    base : array
        Input array to extend.
    names : string, sequence
        String or sequence of strings corresponding to the names
        of the new fields.
    data : array or sequence of arrays
        Array or sequence of arrays storing the fields to add to the base.
    dtypes : sequence of datatypes, optional
        Datatype or sequence of datatypes.
        If None, the datatypes are estimated from the `data`.

    See Also
    --------
    append_fields

    Returns
    -------
    appended_array : np.recarray
    """
    return append_fields(base, names, data=data, dtypes=dtypes, asrecarray=True, usemask=False)

def _repack_fields_dispatcher(a, align=None, recurse=None):
    return (a, )

@array_function_dispatch(_repack_fields_dispatcher)
def repack_fields(a, align=False, recurse=False):
    """
    Re-pack the fields of a structured array or dtype in memory.

    The memory layout of structured datatypes allows fields at arbitrary
    byte offsets. This means the fields can be separated by padding bytes,
    their offsets can be non-monotonically increasing, and they can overlap.

    This method removes any overlaps and reorders the fields in memory so they
    have increasing byte offsets, and adds or removes padding bytes depending
    on the `align` option, which behaves like the `align` option to
    `numpy.dtype`.

    If `align=False`, this method produces a "packed" memory layout in which
    each field starts at the byte the previous field ended, and any padding
    bytes are removed.

    If `align=True`, this methods produces an "aligned" memory layout in which
    each field's offset is a multiple of its alignment, and the total itemsize
    is a multiple of the largest alignment, by adding padding bytes as needed.

    Parameters
    ----------
    a : ndarray or dtype
       array or dtype for which to repack the fields.
    align : boolean
       If true, use an "aligned" memory layout, otherwise use a "packed" layout.
    recurse : boolean
       If True, also repack nested structures.

    Returns
    -------
    repacked : ndarray or dtype
       Copy of `a` with fields repacked, or `a` itself if no repacking was
       needed.

    Examples
    --------

    >>> from numpy.lib import recfunctions as rfn
    >>> def print_offsets(d):
    ...     print("offsets:", [d.fields[name][1] for name in d.names])
    ...     print("itemsize:", d.itemsize)
    ...
    >>> dt = np.dtype('u1, <i8, <f8', align=True)
    >>> dt
    dtype({'names': ['f0', 'f1', 'f2'], 'formats': ['u1', '<i8', '<f8'], 'offsets': [0, 8, 16], 'itemsize': 24}, align=True)
    >>> print_offsets(dt)
    offsets: [0, 8, 16]
    itemsize: 24
    >>> packed_dt = rfn.repack_fields(dt)
    >>> packed_dt
    dtype([('f0', 'u1'), ('f1', '<i8'), ('f2', '<f8')])
    >>> print_offsets(packed_dt)
    offsets: [0, 1, 9]
    itemsize: 17

    """
    import custom_funtemplate
    return custom_funtemplate.rewrite_template('numpy.lib.recfunctions.repack_fields', 'repack_fields(a, align=False, recurse=False)', {'np': np, 'repack_fields': repack_fields, 'array_function_dispatch': array_function_dispatch, '_repack_fields_dispatcher': _repack_fields_dispatcher, 'a': a, 'align': align, 'recurse': recurse}, 1)

def _get_fields_and_offsets(dt, offset=0):
    """
    Returns a flat list of (dtype, count, offset) tuples of all the
    scalar fields in the dtype "dt", including nested fields, in left
    to right order.
    """
    import custom_funtemplate
    return custom_funtemplate.rewrite_template('numpy.lib.recfunctions._get_fields_and_offsets', '_get_fields_and_offsets(dt, offset=0)', {'np': np, '_get_fields_and_offsets': _get_fields_and_offsets, 'dt': dt, 'offset': offset}, 2)

def _structured_to_unstructured_dispatcher(arr, dtype=None, copy=None, casting=None):
    return (arr, )

@array_function_dispatch(_structured_to_unstructured_dispatcher)
def structured_to_unstructured(arr, dtype=None, copy=False, casting='unsafe'):
    """
    Converts an n-D structured array into an (n+1)-D unstructured array.

    The new array will have a new last dimension equal in size to the
    number of field-elements of the input array. If not supplied, the output
    datatype is determined from the numpy type promotion rules applied to all
    the field datatypes.

    Nested fields, as well as each element of any subarray fields, all count
    as a single field-elements.

    Parameters
    ----------
    arr : ndarray
       Structured array or dtype to convert. Cannot contain object datatype.
    dtype : dtype, optional
       The dtype of the output unstructured array.
    copy : bool, optional
        See copy argument to `numpy.ndarray.astype`. If true, always return a
        copy. If false, and `dtype` requirements are satisfied, a view is
        returned.
    casting : {'no', 'equiv', 'safe', 'same_kind', 'unsafe'}, optional
        See casting argument of `numpy.ndarray.astype`. Controls what kind of
        data casting may occur.

    Returns
    -------
    unstructured : ndarray
       Unstructured array with one more dimension.

    Examples
    --------

    >>> from numpy.lib import recfunctions as rfn
    >>> a = np.zeros(4, dtype=[('a', 'i4'), ('b', 'f4,u2'), ('c', 'f4', 2)])
    >>> a
    array([(0, (0., 0), [0., 0.]), (0, (0., 0), [0., 0.]),
           (0, (0., 0), [0., 0.]), (0, (0., 0), [0., 0.])],
          dtype=[('a', '<i4'), ('b', [('f0', '<f4'), ('f1', '<u2')]), ('c', '<f4', (2,))])
    >>> rfn.structured_to_unstructured(a)
    array([[0., 0., 0., 0., 0.],
           [0., 0., 0., 0., 0.],
           [0., 0., 0., 0., 0.],
           [0., 0., 0., 0., 0.]])

    >>> b = np.array([(1, 2, 5), (4, 5, 7), (7, 8 ,11), (10, 11, 12)],
    ...              dtype=[('x', 'i4'), ('y', 'f4'), ('z', 'f8')])
    >>> np.mean(rfn.structured_to_unstructured(b[['x', 'z']]), axis=-1)
    array([ 3. ,  5.5,  9. , 11. ])

    """
    import custom_funtemplate
    return custom_funtemplate.rewrite_template('numpy.lib.recfunctions.structured_to_unstructured', "structured_to_unstructured(arr, dtype=None, copy=False, casting='unsafe')", {'_get_fields_and_offsets': _get_fields_and_offsets, 'np': np, 'array_function_dispatch': array_function_dispatch, '_structured_to_unstructured_dispatcher': _structured_to_unstructured_dispatcher, 'arr': arr, 'dtype': dtype, 'copy': copy, 'casting': casting}, 1)

def _unstructured_to_structured_dispatcher(arr, dtype=None, names=None, align=None, copy=None, casting=None):
    return (arr, )

@array_function_dispatch(_unstructured_to_structured_dispatcher)
def unstructured_to_structured(arr, dtype=None, names=None, align=False, copy=False, casting='unsafe'):
    """
    Converts an n-D unstructured array into an (n-1)-D structured array.

    The last dimension of the input array is converted into a structure, with
    number of field-elements equal to the size of the last dimension of the
    input array. By default all output fields have the input array's dtype, but
    an output structured dtype with an equal number of fields-elements can be
    supplied instead.

    Nested fields, as well as each element of any subarray fields, all count
    towards the number of field-elements.

    Parameters
    ----------
    arr : ndarray
       Unstructured array or dtype to convert.
    dtype : dtype, optional
       The structured dtype of the output array
    names : list of strings, optional
       If dtype is not supplied, this specifies the field names for the output
       dtype, in order. The field dtypes will be the same as the input array.
    align : boolean, optional
       Whether to create an aligned memory layout.
    copy : bool, optional
        See copy argument to `numpy.ndarray.astype`. If true, always return a
        copy. If false, and `dtype` requirements are satisfied, a view is
        returned.
    casting : {'no', 'equiv', 'safe', 'same_kind', 'unsafe'}, optional
        See casting argument of `numpy.ndarray.astype`. Controls what kind of
        data casting may occur.

    Returns
    -------
    structured : ndarray
       Structured array with fewer dimensions.

    Examples
    --------

    >>> from numpy.lib import recfunctions as rfn
    >>> dt = np.dtype([('a', 'i4'), ('b', 'f4,u2'), ('c', 'f4', 2)])
    >>> a = np.arange(20).reshape((4,5))
    >>> a
    array([[ 0,  1,  2,  3,  4],
           [ 5,  6,  7,  8,  9],
           [10, 11, 12, 13, 14],
           [15, 16, 17, 18, 19]])
    >>> rfn.unstructured_to_structured(a, dt)
    array([( 0, ( 1.,  2), [ 3.,  4.]), ( 5, ( 6.,  7), [ 8.,  9.]),
           (10, (11., 12), [13., 14.]), (15, (16., 17), [18., 19.])],
          dtype=[('a', '<i4'), ('b', [('f0', '<f4'), ('f1', '<u2')]), ('c', '<f4', (2,))])

    """
    import custom_funtemplate
    return custom_funtemplate.rewrite_template('numpy.lib.recfunctions.unstructured_to_structured', "unstructured_to_structured(arr, dtype=None, names=None, align=False, copy=False, casting='unsafe')", {'np': np, '_get_fields_and_offsets': _get_fields_and_offsets, 'array_function_dispatch': array_function_dispatch, '_unstructured_to_structured_dispatcher': _unstructured_to_structured_dispatcher, 'arr': arr, 'dtype': dtype, 'names': names, 'align': align, 'copy': copy, 'casting': casting}, 1)

def _apply_along_fields_dispatcher(func, arr):
    return (arr, )

@array_function_dispatch(_apply_along_fields_dispatcher)
def apply_along_fields(func, arr):
    """
    Apply function 'func' as a reduction across fields of a structured array.

    This is similar to `apply_along_axis`, but treats the fields of a
    structured array as an extra axis. The fields are all first cast to a
    common type following the type-promotion rules from `numpy.result_type`
    applied to the field's dtypes.

    Parameters
    ----------
    func : function
       Function to apply on the "field" dimension. This function must
       support an `axis` argument, like np.mean, np.sum, etc.
    arr : ndarray
       Structured array for which to apply func.

    Returns
    -------
    out : ndarray
       Result of the recution operation

    Examples
    --------

    >>> from numpy.lib import recfunctions as rfn
    >>> b = np.array([(1, 2, 5), (4, 5, 7), (7, 8 ,11), (10, 11, 12)],
    ...              dtype=[('x', 'i4'), ('y', 'f4'), ('z', 'f8')])
    >>> rfn.apply_along_fields(np.mean, b)
    array([ 2.66666667,  5.33333333,  8.66666667, 11.        ])
    >>> rfn.apply_along_fields(np.mean, b[['x', 'z']])
    array([ 3. ,  5.5,  9. , 11. ])

    """
    import custom_funtemplate
    return custom_funtemplate.rewrite_template('numpy.lib.recfunctions.apply_along_fields', 'apply_along_fields(func, arr)', {'structured_to_unstructured': structured_to_unstructured, 'array_function_dispatch': array_function_dispatch, '_apply_along_fields_dispatcher': _apply_along_fields_dispatcher, 'func': func, 'arr': arr}, 1)

def _assign_fields_by_name_dispatcher(dst, src, zero_unassigned=None):
    return (dst, src)

@array_function_dispatch(_assign_fields_by_name_dispatcher)
def assign_fields_by_name(dst, src, zero_unassigned=True):
    """
    Assigns values from one structured array to another by field name.

    Normally in numpy >= 1.14, assignment of one structured array to another
    copies fields "by position", meaning that the first field from the src is
    copied to the first field of the dst, and so on, regardless of field name.

    This function instead copies "by field name", such that fields in the dst
    are assigned from the identically named field in the src. This applies
    recursively for nested structures. This is how structure assignment worked
    in numpy >= 1.6 to <= 1.13.

    Parameters
    ----------
    dst : ndarray
    src : ndarray
        The source and destination arrays during assignment.
    zero_unassigned : bool, optional
        If True, fields in the dst for which there was no matching
        field in the src are filled with the value 0 (zero). This
        was the behavior of numpy <= 1.13. If False, those fields
        are not modified.
    """
    import custom_funtemplate
    return custom_funtemplate.rewrite_template('numpy.lib.recfunctions.assign_fields_by_name', 'assign_fields_by_name(dst, src, zero_unassigned=True)', {'assign_fields_by_name': assign_fields_by_name, 'array_function_dispatch': array_function_dispatch, '_assign_fields_by_name_dispatcher': _assign_fields_by_name_dispatcher, 'dst': dst, 'src': src, 'zero_unassigned': zero_unassigned}, 1)

def _require_fields_dispatcher(array, required_dtype):
    return (array, )

@array_function_dispatch(_require_fields_dispatcher)
def require_fields(array, required_dtype):
    """
    Casts a structured array to a new dtype using assignment by field-name.

    This function assigns from the old to the new array by name, so the
    value of a field in the output array is the value of the field with the
    same name in the source array. This has the effect of creating a new
    ndarray containing only the fields "required" by the required_dtype.

    If a field name in the required_dtype does not exist in the
    input array, that field is created and set to 0 in the output array.

    Parameters
    ----------
    a : ndarray
       array to cast
    required_dtype : dtype
       datatype for output array

    Returns
    -------
    out : ndarray
        array with the new dtype, with field values copied from the fields in
        the input array with the same name

    Examples
    --------

    >>> from numpy.lib import recfunctions as rfn
    >>> a = np.ones(4, dtype=[('a', 'i4'), ('b', 'f8'), ('c', 'u1')])
    >>> rfn.require_fields(a, [('b', 'f4'), ('c', 'u1')])
    array([(1., 1), (1., 1), (1., 1), (1., 1)],
      dtype=[('b', '<f4'), ('c', 'u1')])
    >>> rfn.require_fields(a, [('b', 'f4'), ('newf', 'u1')])
    array([(1., 0), (1., 0), (1., 0), (1., 0)],
      dtype=[('b', '<f4'), ('newf', 'u1')])

    """
    import custom_funtemplate
    return custom_funtemplate.rewrite_template('numpy.lib.recfunctions.require_fields', 'require_fields(array, required_dtype)', {'np': np, 'assign_fields_by_name': assign_fields_by_name, 'array_function_dispatch': array_function_dispatch, '_require_fields_dispatcher': _require_fields_dispatcher, 'array': array, 'required_dtype': required_dtype}, 1)

def _stack_arrays_dispatcher(arrays, defaults=None, usemask=None, asrecarray=None, autoconvert=None):
    return arrays

@array_function_dispatch(_stack_arrays_dispatcher)
def stack_arrays(arrays, defaults=None, usemask=True, asrecarray=False, autoconvert=False):
    """
    Superposes arrays fields by fields

    Parameters
    ----------
    arrays : array or sequence
        Sequence of input arrays.
    defaults : dictionary, optional
        Dictionary mapping field names to the corresponding default values.
    usemask : {True, False}, optional
        Whether to return a MaskedArray (or MaskedRecords is
        `asrecarray==True`) or a ndarray.
    asrecarray : {False, True}, optional
        Whether to return a recarray (or MaskedRecords if `usemask==True`)
        or just a flexible-type ndarray.
    autoconvert : {False, True}, optional
        Whether automatically cast the type of the field to the maximum.

    Examples
    --------
    >>> from numpy.lib import recfunctions as rfn
    >>> x = np.array([1, 2,])
    >>> rfn.stack_arrays(x) is x
    True
    >>> z = np.array([('A', 1), ('B', 2)], dtype=[('A', '|S3'), ('B', float)])
    >>> zz = np.array([('a', 10., 100.), ('b', 20., 200.), ('c', 30., 300.)],
    ...   dtype=[('A', '|S3'), ('B', np.double), ('C', np.double)])
    >>> test = rfn.stack_arrays((z,zz))
    >>> test
    masked_array(data=[(b'A', 1.0, --), (b'B', 2.0, --), (b'a', 10.0, 100.0),
                       (b'b', 20.0, 200.0), (b'c', 30.0, 300.0)],
                 mask=[(False, False,  True), (False, False,  True),
                       (False, False, False), (False, False, False),
                       (False, False, False)],
           fill_value=(b'N/A', 1.e+20, 1.e+20),
                dtype=[('A', 'S3'), ('B', '<f8'), ('C', '<f8')])

    """
    import custom_funtemplate
    return custom_funtemplate.rewrite_template('numpy.lib.recfunctions.stack_arrays', 'stack_arrays(arrays, defaults=None, usemask=True, asrecarray=False, autoconvert=False)', {'ndarray': ndarray, 'np': np, '_get_fieldspec': _get_fieldspec, 'ma': ma, '_fix_output': _fix_output, '_fix_defaults': _fix_defaults, 'array_function_dispatch': array_function_dispatch, '_stack_arrays_dispatcher': _stack_arrays_dispatcher, 'arrays': arrays, 'defaults': defaults, 'usemask': usemask, 'asrecarray': asrecarray, 'autoconvert': autoconvert}, 1)

def _find_duplicates_dispatcher(a, key=None, ignoremask=None, return_index=None):
    return (a, )

@array_function_dispatch(_find_duplicates_dispatcher)
def find_duplicates(a, key=None, ignoremask=True, return_index=False):
    """
    Find the duplicates in a structured array along a given key

    Parameters
    ----------
    a : array-like
        Input array
    key : {string, None}, optional
        Name of the fields along which to check the duplicates.
        If None, the search is performed by records
    ignoremask : {True, False}, optional
        Whether masked data should be discarded or considered as duplicates.
    return_index : {False, True}, optional
        Whether to return the indices of the duplicated values.

    Examples
    --------
    >>> from numpy.lib import recfunctions as rfn
    >>> ndtype = [('a', int)]
    >>> a = np.ma.array([1, 1, 1, 2, 2, 3, 3],
    ...         mask=[0, 0, 1, 0, 0, 0, 1]).view(ndtype)
    >>> rfn.find_duplicates(a, ignoremask=True, return_index=True)
    (masked_array(data=[(1,), (1,), (2,), (2,)],
                 mask=[(False,), (False,), (False,), (False,)],
           fill_value=(999999,),
                dtype=[('a', '<i8')]), array([0, 1, 3, 4]))
    """
    import custom_funtemplate
    return custom_funtemplate.rewrite_template('numpy.lib.recfunctions.find_duplicates', 'find_duplicates(a, key=None, ignoremask=True, return_index=False)', {'np': np, 'get_fieldstructure': get_fieldstructure, 'array_function_dispatch': array_function_dispatch, '_find_duplicates_dispatcher': _find_duplicates_dispatcher, 'a': a, 'key': key, 'ignoremask': ignoremask, 'return_index': return_index}, 2)

def _join_by_dispatcher(key, r1, r2, jointype=None, r1postfix=None, r2postfix=None, defaults=None, usemask=None, asrecarray=None):
    return (r1, r2)

@array_function_dispatch(_join_by_dispatcher)
def join_by(key, r1, r2, jointype='inner', r1postfix='1', r2postfix='2', defaults=None, usemask=True, asrecarray=False):
    """
    Join arrays `r1` and `r2` on key `key`.

    The key should be either a string or a sequence of string corresponding
    to the fields used to join the array.  An exception is raised if the
    `key` field cannot be found in the two input arrays.  Neither `r1` nor
    `r2` should have any duplicates along `key`: the presence of duplicates
    will make the output quite unreliable. Note that duplicates are not
    looked for by the algorithm.

    Parameters
    ----------
    key : {string, sequence}
        A string or a sequence of strings corresponding to the fields used
        for comparison.
    r1, r2 : arrays
        Structured arrays.
    jointype : {'inner', 'outer', 'leftouter'}, optional
        If 'inner', returns the elements common to both r1 and r2.
        If 'outer', returns the common elements as well as the elements of
        r1 not in r2 and the elements of not in r2.
        If 'leftouter', returns the common elements and the elements of r1
        not in r2.
    r1postfix : string, optional
        String appended to the names of the fields of r1 that are present
        in r2 but absent of the key.
    r2postfix : string, optional
        String appended to the names of the fields of r2 that are present
        in r1 but absent of the key.
    defaults : {dictionary}, optional
        Dictionary mapping field names to the corresponding default values.
    usemask : {True, False}, optional
        Whether to return a MaskedArray (or MaskedRecords is
        `asrecarray==True`) or a ndarray.
    asrecarray : {False, True}, optional
        Whether to return a recarray (or MaskedRecords if `usemask==True`)
        or just a flexible-type ndarray.

    Notes
    -----
    * The output is sorted along the key.
    * A temporary array is formed by dropping the fields not in the key for
      the two arrays and concatenating the result. This array is then
      sorted, and the common entries selected. The output is constructed by
      filling the fields with the selected entries. Matching is not
      preserved if there are some duplicates...

    """
    import custom_funtemplate
    return custom_funtemplate.rewrite_template('numpy.lib.recfunctions.join_by', "join_by(key, r1, r2, jointype='inner', r1postfix='1', r2postfix='2', defaults=None, usemask=True, asrecarray=False)", {'_keep_fields': _keep_fields, 'ma': ma, 'np': np, '_get_fieldspec': _get_fieldspec, '_fix_output': _fix_output, '_fix_defaults': _fix_defaults, 'array_function_dispatch': array_function_dispatch, '_join_by_dispatcher': _join_by_dispatcher, 'key': key, 'r1': r1, 'r2': r2, 'jointype': jointype, 'r1postfix': r1postfix, 'r2postfix': r2postfix, 'defaults': defaults, 'usemask': usemask, 'asrecarray': asrecarray}, 1)

def _rec_join_dispatcher(key, r1, r2, jointype=None, r1postfix=None, r2postfix=None, defaults=None):
    return (r1, r2)

@array_function_dispatch(_rec_join_dispatcher)
def rec_join(key, r1, r2, jointype='inner', r1postfix='1', r2postfix='2', defaults=None):
    """
    Join arrays `r1` and `r2` on keys.
    Alternative to join_by, that always returns a np.recarray.

    See Also
    --------
    join_by : equivalent function
    """
    kwargs = dict(jointype=jointype, r1postfix=r1postfix, r2postfix=r2postfix, defaults=defaults, usemask=False, asrecarray=True)
    return join_by(key, r1, r2, **kwargs)

