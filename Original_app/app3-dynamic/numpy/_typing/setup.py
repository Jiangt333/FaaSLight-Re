
def configuration(parent_package='', top_path=None):
    print('/home/jiangt/FaaSLight-Re/Original_app/app3-dynamic/numpy/_typing/setup.py=configuration=1')
    from numpy.distutils.misc_util import Configuration
    config = Configuration('_typing', parent_package, top_path)
    config.add_data_files('*.pyi')
    return config
if __name__ == '__main__':
    from numpy.distutils.core import setup
    setup(configuration=configuration)

