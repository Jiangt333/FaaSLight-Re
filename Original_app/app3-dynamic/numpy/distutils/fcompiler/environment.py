import os
from distutils.dist import Distribution
__metaclass__ = type


class EnvironmentConfig:
    
    def __init__(self, distutils_section='ALL', **kw):
        print('/home/jiangt/FaaSLight-Re/Original_app/app3-dynamic/numpy/distutils/fcompiler/environment.py=EnvironmentConfig=__init__=7')
        self._distutils_section = distutils_section
        self._conf_keys = kw
        self._conf = None
        self._hook_handler = None
    
    def dump_variable(self, name):
        print('/home/jiangt/FaaSLight-Re/Original_app/app3-dynamic/numpy/distutils/fcompiler/environment.py=EnvironmentConfig=dump_variable=13')
        conf_desc = self._conf_keys[name]
        (hook, envvar, confvar, convert, append) = conf_desc
        if not convert:
            convert = lambda x: x
        print('%s.%s:' % (self._distutils_section, name))
        v = self._hook_handler(name, hook)
        print('  hook   : %s' % (convert(v), ))
        if envvar:
            v = os.environ.get(envvar, None)
            print('  environ: %s' % (convert(v), ))
        if (confvar and self._conf):
            v = self._conf.get(confvar, (None, None))[1]
            print('  config : %s' % (convert(v), ))
    
    def dump_variables(self):
        print('/home/jiangt/FaaSLight-Re/Original_app/app3-dynamic/numpy/distutils/fcompiler/environment.py=EnvironmentConfig=dump_variables=28')
        for name in self._conf_keys:
            self.dump_variable(name)
    
    def __getattr__(self, name):
        print('/home/jiangt/FaaSLight-Re/Original_app/app3-dynamic/numpy/distutils/fcompiler/environment.py=EnvironmentConfig=__getattr__=32')
        try:
            conf_desc = self._conf_keys[name]
        except KeyError:
            raise AttributeError(f"'EnvironmentConfig' object has no attribute '{name}'") from None
        return self._get_var(name, conf_desc)
    
    def get(self, name, default=None):
        print('/home/jiangt/FaaSLight-Re/Original_app/app3-dynamic/numpy/distutils/fcompiler/environment.py=EnvironmentConfig=get=42')
        try:
            conf_desc = self._conf_keys[name]
        except KeyError:
            return default
        var = self._get_var(name, conf_desc)
        if var is None:
            var = default
        return var
    
    def _get_var(self, name, conf_desc):
        print('/home/jiangt/FaaSLight-Re/Original_app/app3-dynamic/numpy/distutils/fcompiler/environment.py=EnvironmentConfig=_get_var=52')
        (hook, envvar, confvar, convert, append) = conf_desc
        if convert is None:
            convert = lambda x: x
        var = self._hook_handler(name, hook)
        if envvar is not None:
            envvar_contents = os.environ.get(envvar)
            if envvar_contents is not None:
                envvar_contents = convert(envvar_contents)
                if (var and append):
                    if os.environ.get('NPY_DISTUTILS_APPEND_FLAGS', '1') == '1':
                        var.extend(envvar_contents)
                    else:
                        var = envvar_contents
                else:
                    var = envvar_contents
        if (confvar is not None and self._conf):
            if confvar in self._conf:
                (source, confvar_contents) = self._conf[confvar]
                var = convert(confvar_contents)
        return var
    
    def clone(self, hook_handler):
        print('/home/jiangt/FaaSLight-Re/Original_app/app3-dynamic/numpy/distutils/fcompiler/environment.py=EnvironmentConfig=clone=78')
        ec = self.__class__(distutils_section=self._distutils_section, **self._conf_keys)
        ec._hook_handler = hook_handler
        return ec
    
    def use_distribution(self, dist):
        print('/home/jiangt/FaaSLight-Re/Original_app/app3-dynamic/numpy/distutils/fcompiler/environment.py=EnvironmentConfig=use_distribution=84')
        if isinstance(dist, Distribution):
            self._conf = dist.get_option_dict(self._distutils_section)
        else:
            self._conf = dist


