import os

def parse_distributions_h(ffi, inc_dir):
    """
    Parse distributions.h located in inc_dir for CFFI, filling in the ffi.cdef

    Read the function declarations without the "#define ..." macros that will
    be filled in when loading the library.
    """
    print('/home/jiangt/FaaSLight-Re/Original_app/app3-dynamic/numpy/random/_examples/cffi/parse.py=parse_distributions_h=4')
    with open(os.path.join(inc_dir, 'random', 'bitgen.h')) as fid:
        s = []
        for line in fid:
            if line.strip().startswith('#'):
                continue
            s.append(line)
        ffi.cdef('\n'.join(s))
    with open(os.path.join(inc_dir, 'random', 'distributions.h')) as fid:
        s = []
        in_skip = 0
        ignoring = False
        for line in fid:
            if ignoring:
                if line.strip().startswith('#endif'):
                    ignoring = False
                continue
            if line.strip().startswith('#ifdef __cplusplus'):
                ignoring = True
            if line.strip().startswith('#'):
                continue
            if line.strip().startswith('static NPY_INLINE'):
                in_skip += line.count('{')
                continue
            elif in_skip > 0:
                in_skip += line.count('{')
                in_skip -= line.count('}')
                continue
            line = line.replace('DECLDIR', '')
            line = line.replace('NPY_INLINE', '')
            line = line.replace('RAND_INT_TYPE', 'int64_t')
            s.append(line)
        ffi.cdef('\n'.join(s))

