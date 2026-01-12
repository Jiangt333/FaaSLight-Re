"""Utility to compare pep440 compatible version strings.

The LooseVersion and StrictVersion classes that distutils provides don't
work; they don't recognize anything like alpha/beta/rc/dev versions.
"""

import collections
import itertools
import re
__all__ = ['parse', 'Version', 'LegacyVersion', 'InvalidVersion', 'VERSION_PATTERN']


class Infinity:
    
    def __repr__(self):
        print('/home/jiangt/FaaSLight-Re/Original_app/app3-dynamic/numpy/compat/_pep440.py=Infinity=__repr__=46')
        return 'Infinity'
    
    def __hash__(self):
        print('/home/jiangt/FaaSLight-Re/Original_app/app3-dynamic/numpy/compat/_pep440.py=Infinity=__hash__=49')
        return hash(repr(self))
    
    def __lt__(self, other):
        print('/home/jiangt/FaaSLight-Re/Original_app/app3-dynamic/numpy/compat/_pep440.py=Infinity=__lt__=52')
        return False
    
    def __le__(self, other):
        print('/home/jiangt/FaaSLight-Re/Original_app/app3-dynamic/numpy/compat/_pep440.py=Infinity=__le__=55')
        return False
    
    def __eq__(self, other):
        print('/home/jiangt/FaaSLight-Re/Original_app/app3-dynamic/numpy/compat/_pep440.py=Infinity=__eq__=58')
        return isinstance(other, self.__class__)
    
    def __ne__(self, other):
        print('/home/jiangt/FaaSLight-Re/Original_app/app3-dynamic/numpy/compat/_pep440.py=Infinity=__ne__=61')
        return not isinstance(other, self.__class__)
    
    def __gt__(self, other):
        print('/home/jiangt/FaaSLight-Re/Original_app/app3-dynamic/numpy/compat/_pep440.py=Infinity=__gt__=64')
        return True
    
    def __ge__(self, other):
        print('/home/jiangt/FaaSLight-Re/Original_app/app3-dynamic/numpy/compat/_pep440.py=Infinity=__ge__=67')
        return True
    
    def __neg__(self):
        print('/home/jiangt/FaaSLight-Re/Original_app/app3-dynamic/numpy/compat/_pep440.py=Infinity=__neg__=70')
        return NegativeInfinity

Infinity = Infinity()


class NegativeInfinity:
    
    def __repr__(self):
        print('/home/jiangt/FaaSLight-Re/Original_app/app3-dynamic/numpy/compat/_pep440.py=NegativeInfinity=__repr__=78')
        return '-Infinity'
    
    def __hash__(self):
        print('/home/jiangt/FaaSLight-Re/Original_app/app3-dynamic/numpy/compat/_pep440.py=NegativeInfinity=__hash__=81')
        return hash(repr(self))
    
    def __lt__(self, other):
        print('/home/jiangt/FaaSLight-Re/Original_app/app3-dynamic/numpy/compat/_pep440.py=NegativeInfinity=__lt__=84')
        return True
    
    def __le__(self, other):
        print('/home/jiangt/FaaSLight-Re/Original_app/app3-dynamic/numpy/compat/_pep440.py=NegativeInfinity=__le__=87')
        return True
    
    def __eq__(self, other):
        print('/home/jiangt/FaaSLight-Re/Original_app/app3-dynamic/numpy/compat/_pep440.py=NegativeInfinity=__eq__=90')
        return isinstance(other, self.__class__)
    
    def __ne__(self, other):
        print('/home/jiangt/FaaSLight-Re/Original_app/app3-dynamic/numpy/compat/_pep440.py=NegativeInfinity=__ne__=93')
        return not isinstance(other, self.__class__)
    
    def __gt__(self, other):
        print('/home/jiangt/FaaSLight-Re/Original_app/app3-dynamic/numpy/compat/_pep440.py=NegativeInfinity=__gt__=96')
        return False
    
    def __ge__(self, other):
        print('/home/jiangt/FaaSLight-Re/Original_app/app3-dynamic/numpy/compat/_pep440.py=NegativeInfinity=__ge__=99')
        return False
    
    def __neg__(self):
        print('/home/jiangt/FaaSLight-Re/Original_app/app3-dynamic/numpy/compat/_pep440.py=NegativeInfinity=__neg__=102')
        return Infinity

