import os
import genapi
from genapi import TypeApi, GlobalVarApi, FunctionApi, BoolValuesApi
import numpy_api
h_template = '\n#if defined(_MULTIARRAYMODULE) || defined(WITH_CPYCHECKER_STEALS_REFERENCE_TO_ARG_ATTRIBUTE)\n\ntypedef struct {\n        PyObject_HEAD\n        npy_bool obval;\n} PyBoolScalarObject;\n\nextern NPY_NO_EXPORT PyTypeObject PyArrayMapIter_Type;\nextern NPY_NO_EXPORT PyTypeObject PyArrayNeighborhoodIter_Type;\nextern NPY_NO_EXPORT PyBoolScalarObject _PyArrayScalar_BoolValues[2];\n\n%s\n\n#else\n\n#if defined(PY_ARRAY_UNIQUE_SYMBOL)\n#define PyArray_API PY_ARRAY_UNIQUE_SYMBOL\n#endif\n\n#if defined(NO_IMPORT) || defined(NO_IMPORT_ARRAY)\nextern void **PyArray_API;\n#else\n#if defined(PY_ARRAY_UNIQUE_SYMBOL)\nvoid **PyArray_API;\n#else\nstatic void **PyArray_API=NULL;\n#endif\n#endif\n\n%s\n\n#if !defined(NO_IMPORT_ARRAY) && !defined(NO_IMPORT)\nstatic int\n_import_array(void)\n{\n  int st;\n  PyObject *numpy = PyImport_ImportModule("numpy.core._multiarray_umath");\n  PyObject *c_api = NULL;\n\n  if (numpy == NULL) {\n      return -1;\n  }\n  c_api = PyObject_GetAttrString(numpy, "_ARRAY_API");\n  Py_DECREF(numpy);\n  if (c_api == NULL) {\n      PyErr_SetString(PyExc_AttributeError, "_ARRAY_API not found");\n      return -1;\n  }\n\n  if (!PyCapsule_CheckExact(c_api)) {\n      PyErr_SetString(PyExc_RuntimeError, "_ARRAY_API is not PyCapsule object");\n      Py_DECREF(c_api);\n      return -1;\n  }\n  PyArray_API = (void **)PyCapsule_GetPointer(c_api, NULL);\n  Py_DECREF(c_api);\n  if (PyArray_API == NULL) {\n      PyErr_SetString(PyExc_RuntimeError, "_ARRAY_API is NULL pointer");\n      return -1;\n  }\n\n  /* Perform runtime check of C API version */\n  if (NPY_VERSION != PyArray_GetNDArrayCVersion()) {\n      PyErr_Format(PyExc_RuntimeError, "module compiled against "\\\n             "ABI version 0x%%x but this version of numpy is 0x%%x", \\\n             (int) NPY_VERSION, (int) PyArray_GetNDArrayCVersion());\n      return -1;\n  }\n  if (NPY_FEATURE_VERSION > PyArray_GetNDArrayCFeatureVersion()) {\n      PyErr_Format(PyExc_RuntimeError, "module compiled against "\\\n             "API version 0x%%x but this version of numpy is 0x%%x . "\\\n             "Check the section C-API incompatibility at the "\\\n             "Troubleshooting ImportError section at "\\\n             "https://numpy.org/devdocs/user/troubleshooting-importerror.html"\\\n             "#c-api-incompatibility "\\\n              "for indications on how to solve this problem .", \\\n             (int) NPY_FEATURE_VERSION, (int) PyArray_GetNDArrayCFeatureVersion());\n      return -1;\n  }\n\n  /*\n   * Perform runtime check of endianness and check it matches the one set by\n   * the headers (npy_endian.h) as a safeguard\n   */\n  st = PyArray_GetEndianness();\n  if (st == NPY_CPU_UNKNOWN_ENDIAN) {\n      PyErr_SetString(PyExc_RuntimeError,\n                      "FATAL: module compiled as unknown endian");\n      return -1;\n  }\n#if NPY_BYTE_ORDER == NPY_BIG_ENDIAN\n  if (st != NPY_CPU_BIG) {\n      PyErr_SetString(PyExc_RuntimeError,\n                      "FATAL: module compiled as big endian, but "\n                      "detected different endianness at runtime");\n      return -1;\n  }\n#elif NPY_BYTE_ORDER == NPY_LITTLE_ENDIAN\n  if (st != NPY_CPU_LITTLE) {\n      PyErr_SetString(PyExc_RuntimeError,\n                      "FATAL: module compiled as little endian, but "\n                      "detected different endianness at runtime");\n      return -1;\n  }\n#endif\n\n  return 0;\n}\n\n#define import_array() {if (_import_array() < 0) {PyErr_Print(); PyErr_SetString(PyExc_ImportError, "numpy.core.multiarray failed to import"); return NULL; } }\n\n#define import_array1(ret) {if (_import_array() < 0) {PyErr_Print(); PyErr_SetString(PyExc_ImportError, "numpy.core.multiarray failed to import"); return ret; } }\n\n#define import_array2(msg, ret) {if (_import_array() < 0) {PyErr_Print(); PyErr_SetString(PyExc_ImportError, msg); return ret; } }\n\n#endif\n\n#endif\n'
c_template = '\n/* These pointers will be stored in the C-object for use in other\n    extension modules\n*/\n\nvoid *PyArray_API[] = {\n%s\n};\n'
c_api_header = '\n===========\nNumPy C-API\n===========\n'

