import os
import sys
import textwrap
import types
import re
import warnings
import functools
from numpy.core.numerictypes import issubclass_, issubsctype, issubdtype
from numpy.core.overrides import set_module
from numpy.core import ndarray, ufunc, asarray
import numpy as np
__all__ = ['issubclass_', 'issubsctype', 'issubdtype', 'deprecate', 'deprecate_with_doc', 'get_include', 'info', 'source', 'who', 'lookfor', 'byte_bounds', 'safe_eval', 'show_runtime']

def show_runtime():
    """
    Print information about various resources in the system
    including available intrinsic support and BLAS/LAPACK library
    in use

    See Also
    --------
    show_config : Show libraries in the system on which NumPy was built.

    Notes
    -----
    1. Information is derived with the help of `threadpoolctl <https://pypi.org/project/threadpoolctl/>`_
       library.
    2. SIMD related information is derived from ``__cpu_features__``,
       ``__cpu_baseline__`` and ``__cpu_dispatch__``

    Examples
    --------
    >>> import numpy as np
    >>> np.show_runtime()
    [{'simd_extensions': {'baseline': ['SSE', 'SSE2', 'SSE3'],
                          'found': ['SSSE3',
                                    'SSE41',
                                    'POPCNT',
                                    'SSE42',
                                    'AVX',
                                    'F16C',
                                    'FMA3',
                                    'AVX2'],
                          'not_found': ['AVX512F',
                                        'AVX512CD',
                                        'AVX512_KNL',
                                        'AVX512_KNM',
                                        'AVX512_SKX',
                                        'AVX512_CLX',
                                        'AVX512_CNL',
                                        'AVX512_ICL']}},
     {'architecture': 'Zen',
      'filepath': '/usr/lib/x86_64-linux-gnu/openblas-pthread/libopenblasp-r0.3.20.so',
      'internal_api': 'openblas',
      'num_threads': 12,
      'prefix': 'libopenblas',
      'threading_layer': 'pthreads',
      'user_api': 'blas',
      'version': '0.3.20'}]
    """
    import custom_funtemplate
    custom_funtemplate.rewrite_template('numpy.lib.utils.show_runtime', 'show_runtime()', {}, 0)

def get_include():
    """
    Return the directory that contains the NumPy \*.h header files.

    Extension modules that need to compile against NumPy should use this
    function to locate the appropriate include directory.

    Notes
    -----
    When using ``distutils``, for example in ``setup.py``::

        import numpy as np
        ...
        Extension('extension_name', ...
                include_dirs=[np.get_include()])
        ...

    """
    import numpy
    if numpy.show_config is None:
        d = os.path.join(os.path.dirname(numpy.__file__), 'core', 'include')
    else:
        import numpy.core as core
        d = os.path.join(os.path.dirname(core.__file__), 'include')
    return d


class _Deprecate:
    """
    Decorator class to deprecate old functions.

    Refer to `deprecate` for details.

    See Also
    --------
    deprecate

    """
    
    def __init__(self, old_name=None, new_name=None, message=None):
        self.old_name = old_name
        self.new_name = new_name
        self.message = message
    
    def __call__(self, func, *args, **kwargs):
        """
        Decorator call.  Refer to ``decorate``.

        """
        old_name = self.old_name
        new_name = self.new_name
        message = self.message
        if old_name is None:
            old_name = func.__name__
        if new_name is None:
            depdoc = '`%s` is deprecated!' % old_name
        else:
            depdoc = '`%s` is deprecated, use `%s` instead!' % (old_name, new_name)
        if message is not None:
            depdoc += '\n' + message
        
        @functools.wraps(func)
        def newfunc(*args, **kwds):
            warnings.warn(depdoc, DeprecationWarning, stacklevel=2)
            return func(*args, **kwds)
        newfunc.__name__ = old_name
        doc = func.__doc__
        if doc is None:
            doc = depdoc
        else:
            lines = doc.expandtabs().split('\n')
            indent = _get_indent(lines[1:])
            if lines[0].lstrip():
                doc = indent * ' ' + doc
            else:
                skip = len(lines[0]) + 1
                for line in lines[1:]:
                    if len(line) > indent:
                        break
                    skip += len(line) + 1
                doc = doc[skip:]
            depdoc = textwrap.indent(depdoc, ' ' * indent)
            doc = '\n\n'.join([depdoc, doc])
        newfunc.__doc__ = doc
        return newfunc


def _get_indent(lines):
    """
    Determines the leading whitespace that could be removed from all the lines.
    """
    import custom_funtemplate
    return custom_funtemplate.rewrite_template('numpy.lib.utils._get_indent', '_get_indent(lines)', {'sys': sys, 'lines': lines}, 1)