NegativeInfinity = NegativeInfinity()
_Version = collections.namedtuple('_Version', ['epoch', 'release', 'dev', 'pre', 'post', 'local'])

def parse(version):
    """
    Parse the given version string and return either a :class:`Version` object
    or a :class:`LegacyVersion` object depending on if the given version is
    a valid PEP 440 version or a legacy version.
    """
    print('/home/jiangt/FaaSLight-Re/Original_app/app3-dynamic/numpy/compat/_pep440.py=parse=117')
    try:
        return Version(version)
    except InvalidVersion:
        return LegacyVersion(version)


class InvalidVersion(ValueError):
    """
    An invalid version was found, users should refer to PEP 440.
    """
    



class _BaseVersion:
    
    def __hash__(self):
        print('/home/jiangt/FaaSLight-Re/Original_app/app3-dynamic/numpy/compat/_pep440.py=_BaseVersion=__hash__=137')
        return hash(self._key)
    
    def __lt__(self, other):
        print('/home/jiangt/FaaSLight-Re/Original_app/app3-dynamic/numpy/compat/_pep440.py=_BaseVersion=__lt__=140')
        return self._compare(other, lambda s, o: s < o)
    
    def __le__(self, other):
        print('/home/jiangt/FaaSLight-Re/Original_app/app3-dynamic/numpy/compat/_pep440.py=_BaseVersion=__le__=143')
        return self._compare(other, lambda s, o: s <= o)
    
    def __eq__(self, other):
        print('/home/jiangt/FaaSLight-Re/Original_app/app3-dynamic/numpy/compat/_pep440.py=_BaseVersion=__eq__=146')
        return self._compare(other, lambda s, o: s == o)
    
    def __ge__(self, other):
        print('/home/jiangt/FaaSLight-Re/Original_app/app3-dynamic/numpy/compat/_pep440.py=_BaseVersion=__ge__=149')
        return self._compare(other, lambda s, o: s >= o)
    
    def __gt__(self, other):
        print('/home/jiangt/FaaSLight-Re/Original_app/app3-dynamic/numpy/compat/_pep440.py=_BaseVersion=__gt__=152')
        return self._compare(other, lambda s, o: s > o)
    
    def __ne__(self, other):
        print('/home/jiangt/FaaSLight-Re/Original_app/app3-dynamic/numpy/compat/_pep440.py=_BaseVersion=__ne__=155')
        return self._compare(other, lambda s, o: s != o)
    
    def _compare(self, other, method):
        print('/home/jiangt/FaaSLight-Re/Original_app/app3-dynamic/numpy/compat/_pep440.py=_BaseVersion=_compare=158')
        if not isinstance(other, _BaseVersion):
            return NotImplemented
        return method(self._key, other._key)



class LegacyVersion(_BaseVersion):
    
    def __init__(self, version):
        print('/home/jiangt/FaaSLight-Re/Original_app/app3-dynamic/numpy/compat/_pep440.py=LegacyVersion=__init__=167')
        self._version = str(version)
        self._key = _legacy_cmpkey(self._version)
    
    def __str__(self):
        print('/home/jiangt/FaaSLight-Re/Original_app/app3-dynamic/numpy/compat/_pep440.py=LegacyVersion=__str__=171')
        return self._version
    
    def __repr__(self):
        print('/home/jiangt/FaaSLight-Re/Original_app/app3-dynamic/numpy/compat/_pep440.py=LegacyVersion=__repr__=174')
        return '<LegacyVersion({0})>'.format(repr(str(self)))
    
    @property
    def public(self):
        print('/home/jiangt/FaaSLight-Re/Original_app/app3-dynamic/numpy/compat/_pep440.py=LegacyVersion=public=177')
        return self._version
    
    @property
    def base_version(self):
        print('/home/jiangt/FaaSLight-Re/Original_app/app3-dynamic/numpy/compat/_pep440.py=LegacyVersion=base_version=181')
        return self._version
    
    @property
    def local(self):
        print('/home/jiangt/FaaSLight-Re/Original_app/app3-dynamic/numpy/compat/_pep440.py=LegacyVersion=local=185')
        return None
    
    @property
    def is_prerelease(self):
        print('/home/jiangt/FaaSLight-Re/Original_app/app3-dynamic/numpy/compat/_pep440.py=LegacyVersion=is_prerelease=189')
        return False
    
    @property
    def is_postrelease(self):
        print('/home/jiangt/FaaSLight-Re/Original_app/app3-dynamic/numpy/compat/_pep440.py=LegacyVersion=is_postrelease=193')
        return False

