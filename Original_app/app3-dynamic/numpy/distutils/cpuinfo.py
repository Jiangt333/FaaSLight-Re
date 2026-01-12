"""
cpuinfo

Copyright 2002 Pearu Peterson all rights reserved,
Pearu Peterson <pearu@cens.ioc.ee>
Permission to use, modify, and distribute this software is given under the
terms of the NumPy (BSD style) license.  See LICENSE.txt that came with
this distribution for specifics.

NO WARRANTY IS EXPRESSED OR IMPLIED.  USE AT YOUR OWN RISK.
Pearu Peterson

"""

__all__ = ['cpu']
import os
import platform
import re
import sys
import types
import warnings
from subprocess import getstatusoutput

def getoutput(cmd, successful_status=(0, ), stacklevel=1):
    print('/home/jiangt/FaaSLight-Re/Original_app/app3-dynamic/numpy/distutils/cpuinfo.py=getoutput=27')
    try:
        (status, output) = getstatusoutput(cmd)
    except OSError as e:
        warnings.warn(str(e), UserWarning, stacklevel=stacklevel)
        return (False, '')
    if (os.WIFEXITED(status) and os.WEXITSTATUS(status) in successful_status):
        return (True, output)
    return (False, output)

def command_info(successful_status=(0, ), stacklevel=1, **kw):
    print('/home/jiangt/FaaSLight-Re/Original_app/app3-dynamic/numpy/distutils/cpuinfo.py=command_info=37')
    info = {}
    for key in kw:
        (ok, output) = getoutput(kw[key], successful_status=successful_status, stacklevel=stacklevel + 1)
        if ok:
            info[key] = output.strip()
    return info

def command_by_line(cmd, successful_status=(0, ), stacklevel=1):
    print('/home/jiangt/FaaSLight-Re/Original_app/app3-dynamic/numpy/distutils/cpuinfo.py=command_by_line=46')
    (ok, output) = getoutput(cmd, successful_status=successful_status, stacklevel=stacklevel + 1)
    if not ok:
        return
    for line in output.splitlines():
        yield line.strip()

def key_value_from_command(cmd, sep, successful_status=(0, ), stacklevel=1):
    print('/home/jiangt/FaaSLight-Re/Original_app/app3-dynamic/numpy/distutils/cpuinfo.py=key_value_from_command=54')
    d = {}
    for line in command_by_line(cmd, successful_status=successful_status, stacklevel=stacklevel + 1):
        l = [s.strip() for s in line.split(sep, 1)]
        if len(l) == 2:
            d[l[0]] = l[1]
    return d


class CPUInfoBase:
    """Holds CPU information and provides methods for requiring
    the availability of various CPU features.
    """
    
    def _try_call(self, func):
        print('/home/jiangt/FaaSLight-Re/Original_app/app3-dynamic/numpy/distutils/cpuinfo.py=CPUInfoBase=_try_call=69')
        try:
            return func()
        except Exception:
            pass
    
    def __getattr__(self, name):
        print('/home/jiangt/FaaSLight-Re/Original_app/app3-dynamic/numpy/distutils/cpuinfo.py=CPUInfoBase=__getattr__=75')
        if not name.startswith('_'):
            if hasattr(self, '_' + name):
                attr = getattr(self, '_' + name)
                if isinstance(attr, types.MethodType):
                    return lambda func=self._try_call, attr=attr: func(attr)
            else:
                return lambda: None
        raise AttributeError(name)
    
    def _getNCPUs(self):
        print('/home/jiangt/FaaSLight-Re/Original_app/app3-dynamic/numpy/distutils/cpuinfo.py=CPUInfoBase=_getNCPUs=85')
        return 1
    
    def __get_nbits(self):
        print('/home/jiangt/FaaSLight-Re/Original_app/app3-dynamic/numpy/distutils/cpuinfo.py=CPUInfoBase=__get_nbits=88')
        abits = platform.architecture()[0]
        nbits = re.compile('(\\d+)bit').search(abits).group(1)
        return nbits
    
    def _is_32bit(self):
        print('/home/jiangt/FaaSLight-Re/Original_app/app3-dynamic/numpy/distutils/cpuinfo.py=CPUInfoBase=_is_32bit=93')
        return self.__get_nbits() == '32'
    
    def _is_64bit(self):
        print('/home/jiangt/FaaSLight-Re/Original_app/app3-dynamic/numpy/distutils/cpuinfo.py=CPUInfoBase=_is_64bit=96')
        return self.__get_nbits() == '64'