def deprecate(*args, **kwargs):
    """
    Issues a DeprecationWarning, adds warning to `old_name`'s
    docstring, rebinds ``old_name.__name__`` and returns the new
    function object.

    This function may also be used as a decorator.

    Parameters
    ----------
    func : function
        The function to be deprecated.
    old_name : str, optional
        The name of the function to be deprecated. Default is None, in
        which case the name of `func` is used.
    new_name : str, optional
        The new name for the function. Default is None, in which case the
        deprecation message is that `old_name` is deprecated. If given, the
        deprecation message is that `old_name` is deprecated and `new_name`
        should be used instead.
    message : str, optional
        Additional explanation of the deprecation.  Displayed in the
        docstring after the warning.

    Returns
    -------
    old_func : function
        The deprecated function.

    Examples
    --------
    Note that ``olduint`` returns a value after printing Deprecation
    Warning:

    >>> olduint = np.deprecate(np.uint)
    DeprecationWarning: `uint64` is deprecated! # may vary
    >>> olduint(6)
    6

    """
    import custom_funtemplate
    return custom_funtemplate.rewrite_template('numpy.lib.utils.deprecate', 'deprecate(*args, **kwargs)', {'_Deprecate': _Deprecate, 'args': args, 'kwargs': kwargs}, 1)

def deprecate_with_doc(msg):
    """
    Deprecates a function and includes the deprecation in its docstring.

    This function is used as a decorator. It returns an object that can be
    used to issue a DeprecationWarning, by passing the to-be decorated
    function as argument, this adds warning to the to-be decorated function's
    docstring and returns the new function object.

    See Also
    --------
    deprecate : Decorate a function such that it issues a `DeprecationWarning`

    Parameters
    ----------
    msg : str
        Additional explanation of the deprecation. Displayed in the
        docstring after the warning.

    Returns
    -------
    obj : object

    """
    return _Deprecate(message=msg)

def byte_bounds(a):
    """
    Returns pointers to the end-points of an array.

    Parameters
    ----------
    a : ndarray
        Input array. It must conform to the Python-side of the array
        interface.

    Returns
    -------
    (low, high) : tuple of 2 integers
        The first integer is the first byte of the array, the second
        integer is just past the last byte of the array.  If `a` is not
        contiguous it will not use every byte between the (`low`, `high`)
        values.

    Examples
    --------
    >>> I = np.eye(2, dtype='f'); I.dtype
    dtype('float32')
    >>> low, high = np.byte_bounds(I)
    >>> high - low == I.size*I.itemsize
    True
    >>> I = np.eye(2); I.dtype
    dtype('float64')
    >>> low, high = np.byte_bounds(I)
    >>> high - low == I.size*I.itemsize
    True

    """
    import custom_funtemplate
    return custom_funtemplate.rewrite_template('numpy.lib.utils.byte_bounds', 'byte_bounds(a)', {'asarray': asarray, 'a': a}, 2)

def who(vardict=None):
    """
    Print the NumPy arrays in the given dictionary.

    If there is no dictionary passed in or `vardict` is None then returns
    NumPy arrays in the globals() dictionary (all NumPy arrays in the
    namespace).

    Parameters
    ----------
    vardict : dict, optional
        A dictionary possibly containing ndarrays.  Default is globals().

    Returns
    -------
    out : None
        Returns 'None'.

    Notes
    -----
    Prints out the name, shape, bytes and type of all of the ndarrays
    present in `vardict`.

    Examples
    --------
    >>> a = np.arange(10)
    >>> b = np.ones(20)
    >>> np.who()
    Name            Shape            Bytes            Type
    ===========================================================
    a               10               80               int64
    b               20               160              float64
    Upper bound on total bytes  =       240

    >>> d = {'x': np.arange(2.0), 'y': np.arange(3.0), 'txt': 'Some str',
    ... 'idx':5}
    >>> np.who(d)
    Name            Shape            Bytes            Type
    ===========================================================
    x               2                16               float64
    y               3                24               float64
    Upper bound on total bytes  =       40

    """
    import custom_funtemplate
    return custom_funtemplate.rewrite_template('numpy.lib.utils.who', 'who(vardict=None)', {'sys': sys, 'ndarray': ndarray, 'vardict': vardict}, 1)

def _split_line(name, arguments, width):
    import custom_funtemplate
    return custom_funtemplate.rewrite_template('numpy.lib.utils._split_line', '_split_line(name, arguments, width)', {'name': name, 'arguments': arguments, 'width': width}, 1)
_namedict = None
_dictlist = None

def _makenamedict(module='numpy'):
    import custom_funtemplate
    return custom_funtemplate.rewrite_template('numpy.lib.utils._makenamedict', "_makenamedict(module='numpy')", {'types': types, 'module': module}, 2)