_legacy_version_component_re = re.compile('(\\d+ | [a-z]+ | \\.| -)', re.VERBOSE)
_legacy_version_replacement_map = {'pre': 'c', 'preview': 'c', '-': 'final-', 'rc': 'c', 'dev': '@'}

def _parse_version_parts(s):
    print('/home/jiangt/FaaSLight-Re/Original_app/app3-dynamic/numpy/compat/_pep440.py=_parse_version_parts=207')
    for part in _legacy_version_component_re.split(s):
        part = _legacy_version_replacement_map.get(part, part)
        if (not part or part == '.'):
            continue
        if part[:1] in '0123456789':
            yield part.zfill(8)
        else:
            yield '*' + part
    yield '*final'

def _legacy_cmpkey(version):
    print('/home/jiangt/FaaSLight-Re/Original_app/app3-dynamic/numpy/compat/_pep440.py=_legacy_cmpkey=224')
    epoch = -1
    parts = []
    for part in _parse_version_parts(version.lower()):
        if part.startswith('*'):
            if part < '*final':
                while (parts and parts[-1] == '*final-'):
                    parts.pop()
            while (parts and parts[-1] == '00000000'):
                parts.pop()
        parts.append(part)
    parts = tuple(parts)
    return (epoch, parts)
VERSION_PATTERN = '\n    v?\n    (?:\n        (?:(?P<epoch>[0-9]+)!)?                           # epoch\n        (?P<release>[0-9]+(?:\\.[0-9]+)*)                  # release segment\n        (?P<pre>                                          # pre-release\n            [-_\\.]?\n            (?P<pre_l>(a|b|c|rc|alpha|beta|pre|preview))\n            [-_\\.]?\n            (?P<pre_n>[0-9]+)?\n        )?\n        (?P<post>                                         # post release\n            (?:-(?P<post_n1>[0-9]+))\n            |\n            (?:\n                [-_\\.]?\n                (?P<post_l>post|rev|r)\n                [-_\\.]?\n                (?P<post_n2>[0-9]+)?\n            )\n        )?\n        (?P<dev>                                          # dev release\n            [-_\\.]?\n            (?P<dev_l>dev)\n            [-_\\.]?\n            (?P<dev_n>[0-9]+)?\n        )?\n    )\n    (?:\\+(?P<local>[a-z0-9]+(?:[-_\\.][a-z0-9]+)*))?       # local version\n'


