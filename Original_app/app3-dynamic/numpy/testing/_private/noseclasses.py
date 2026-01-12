import os
import sys
import doctest
import inspect
import numpy
import nose
from nose.plugins import doctests as npd
from nose.plugins.errorclass import ErrorClass, ErrorClassPlugin
from nose.plugins.base import Plugin
from nose.util import src
from .nosetester import get_package_name
from .utils import KnownFailureException, KnownFailureTest


class NumpyDocTestFinder(doctest.DocTestFinder):
    
    def _from_module(self, module, object):
        """
        Return true if the given object is defined in the given
        module.
        """
        print('/home/jiangt/FaaSLight-Re/Original_app/app3-dynamic/numpy/testing/_private/noseclasses.py=NumpyDocTestFinder=_from_module=30')
        if module is None:
            return True
        elif inspect.isfunction(object):
            return module.__dict__ is object.__globals__
        elif inspect.isbuiltin(object):
            return module.__name__ == object.__module__
        elif inspect.isclass(object):
            return module.__name__ == object.__module__
        elif inspect.ismethod(object):
            return module.__name__ == object.__self__.__class__.__module__
        elif inspect.getmodule(object) is not None:
            return module is inspect.getmodule(object)
        elif hasattr(object, '__module__'):
            return module.__name__ == object.__module__
        elif isinstance(object, property):
            return True
        else:
            raise ValueError('object must be a class or function')
    
    def _find(self, tests, obj, name, module, source_lines, globs, seen):
        """
        Find tests for the given object and any contained objects, and
        add them to `tests`.
        """
        print('/home/jiangt/FaaSLight-Re/Original_app/app3-dynamic/numpy/testing/_private/noseclasses.py=NumpyDocTestFinder=_find=58')
        doctest.DocTestFinder._find(self, tests, obj, name, module, source_lines, globs, seen)
        from inspect import isroutine, isclass, ismodule, isfunction, ismethod
        if (ismodule(obj) and self._recurse):
            for (valname, val) in obj.__dict__.items():
                valname1 = f'{name}.{valname}'
                if (((isroutine(val) or isclass(val))) and self._from_module(module, val)):
                    self._find(tests, val, valname1, module, source_lines, globs, seen)
        if (isclass(obj) and self._recurse):
            for (valname, val) in obj.__dict__.items():
                if isinstance(val, staticmethod):
                    val = getattr(obj, valname)
                if isinstance(val, classmethod):
                    val = getattr(obj, valname).__func__
                if (((isfunction(val) or isclass(val) or ismethod(val) or isinstance(val, property))) and self._from_module(module, val)):
                    valname = f'{name}.{valname}'
                    self._find(tests, val, valname, module, source_lines, globs, seen)



class NumpyOutputChecker(doctest.OutputChecker):
    
    def check_output(self, want, got, optionflags):
        print('/home/jiangt/FaaSLight-Re/Original_app/app3-dynamic/numpy/testing/_private/noseclasses.py=NumpyOutputChecker=check_output=108')
        ret = doctest.OutputChecker.check_output(self, want, got, optionflags)
        if not ret:
            if '#random' in want:
                return True
            got = got.replace("'>", "'<")
            want = want.replace("'>", "'<")
            for sz in [4, 8]:
                got = got.replace("'<i%d'" % sz, 'int')
                want = want.replace("'<i%d'" % sz, 'int')
            ret = doctest.OutputChecker.check_output(self, want, got, optionflags)
        return ret



class NumpyDocTestCase(npd.DocTestCase):
    
    def __init__(self, test, optionflags=0, setUp=None, tearDown=None, checker=None, obj=None, result_var='_'):
        print('/home/jiangt/FaaSLight-Re/Original_app/app3-dynamic/numpy/testing/_private/noseclasses.py=NumpyDocTestCase=__init__=137')
        self._result_var = result_var
        self._nose_obj = obj
        doctest.DocTestCase.__init__(self, test, optionflags=optionflags, setUp=setUp, tearDown=tearDown, checker=checker)

