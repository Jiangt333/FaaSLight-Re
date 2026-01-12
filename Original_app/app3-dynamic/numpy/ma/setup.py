
def configuration(parent_package='', top_path=None):
    print('/home/jiangt/FaaSLight-Re/Original_app/app3-dynamic/numpy/ma/setup.py=configuration=2')
    from numpy.distutils.misc_util import Configuration
    config = Configuration('ma', parent_package, top_path)
    config.add_subpackage('tests')
    config.add_data_files('*.pyi')
    return config
if __name__ == '__main__':
    from numpy.distutils.core import setup
    config = configuration(top_path='').todict()
    setup(**config)

