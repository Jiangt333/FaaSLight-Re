from numpy.distutils.fcompiler import FCompiler
compilers = ['HPUXFCompiler']


class HPUXFCompiler(FCompiler):
    compiler_type = 'hpux'
    description = 'HP Fortran 90 Compiler'
    version_pattern = 'HP F90 (?P<version>[^\\s*,]*)'
    executables = {'version_cmd': ['f90', '+version'], 'compiler_f77': ['f90'], 'compiler_fix': ['f90'], 'compiler_f90': ['f90'], 'linker_so': ['ld', '-b'], 'archiver': ['ar', '-cr'], 'ranlib': ['ranlib']}
    module_dir_switch = None
    module_include_switch = None
    pic_flags = ['+Z']
    
    def get_flags(self):
        print('/home/jiangt/FaaSLight-Re/Original_app/app3-dynamic/numpy/distutils/fcompiler/hpux.py=HPUXFCompiler=get_flags=23')
        return self.pic_flags + ['+ppu', '+DD64']
    
    def get_flags_opt(self):
        print('/home/jiangt/FaaSLight-Re/Original_app/app3-dynamic/numpy/distutils/fcompiler/hpux.py=HPUXFCompiler=get_flags_opt=25')
        return ['-O3']
    
    def get_libraries(self):
        print('/home/jiangt/FaaSLight-Re/Original_app/app3-dynamic/numpy/distutils/fcompiler/hpux.py=HPUXFCompiler=get_libraries=27')
        return ['m']
    
    def get_library_dirs(self):
        print('/home/jiangt/FaaSLight-Re/Original_app/app3-dynamic/numpy/distutils/fcompiler/hpux.py=HPUXFCompiler=get_library_dirs=29')
        opt = ['/usr/lib/hpux64']
        return opt
    
    def get_version(self, force=0, ok_status=[256, 0, 1]):
        print('/home/jiangt/FaaSLight-Re/Original_app/app3-dynamic/numpy/distutils/fcompiler/hpux.py=HPUXFCompiler=get_version=32')
        return FCompiler.get_version(self, force, ok_status)

if __name__ == '__main__':
    from distutils import log
    log.set_verbosity(10)
    from numpy.distutils import customized_fcompiler
    print(customized_fcompiler(compiler='hpux').get_version())

