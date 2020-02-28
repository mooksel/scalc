import typing as t

import pytest

from scalc.tokens import Token, TokenType, TokenParser
from scalc.exceptions import SyntaxException


_VALID_FUNC_NAME_TOKEN_VALUES = (
    "SUM",
    "INT",
    "DIF",
    "SOME_VERY_VERY_LONG_FUNCTION_NAME",
    "S",
)

_VALID_FILE_NAME_TOKEN_VALUES = (
    "a_1.txt",
    "zz.numbers",
    "a888",
    "some_very_very_long_file_name.very_long_file_extension",
    "a",
    "some/path/to/file.txt",
)

_VALID_TOKEN_VALUES = (
    _VALID_FUNC_NAME_TOKEN_VALUES
    + _VALID_FILE_NAME_TOKEN_VALUES
    + ("[", "]")
)

_INVALID_TOKEN_CHARS = ("*", "%", "^", "&", "*", "(", ")", "$", "#")
_INVALID_TOKEN_VALUES = (
    f"{valid_token_value}{invalid_token_char}"
    for valid_token_value in _VALID_TOKEN_VALUES
    for invalid_token_char in _INVALID_TOKEN_CHARS
)
_INVALID_SOURCE_STRS = (
    f"{valid_source_token} {invalid_source_token}"
    for valid_source_token in _VALID_TOKEN_VALUES
    for invalid_source_token in _INVALID_TOKEN_VALUES
)


@pytest.mark.parametrize(
    ("valid_source_str", "expected_tokens"),
    (
        ("[", (Token(token_type=TokenType.FUNC_CALL_START, token_value="["), )),
        ("]", (Token(token_type=TokenType.FUNC_CALL_END, token_value="]"), )),
        *tuple(
            (token_value, (Token(token_type=TokenType.FUNC_NAME, token_value=token_value), ))
            for token_value in _VALID_FUNC_NAME_TOKEN_VALUES
        ),
        *tuple(
            (token_value, (Token(token_type=TokenType.FILE_NAME, token_value=token_value), ))
            for token_value in _VALID_FILE_NAME_TOKEN_VALUES
        ),
        (
            "[ ] SUM a.txt ",
            (
                Token(token_type=TokenType.FUNC_CALL_START, token_value="["),
                Token(token_type=TokenType.FUNC_CALL_END, token_value="]"),
                Token(token_type=TokenType.FUNC_NAME, token_value="SUM"),
                Token(token_type=TokenType.FILE_NAME, token_value="a.txt"),
            ),
        ),
    ),
)
def test_parse_with_valid_token_source_str_should_return_valid_parsed_tokens(
    valid_source_str: str,
    expected_tokens: t.Sequence[Token],
):
    token_parser = TokenParser(source_str=valid_source_str)
    parsed_tokens = token_parser.parse()
    assert tuple(parsed_tokens) == expected_tokens


@pytest.mark.parametrize(
    "invalid_source_str",
    (
        (invalid_src_str for invalid_src_str in _INVALID_SOURCE_STRS)
    ),
)
def test_parse_with_invalid_source_str_should_raise(
    invalid_source_str: str,
):
    token_parser = TokenParser(source_str=invalid_source_str)
    with pytest.raises(SyntaxException):
        token_parser.parse()

