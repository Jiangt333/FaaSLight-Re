"""This module implements additional tests ala autoconf which can be useful.

"""

import textwrap

def check_inline(cmd):
    """Return the inline identifier (may be empty)."""
    print('/home/jiangt/FaaSLight-Re/Original_app/app3-dynamic/numpy/distutils/command/autodist.py=check_inline=8')
    cmd._check_compiler()
    body = textwrap.dedent('\n        #ifndef __cplusplus\n        static %(inline)s int static_func (void)\n        {\n            return 0;\n        }\n        %(inline)s int nostatic_func (void)\n        {\n            return 0;\n        }\n        #endif')
    for kw in ['inline', '__inline__', '__inline']:
        st = cmd.try_compile(body % {'inline': kw}, None, None)
        if st:
            return kw
    return ''

def check_restrict(cmd):
    """Return the restrict identifier (may be empty)."""
    print('/home/jiangt/FaaSLight-Re/Original_app/app3-dynamic/numpy/distutils/command/autodist.py=check_restrict=31')
    cmd._check_compiler()
    body = textwrap.dedent('\n        static int static_func (char * %(restrict)s a)\n        {\n            return 0;\n        }\n        ')
    for kw in ['restrict', '__restrict__', '__restrict']:
        st = cmd.try_compile(body % {'restrict': kw}, None, None)
        if st:
            return kw
    return ''

def check_compiler_gcc(cmd):
    """Check if the compiler is GCC."""
    print('/home/jiangt/FaaSLight-Re/Original_app/app3-dynamic/numpy/distutils/command/autodist.py=check_compiler_gcc=49')
    cmd._check_compiler()
    body = textwrap.dedent('\n        int\n        main()\n        {\n        #if (! defined __GNUC__)\n        #error gcc required\n        #endif\n            return 0;\n        }\n        ')
    return cmd.try_compile(body, None, None)

def check_gcc_version_at_least(cmd, major, minor=0, patchlevel=0):
    """
    Check that the gcc version is at least the specified version."""
    print('/home/jiangt/FaaSLight-Re/Original_app/app3-dynamic/numpy/distutils/command/autodist.py=check_gcc_version_at_least=66')
    cmd._check_compiler()
    version = '.'.join([str(major), str(minor), str(patchlevel)])
    body = textwrap.dedent('\n        int\n        main()\n        {\n        #if (! defined __GNUC__) || (__GNUC__ < %(major)d) || \\\n                (__GNUC_MINOR__ < %(minor)d) || \\\n                (__GNUC_PATCHLEVEL__ < %(patchlevel)d)\n        #error gcc >= %(version)s required\n        #endif\n            return 0;\n        }\n        ')
    kw = {'version': version, 'major': major, 'minor': minor, 'patchlevel': patchlevel}
    return cmd.try_compile(body % kw, None, None)

def check_gcc_function_attribute(cmd, attribute, name):
    """Return True if the given function attribute is supported."""
    print('/home/jiangt/FaaSLight-Re/Original_app/app3-dynamic/numpy/distutils/command/autodist.py=check_gcc_function_attribute=90')
    cmd._check_compiler()
    body = textwrap.dedent('\n        #pragma GCC diagnostic error "-Wattributes"\n        #pragma clang diagnostic error "-Wattributes"\n\n        int %s %s(void* unused)\n        {\n            return 0;\n        }\n\n        int\n        main()\n        {\n            return 0;\n        }\n        ') % (attribute, name)
    return cmd.try_compile(body, None, None) != 0

def check_gcc_function_attribute_with_intrinsics(cmd, attribute, name, code, include):
    """Return True if the given function attribute is supported with
    intrinsics."""
    print('/home/jiangt/FaaSLight-Re/Original_app/app3-dynamic/numpy/distutils/command/autodist.py=check_gcc_function_attribute_with_intrinsics=111')
    cmd._check_compiler()
    body = textwrap.dedent('\n        #include<%s>\n        int %s %s(void)\n        {\n            %s;\n            return 0;\n        }\n\n        int\n        main()\n        {\n            return 0;\n        }\n        ') % (include, attribute, name, code)
    return cmd.try_compile(body, None, None) != 0

def check_gcc_variable_attribute(cmd, attribute):
    """Return True if the given variable attribute is supported."""
    print('/home/jiangt/FaaSLight-Re/Original_app/app3-dynamic/numpy/distutils/command/autodist.py=check_gcc_variable_attribute=133')
    cmd._check_compiler()
    body = textwrap.dedent('\n        #pragma GCC diagnostic error "-Wattributes"\n        #pragma clang diagnostic error "-Wattributes"\n\n        int %s foo;\n\n        int\n        main()\n        {\n            return 0;\n        }\n        ') % (attribute, )
    return cmd.try_compile(body, None, None) != 0

