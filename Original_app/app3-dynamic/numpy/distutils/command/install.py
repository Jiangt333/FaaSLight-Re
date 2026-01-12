import sys
if 'setuptools' in sys.modules:
    import setuptools.command.install as old_install_mod
    have_setuptools = True
else:
    import distutils.command.install as old_install_mod
    have_setuptools = False
from distutils.file_util import write_file
old_install = old_install_mod.install


class install(old_install):
    sub_commands = old_install.sub_commands + [('install_clib', lambda x: True)]
    
    def finalize_options(self):
        print('/home/jiangt/FaaSLight-Re/Original_app/app3-dynamic/numpy/distutils/command/install.py=install=finalize_options=20')
        old_install.finalize_options(self)
        self.install_lib = self.install_libbase
    
    def setuptools_run(self):
        """ The setuptools version of the .run() method.

        We must pull in the entire code so we can override the level used in the
        _getframe() call since we wrap this call by one more level.
        """
        print('/home/jiangt/FaaSLight-Re/Original_app/app3-dynamic/numpy/distutils/command/install.py=install=setuptools_run=24')
        from distutils.command.install import install as distutils_install
        if (self.old_and_unmanageable or self.single_version_externally_managed):
            return distutils_install.run(self)
        caller = sys._getframe(3)
        caller_module = caller.f_globals.get('__name__', '')
        caller_name = caller.f_code.co_name
        if (caller_module != 'distutils.dist' or caller_name != 'run_commands'):
            distutils_install.run(self)
        else:
            self.do_egg_install()
    
    def run(self):
        print('/home/jiangt/FaaSLight-Re/Original_app/app3-dynamic/numpy/distutils/command/install.py=install=run=56')
        if not have_setuptools:
            r = old_install.run(self)
        else:
            r = self.setuptools_run()
        if self.record:
            with open(self.record, 'r') as f:
                lines = []
                need_rewrite = False
                for l in f:
                    l = l.rstrip()
                    if ' ' in l:
                        need_rewrite = True
                        l = '"%s"' % l
                    lines.append(l)
            if need_rewrite:
                self.execute(write_file, (self.record, lines), "re-writing list of installed files to '%s'" % self.record)
        return r