print_state = numpy.get_printoptions()


class NumpyDoctest(npd.Doctest):
    name = 'numpydoctest'
    score = 1000
    doctest_optflags = doctest.NORMALIZE_WHITESPACE | doctest.ELLIPSIS
    doctest_ignore = ['generate_numpy_api.py', 'setup.py']
    doctest_case_class = NumpyDocTestCase
    out_check_class = NumpyOutputChecker
    test_finder_class = NumpyDocTestFinder
    
    def options(self, parser, env=os.environ):
        print('/home/jiangt/FaaSLight-Re/Original_app/app3-dynamic/numpy/testing/_private/noseclasses.py=NumpyDoctest=options=166')
        Plugin.options(self, parser, env)
        self.doctest_tests = True
        self.doctest_result_var = None
    
    def configure(self, options, config):
        print('/home/jiangt/FaaSLight-Re/Original_app/app3-dynamic/numpy/testing/_private/noseclasses.py=NumpyDoctest=configure=175')
        Plugin.configure(self, options, config)
        self.finder = self.test_finder_class()
        self.parser = doctest.DocTestParser()
        if self.enabled:
            config.plugins.plugins = [p for p in config.plugins.plugins if p.name != 'doctest']
    
    def set_test_context(self, test):
        """ Configure `test` object to set test context

        We set the numpy / scipy standard doctest namespace

        Parameters
        ----------
        test : test object
            with ``globs`` dictionary defining namespace

        Returns
        -------
        None

        Notes
        -----
        `test` object modified in place
        """
        print('/home/jiangt/FaaSLight-Re/Original_app/app3-dynamic/numpy/testing/_private/noseclasses.py=NumpyDoctest=set_test_context=188')
        pkg_name = get_package_name(os.path.dirname(test.filename))
        test.globs = {'__builtins__': __builtins__, '__file__': '__main__', '__name__': '__main__', 'np': numpy}
        if 'scipy' in pkg_name:
            p = pkg_name.split('.')
            p2 = p[-1]
            test.globs[p2] = __import__(pkg_name, test.globs, {}, [p2])
    
    def loadTestsFromModule(self, module):
        print('/home/jiangt/FaaSLight-Re/Original_app/app3-dynamic/numpy/testing/_private/noseclasses.py=NumpyDoctest=loadTestsFromModule=230')
        if not self.matches(module.__name__):
            npd.log.debug("Doctest doesn't want module %s", module)
            return
        try:
            tests = self.finder.find(module)
        except AttributeError:
            return
        if not tests:
            return
        tests.sort()
        module_file = src(module.__file__)
        for test in tests:
            if not test.examples:
                continue
            if not test.filename:
                test.filename = module_file
            self.set_test_context(test)
            yield self.doctest_case_class(test, optionflags=self.doctest_optflags, checker=self.out_check_class(), result_var=self.doctest_result_var)
    
    def afterContext(self):
        print('/home/jiangt/FaaSLight-Re/Original_app/app3-dynamic/numpy/testing/_private/noseclasses.py=NumpyDoctest=afterContext=258')
        numpy.set_printoptions(**print_state)
    
    def wantFile(self, file):
        print('/home/jiangt/FaaSLight-Re/Original_app/app3-dynamic/numpy/testing/_private/noseclasses.py=NumpyDoctest=wantFile=262')
        bn = os.path.basename(file)
        if bn in self.doctest_ignore:
            return False
        return npd.Doctest.wantFile(self, file)



