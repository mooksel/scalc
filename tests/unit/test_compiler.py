import typing as t

import pytest

from scalc.tokens import Token, TokenType
from scalc.functions import SetCalcFunc
from scalc.compiler import Compiler
from scalc.expressions import Expression, FunctionCallExpression, LoadFromFileExpression
from scalc.exceptions import CompileException
from scalc.functions import load_functions


_FUNCTIONS_MAPPING = load_functions()


@pytest.mark.parametrize(
    ("valid_tokens", "expected_expression"),
    (
        (
            (
                Token(token_type=TokenType.FUNC_CALL_START, token_value="["),
                Token(token_type=TokenType.FUNC_NAME, token_value="SUM"),
                Token(token_type=TokenType.FILE_NAME, token_value="a.txt"),
                Token(token_type=TokenType.FILE_NAME, token_value="b.txt"),
                Token(token_type=TokenType.FUNC_CALL_END, token_value="]"),
            ),
            FunctionCallExpression(
                func=_FUNCTIONS_MAPPING["SUM"],
                func_args=(
                    LoadFromFileExpression(file_name="a.txt"),
                    LoadFromFileExpression(file_name="b.txt"),
                )
            ),
        ),
        (
            (
                Token(token_type=TokenType.FUNC_CALL_START, token_value="["),
                Token(token_type=TokenType.FUNC_NAME, token_value="SUM"),
                Token(token_type=TokenType.FUNC_CALL_START, token_value="["),
                Token(token_type=TokenType.FUNC_NAME, token_value="DIF"),
                Token(token_type=TokenType.FILE_NAME, token_value="a.txt"),
                Token(token_type=TokenType.FILE_NAME, token_value="b.txt"),
                Token(token_type=TokenType.FILE_NAME, token_value="c.txt"),
                Token(token_type=TokenType.FUNC_CALL_END, token_value="]"),
                Token(token_type=TokenType.FUNC_CALL_START, token_value="["),
                Token(token_type=TokenType.FUNC_NAME, token_value="INT"),
                Token(token_type=TokenType.FILE_NAME, token_value="b.txt"),
                Token(token_type=TokenType.FILE_NAME, token_value="c.txt"),
                Token(token_type=TokenType.FUNC_CALL_END, token_value="]"),
                Token(token_type=TokenType.FUNC_CALL_END, token_value="]"),
            ),
            FunctionCallExpression(
                func=_FUNCTIONS_MAPPING["SUM"],
                func_args=(
                    FunctionCallExpression(
                        func=_FUNCTIONS_MAPPING["DIF"],
                        func_args=(
                            LoadFromFileExpression(file_name="a.txt"),
                            LoadFromFileExpression(file_name="b.txt"),
                            LoadFromFileExpression(file_name="c.txt"),
                        )
                    ),
                    FunctionCallExpression(
                        func=_FUNCTIONS_MAPPING["INT"],
                        func_args=(
                            LoadFromFileExpression(file_name="b.txt"),
                            LoadFromFileExpression(file_name="c.txt"),
                        )
                    ),
                )
            ),
        ),
        (
            (
                Token(token_type=TokenType.FILE_NAME, token_value="a.txt"),
            ),
            LoadFromFileExpression(file_name="a.txt"),
        ),
    ),
)
def test_compile_with_valid_tokens_should_return_valid_compiled_expressions(
    valid_tokens: t.Sequence[Token],
    expected_expression: Expression,
):
    compiler = Compiler(
        tokens=valid_tokens,
        functions_mapping=_FUNCTIONS_MAPPING,
    )

    compiled_expression = compiler.compile()
    assert compiled_expression == expected_expression


@pytest.mark.parametrize(
    "invalid_tokens",
    (
        (
            Token(token_type=TokenType.FUNC_CALL_START, token_value="["),
            Token(token_type=TokenType.FUNC_NAME, token_value="SUM"),
            Token(token_type=TokenType.FILE_NAME, token_value="a.txt"),
            Token(token_type=TokenType.FILE_NAME, token_value="b.txt"),
        ),
        (
            Token(token_type=TokenType.FUNC_CALL_START, token_value="["),
            Token(token_type=TokenType.FUNC_NAME, token_value="UNDEFINED_FUNCTION"),
            Token(token_type=TokenType.FILE_NAME, token_value="a.txt"),
            Token(token_type=TokenType.FILE_NAME, token_value="b.txt"),
            Token(token_type=TokenType.FUNC_CALL_END, token_value="]"),
        ),
        (
            Token(token_type=TokenType.FILE_NAME, token_value="a.txt"),
            Token(token_type=TokenType.FILE_NAME, token_value="b.txt"),
        ),
        (
            Token(token_type=TokenType.FUNC_CALL_START, token_value="["),
            Token(token_type=TokenType.FUNC_NAME, token_value="DIF"),
            Token(token_type=TokenType.FUNC_CALL_END, token_value="]"),
        ),
    )
)
def test_compile_with_invalid_tokens_should_raise(
    invalid_tokens: t.Sequence[Token],
):
    compiler = Compiler(
        tokens=invalid_tokens,
        functions_mapping=_FUNCTIONS_MAPPING,
    )

    with pytest.raises(CompileException):
        compiler.compile()