def _info(obj, output=None):
    """Provide information about ndarray obj.

    Parameters
    ----------
    obj : ndarray
        Must be ndarray, not checked.
    output
        Where printed output goes.

    Notes
    -----
    Copied over from the numarray module prior to its removal.
    Adapted somewhat as only numpy is an option now.

    Called by info.

    """
    import custom_funtemplate
    custom_funtemplate.rewrite_template('numpy.lib.utils._info', '_info(obj, output=None)', {'sys': sys, 'obj': obj, 'output': output}, 0)

@set_module('numpy')
def info(object=None, maxwidth=76, output=None, toplevel='numpy'):
    """
    Get help information for a function, class, or module.

    Parameters
    ----------
    object : object or str, optional
        Input object or name to get information about. If `object` is a
        numpy object, its docstring is given. If it is a string, available
        modules are searched for matching objects.  If None, information
        about `info` itself is returned.
    maxwidth : int, optional
        Printing width.
    output : file like object, optional
        File like object that the output is written to, default is
        ``None``, in which case ``sys.stdout`` will be used.
        The object has to be opened in 'w' or 'a' mode.
    toplevel : str, optional
        Start search at this level.

    See Also
    --------
    source, lookfor

    Notes
    -----
    When used interactively with an object, ``np.info(obj)`` is equivalent
    to ``help(obj)`` on the Python prompt or ``obj?`` on the IPython
    prompt.

    Examples
    --------
    >>> np.info(np.polyval) # doctest: +SKIP
       polyval(p, x)
         Evaluate the polynomial p at x.
         ...

    When using a string for `object` it is possible to get multiple results.

    >>> np.info('fft') # doctest: +SKIP
         *** Found in numpy ***
    Core FFT routines
    ...
         *** Found in numpy.fft ***
     fft(a, n=None, axis=-1)
    ...
         *** Repeat reference found in numpy.fft.fftpack ***
         *** Total of 3 references found. ***

    """
    import custom_funtemplate
    custom_funtemplate.rewrite_template('numpy.lib.utils.info', "info(object=None, maxwidth=76, output=None, toplevel='numpy')", {'sys': sys, 'info': info, 'ndarray': ndarray, '_info': _info, '_makenamedict': _makenamedict, '_split_line': _split_line, 'set_module': set_module, 'object': object, 'maxwidth': maxwidth, 'output': output, 'toplevel': toplevel}, 0)

@set_module('numpy')
def source(object, output=sys.stdout):
    """
    Print or write to a file the source code for a NumPy object.

    The source code is only returned for objects written in Python. Many
    functions and classes are defined in C and will therefore not return
    useful information.

    Parameters
    ----------
    object : numpy object
        Input object. This can be any object (function, class, module,
        ...).
    output : file object, optional
        If `output` not supplied then source code is printed to screen
        (sys.stdout).  File object must be created with either write 'w' or
        append 'a' modes.

    See Also
    --------
    lookfor, info

    Examples
    --------
    >>> np.source(np.interp)                        #doctest: +SKIP
    In file: /usr/lib/python2.6/dist-packages/numpy/lib/function_base.py
    def interp(x, xp, fp, left=None, right=None):
        ".... (full docstring printed)"
        if isinstance(x, (float, int, number)):
            return compiled_interp([x], xp, fp, left, right).item()
        else:
            return compiled_interp(x, xp, fp, left, right)

    The source code is only returned for objects written in Python.

    >>> np.source(np.array)                         #doctest: +SKIP
    Not available for this object.

    """
    import inspect
    try:
        print('In file: %s\n' % inspect.getsourcefile(object), file=output)
        print(inspect.getsource(object), file=output)
    except Exception:
        print('Not available for this object.', file=output)
_lookfor_caches = {}
_function_signature_re = re.compile('[a-z0-9_]+\\(.*[,=].*\\)', re.I)