class Version(_BaseVersion):
    _regex = re.compile('^\\s*' + VERSION_PATTERN + '\\s*$', re.VERBOSE | re.IGNORECASE)
    
    def __init__(self, version):
        print('/home/jiangt/FaaSLight-Re/Original_app/app3-dynamic/numpy/compat/_pep440.py=Version=__init__=292')
        match = self._regex.search(version)
        if not match:
            raise InvalidVersion("Invalid version: '{0}'".format(version))
        self._version = _Version(epoch=(int(match.group('epoch')) if match.group('epoch') else 0), release=tuple((int(i) for i in match.group('release').split('.'))), pre=_parse_letter_version(match.group('pre_l'), match.group('pre_n')), post=_parse_letter_version(match.group('post_l'), (match.group('post_n1') or match.group('post_n2'))), dev=_parse_letter_version(match.group('dev_l'), match.group('dev_n')), local=_parse_local_version(match.group('local')))
        self._key = _cmpkey(self._version.epoch, self._version.release, self._version.pre, self._version.post, self._version.dev, self._version.local)
    
    def __repr__(self):
        print('/home/jiangt/FaaSLight-Re/Original_app/app3-dynamic/numpy/compat/_pep440.py=Version=__repr__=327')
        return '<Version({0})>'.format(repr(str(self)))
    
    def __str__(self):
        print('/home/jiangt/FaaSLight-Re/Original_app/app3-dynamic/numpy/compat/_pep440.py=Version=__str__=330')
        parts = []
        if self._version.epoch != 0:
            parts.append('{0}!'.format(self._version.epoch))
        parts.append('.'.join((str(x) for x in self._version.release)))
        if self._version.pre is not None:
            parts.append(''.join((str(x) for x in self._version.pre)))
        if self._version.post is not None:
            parts.append('.post{0}'.format(self._version.post[1]))
        if self._version.dev is not None:
            parts.append('.dev{0}'.format(self._version.dev[1]))
        if self._version.local is not None:
            parts.append('+{0}'.format('.'.join((str(x) for x in self._version.local))))
        return ''.join(parts)
    
    @property
    def public(self):
        print('/home/jiangt/FaaSLight-Re/Original_app/app3-dynamic/numpy/compat/_pep440.py=Version=public=360')
        return str(self).split('+', 1)[0]
    
    @property
    def base_version(self):
        print('/home/jiangt/FaaSLight-Re/Original_app/app3-dynamic/numpy/compat/_pep440.py=Version=base_version=364')
        parts = []
        if self._version.epoch != 0:
            parts.append('{0}!'.format(self._version.epoch))
        parts.append('.'.join((str(x) for x in self._version.release)))
        return ''.join(parts)
    
    @property
    def local(self):
        print('/home/jiangt/FaaSLight-Re/Original_app/app3-dynamic/numpy/compat/_pep440.py=Version=local=377')
        version_string = str(self)
        if '+' in version_string:
            return version_string.split('+', 1)[1]
    
    @property
    def is_prerelease(self):
        print('/home/jiangt/FaaSLight-Re/Original_app/app3-dynamic/numpy/compat/_pep440.py=Version=is_prerelease=383')
        return bool((self._version.dev or self._version.pre))
    
    @property
    def is_postrelease(self):
        print('/home/jiangt/FaaSLight-Re/Original_app/app3-dynamic/numpy/compat/_pep440.py=Version=is_postrelease=387')
        return bool(self._version.post)


def _parse_letter_version(letter, number):
    print('/home/jiangt/FaaSLight-Re/Original_app/app3-dynamic/numpy/compat/_pep440.py=_parse_letter_version=392')
    if letter:
        if number is None:
            number = 0
        letter = letter.lower()
        if letter == 'alpha':
            letter = 'a'
        elif letter == 'beta':
            letter = 'b'
        elif letter in ['c', 'pre', 'preview']:
            letter = 'rc'
        elif letter in ['rev', 'r']:
            letter = 'post'
        return (letter, int(number))
    if (not letter and number):
        letter = 'post'
        return (letter, int(number))
_local_version_seperators = re.compile('[\\._-]')

def _parse_local_version(local):
    """
    Takes a string like abc.1.twelve and turns it into ("abc", 1, "twelve").
    """
    print('/home/jiangt/FaaSLight-Re/Original_app/app3-dynamic/numpy/compat/_pep440.py=_parse_local_version=426')
    if local is not None:
        return tuple(((part.lower() if not part.isdigit() else int(part)) for part in _local_version_seperators.split(local)))

def _cmpkey(epoch, release, pre, post, dev, local):
    print('/home/jiangt/FaaSLight-Re/Original_app/app3-dynamic/numpy/compat/_pep440.py=_cmpkey=437')
    release = tuple(reversed(list(itertools.dropwhile(lambda x: x == 0, reversed(release)))))
    if (pre is None and post is None and dev is not None):
        pre = -Infinity
    elif pre is None:
        pre = Infinity
    if post is None:
        post = -Infinity
    if dev is None:
        dev = Infinity
    if local is None:
        local = -Infinity
    else:
        local = tuple((((i, '') if isinstance(i, int) else (-Infinity, i)) for i in local))
    return (epoch, release, pre, post, dev, local)

