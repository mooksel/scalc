import abc
import typing as t

from scalc.exceptions import RuntimeException
from scalc.functions import SetCalcFunc


class Expression(abc.ABC):
    """
        Expression - AST Node type which can be evaluated to `collections.abc.Set` type.
    """

    @abc.abstractmethod
    def evaluate(self) -> t.AbstractSet[int]:
        pass


class LoadFromFileExpression(Expression):

    def __init__(self, file_name: str):
        self._file_name = file_name

    def __eq__(self, obj) -> bool:
        if type(self) != type(obj):
            return False
        return self.file_name == obj.file_name

    @property
    def file_name(self) -> str:
        return self._file_name

    def _parse_set_or_raise(self, lines: t.Iterable[str]) -> t.AbstractSet[int]:
        result_set = set()
        for line_number, line in enumerate(lines):
            try:
                result_set.add(int(line))
            except ValueError:
                raise RuntimeException(
                    reason= (
                        f"Invalid integer: '{line}' "
                        " in file: '{self.file_name}' at line: {line_number}."
                    ),
                )

        return result_set


    def evaluate(self) -> t.AbstractSet[int]:
        try:
            with open(self.file_name, "r") as f:
                return self._parse_set_or_raise(f.readlines())
        except FileNotFoundError:
            raise RuntimeException(
                reason=f"File: '{self.file_name}' not found.",
            )


class FunctionCallExpression(Expression):

    def __init__(self, func: SetCalcFunc, func_args: t.Sequence[Expression]):
        self._func = func
        self._func_args = tuple(func_args)

    def __eq__(self, obj) -> bool:
        if type(self) != type(obj):
            return False

        if self.func != obj.func:
            return False

        return self.func_args == obj.func_args

    @property
    def func(self) -> SetCalcFunc:
        return self._func

    @property
    def func_args(self) -> t.Sequence[Expression]:
        return self._func_args

    def evaluate(self) -> t.AbstractSet[int]:
        evaluated_args = [arg.evaluate() for arg in self.func_args]
        return self.func.call(args=evaluated_args)
