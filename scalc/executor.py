import typing as t

from scalc.expressions import Expression
from scalc.functions import SetCalcFunc


class Executor:

    def __init__(
        self,
        root_expression: Expression,
        functions_mapping: t.Mapping[str, SetCalcFunc],
    ):
        self._root_expression = root_expression
        self._functions_mapping = functions_mapping

    @property
    def root_expression(self) -> Expression:
        return self._root_expression

    @property
    def functions_mapping(self) -> t.Mapping[str, SetCalcFunc]:
        return self._functions_mapping

    def execute(self) -> t.AbstractSet[int]:
        return self.root_expression.evaluate()
