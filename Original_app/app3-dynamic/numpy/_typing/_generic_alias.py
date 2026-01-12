from __future__ import annotations
import sys
import types
from collections.abc import Generator, Iterable, Iterator
from typing import Any, ClassVar, NoReturn, TypeVar, TYPE_CHECKING
import numpy as np
__all__ = ['_GenericAlias', 'NDArray']
_T = TypeVar('_T', bound='_GenericAlias')

def _to_str(obj: object) -> str:
    """Helper function for `_GenericAlias.__repr__`."""
    print('/home/jiangt/FaaSLight-Re/Original_app/app3-dynamic/numpy/_typing/_generic_alias.py=_to_str=21')
    if obj is Ellipsis:
        return '...'
    elif (isinstance(obj, type) and not isinstance(obj, _GENERIC_ALIAS_TYPE)):
        if obj.__module__ == 'builtins':
            return obj.__qualname__
        else:
            return f'{obj.__module__}.{obj.__qualname__}'
    else:
        return repr(obj)

def _parse_parameters(args: Iterable[Any]) -> Generator[(TypeVar, None, None)]:
    """Search for all typevars and typevar-containing objects in `args`.

    Helper function for `_GenericAlias.__init__`.

    """
    print('/home/jiangt/FaaSLight-Re/Original_app/app3-dynamic/numpy/_typing/_generic_alias.py=_parse_parameters=34')
    for i in args:
        if hasattr(i, '__parameters__'):
            yield from i.__parameters__
        elif isinstance(i, TypeVar):
            yield i

def _reconstruct_alias(alias: _T, parameters: Iterator[TypeVar]) -> _T:
    """Recursively replace all typevars with those from `parameters`.

    Helper function for `_GenericAlias.__getitem__`.

    """
    print('/home/jiangt/FaaSLight-Re/Original_app/app3-dynamic/numpy/_typing/_generic_alias.py=_reconstruct_alias=47')
    args = []
    for i in alias.__args__:
        if isinstance(i, TypeVar):
            value: Any = next(parameters)
        elif isinstance(i, _GenericAlias):
            value = _reconstruct_alias(i, parameters)
        elif hasattr(i, '__parameters__'):
            prm_tup = tuple((next(parameters) for _ in i.__parameters__))
            value = i[prm_tup]
        else:
            value = i
        args.append(value)
    cls = type(alias)
    return cls(alias.__origin__, tuple(args), alias.__unpacked__)


