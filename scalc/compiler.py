import typing as t

from scalc.tokens import Token, TokenType
from scalc.functions import SetCalcFunc
from scalc.exceptions import CompileException
from scalc.expressions import (
    Expression,
    LoadFromFileExpression,
    FunctionCallExpression,
)


class Compiler:

    def __init__(
        self,
        tokens: t.Sequence[Token],
        functions_mapping: t.Mapping[str, SetCalcFunc],
    ):
        self._tokens = tokens
        self._functions_mapping = functions_mapping

    @property
    def tokens(self) -> t.Sequence[Token]:
        return self._tokens

    @property
    def functions_mapping(self) -> t.Mapping[str, SetCalcFunc]:
        return self._functions_mapping

    def compile(self) -> Expression:
        root_expression, used_tokens_count = self._build_expression_from_idx(idx=0)

        if used_tokens_count < len(self.tokens):
            raise CompileException(
                reason="Unexpected extra tokens after root expression"
            )

        return root_expression

    def _get_token_by_idx_or_raise(self, idx: int) -> Token:
        if len(self.tokens) < idx + 1:
            raise CompileException(reason="Unexpected EOF")
        return self.tokens[idx]

    def _get_expected_token_by_idx_or_raise(
        self,
        idx: int,
        expected_types: t.AbstractSet[TokenType],
    ):
        token = self._get_token_by_idx_or_raise(idx=idx)
        if token.token_type not in expected_types:
            raise CompileException(
                reason=(
                    f"Unexpected token. Expected {expected_types}"
                    f" but received {oken.token_type}"
                ),
            )
        return token

    def _build_func_call_expression_from_idx(
        self,
        idx: int,
    ) -> t.Tuple[FunctionCallExpression, int]:
        func_start_token = self._get_expected_token_by_idx_or_raise(
            idx=idx,
            expected_types={TokenType.FUNC_CALL_START},
        )
        used_tokens_count = 1

        func_name_token = self._get_expected_token_by_idx_or_raise(
            idx=idx + used_tokens_count,
            expected_types={TokenType.FUNC_NAME},
        )
        used_tokens_count += 1

        func_name = func_name_token.token_value
        if func_name not in self.functions_mapping:
            raise CompileException(
                reason=f"Unknown function: {func_name}",
            )
        func = self.functions_mapping[func_name]

        func_args = []
        next_token = self._get_token_by_idx_or_raise(idx=idx + used_tokens_count)
        while next_token.token_type != TokenType.FUNC_CALL_END:
            func_arg, arg_used_tokens_count = self._build_expression_from_idx(
                idx=idx + used_tokens_count,
            )
            func_args.append(func_arg)
            used_tokens_count += arg_used_tokens_count
            next_token = self._get_token_by_idx_or_raise(idx=idx + used_tokens_count)

        if len(func_args) == 0:
            raise CompileException(
                reason="Function call excpects at least one argument",
            )

        used_tokens_count += 1  # For `FUNC_CALL_END` token
        return FunctionCallExpression(
            func=func,
            func_args=func_args,
        ), used_tokens_count

    def _build_load_from_file_expression_from_idx(
        self,
        idx: int,
    ) -> t.Tuple[LoadFromFileExpression, int]:
        token = self._get_expected_token_by_idx_or_raise(
            idx=idx,
            expected_types={TokenType.FILE_NAME},
        )
        return LoadFromFileExpression(file_name=token.token_value), 1


    def _build_expression_from_idx(self, idx: int) -> t.Tuple[Expression, int]:
        """
            :return: parsed expression, tokens count used to build expression.
        """
        first_expression_token = self._get_token_by_idx_or_raise(idx=idx)

        if first_expression_token.token_type == TokenType.FUNC_CALL_START:
            return self._build_func_call_expression_from_idx(idx=idx)
        elif first_expression_token.token_type == TokenType.FILE_NAME:
            return self._build_load_from_file_expression_from_idx(idx=idx)
        else:
            raise CompileException(
                reason=(
                    f"Unexpected token. Expected {TokenType.FUNC_CALL_START}"
                    f" or {TokenType.FILE_NAME} but received {irst_expression_token.token_type}"
                ),
            )
