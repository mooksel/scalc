import typing as t

import pytest

from scalc.executor import Executor
from scalc.functions import load_functions
from scalc.expressions import FunctionCallExpression, LoadFromFileExpression, Expression


_FUNCTIONS_MAPPING = load_functions()


_PATH_TO_RESOURCES = "tests/resources"

_PATH_TO_VALID_FILES = f"{_PATH_TO_RESOURCES}/valid"
_PATH_TO_VALID_FILE_A = f"{_PATH_TO_VALID_FILES}/a.txt"
_PATH_TO_VALID_FILE_B = f"{_PATH_TO_VALID_FILES}/b.txt"
_PATH_TO_VALID_FILE_C = f"{_PATH_TO_VALID_FILES}/c.txt"
_PATH_TO_VALID_EMPTY_FILE = f"{_PATH_TO_VALID_FILES}/empty.txt"

_PATH_TO_INVALID_FILES = f"{_PATH_TO_RESOURCES}/invalid"
_PATH_TO_INVALID_FILE_A = f"{_PATH_TO_INVALID_FILES}/a.txt"

_PATH_TO_UNEXISTENT_FILE = f"{_PATH_TO_RESOURCES}/unexistent"


@pytest.mark.parametrize(
    ("root_expression", "expected_result"),
    (
        (
            FunctionCallExpression(
                func=_FUNCTIONS_MAPPING["SUM"],
                func_args=(
                    LoadFromFileExpression(file_name=_PATH_TO_VALID_FILE_A),
                    LoadFromFileExpression(file_name=_PATH_TO_VALID_FILE_B),
                )
            ),
            {1, 3, 4},
        ),
        (
            FunctionCallExpression(
                func=_FUNCTIONS_MAPPING["SUM"],
                func_args=(
                    FunctionCallExpression(
                        func=_FUNCTIONS_MAPPING["DIF"],
                        func_args=(
                            LoadFromFileExpression(file_name=_PATH_TO_VALID_FILE_A),
                            LoadFromFileExpression(file_name=_PATH_TO_VALID_FILE_B),
                            LoadFromFileExpression(file_name=_PATH_TO_VALID_FILE_C),
                        )
                    ),
                    FunctionCallExpression(
                        func=_FUNCTIONS_MAPPING["INT"],
                        func_args=(
                            LoadFromFileExpression(file_name=_PATH_TO_VALID_FILE_B),
                            LoadFromFileExpression(file_name=_PATH_TO_VALID_FILE_C),
                        )
                    ),
                )
            ),
            {1, 3, 4},
        ),
        (
            FunctionCallExpression(
                func=_FUNCTIONS_MAPPING["SUM"],
                func_args=(
                    LoadFromFileExpression(file_name=_PATH_TO_VALID_FILE_A),
                    LoadFromFileExpression(file_name=_PATH_TO_VALID_EMPTY_FILE),
                )
            ),
            {1, 2, 3},
        ),
        (
            FunctionCallExpression(
                func=_FUNCTIONS_MAPPING["INT"],
                func_args=(
                    LoadFromFileExpression(file_name=_PATH_TO_VALID_FILE_B),
                    LoadFromFileExpression(file_name=_PATH_TO_VALID_EMPTY_FILE),
                )
            ),
            set(),
        ),
        (
            FunctionCallExpression(
                func=_FUNCTIONS_MAPPING["DIF"],
                func_args=(
                    LoadFromFileExpression(file_name=_PATH_TO_VALID_FILE_C),
                    LoadFromFileExpression(file_name=_PATH_TO_VALID_EMPTY_FILE),
                )
            ),
            {3, 4, 5},
        ),
    ),
)
def test_execute_should_return_valid_result(
    root_expression: Expression,
    expected_result: t.AbstractSet[int],
):
    executor = Executor(
        root_expression=root_expression,
        functions_mapping=_FUNCTIONS_MAPPING,
    )

    execute_result = executor.execute()
    assert execute_result == execute_result
