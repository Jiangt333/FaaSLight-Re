from distutils.command.build_py import build_py as old_build_py
from numpy.distutils.misc_util import is_string


class build_py(old_build_py):
    
    def run(self):
        print('/home/jiangt/FaaSLight-Re/Original_app/app3-dynamic/numpy/distutils/command/build_py.py=build_py=run=6')
        build_src = self.get_finalized_command('build_src')
        if (build_src.py_modules_dict and self.packages is None):
            self.packages = list(build_src.py_modules_dict.keys())
        old_build_py.run(self)
    
    def find_package_modules(self, package, package_dir):
        print('/home/jiangt/FaaSLight-Re/Original_app/app3-dynamic/numpy/distutils/command/build_py.py=build_py=find_package_modules=12')
        modules = old_build_py.find_package_modules(self, package, package_dir)
        build_src = self.get_finalized_command('build_src')
        modules += build_src.py_modules_dict.get(package, [])
        return modules
    
    def find_modules(self):
        print('/home/jiangt/FaaSLight-Re/Original_app/app3-dynamic/numpy/distutils/command/build_py.py=build_py=find_modules=21')
        old_py_modules = self.py_modules[:]
        new_py_modules = [_m for _m in self.py_modules if is_string(_m)]
        self.py_modules[:] = new_py_modules
        modules = old_build_py.find_modules(self)
        self.py_modules[:] = old_py_modules
        return modules