class LinuxCPUInfo(CPUInfoBase):
    info = None
    
    def __init__(self):
        print('/home/jiangt/FaaSLight-Re/Original_app/app3-dynamic/numpy/distutils/cpuinfo.py=LinuxCPUInfo=__init__=103')
        if self.info is not None:
            return
        info = [{}]
        (ok, output) = getoutput('uname -m')
        if ok:
            info[0]['uname_m'] = output.strip()
        try:
            fo = open('/proc/cpuinfo')
        except OSError as e:
            warnings.warn(str(e), UserWarning, stacklevel=2)
        else:
            for line in fo:
                name_value = [s.strip() for s in line.split(':', 1)]
                if len(name_value) != 2:
                    continue
                (name, value) = name_value
                if (not info or name in info[-1]):
                    info.append({})
                info[-1][name] = value
            fo.close()
        self.__class__.info = info
    
    def _not_impl(self):
        print('/home/jiangt/FaaSLight-Re/Original_app/app3-dynamic/numpy/distutils/cpuinfo.py=LinuxCPUInfo=_not_impl=126')
        pass
    
    def _is_AMD(self):
        print('/home/jiangt/FaaSLight-Re/Original_app/app3-dynamic/numpy/distutils/cpuinfo.py=LinuxCPUInfo=_is_AMD=130')
        return self.info[0]['vendor_id'] == 'AuthenticAMD'
    
    def _is_AthlonK6_2(self):
        print('/home/jiangt/FaaSLight-Re/Original_app/app3-dynamic/numpy/distutils/cpuinfo.py=LinuxCPUInfo=_is_AthlonK6_2=133')
        return (self._is_AMD() and self.info[0]['model'] == '2')
    
    def _is_AthlonK6_3(self):
        print('/home/jiangt/FaaSLight-Re/Original_app/app3-dynamic/numpy/distutils/cpuinfo.py=LinuxCPUInfo=_is_AthlonK6_3=136')
        return (self._is_AMD() and self.info[0]['model'] == '3')
    
    def _is_AthlonK6(self):
        print('/home/jiangt/FaaSLight-Re/Original_app/app3-dynamic/numpy/distutils/cpuinfo.py=LinuxCPUInfo=_is_AthlonK6=139')
        return re.match('.*?AMD-K6', self.info[0]['model name']) is not None
    
    def _is_AthlonK7(self):
        print('/home/jiangt/FaaSLight-Re/Original_app/app3-dynamic/numpy/distutils/cpuinfo.py=LinuxCPUInfo=_is_AthlonK7=142')
        return re.match('.*?AMD-K7', self.info[0]['model name']) is not None
    
    def _is_AthlonMP(self):
        print('/home/jiangt/FaaSLight-Re/Original_app/app3-dynamic/numpy/distutils/cpuinfo.py=LinuxCPUInfo=_is_AthlonMP=145')
        return re.match('.*?Athlon\\(tm\\) MP\\b', self.info[0]['model name']) is not None
    
    def _is_AMD64(self):
        print('/home/jiangt/FaaSLight-Re/Original_app/app3-dynamic/numpy/distutils/cpuinfo.py=LinuxCPUInfo=_is_AMD64=149')
        return (self.is_AMD() and self.info[0]['family'] == '15')
    
    def _is_Athlon64(self):
        print('/home/jiangt/FaaSLight-Re/Original_app/app3-dynamic/numpy/distutils/cpuinfo.py=LinuxCPUInfo=_is_Athlon64=152')
        return re.match('.*?Athlon\\(tm\\) 64\\b', self.info[0]['model name']) is not None
    
    def _is_AthlonHX(self):
        print('/home/jiangt/FaaSLight-Re/Original_app/app3-dynamic/numpy/distutils/cpuinfo.py=LinuxCPUInfo=_is_AthlonHX=156')
        return re.match('.*?Athlon HX\\b', self.info[0]['model name']) is not None
    
    def _is_Opteron(self):
        print('/home/jiangt/FaaSLight-Re/Original_app/app3-dynamic/numpy/distutils/cpuinfo.py=LinuxCPUInfo=_is_Opteron=160')
        return re.match('.*?Opteron\\b', self.info[0]['model name']) is not None
    
    def _is_Hammer(self):
        print('/home/jiangt/FaaSLight-Re/Original_app/app3-dynamic/numpy/distutils/cpuinfo.py=LinuxCPUInfo=_is_Hammer=164')
        return re.match('.*?Hammer\\b', self.info[0]['model name']) is not None
    
    def _is_Alpha(self):
        print('/home/jiangt/FaaSLight-Re/Original_app/app3-dynamic/numpy/distutils/cpuinfo.py=LinuxCPUInfo=_is_Alpha=170')
        return self.info[0]['cpu'] == 'Alpha'
    
    def _is_EV4(self):
        print('/home/jiangt/FaaSLight-Re/Original_app/app3-dynamic/numpy/distutils/cpuinfo.py=LinuxCPUInfo=_is_EV4=173')
        return (self.is_Alpha() and self.info[0]['cpu model'] == 'EV4')
    
    def _is_EV5(self):
        print('/home/jiangt/FaaSLight-Re/Original_app/app3-dynamic/numpy/distutils/cpuinfo.py=LinuxCPUInfo=_is_EV5=176')
        return (self.is_Alpha() and self.info[0]['cpu model'] == 'EV5')
    
    def _is_EV56(self):
        print('/home/jiangt/FaaSLight-Re/Original_app/app3-dynamic/numpy/distutils/cpuinfo.py=LinuxCPUInfo=_is_EV56=179')
        return (self.is_Alpha() and self.info[0]['cpu model'] == 'EV56')
    
    def _is_PCA56(self):
        print('/home/jiangt/FaaSLight-Re/Original_app/app3-dynamic/numpy/distutils/cpuinfo.py=LinuxCPUInfo=_is_PCA56=182')
        return (self.is_Alpha() and self.info[0]['cpu model'] == 'PCA56')
    _is_i386 = _not_impl
    
    def _is_Intel(self):
        print('/home/jiangt/FaaSLight-Re/Original_app/app3-dynamic/numpy/distutils/cpuinfo.py=LinuxCPUInfo=_is_Intel=190')
        return self.info[0]['vendor_id'] == 'GenuineIntel'
    
    def _is_i486(self):
        print('/home/jiangt/FaaSLight-Re/Original_app/app3-dynamic/numpy/distutils/cpuinfo.py=LinuxCPUInfo=_is_i486=193')
        return self.info[0]['cpu'] == 'i486'
    
    def _is_i586(self):
        print('/home/jiangt/FaaSLight-Re/Original_app/app3-dynamic/numpy/distutils/cpuinfo.py=LinuxCPUInfo=_is_i586=196')
        return (self.is_Intel() and self.info[0]['cpu family'] == '5')
    
    def _is_i686(self):
        print('/home/jiangt/FaaSLight-Re/Original_app/app3-dynamic/numpy/distutils/cpuinfo.py=LinuxCPUInfo=_is_i686=199')
        return (self.is_Intel() and self.info[0]['cpu family'] == '6')
    
    def _is_Celeron(self):
        print('/home/jiangt/FaaSLight-Re/Original_app/app3-dynamic/numpy/distutils/cpuinfo.py=LinuxCPUInfo=_is_Celeron=202')
        return re.match('.*?Celeron', self.info[0]['model name']) is not None
    
    def _is_Pentium(self):
        print('/home/jiangt/FaaSLight-Re/Original_app/app3-dynamic/numpy/distutils/cpuinfo.py=LinuxCPUInfo=_is_Pentium=206')
        return re.match('.*?Pentium', self.info[0]['model name']) is not None
    
    def _is_PentiumII(self):
        print('/home/jiangt/FaaSLight-Re/Original_app/app3-dynamic/numpy/distutils/cpuinfo.py=LinuxCPUInfo=_is_PentiumII=210')
        return re.match('.*?Pentium.*?II\\b', self.info[0]['model name']) is not None
    
    def _is_PentiumPro(self):
        print('/home/jiangt/FaaSLight-Re/Original_app/app3-dynamic/numpy/distutils/cpuinfo.py=LinuxCPUInfo=_is_PentiumPro=214')
        return re.match('.*?PentiumPro\\b', self.info[0]['model name']) is not None
    
    def _is_PentiumMMX(self):
        print('/home/jiangt/FaaSLight-Re/Original_app/app3-dynamic/numpy/distutils/cpuinfo.py=LinuxCPUInfo=_is_PentiumMMX=218')
        return re.match('.*?Pentium.*?MMX\\b', self.info[0]['model name']) is not None
    
    def _is_PentiumIII(self):
        print('/home/jiangt/FaaSLight-Re/Original_app/app3-dynamic/numpy/distutils/cpuinfo.py=LinuxCPUInfo=_is_PentiumIII=222')
        return re.match('.*?Pentium.*?III\\b', self.info[0]['model name']) is not None
    
    def _is_PentiumIV(self):
        print('/home/jiangt/FaaSLight-Re/Original_app/app3-dynamic/numpy/distutils/cpuinfo.py=LinuxCPUInfo=_is_PentiumIV=226')
        return re.match('.*?Pentium.*?(IV|4)\\b', self.info[0]['model name']) is not None
    
    def _is_PentiumM(self):
        print('/home/jiangt/FaaSLight-Re/Original_app/app3-dynamic/numpy/distutils/cpuinfo.py=LinuxCPUInfo=_is_PentiumM=230')
        return re.match('.*?Pentium.*?M\\b', self.info[0]['model name']) is not None
    
    def _is_Prescott(self):
        print('/home/jiangt/FaaSLight-Re/Original_app/app3-dynamic/numpy/distutils/cpuinfo.py=LinuxCPUInfo=_is_Prescott=234')
        return (self.is_PentiumIV() and self.has_sse3())
    
    def _is_Nocona(self):
        print('/home/jiangt/FaaSLight-Re/Original_app/app3-dynamic/numpy/distutils/cpuinfo.py=LinuxCPUInfo=_is_Nocona=237')
        return (self.is_Intel() and ((self.info[0]['cpu family'] == '6' or self.info[0]['cpu family'] == '15')) and (self.has_sse3() and not self.has_ssse3()) and re.match('.*?\\blm\\b', self.info[0]['flags']) is not None)
    
    def _is_Core2(self):
        print('/home/jiangt/FaaSLight-Re/Original_app/app3-dynamic/numpy/distutils/cpuinfo.py=LinuxCPUInfo=_is_Core2=244')
        return (self.is_64bit() and self.is_Intel() and re.match('.*?Core\\(TM\\)2\\b', self.info[0]['model name']) is not None)
    
    def _is_Itanium(self):
        print('/home/jiangt/FaaSLight-Re/Original_app/app3-dynamic/numpy/distutils/cpuinfo.py=LinuxCPUInfo=_is_Itanium=249')
        return re.match('.*?Itanium\\b', self.info[0]['family']) is not None
    
    def _is_XEON(self):
        print('/home/jiangt/FaaSLight-Re/Original_app/app3-dynamic/numpy/distutils/cpuinfo.py=LinuxCPUInfo=_is_XEON=253')
        return re.match('.*?XEON\\b', self.info[0]['model name'], re.IGNORECASE) is not None
    _is_Xeon = _is_XEON
    
    def _is_singleCPU(self):
        print('/home/jiangt/FaaSLight-Re/Original_app/app3-dynamic/numpy/distutils/cpuinfo.py=LinuxCPUInfo=_is_singleCPU=261')
        return len(self.info) == 1
    
    def _getNCPUs(self):
        print('/home/jiangt/FaaSLight-Re/Original_app/app3-dynamic/numpy/distutils/cpuinfo.py=LinuxCPUInfo=_getNCPUs=264')
        return len(self.info)
    
    def _has_fdiv_bug(self):
        print('/home/jiangt/FaaSLight-Re/Original_app/app3-dynamic/numpy/distutils/cpuinfo.py=LinuxCPUInfo=_has_fdiv_bug=267')
        return self.info[0]['fdiv_bug'] == 'yes'
    
    def _has_f00f_bug(self):
        print('/home/jiangt/FaaSLight-Re/Original_app/app3-dynamic/numpy/distutils/cpuinfo.py=LinuxCPUInfo=_has_f00f_bug=270')
        return self.info[0]['f00f_bug'] == 'yes'
    
    def _has_mmx(self):
        print('/home/jiangt/FaaSLight-Re/Original_app/app3-dynamic/numpy/distutils/cpuinfo.py=LinuxCPUInfo=_has_mmx=273')
        return re.match('.*?\\bmmx\\b', self.info[0]['flags']) is not None
    
    def _has_sse(self):
        print('/home/jiangt/FaaSLight-Re/Original_app/app3-dynamic/numpy/distutils/cpuinfo.py=LinuxCPUInfo=_has_sse=276')
        return re.match('.*?\\bsse\\b', self.info[0]['flags']) is not None
    
    def _has_sse2(self):
        print('/home/jiangt/FaaSLight-Re/Original_app/app3-dynamic/numpy/distutils/cpuinfo.py=LinuxCPUInfo=_has_sse2=279')
        return re.match('.*?\\bsse2\\b', self.info[0]['flags']) is not None
    
    def _has_sse3(self):
        print('/home/jiangt/FaaSLight-Re/Original_app/app3-dynamic/numpy/distutils/cpuinfo.py=LinuxCPUInfo=_has_sse3=282')
        return re.match('.*?\\bpni\\b', self.info[0]['flags']) is not None
    
    def _has_ssse3(self):
        print('/home/jiangt/FaaSLight-Re/Original_app/app3-dynamic/numpy/distutils/cpuinfo.py=LinuxCPUInfo=_has_ssse3=285')
        return re.match('.*?\\bssse3\\b', self.info[0]['flags']) is not None
    
    def _has_3dnow(self):
        print('/home/jiangt/FaaSLight-Re/Original_app/app3-dynamic/numpy/distutils/cpuinfo.py=LinuxCPUInfo=_has_3dnow=288')
        return re.match('.*?\\b3dnow\\b', self.info[0]['flags']) is not None
    
    def _has_3dnowext(self):
        print('/home/jiangt/FaaSLight-Re/Original_app/app3-dynamic/numpy/distutils/cpuinfo.py=LinuxCPUInfo=_has_3dnowext=291')
        return re.match('.*?\\b3dnowext\\b', self.info[0]['flags']) is not None



