import typing as t

import pytest

from scalc.functions import (
    SetCalcFunc,
    SumFunc,
    IntFunc,
    DifFunc,
)


@pytest.mark.parametrize(
    ("func", "args", "expected_result"),
    (
        (SumFunc(), [{1, 2}, {2, 3}, {3, 4}], {1, 2, 3, 4}),
        (SumFunc(), [{1, 2}], {1, 2}),
        (SumFunc(), [{1, 2}, set()], {1, 2}),

        (IntFunc(), [{1, 2}, {2, 3}, {3, 4}], set()),
        (IntFunc(), [{1, 2, 3}, {2, 3}, {3, 4, 5}], {3}),
        (IntFunc(), [{1, 2}, set()], set()),
        (IntFunc(), [{1, 2}], {1, 2}),

        (DifFunc(), [{0, 1, 2, 3}, {2, 3}, {3, 4}], {0, 1}),
        (DifFunc(), [{1, 2, 3}, {1, 2}, {2, 3}], set()),
        (DifFunc(), [{1, 2}, set()], {1, 2}),
        (DifFunc(), [{1, 2}], {1, 2}),

    ),
)
def test_set_calc_func_should_return_valid_result(
    func: SetCalcFunc,
    args: t.Sequence[t.AbstractSet[int]],
    expected_result: t.AbstractSet[int],
):
    assert func.call(args=args) == expected_result