@set_module('numpy')
def lookfor(what, module=None, import_modules=True, regenerate=False, output=None):
    """
    Do a keyword search on docstrings.

    A list of objects that matched the search is displayed,
    sorted by relevance. All given keywords need to be found in the
    docstring for it to be returned as a result, but the order does
    not matter.

    Parameters
    ----------
    what : str
        String containing words to look for.
    module : str or list, optional
        Name of module(s) whose docstrings to go through.
    import_modules : bool, optional
        Whether to import sub-modules in packages. Default is True.
    regenerate : bool, optional
        Whether to re-generate the docstring cache. Default is False.
    output : file-like, optional
        File-like object to write the output to. If omitted, use a pager.

    See Also
    --------
    source, info

    Notes
    -----
    Relevance is determined only roughly, by checking if the keywords occur
    in the function name, at the start of a docstring, etc.

    Examples
    --------
    >>> np.lookfor('binary representation') # doctest: +SKIP
    Search results for 'binary representation'
    ------------------------------------------
    numpy.binary_repr
        Return the binary representation of the input number as a string.
    numpy.core.setup_common.long_double_representation
        Given a binary dump as given by GNU od -b, look for long double
    numpy.base_repr
        Return a string representation of a number in the given base system.
    ...

    """
    import custom_funtemplate
    return custom_funtemplate.rewrite_template('numpy.lib.utils.lookfor', 'lookfor(what, module=None, import_modules=True, regenerate=False, output=None)', {'_lookfor_generate_cache': _lookfor_generate_cache, '_function_signature_re': _function_signature_re, 'set_module': set_module, 'what': what, 'module': module, 'import_modules': import_modules, 'regenerate': regenerate, 'output': output}, 1)

def _lookfor_generate_cache(module, import_modules, regenerate):
    """
    Generate docstring cache for given module.

    Parameters
    ----------
    module : str, None, module
        Module for which to generate docstring cache
    import_modules : bool
        Whether to import sub-modules in packages.
    regenerate : bool
        Re-generate the docstring cache

    Returns
    -------
    cache : dict {obj_full_name: (docstring, kind, index), ...}
        Docstring cache for the module, either cached one (regenerate=False)
        or newly generated.

    """
    import custom_funtemplate
    return custom_funtemplate.rewrite_template('numpy.lib.utils._lookfor_generate_cache', '_lookfor_generate_cache(module, import_modules, regenerate)', {'sys': sys, '_lookfor_generate_cache': _lookfor_generate_cache, '_lookfor_caches': _lookfor_caches, 'os': os, '_getmembers': _getmembers, 'ufunc': ufunc, 'module': module, 'import_modules': import_modules, 'regenerate': regenerate}, 1)

def _getmembers(item):
    import custom_funtemplate
    return custom_funtemplate.rewrite_template('numpy.lib.utils._getmembers', '_getmembers(item)', {'item': item}, 1)

def safe_eval(source):
    """
    Protected string evaluation.

    Evaluate a string containing a Python literal expression without
    allowing the execution of arbitrary non-literal code.

    .. warning::

        This function is identical to :py:meth:`ast.literal_eval` and
        has the same security implications.  It may not always be safe
        to evaluate large input strings.

    Parameters
    ----------
    source : str
        The string to evaluate.

    Returns
    -------
    obj : object
       The result of evaluating `source`.

    Raises
    ------
    SyntaxError
        If the code has invalid Python syntax, or if it contains
        non-literal code.

    Examples
    --------
    >>> np.safe_eval('1')
    1
    >>> np.safe_eval('[1, 2, 3]')
    [1, 2, 3]
    >>> np.safe_eval('{"foo": ("bar", 10.0)}')
    {'foo': ('bar', 10.0)}

    >>> np.safe_eval('import os')
    Traceback (most recent call last):
      ...
    SyntaxError: invalid syntax

    >>> np.safe_eval('open("/home/user/.ssh/id_dsa").read()')
    Traceback (most recent call last):
      ...
    ValueError: malformed node or string: <_ast.Call object at 0x...>

    """
    import ast
    return ast.literal_eval(source)

def _median_nancheck(data, result, axis):
    """
    Utility function to check median result from data for NaN values at the end
    and return NaN in that case. Input result can also be a MaskedArray.

    Parameters
    ----------
    data : array
        Sorted input data to median function
    result : Array or MaskedArray
        Result of median function.
    axis : int
        Axis along which the median was computed.

    Returns
    -------
    result : scalar or ndarray
        Median or NaN in axes which contained NaN in the input.  If the input
        was an array, NaN will be inserted in-place.  If a scalar, either the
        input itself or a scalar NaN.
    """
    if data.size == 0:
        return result
    n = np.isnan(data.take(-1, axis=axis))
    if np.ma.isMaskedArray(n):
        n = n.filled(False)
    if np.count_nonzero(n.ravel()) > 0:
        if isinstance(result, np.generic):
            return data.dtype.type(np.nan)
        result[n] = np.nan
    return result

def _opt_info():
    """
    Returns a string contains the supported CPU features by the current build.

    The string format can be explained as follows:
        - dispatched features that are supported by the running machine
          end with `*`.
        - dispatched features that are "not" supported by the running machine
          end with `?`.
        - remained features are representing the baseline.
    """
    import custom_funtemplate
    return custom_funtemplate.rewrite_template('numpy.lib.utils._opt_info', '_opt_info()', {}, 1)