class IRIXCPUInfo(CPUInfoBase):
    info = None
    
    def __init__(self):
        print('/home/jiangt/FaaSLight-Re/Original_app/app3-dynamic/numpy/distutils/cpuinfo.py=IRIXCPUInfo=__init__=297')
        if self.info is not None:
            return
        info = key_value_from_command('sysconf', sep=' ', successful_status=(0, 1))
        self.__class__.info = info
    
    def _not_impl(self):
        print('/home/jiangt/FaaSLight-Re/Original_app/app3-dynamic/numpy/distutils/cpuinfo.py=IRIXCPUInfo=_not_impl=304')
        pass
    
    def _is_singleCPU(self):
        print('/home/jiangt/FaaSLight-Re/Original_app/app3-dynamic/numpy/distutils/cpuinfo.py=IRIXCPUInfo=_is_singleCPU=306')
        return self.info.get('NUM_PROCESSORS') == '1'
    
    def _getNCPUs(self):
        print('/home/jiangt/FaaSLight-Re/Original_app/app3-dynamic/numpy/distutils/cpuinfo.py=IRIXCPUInfo=_getNCPUs=309')
        return int(self.info.get('NUM_PROCESSORS', 1))
    
    def __cputype(self, n):
        print('/home/jiangt/FaaSLight-Re/Original_app/app3-dynamic/numpy/distutils/cpuinfo.py=IRIXCPUInfo=__cputype=312')
        return self.info.get('PROCESSORS').split()[0].lower() == 'r%s' % n
    
    def _is_r2000(self):
        print('/home/jiangt/FaaSLight-Re/Original_app/app3-dynamic/numpy/distutils/cpuinfo.py=IRIXCPUInfo=_is_r2000=314')
        return self.__cputype(2000)
    
    def _is_r3000(self):
        print('/home/jiangt/FaaSLight-Re/Original_app/app3-dynamic/numpy/distutils/cpuinfo.py=IRIXCPUInfo=_is_r3000=315')
        return self.__cputype(3000)
    
    def _is_r3900(self):
        print('/home/jiangt/FaaSLight-Re/Original_app/app3-dynamic/numpy/distutils/cpuinfo.py=IRIXCPUInfo=_is_r3900=316')
        return self.__cputype(3900)
    
    def _is_r4000(self):
        print('/home/jiangt/FaaSLight-Re/Original_app/app3-dynamic/numpy/distutils/cpuinfo.py=IRIXCPUInfo=_is_r4000=317')
        return self.__cputype(4000)
    
    def _is_r4100(self):
        print('/home/jiangt/FaaSLight-Re/Original_app/app3-dynamic/numpy/distutils/cpuinfo.py=IRIXCPUInfo=_is_r4100=318')
        return self.__cputype(4100)
    
    def _is_r4300(self):
        print('/home/jiangt/FaaSLight-Re/Original_app/app3-dynamic/numpy/distutils/cpuinfo.py=IRIXCPUInfo=_is_r4300=319')
        return self.__cputype(4300)
    
    def _is_r4400(self):
        print('/home/jiangt/FaaSLight-Re/Original_app/app3-dynamic/numpy/distutils/cpuinfo.py=IRIXCPUInfo=_is_r4400=320')
        return self.__cputype(4400)
    
    def _is_r4600(self):
        print('/home/jiangt/FaaSLight-Re/Original_app/app3-dynamic/numpy/distutils/cpuinfo.py=IRIXCPUInfo=_is_r4600=321')
        return self.__cputype(4600)
    
    def _is_r4650(self):
        print('/home/jiangt/FaaSLight-Re/Original_app/app3-dynamic/numpy/distutils/cpuinfo.py=IRIXCPUInfo=_is_r4650=322')
        return self.__cputype(4650)
    
    def _is_r5000(self):
        print('/home/jiangt/FaaSLight-Re/Original_app/app3-dynamic/numpy/distutils/cpuinfo.py=IRIXCPUInfo=_is_r5000=323')
        return self.__cputype(5000)
    
    def _is_r6000(self):
        print('/home/jiangt/FaaSLight-Re/Original_app/app3-dynamic/numpy/distutils/cpuinfo.py=IRIXCPUInfo=_is_r6000=324')
        return self.__cputype(6000)
    
    def _is_r8000(self):
        print('/home/jiangt/FaaSLight-Re/Original_app/app3-dynamic/numpy/distutils/cpuinfo.py=IRIXCPUInfo=_is_r8000=325')
        return self.__cputype(8000)
    
    def _is_r10000(self):
        print('/home/jiangt/FaaSLight-Re/Original_app/app3-dynamic/numpy/distutils/cpuinfo.py=IRIXCPUInfo=_is_r10000=326')
        return self.__cputype(10000)
    
    def _is_r12000(self):
        print('/home/jiangt/FaaSLight-Re/Original_app/app3-dynamic/numpy/distutils/cpuinfo.py=IRIXCPUInfo=_is_r12000=327')
        return self.__cputype(12000)
    
    def _is_rorion(self):
        print('/home/jiangt/FaaSLight-Re/Original_app/app3-dynamic/numpy/distutils/cpuinfo.py=IRIXCPUInfo=_is_rorion=328')
        return self.__cputype('orion')
    
    def get_ip(self):
        print('/home/jiangt/FaaSLight-Re/Original_app/app3-dynamic/numpy/distutils/cpuinfo.py=IRIXCPUInfo=get_ip=330')
        try:
            return self.info.get('MACHINE')
        except Exception:
            pass
    
    def __machine(self, n):
        print('/home/jiangt/FaaSLight-Re/Original_app/app3-dynamic/numpy/distutils/cpuinfo.py=IRIXCPUInfo=__machine=333')
        return self.info.get('MACHINE').lower() == 'ip%s' % n
    
    def _is_IP19(self):
        print('/home/jiangt/FaaSLight-Re/Original_app/app3-dynamic/numpy/distutils/cpuinfo.py=IRIXCPUInfo=_is_IP19=335')
        return self.__machine(19)
    
    def _is_IP20(self):
        print('/home/jiangt/FaaSLight-Re/Original_app/app3-dynamic/numpy/distutils/cpuinfo.py=IRIXCPUInfo=_is_IP20=336')
        return self.__machine(20)
    
    def _is_IP21(self):
        print('/home/jiangt/FaaSLight-Re/Original_app/app3-dynamic/numpy/distutils/cpuinfo.py=IRIXCPUInfo=_is_IP21=337')
        return self.__machine(21)
    
    def _is_IP22(self):
        print('/home/jiangt/FaaSLight-Re/Original_app/app3-dynamic/numpy/distutils/cpuinfo.py=IRIXCPUInfo=_is_IP22=338')
        return self.__machine(22)
    
    def _is_IP22_4k(self):
        print('/home/jiangt/FaaSLight-Re/Original_app/app3-dynamic/numpy/distutils/cpuinfo.py=IRIXCPUInfo=_is_IP22_4k=339')
        return (self.__machine(22) and self._is_r4000())
    
    def _is_IP22_5k(self):
        print('/home/jiangt/FaaSLight-Re/Original_app/app3-dynamic/numpy/distutils/cpuinfo.py=IRIXCPUInfo=_is_IP22_5k=340')
        return (self.__machine(22) and self._is_r5000())
    
    def _is_IP24(self):
        print('/home/jiangt/FaaSLight-Re/Original_app/app3-dynamic/numpy/distutils/cpuinfo.py=IRIXCPUInfo=_is_IP24=341')
        return self.__machine(24)
    
    def _is_IP25(self):
        print('/home/jiangt/FaaSLight-Re/Original_app/app3-dynamic/numpy/distutils/cpuinfo.py=IRIXCPUInfo=_is_IP25=342')
        return self.__machine(25)
    
    def _is_IP26(self):
        print('/home/jiangt/FaaSLight-Re/Original_app/app3-dynamic/numpy/distutils/cpuinfo.py=IRIXCPUInfo=_is_IP26=343')
        return self.__machine(26)
    
    def _is_IP27(self):
        print('/home/jiangt/FaaSLight-Re/Original_app/app3-dynamic/numpy/distutils/cpuinfo.py=IRIXCPUInfo=_is_IP27=344')
        return self.__machine(27)
    
    def _is_IP28(self):
        print('/home/jiangt/FaaSLight-Re/Original_app/app3-dynamic/numpy/distutils/cpuinfo.py=IRIXCPUInfo=_is_IP28=345')
        return self.__machine(28)
    
    def _is_IP30(self):
        print('/home/jiangt/FaaSLight-Re/Original_app/app3-dynamic/numpy/distutils/cpuinfo.py=IRIXCPUInfo=_is_IP30=346')
        return self.__machine(30)
    
    def _is_IP32(self):
        print('/home/jiangt/FaaSLight-Re/Original_app/app3-dynamic/numpy/distutils/cpuinfo.py=IRIXCPUInfo=_is_IP32=347')
        return self.__machine(32)
    
    def _is_IP32_5k(self):
        print('/home/jiangt/FaaSLight-Re/Original_app/app3-dynamic/numpy/distutils/cpuinfo.py=IRIXCPUInfo=_is_IP32_5k=348')
        return (self.__machine(32) and self._is_r5000())
    
    def _is_IP32_10k(self):
        print('/home/jiangt/FaaSLight-Re/Original_app/app3-dynamic/numpy/distutils/cpuinfo.py=IRIXCPUInfo=_is_IP32_10k=349')
        return (self.__machine(32) and self._is_r10000())



