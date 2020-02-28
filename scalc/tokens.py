import enum
import re
import typing as t
from dataclasses import dataclass

from scalc.exceptions import SyntaxException


class TokenType(str, enum.Enum):
    FUNC_CALL_START = "FUNC_CALL_START"
    FUNC_CALL_END = "FUNC_CALL_END"
    FUNC_NAME = "FUNC_NAME"
    FILE_NAME = "FILE_NAME"


@dataclass(frozen=True)
class Token:
    token_type: TokenType
    token_value: str


class TokenParser:

    def __init__(self, source_str: str):
        self._source_str = source_str
        self._func_name_re_pattern = re.compile(r"^[A-Z][A-Z_]*$")
        self._file_name_re_pattern = re.compile(r"^[a-z][a-z0-9_\.]*$")

    @property
    def source_str(self) -> str:
        return self._source_str

    @property
    def func_name_re_pattern(self) -> re.Pattern:
        return self._func_name_re_pattern

    @property
    def file_name_re_pattern(self) -> re.Pattern:
        return self._file_name_re_pattern

    def parse(self) -> t.Sequence[Token]:
        tokens_values = self.source_str.split()
        tokens = []

        for token_value in tokens_values:
            token_type = self._token_type_for_value_or_raise(token_value=token_value)
            tokens.append(Token(
                token_type=token_type,
                token_value=token_value,
            ))

        return tokens

    def _match_func_call_start_token(self, token_value: str) -> bool:
        return token_value == "["

    def _match_func_call_end_token(self, token_value: str) -> bool:
        return token_value == "]"

    def _match_func_name_token(self, token_value: str) -> bool:
        return self.func_name_re_pattern.match(token_value) is not None

    def _match_file_name_token(self, token_value: str) -> bool:
        return self.file_name_re_pattern.match(token_value) is not None

    def _token_type_for_value_or_raise(self, token_value: str) -> TokenType:
        if self._match_func_call_start_token(token_value=token_value):
            return TokenType.FUNC_CALL_START
        elif self._match_func_call_end_token(token_value=token_value):
            return TokenType.FUNC_CALL_END
        elif self._match_func_name_token(token_value=token_value):
            return TokenType.FUNC_NAME
        elif self._match_file_name_token(token_value=token_value):
            return TokenType.FILE_NAME
        else:
            raise SyntaxException(
                reason=f"Unknown token: {token_value}",
            )


__all__ = (
    TokenType.__name__,
    Token.__name__,
    TokenParser.__name__,
)