class _GenericAlias:
    """A python-based backport of the `types.GenericAlias` class.

    E.g. for ``t = list[int]``, ``t.__origin__`` is ``list`` and
    ``t.__args__`` is ``(int,)``.

    See Also
    --------
    :pep:`585`
        The PEP responsible for introducing `types.GenericAlias`.

    """
    __slots__ = ('__weakref__', '_origin', '_args', '_parameters', '_hash', '_starred')
    
    @property
    def __origin__(self) -> type:
        print('/home/jiangt/FaaSLight-Re/Original_app/app3-dynamic/numpy/_typing/_generic_alias.py=_GenericAlias=__origin__=92')
        return super().__getattribute__('_origin')
    
    @property
    def __args__(self) -> tuple[(object, ...)]:
        print('/home/jiangt/FaaSLight-Re/Original_app/app3-dynamic/numpy/_typing/_generic_alias.py=_GenericAlias=__args__=96')
        return super().__getattribute__('_args')
    
    @property
    def __parameters__(self) -> tuple[(TypeVar, ...)]:
        """Type variables in the ``GenericAlias``."""
        print('/home/jiangt/FaaSLight-Re/Original_app/app3-dynamic/numpy/_typing/_generic_alias.py=_GenericAlias=__parameters__=100')
        return super().__getattribute__('_parameters')
    
    @property
    def __unpacked__(self) -> bool:
        print('/home/jiangt/FaaSLight-Re/Original_app/app3-dynamic/numpy/_typing/_generic_alias.py=_GenericAlias=__unpacked__=105')
        return super().__getattribute__('_starred')
    
    @property
    def __typing_unpacked_tuple_args__(self) -> tuple[(object, ...)] | None:
        print('/home/jiangt/FaaSLight-Re/Original_app/app3-dynamic/numpy/_typing/_generic_alias.py=_GenericAlias=__typing_unpacked_tuple_args__=109')
        return None
    
    def __init__(self, origin: type, args: object | tuple[(object, ...)], starred: bool = False) -> None:
        print('/home/jiangt/FaaSLight-Re/Original_app/app3-dynamic/numpy/_typing/_generic_alias.py=_GenericAlias=__init__=116')
        self._origin = origin
        self._args = (args if isinstance(args, tuple) else (args, ))
        self._parameters = tuple(_parse_parameters(self.__args__))
        self._starred = starred
    
    @property
    def __call__(self) -> type[Any]:
        print('/home/jiangt/FaaSLight-Re/Original_app/app3-dynamic/numpy/_typing/_generic_alias.py=_GenericAlias=__call__=127')
        return self.__origin__
    
    def __reduce__(self: _T) -> tuple[(type[_T], tuple[(type[Any], tuple[(object, ...)], bool)])]:
        print('/home/jiangt/FaaSLight-Re/Original_app/app3-dynamic/numpy/_typing/_generic_alias.py=_GenericAlias=__reduce__=131')
        cls = type(self)
        return (cls, (self.__origin__, self.__args__, self.__unpacked__))
    
    def __mro_entries__(self, bases: Iterable[object]) -> tuple[type[Any]]:
        print('/home/jiangt/FaaSLight-Re/Original_app/app3-dynamic/numpy/_typing/_generic_alias.py=_GenericAlias=__mro_entries__=138')
        return (self.__origin__, )
    
    def __dir__(self) -> list[str]:
        """Implement ``dir(self)``."""
        print('/home/jiangt/FaaSLight-Re/Original_app/app3-dynamic/numpy/_typing/_generic_alias.py=_GenericAlias=__dir__=141')
        cls = type(self)
        dir_origin = set(dir(self.__origin__))
        return sorted(cls._ATTR_EXCEPTIONS | dir_origin)
    
    def __hash__(self) -> int:
        """Return ``hash(self)``."""
        print('/home/jiangt/FaaSLight-Re/Original_app/app3-dynamic/numpy/_typing/_generic_alias.py=_GenericAlias=__hash__=147')
        try:
            return super().__getattribute__('_hash')
        except AttributeError:
            self._hash: int = hash(self.__origin__) ^ hash(self.__args__) ^ hash(self.__unpacked__)
            return super().__getattribute__('_hash')
    
    def __instancecheck__(self, obj: object) -> NoReturn:
        """Check if an `obj` is an instance."""
        print('/home/jiangt/FaaSLight-Re/Original_app/app3-dynamic/numpy/_typing/_generic_alias.py=_GenericAlias=__instancecheck__=160')
        raise TypeError('isinstance() argument 2 cannot be a parameterized generic')
    
    def __subclasscheck__(self, cls: type) -> NoReturn:
        """Check if a `cls` is a subclass."""
        print('/home/jiangt/FaaSLight-Re/Original_app/app3-dynamic/numpy/_typing/_generic_alias.py=_GenericAlias=__subclasscheck__=165')
        raise TypeError('issubclass() argument 2 cannot be a parameterized generic')
    
    def __repr__(self) -> str:
        """Return ``repr(self)``."""
        print('/home/jiangt/FaaSLight-Re/Original_app/app3-dynamic/numpy/_typing/_generic_alias.py=_GenericAlias=__repr__=170')
        args = ', '.join((_to_str(i) for i in self.__args__))
        origin = _to_str(self.__origin__)
        prefix = ('*' if self.__unpacked__ else '')
        return f'{prefix}{origin}[{args}]'
    
    def __getitem__(self: _T, key: object | tuple[(object, ...)]) -> _T:
        """Return ``self[key]``."""
        print('/home/jiangt/FaaSLight-Re/Original_app/app3-dynamic/numpy/_typing/_generic_alias.py=_GenericAlias=__getitem__=177')
        key_tup = (key if isinstance(key, tuple) else (key, ))
        if len(self.__parameters__) == 0:
            raise TypeError(f'There are no type variables left in {self}')
        elif len(key_tup) > len(self.__parameters__):
            raise TypeError(f'Too many arguments for {self}')
        elif len(key_tup) < len(self.__parameters__):
            raise TypeError(f'Too few arguments for {self}')
        key_iter = iter(key_tup)
        return _reconstruct_alias(self, key_iter)
    
    def __eq__(self, value: object) -> bool:
        """Return ``self == value``."""
        print('/home/jiangt/FaaSLight-Re/Original_app/app3-dynamic/numpy/_typing/_generic_alias.py=_GenericAlias=__eq__=191')
        if not isinstance(value, _GENERIC_ALIAS_TYPE):
            return NotImplemented
        return (self.__origin__ == value.__origin__ and self.__args__ == value.__args__ and self.__unpacked__ == getattr(value, '__unpacked__', self.__unpacked__))
    
    def __iter__(self: _T) -> Generator[(_T, None, None)]:
        """Return ``iter(self)``."""
        print('/home/jiangt/FaaSLight-Re/Original_app/app3-dynamic/numpy/_typing/_generic_alias.py=_GenericAlias=__iter__=203')
        cls = type(self)
        yield cls(self.__origin__, self.__args__, True)
    _ATTR_EXCEPTIONS: ClassVar[frozenset[str]] = frozenset({'__origin__', '__args__', '__parameters__', '__mro_entries__', '__reduce__', '__reduce_ex__', '__copy__', '__deepcopy__', '__unpacked__', '__typing_unpacked_tuple_args__', '__class__'})
    
    def __getattribute__(self, name: str) -> Any:
        """Return ``getattr(self, name)``."""
        print('/home/jiangt/FaaSLight-Re/Original_app/app3-dynamic/numpy/_typing/_generic_alias.py=_GenericAlias=__getattribute__=222')
        cls = type(self)
        if name in cls._ATTR_EXCEPTIONS:
            return super().__getattribute__(name)
        return getattr(self.__origin__, name)

if sys.version_info >= (3, 9):
    _GENERIC_ALIAS_TYPE = (_GenericAlias, types.GenericAlias)
else:
    _GENERIC_ALIAS_TYPE = (_GenericAlias, )
ScalarType = TypeVar('ScalarType', bound=np.generic, covariant=True)
if (TYPE_CHECKING or sys.version_info >= (3, 9)):
    _DType = np.dtype[ScalarType]
    NDArray = np.ndarray[(Any, np.dtype[ScalarType])]
else:
    _DType = _GenericAlias(np.dtype, (ScalarType, ))
    NDArray = _GenericAlias(np.ndarray, (Any, _DType))