class DarwinCPUInfo(CPUInfoBase):
    info = None
    
    def __init__(self):
        print('/home/jiangt/FaaSLight-Re/Original_app/app3-dynamic/numpy/distutils/cpuinfo.py=DarwinCPUInfo=__init__=355')
        if self.info is not None:
            return
        info = command_info(arch='arch', machine='machine')
        info['sysctl_hw'] = key_value_from_command('sysctl hw', sep='=')
        self.__class__.info = info
    
    def _not_impl(self):
        print('/home/jiangt/FaaSLight-Re/Original_app/app3-dynamic/numpy/distutils/cpuinfo.py=DarwinCPUInfo=_not_impl=363')
        pass
    
    def _getNCPUs(self):
        print('/home/jiangt/FaaSLight-Re/Original_app/app3-dynamic/numpy/distutils/cpuinfo.py=DarwinCPUInfo=_getNCPUs=365')
        return int(self.info['sysctl_hw'].get('hw.ncpu', 1))
    
    def _is_Power_Macintosh(self):
        print('/home/jiangt/FaaSLight-Re/Original_app/app3-dynamic/numpy/distutils/cpuinfo.py=DarwinCPUInfo=_is_Power_Macintosh=368')
        return self.info['sysctl_hw']['hw.machine'] == 'Power Macintosh'
    
    def _is_i386(self):
        print('/home/jiangt/FaaSLight-Re/Original_app/app3-dynamic/numpy/distutils/cpuinfo.py=DarwinCPUInfo=_is_i386=371')
        return self.info['arch'] == 'i386'
    
    def _is_ppc(self):
        print('/home/jiangt/FaaSLight-Re/Original_app/app3-dynamic/numpy/distutils/cpuinfo.py=DarwinCPUInfo=_is_ppc=373')
        return self.info['arch'] == 'ppc'
    
    def __machine(self, n):
        print('/home/jiangt/FaaSLight-Re/Original_app/app3-dynamic/numpy/distutils/cpuinfo.py=DarwinCPUInfo=__machine=376')
        return self.info['machine'] == 'ppc%s' % n
    
    def _is_ppc601(self):
        print('/home/jiangt/FaaSLight-Re/Original_app/app3-dynamic/numpy/distutils/cpuinfo.py=DarwinCPUInfo=_is_ppc601=378')
        return self.__machine(601)
    
    def _is_ppc602(self):
        print('/home/jiangt/FaaSLight-Re/Original_app/app3-dynamic/numpy/distutils/cpuinfo.py=DarwinCPUInfo=_is_ppc602=379')
        return self.__machine(602)
    
    def _is_ppc603(self):
        print('/home/jiangt/FaaSLight-Re/Original_app/app3-dynamic/numpy/distutils/cpuinfo.py=DarwinCPUInfo=_is_ppc603=380')
        return self.__machine(603)
    
    def _is_ppc603e(self):
        print('/home/jiangt/FaaSLight-Re/Original_app/app3-dynamic/numpy/distutils/cpuinfo.py=DarwinCPUInfo=_is_ppc603e=381')
        return self.__machine('603e')
    
    def _is_ppc604(self):
        print('/home/jiangt/FaaSLight-Re/Original_app/app3-dynamic/numpy/distutils/cpuinfo.py=DarwinCPUInfo=_is_ppc604=382')
        return self.__machine(604)
    
    def _is_ppc604e(self):
        print('/home/jiangt/FaaSLight-Re/Original_app/app3-dynamic/numpy/distutils/cpuinfo.py=DarwinCPUInfo=_is_ppc604e=383')
        return self.__machine('604e')
    
    def _is_ppc620(self):
        print('/home/jiangt/FaaSLight-Re/Original_app/app3-dynamic/numpy/distutils/cpuinfo.py=DarwinCPUInfo=_is_ppc620=384')
        return self.__machine(620)
    
    def _is_ppc630(self):
        print('/home/jiangt/FaaSLight-Re/Original_app/app3-dynamic/numpy/distutils/cpuinfo.py=DarwinCPUInfo=_is_ppc630=385')
        return self.__machine(630)
    
    def _is_ppc740(self):
        print('/home/jiangt/FaaSLight-Re/Original_app/app3-dynamic/numpy/distutils/cpuinfo.py=DarwinCPUInfo=_is_ppc740=386')
        return self.__machine(740)
    
    def _is_ppc7400(self):
        print('/home/jiangt/FaaSLight-Re/Original_app/app3-dynamic/numpy/distutils/cpuinfo.py=DarwinCPUInfo=_is_ppc7400=387')
        return self.__machine(7400)
    
    def _is_ppc7450(self):
        print('/home/jiangt/FaaSLight-Re/Original_app/app3-dynamic/numpy/distutils/cpuinfo.py=DarwinCPUInfo=_is_ppc7450=388')
        return self.__machine(7450)
    
    def _is_ppc750(self):
        print('/home/jiangt/FaaSLight-Re/Original_app/app3-dynamic/numpy/distutils/cpuinfo.py=DarwinCPUInfo=_is_ppc750=389')
        return self.__machine(750)
    
    def _is_ppc403(self):
        print('/home/jiangt/FaaSLight-Re/Original_app/app3-dynamic/numpy/distutils/cpuinfo.py=DarwinCPUInfo=_is_ppc403=390')
        return self.__machine(403)
    
    def _is_ppc505(self):
        print('/home/jiangt/FaaSLight-Re/Original_app/app3-dynamic/numpy/distutils/cpuinfo.py=DarwinCPUInfo=_is_ppc505=391')
        return self.__machine(505)
    
    def _is_ppc801(self):
        print('/home/jiangt/FaaSLight-Re/Original_app/app3-dynamic/numpy/distutils/cpuinfo.py=DarwinCPUInfo=_is_ppc801=392')
        return self.__machine(801)
    
    def _is_ppc821(self):
        print('/home/jiangt/FaaSLight-Re/Original_app/app3-dynamic/numpy/distutils/cpuinfo.py=DarwinCPUInfo=_is_ppc821=393')
        return self.__machine(821)
    
    def _is_ppc823(self):
        print('/home/jiangt/FaaSLight-Re/Original_app/app3-dynamic/numpy/distutils/cpuinfo.py=DarwinCPUInfo=_is_ppc823=394')
        return self.__machine(823)
    
    def _is_ppc860(self):
        print('/home/jiangt/FaaSLight-Re/Original_app/app3-dynamic/numpy/distutils/cpuinfo.py=DarwinCPUInfo=_is_ppc860=395')
        return self.__machine(860)



