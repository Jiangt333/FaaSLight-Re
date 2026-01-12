from distutils.core import Distribution


class NumpyDistribution(Distribution):
    
    def __init__(self, attrs=None):
        print('/home/jiangt/FaaSLight-Re/Original_app/app3-dynamic/numpy/distutils/numpy_distribution.py=NumpyDistribution=__init__=7')
        self.scons_data = []
        self.installed_libraries = []
        self.installed_pkg_config = {}
        Distribution.__init__(self, attrs)
    
    def has_scons_scripts(self):
        print('/home/jiangt/FaaSLight-Re/Original_app/app3-dynamic/numpy/distutils/numpy_distribution.py=NumpyDistribution=has_scons_scripts=16')
        return bool(self.scons_data)


