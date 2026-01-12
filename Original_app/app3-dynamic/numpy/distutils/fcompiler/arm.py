import sys
from numpy.distutils.fcompiler import FCompiler, dummy_fortran_file
from sys import platform
from os.path import join, dirname, normpath
compilers = ['ArmFlangCompiler']
import functools


class ArmFlangCompiler(FCompiler):
    compiler_type = 'arm'
    description = 'Arm Compiler'
    version_pattern = '\\s*Arm.*version (?P<version>[\\d.-]+).*'
    ar_exe = 'lib.exe'
    possible_executables = ['armflang']
    executables = {'version_cmd': ['', '--version'], 'compiler_f77': ['armflang', '-fPIC'], 'compiler_fix': ['armflang', '-fPIC', '-ffixed-form'], 'compiler_f90': ['armflang', '-fPIC'], 'linker_so': ['armflang', '-fPIC', '-shared'], 'archiver': ['ar', '-cr'], 'ranlib': None}
    pic_flags = ['-fPIC', '-DPIC']
    c_compiler = 'arm'
    module_dir_switch = '-module '
    
    def get_libraries(self):
        print('/home/jiangt/FaaSLight-Re/Original_app/app3-dynamic/numpy/distutils/fcompiler/arm.py=ArmFlangCompiler=get_libraries=33')
        opt = FCompiler.get_libraries(self)
        opt.extend(['flang', 'flangrti', 'ompstub'])
        return opt
    
    @functools.lru_cache(maxsize=128)
    def get_library_dirs(self):
        """List of compiler library directories."""
        print('/home/jiangt/FaaSLight-Re/Original_app/app3-dynamic/numpy/distutils/fcompiler/arm.py=ArmFlangCompiler=get_library_dirs=38')
        opt = FCompiler.get_library_dirs(self)
        flang_dir = dirname(self.executables['compiler_f77'][0])
        opt.append(normpath(join(flang_dir, '..', 'lib')))
        return opt
    
    def get_flags(self):
        print('/home/jiangt/FaaSLight-Re/Original_app/app3-dynamic/numpy/distutils/fcompiler/arm.py=ArmFlangCompiler=get_flags=47')
        return []
    
    def get_flags_free(self):
        print('/home/jiangt/FaaSLight-Re/Original_app/app3-dynamic/numpy/distutils/fcompiler/arm.py=ArmFlangCompiler=get_flags_free=50')
        return []
    
    def get_flags_debug(self):
        print('/home/jiangt/FaaSLight-Re/Original_app/app3-dynamic/numpy/distutils/fcompiler/arm.py=ArmFlangCompiler=get_flags_debug=53')
        return ['-g']
    
    def get_flags_opt(self):
        print('/home/jiangt/FaaSLight-Re/Original_app/app3-dynamic/numpy/distutils/fcompiler/arm.py=ArmFlangCompiler=get_flags_opt=56')
        return ['-O3']
    
    def get_flags_arch(self):
        print('/home/jiangt/FaaSLight-Re/Original_app/app3-dynamic/numpy/distutils/fcompiler/arm.py=ArmFlangCompiler=get_flags_arch=59')
        return []
    
    def runtime_library_dir_option(self, dir):
        print('/home/jiangt/FaaSLight-Re/Original_app/app3-dynamic/numpy/distutils/fcompiler/arm.py=ArmFlangCompiler=runtime_library_dir_option=62')
        return '-Wl,-rpath=%s' % dir

if __name__ == '__main__':
    from distutils import log
    log.set_verbosity(2)
    from numpy.distutils import customized_fcompiler
    print(customized_fcompiler(compiler='armflang').get_version())