class Unplugger:
    """ Nose plugin to remove named plugin late in loading

    By default it removes the "doctest" plugin.
    """
    name = 'unplugger'
    enabled = True
    score = 4000
    
    def __init__(self, to_unplug='doctest'):
        print('/home/jiangt/FaaSLight-Re/Original_app/app3-dynamic/numpy/testing/_private/noseclasses.py=Unplugger=__init__=278')
        self.to_unplug = to_unplug
    
    def options(self, parser, env):
        print('/home/jiangt/FaaSLight-Re/Original_app/app3-dynamic/numpy/testing/_private/noseclasses.py=Unplugger=options=281')
        pass
    
    def configure(self, options, config):
        print('/home/jiangt/FaaSLight-Re/Original_app/app3-dynamic/numpy/testing/_private/noseclasses.py=Unplugger=configure=284')
        config.plugins.plugins = [p for p in config.plugins.plugins if p.name != self.to_unplug]



class KnownFailurePlugin(ErrorClassPlugin):
    """Plugin that installs a KNOWNFAIL error class for the
    KnownFailureClass exception.  When KnownFailure is raised,
    the exception will be logged in the knownfail attribute of the
    result, 'K' or 'KNOWNFAIL' (verbose) will be output, and the
    exception will not be counted as an error or failure."""
    enabled = True
    knownfail = ErrorClass(KnownFailureException, label='KNOWNFAIL', isfailure=False)
    
    def options(self, parser, env=os.environ):
        print('/home/jiangt/FaaSLight-Re/Original_app/app3-dynamic/numpy/testing/_private/noseclasses.py=KnownFailurePlugin=options=301')
        env_opt = 'NOSE_WITHOUT_KNOWNFAIL'
        parser.add_option('--no-knownfail', action='store_true', dest='noKnownFail', default=env.get(env_opt, False), help='Disable special handling of KnownFailure exceptions')
    
    def configure(self, options, conf):
        print('/home/jiangt/FaaSLight-Re/Original_app/app3-dynamic/numpy/testing/_private/noseclasses.py=KnownFailurePlugin=configure=308')
        if not self.can_configure:
            return
        self.conf = conf
        disable = getattr(options, 'noKnownFail', False)
        if disable:
            self.enabled = False

KnownFailure = KnownFailurePlugin


class FPUModeCheckPlugin(Plugin):
    """
    Plugin that checks the FPU mode before and after each test,
    raising failures if the test changed the mode.
    """
    
    def prepareTestCase(self, test):
        print('/home/jiangt/FaaSLight-Re/Original_app/app3-dynamic/numpy/testing/_private/noseclasses.py=FPUModeCheckPlugin=prepareTestCase=325')
        from numpy.core._multiarray_tests import get_fpu_mode
        
        def run(result):
            print('/home/jiangt/FaaSLight-Re/Original_app/app3-dynamic/numpy/testing/_private/noseclasses.py=FPUModeCheckPlugin=prepareTestCase=run=328')
            old_mode = get_fpu_mode()
            test.test(result)
            new_mode = get_fpu_mode()
            if old_mode != new_mode:
                try:
                    raise AssertionError('FPU mode changed from {0:#x} to {1:#x} during the test'.format(old_mode, new_mode))
                except AssertionError:
                    result.addFailure(test, sys.exc_info())
        return run



class NumpyTestProgram(nose.core.TestProgram):
    
    def runTests(self):
        """Run Tests. Returns true on success, false on failure, and
        sets self.success to the same value.

        Because nose currently discards the test result object, but we need
        to return it to the user, override TestProgram.runTests to retain
        the result
        """
        print('/home/jiangt/FaaSLight-Re/Original_app/app3-dynamic/numpy/testing/_private/noseclasses.py=NumpyTestProgram=runTests=347')
        if self.testRunner is None:
            self.testRunner = nose.core.TextTestRunner(stream=self.config.stream, verbosity=self.config.verbosity, config=self.config)
        plug_runner = self.config.plugins.prepareTestRunner(self.testRunner)
        if plug_runner is not None:
            self.testRunner = plug_runner
        self.result = self.testRunner.run(self.test)
        self.success = self.result.wasSuccessful()
        return self.success


