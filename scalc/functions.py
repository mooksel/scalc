import typing as t
import functools
import abc

from scalc.exceptions import RuntimeException


class SetCalcFunc(abc.ABC):

    @abc.abstractmethod
    def call(self, args: t.Sequence[t.AbstractSet[int]]) -> t.AbstractSet[int]:
        pass


class SumFunc(SetCalcFunc):

    def call(self, args: t.Sequence[t.AbstractSet[int]]) -> t.AbstractSet[int]:
        return functools.reduce(lambda s1, s2: s1 | s2, args)


class IntFunc(SetCalcFunc):

    def call(self, args: t.Sequence[t.AbstractSet[int]]) -> t.AbstractSet[int]:
        return functools.reduce(lambda s1, s2: s1 & s2, args)


class DifFunc(SetCalcFunc):

    def call(self, args: t.Sequence[t.AbstractSet[int]]) -> t.AbstractSet[int]:
        return functools.reduce(lambda s1, s2: s1 - s2, args)


def load_functions() -> t.Mapping[str, SetCalcFunc]:
    return {
        "SUM": SumFunc(),
        "INT": IntFunc(),
        "DIF": DifFunc(),
    }


__all__ = (
    load_functions.__name__,
    SetCalcFunc.__name__,
    SumFunc.__name__,
    IntFunc.__name__,
    DifFunc.__name__,
)
