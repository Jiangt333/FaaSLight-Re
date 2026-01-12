from numpy.distutils.fcompiler import FCompiler
compilers = ['G95FCompiler']


class G95FCompiler(FCompiler):
    compiler_type = 'g95'
    description = 'G95 Fortran Compiler'
    version_pattern = 'G95 \\((GCC (?P<gccversion>[\\d.]+)|.*?) \\(g95 (?P<version>.*)!\\) (?P<date>.*)\\).*'
    executables = {'version_cmd': ['<F90>', '--version'], 'compiler_f77': ['g95', '-ffixed-form'], 'compiler_fix': ['g95', '-ffixed-form'], 'compiler_f90': ['g95'], 'linker_so': ['<F90>', '-shared'], 'archiver': ['ar', '-cr'], 'ranlib': ['ranlib']}
    pic_flags = ['-fpic']
    module_dir_switch = '-fmod='
    module_include_switch = '-I'
    
    def get_flags(self):
        print('/home/jiangt/FaaSLight-Re/Original_app/app3-dynamic/numpy/distutils/fcompiler/g95.py=G95FCompiler=get_flags=31')
        return ['-fno-second-underscore']
    
    def get_flags_opt(self):
        print('/home/jiangt/FaaSLight-Re/Original_app/app3-dynamic/numpy/distutils/fcompiler/g95.py=G95FCompiler=get_flags_opt=33')
        return ['-O']
    
    def get_flags_debug(self):
        print('/home/jiangt/FaaSLight-Re/Original_app/app3-dynamic/numpy/distutils/fcompiler/g95.py=G95FCompiler=get_flags_debug=35')
        return ['-g']

if __name__ == '__main__':
    from distutils import log
    from numpy.distutils import customized_fcompiler
    log.set_verbosity(2)
    print(customized_fcompiler('g95').get_version())