class SunOSCPUInfo(CPUInfoBase):
    info = None
    
    def __init__(self):
        print('/home/jiangt/FaaSLight-Re/Original_app/app3-dynamic/numpy/distutils/cpuinfo.py=SunOSCPUInfo=__init__=402')
        if self.info is not None:
            return
        info = command_info(arch='arch', mach='mach', uname_i='uname_i', isainfo_b='isainfo -b', isainfo_n='isainfo -n')
        info['uname_X'] = key_value_from_command('uname -X', sep='=')
        for line in command_by_line('psrinfo -v 0'):
            m = re.match('\\s*The (?P<p>[\\w\\d]+) processor operates at', line)
            if m:
                info['processor'] = m.group('p')
                break
        self.__class__.info = info
    
    def _not_impl(self):
        print('/home/jiangt/FaaSLight-Re/Original_app/app3-dynamic/numpy/distutils/cpuinfo.py=SunOSCPUInfo=_not_impl=419')
        pass
    
    def _is_i386(self):
        print('/home/jiangt/FaaSLight-Re/Original_app/app3-dynamic/numpy/distutils/cpuinfo.py=SunOSCPUInfo=_is_i386=421')
        return self.info['isainfo_n'] == 'i386'
    
    def _is_sparc(self):
        print('/home/jiangt/FaaSLight-Re/Original_app/app3-dynamic/numpy/distutils/cpuinfo.py=SunOSCPUInfo=_is_sparc=423')
        return self.info['isainfo_n'] == 'sparc'
    
    def _is_sparcv9(self):
        print('/home/jiangt/FaaSLight-Re/Original_app/app3-dynamic/numpy/distutils/cpuinfo.py=SunOSCPUInfo=_is_sparcv9=425')
        return self.info['isainfo_n'] == 'sparcv9'
    
    def _getNCPUs(self):
        print('/home/jiangt/FaaSLight-Re/Original_app/app3-dynamic/numpy/distutils/cpuinfo.py=SunOSCPUInfo=_getNCPUs=428')
        return int(self.info['uname_X'].get('NumCPU', 1))
    
    def _is_sun4(self):
        print('/home/jiangt/FaaSLight-Re/Original_app/app3-dynamic/numpy/distutils/cpuinfo.py=SunOSCPUInfo=_is_sun4=431')
        return self.info['arch'] == 'sun4'
    
    def _is_SUNW(self):
        print('/home/jiangt/FaaSLight-Re/Original_app/app3-dynamic/numpy/distutils/cpuinfo.py=SunOSCPUInfo=_is_SUNW=434')
        return re.match('SUNW', self.info['uname_i']) is not None
    
    def _is_sparcstation5(self):
        print('/home/jiangt/FaaSLight-Re/Original_app/app3-dynamic/numpy/distutils/cpuinfo.py=SunOSCPUInfo=_is_sparcstation5=436')
        return re.match('.*SPARCstation-5', self.info['uname_i']) is not None
    
    def _is_ultra1(self):
        print('/home/jiangt/FaaSLight-Re/Original_app/app3-dynamic/numpy/distutils/cpuinfo.py=SunOSCPUInfo=_is_ultra1=438')
        return re.match('.*Ultra-1', self.info['uname_i']) is not None
    
    def _is_ultra250(self):
        print('/home/jiangt/FaaSLight-Re/Original_app/app3-dynamic/numpy/distutils/cpuinfo.py=SunOSCPUInfo=_is_ultra250=440')
        return re.match('.*Ultra-250', self.info['uname_i']) is not None
    
    def _is_ultra2(self):
        print('/home/jiangt/FaaSLight-Re/Original_app/app3-dynamic/numpy/distutils/cpuinfo.py=SunOSCPUInfo=_is_ultra2=442')
        return re.match('.*Ultra-2', self.info['uname_i']) is not None
    
    def _is_ultra30(self):
        print('/home/jiangt/FaaSLight-Re/Original_app/app3-dynamic/numpy/distutils/cpuinfo.py=SunOSCPUInfo=_is_ultra30=444')
        return re.match('.*Ultra-30', self.info['uname_i']) is not None
    
    def _is_ultra4(self):
        print('/home/jiangt/FaaSLight-Re/Original_app/app3-dynamic/numpy/distutils/cpuinfo.py=SunOSCPUInfo=_is_ultra4=446')
        return re.match('.*Ultra-4', self.info['uname_i']) is not None
    
    def _is_ultra5_10(self):
        print('/home/jiangt/FaaSLight-Re/Original_app/app3-dynamic/numpy/distutils/cpuinfo.py=SunOSCPUInfo=_is_ultra5_10=448')
        return re.match('.*Ultra-5_10', self.info['uname_i']) is not None
    
    def _is_ultra5(self):
        print('/home/jiangt/FaaSLight-Re/Original_app/app3-dynamic/numpy/distutils/cpuinfo.py=SunOSCPUInfo=_is_ultra5=450')
        return re.match('.*Ultra-5', self.info['uname_i']) is not None
    
    def _is_ultra60(self):
        print('/home/jiangt/FaaSLight-Re/Original_app/app3-dynamic/numpy/distutils/cpuinfo.py=SunOSCPUInfo=_is_ultra60=452')
        return re.match('.*Ultra-60', self.info['uname_i']) is not None
    
    def _is_ultra80(self):
        print('/home/jiangt/FaaSLight-Re/Original_app/app3-dynamic/numpy/distutils/cpuinfo.py=SunOSCPUInfo=_is_ultra80=454')
        return re.match('.*Ultra-80', self.info['uname_i']) is not None
    
    def _is_ultraenterprice(self):
        print('/home/jiangt/FaaSLight-Re/Original_app/app3-dynamic/numpy/distutils/cpuinfo.py=SunOSCPUInfo=_is_ultraenterprice=456')
        return re.match('.*Ultra-Enterprise', self.info['uname_i']) is not None
    
    def _is_ultraenterprice10k(self):
        print('/home/jiangt/FaaSLight-Re/Original_app/app3-dynamic/numpy/distutils/cpuinfo.py=SunOSCPUInfo=_is_ultraenterprice10k=458')
        return re.match('.*Ultra-Enterprise-10000', self.info['uname_i']) is not None
    
    def _is_sunfire(self):
        print('/home/jiangt/FaaSLight-Re/Original_app/app3-dynamic/numpy/distutils/cpuinfo.py=SunOSCPUInfo=_is_sunfire=460')
        return re.match('.*Sun-Fire', self.info['uname_i']) is not None
    
    def _is_ultra(self):
        print('/home/jiangt/FaaSLight-Re/Original_app/app3-dynamic/numpy/distutils/cpuinfo.py=SunOSCPUInfo=_is_ultra=462')
        return re.match('.*Ultra', self.info['uname_i']) is not None
    
    def _is_cpusparcv7(self):
        print('/home/jiangt/FaaSLight-Re/Original_app/app3-dynamic/numpy/distutils/cpuinfo.py=SunOSCPUInfo=_is_cpusparcv7=465')
        return self.info['processor'] == 'sparcv7'
    
    def _is_cpusparcv8(self):
        print('/home/jiangt/FaaSLight-Re/Original_app/app3-dynamic/numpy/distutils/cpuinfo.py=SunOSCPUInfo=_is_cpusparcv8=467')
        return self.info['processor'] == 'sparcv8'
    
    def _is_cpusparcv9(self):
        print('/home/jiangt/FaaSLight-Re/Original_app/app3-dynamic/numpy/distutils/cpuinfo.py=SunOSCPUInfo=_is_cpusparcv9=469')
        return self.info['processor'] == 'sparcv9'