def generate_api(output_dir, force=False):
    print('/home/jiangt/FaaSLight-Re/Original_app/app3-dynamic/numpy/core/generate_numpy_api.py=generate_api=148')
    basename = 'multiarray_api'
    h_file = os.path.join(output_dir, '__%s.h' % basename)
    c_file = os.path.join(output_dir, '__%s.c' % basename)
    d_file = os.path.join(output_dir, '%s.txt' % basename)
    targets = (h_file, c_file, d_file)
    sources = numpy_api.multiarray_api
    if (not force and not genapi.should_rebuild(targets, [numpy_api.__file__, __file__])):
        return targets
    else:
        do_generate_api(targets, sources)
    return targets

def do_generate_api(targets, sources):
    print('/home/jiangt/FaaSLight-Re/Original_app/app3-dynamic/numpy/core/generate_numpy_api.py=do_generate_api=165')
    header_file = targets[0]
    c_file = targets[1]
    doc_file = targets[2]
    global_vars = sources[0]
    scalar_bool_values = sources[1]
    types_api = sources[2]
    multiarray_funcs = sources[3]
    multiarray_api = sources[:]
    module_list = []
    extension_list = []
    init_list = []
    multiarray_api_index = genapi.merge_api_dicts(multiarray_api)
    genapi.check_api_dict(multiarray_api_index)
    numpyapi_list = genapi.get_api_functions('NUMPY_API', multiarray_funcs)
    api_name = 'PyArray_API'
    multiarray_api_dict = {}
    for f in numpyapi_list:
        name = f.name
        index = multiarray_funcs[name][0]
        annotations = multiarray_funcs[name][1:]
        multiarray_api_dict[f.name] = FunctionApi(f.name, index, annotations, f.return_type, f.args, api_name)
    for (name, val) in global_vars.items():
        (index, type) = val
        multiarray_api_dict[name] = GlobalVarApi(name, index, type, api_name)
    for (name, val) in scalar_bool_values.items():
        index = val[0]
        multiarray_api_dict[name] = BoolValuesApi(name, index, api_name)
    for (name, val) in types_api.items():
        index = val[0]
        internal_type = (None if len(val) == 1 else val[1])
        multiarray_api_dict[name] = TypeApi(name, index, 'PyTypeObject', api_name, internal_type)
    if len(multiarray_api_dict) != len(multiarray_api_index):
        keys_dict = set(multiarray_api_dict.keys())
        keys_index = set(multiarray_api_index.keys())
        raise AssertionError('Multiarray API size mismatch - index has extra keys {}, dict has extra keys {}'.format(keys_index - keys_dict, keys_dict - keys_index))
    extension_list = []
    for (name, index) in genapi.order_dict(multiarray_api_index):
        api_item = multiarray_api_dict[name]
        extension_list.append(api_item.define_from_array_api_string())
        init_list.append(api_item.array_api_define())
        module_list.append(api_item.internal_define())
    s = h_template % ('\n'.join(module_list), '\n'.join(extension_list))
    genapi.write_file(header_file, s)
    s = c_template % ',\n'.join(init_list)
    genapi.write_file(c_file, s)
    s = c_api_header
    for func in numpyapi_list:
        s += func.to_ReST()
        s += '\n\n'
    genapi.write_file(doc_file, s)
    return targets