class Win32CPUInfo(CPUInfoBase):
    info = None
    pkey = 'HARDWARE\\DESCRIPTION\\System\\CentralProcessor'
    
    def __init__(self):
        print('/home/jiangt/FaaSLight-Re/Original_app/app3-dynamic/numpy/distutils/cpuinfo.py=Win32CPUInfo=__init__=480')
        if self.info is not None:
            return
        info = []
        try:
            import winreg
            prgx = re.compile('family\\s+(?P<FML>\\d+)\\s+model\\s+(?P<MDL>\\d+)\\s+stepping\\s+(?P<STP>\\d+)', re.IGNORECASE)
            chnd = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, self.pkey)
            pnum = 0
            while True:
                try:
                    proc = winreg.EnumKey(chnd, pnum)
                except winreg.error:
                    break
                else:
                    pnum += 1
                    info.append({'Processor': proc})
                    phnd = winreg.OpenKey(chnd, proc)
                    pidx = 0
                    while True:
                        try:
                            (name, value, vtpe) = winreg.EnumValue(phnd, pidx)
                        except winreg.error:
                            break
                        else:
                            pidx = pidx + 1
                            info[-1][name] = value
                            if name == 'Identifier':
                                srch = prgx.search(value)
                                if srch:
                                    info[-1]['Family'] = int(srch.group('FML'))
                                    info[-1]['Model'] = int(srch.group('MDL'))
                                    info[-1]['Stepping'] = int(srch.group('STP'))
        except Exception as e:
            print(e, '(ignoring)')
        self.__class__.info = info
    
    def _not_impl(self):
        print('/home/jiangt/FaaSLight-Re/Original_app/app3-dynamic/numpy/distutils/cpuinfo.py=Win32CPUInfo=_not_impl=520')
        pass
    
    def _is_AMD(self):
        print('/home/jiangt/FaaSLight-Re/Original_app/app3-dynamic/numpy/distutils/cpuinfo.py=Win32CPUInfo=_is_AMD=524')
        return self.info[0]['VendorIdentifier'] == 'AuthenticAMD'
    
    def _is_Am486(self):
        print('/home/jiangt/FaaSLight-Re/Original_app/app3-dynamic/numpy/distutils/cpuinfo.py=Win32CPUInfo=_is_Am486=527')
        return (self.is_AMD() and self.info[0]['Family'] == 4)
    
    def _is_Am5x86(self):
        print('/home/jiangt/FaaSLight-Re/Original_app/app3-dynamic/numpy/distutils/cpuinfo.py=Win32CPUInfo=_is_Am5x86=530')
        return (self.is_AMD() and self.info[0]['Family'] == 4)
    
    def _is_AMDK5(self):
        print('/home/jiangt/FaaSLight-Re/Original_app/app3-dynamic/numpy/distutils/cpuinfo.py=Win32CPUInfo=_is_AMDK5=533')
        return (self.is_AMD() and self.info[0]['Family'] == 5 and self.info[0]['Model'] in [0, 1, 2, 3])
    
    def _is_AMDK6(self):
        print('/home/jiangt/FaaSLight-Re/Original_app/app3-dynamic/numpy/distutils/cpuinfo.py=Win32CPUInfo=_is_AMDK6=537')
        return (self.is_AMD() and self.info[0]['Family'] == 5 and self.info[0]['Model'] in [6, 7])
    
    def _is_AMDK6_2(self):
        print('/home/jiangt/FaaSLight-Re/Original_app/app3-dynamic/numpy/distutils/cpuinfo.py=Win32CPUInfo=_is_AMDK6_2=541')
        return (self.is_AMD() and self.info[0]['Family'] == 5 and self.info[0]['Model'] == 8)
    
    def _is_AMDK6_3(self):
        print('/home/jiangt/FaaSLight-Re/Original_app/app3-dynamic/numpy/distutils/cpuinfo.py=Win32CPUInfo=_is_AMDK6_3=545')
        return (self.is_AMD() and self.info[0]['Family'] == 5 and self.info[0]['Model'] == 9)
    
    def _is_AMDK7(self):
        print('/home/jiangt/FaaSLight-Re/Original_app/app3-dynamic/numpy/distutils/cpuinfo.py=Win32CPUInfo=_is_AMDK7=549')
        return (self.is_AMD() and self.info[0]['Family'] == 6)
    
    def _is_AMD64(self):
        print('/home/jiangt/FaaSLight-Re/Original_app/app3-dynamic/numpy/distutils/cpuinfo.py=Win32CPUInfo=_is_AMD64=556')
        return (self.is_AMD() and self.info[0]['Family'] == 15)
    
    def _is_Intel(self):
        print('/home/jiangt/FaaSLight-Re/Original_app/app3-dynamic/numpy/distutils/cpuinfo.py=Win32CPUInfo=_is_Intel=561')
        return self.info[0]['VendorIdentifier'] == 'GenuineIntel'
    
    def _is_i386(self):
        print('/home/jiangt/FaaSLight-Re/Original_app/app3-dynamic/numpy/distutils/cpuinfo.py=Win32CPUInfo=_is_i386=564')
        return self.info[0]['Family'] == 3
    
    def _is_i486(self):
        print('/home/jiangt/FaaSLight-Re/Original_app/app3-dynamic/numpy/distutils/cpuinfo.py=Win32CPUInfo=_is_i486=567')
        return self.info[0]['Family'] == 4
    
    def _is_i586(self):
        print('/home/jiangt/FaaSLight-Re/Original_app/app3-dynamic/numpy/distutils/cpuinfo.py=Win32CPUInfo=_is_i586=570')
        return (self.is_Intel() and self.info[0]['Family'] == 5)
    
    def _is_i686(self):
        print('/home/jiangt/FaaSLight-Re/Original_app/app3-dynamic/numpy/distutils/cpuinfo.py=Win32CPUInfo=_is_i686=573')
        return (self.is_Intel() and self.info[0]['Family'] == 6)
    
    def _is_Pentium(self):
        print('/home/jiangt/FaaSLight-Re/Original_app/app3-dynamic/numpy/distutils/cpuinfo.py=Win32CPUInfo=_is_Pentium=576')
        return (self.is_Intel() and self.info[0]['Family'] == 5)
    
    def _is_PentiumMMX(self):
        print('/home/jiangt/FaaSLight-Re/Original_app/app3-dynamic/numpy/distutils/cpuinfo.py=Win32CPUInfo=_is_PentiumMMX=579')
        return (self.is_Intel() and self.info[0]['Family'] == 5 and self.info[0]['Model'] == 4)
    
    def _is_PentiumPro(self):
        print('/home/jiangt/FaaSLight-Re/Original_app/app3-dynamic/numpy/distutils/cpuinfo.py=Win32CPUInfo=_is_PentiumPro=583')
        return (self.is_Intel() and self.info[0]['Family'] == 6 and self.info[0]['Model'] == 1)
    
    def _is_PentiumII(self):
        print('/home/jiangt/FaaSLight-Re/Original_app/app3-dynamic/numpy/distutils/cpuinfo.py=Win32CPUInfo=_is_PentiumII=587')
        return (self.is_Intel() and self.info[0]['Family'] == 6 and self.info[0]['Model'] in [3, 5, 6])
    
    def _is_PentiumIII(self):
        print('/home/jiangt/FaaSLight-Re/Original_app/app3-dynamic/numpy/distutils/cpuinfo.py=Win32CPUInfo=_is_PentiumIII=591')
        return (self.is_Intel() and self.info[0]['Family'] == 6 and self.info[0]['Model'] in [7, 8, 9, 10, 11])
    
    def _is_PentiumIV(self):
        print('/home/jiangt/FaaSLight-Re/Original_app/app3-dynamic/numpy/distutils/cpuinfo.py=Win32CPUInfo=_is_PentiumIV=595')
        return (self.is_Intel() and self.info[0]['Family'] == 15)
    
    def _is_PentiumM(self):
        print('/home/jiangt/FaaSLight-Re/Original_app/app3-dynamic/numpy/distutils/cpuinfo.py=Win32CPUInfo=_is_PentiumM=598')
        return (self.is_Intel() and self.info[0]['Family'] == 6 and self.info[0]['Model'] in [9, 13, 14])
    
    def _is_Core2(self):
        print('/home/jiangt/FaaSLight-Re/Original_app/app3-dynamic/numpy/distutils/cpuinfo.py=Win32CPUInfo=_is_Core2=602')
        return (self.is_Intel() and self.info[0]['Family'] == 6 and self.info[0]['Model'] in [15, 16, 17])
    
    def _is_singleCPU(self):
        print('/home/jiangt/FaaSLight-Re/Original_app/app3-dynamic/numpy/distutils/cpuinfo.py=Win32CPUInfo=_is_singleCPU=608')
        return len(self.info) == 1
    
    def _getNCPUs(self):
        print('/home/jiangt/FaaSLight-Re/Original_app/app3-dynamic/numpy/distutils/cpuinfo.py=Win32CPUInfo=_getNCPUs=611')
        return len(self.info)
    
    def _has_mmx(self):
        print('/home/jiangt/FaaSLight-Re/Original_app/app3-dynamic/numpy/distutils/cpuinfo.py=Win32CPUInfo=_has_mmx=614')
        if self.is_Intel():
            return ((self.info[0]['Family'] == 5 and self.info[0]['Model'] == 4) or self.info[0]['Family'] in [6, 15])
        elif self.is_AMD():
            return self.info[0]['Family'] in [5, 6, 15]
        else:
            return False
    
    def _has_sse(self):
        print('/home/jiangt/FaaSLight-Re/Original_app/app3-dynamic/numpy/distutils/cpuinfo.py=Win32CPUInfo=_has_sse=623')
        if self.is_Intel():
            return ((self.info[0]['Family'] == 6 and self.info[0]['Model'] in [7, 8, 9, 10, 11]) or self.info[0]['Family'] == 15)
        elif self.is_AMD():
            return ((self.info[0]['Family'] == 6 and self.info[0]['Model'] in [6, 7, 8, 10]) or self.info[0]['Family'] == 15)
        else:
            return False
    
    def _has_sse2(self):
        print('/home/jiangt/FaaSLight-Re/Original_app/app3-dynamic/numpy/distutils/cpuinfo.py=Win32CPUInfo=_has_sse2=635')
        if self.is_Intel():
            return (self.is_Pentium4() or self.is_PentiumM() or self.is_Core2())
        elif self.is_AMD():
            return self.is_AMD64()
        else:
            return False
    
    def _has_3dnow(self):
        print('/home/jiangt/FaaSLight-Re/Original_app/app3-dynamic/numpy/distutils/cpuinfo.py=Win32CPUInfo=_has_3dnow=644')
        return (self.is_AMD() and self.info[0]['Family'] in [5, 6, 15])
    
    def _has_3dnowext(self):
        print('/home/jiangt/FaaSLight-Re/Original_app/app3-dynamic/numpy/distutils/cpuinfo.py=Win32CPUInfo=_has_3dnowext=647')
        return (self.is_AMD() and self.info[0]['Family'] in [6, 15])

if sys.platform.startswith('linux'):
    cpuinfo = LinuxCPUInfo
elif sys.platform.startswith('irix'):
    cpuinfo = IRIXCPUInfo
elif sys.platform == 'darwin':
    cpuinfo = DarwinCPUInfo
elif sys.platform.startswith('sunos'):
    cpuinfo = SunOSCPUInfo
elif sys.platform.startswith('win32'):
    cpuinfo = Win32CPUInfo
elif sys.platform.startswith('cygwin'):
    cpuinfo = LinuxCPUInfo
else:
    cpuinfo = CPUInfoBase
cpu = cpuinfo()

