class SetCalcException(Exception):

    def __init__(self, reason: str):
        self._reason = reason

    @property
    def reason(self) -> str:
        return self._reason

    def __str__(self) -> str:
        return self.reason


class SyntaxException(SetCalcException):

    def __str__(self) -> str:
        return f"SYNTAX ERROR: {self.reason}"


class CompileException(SetCalcException):

    def __str__(self) -> str:
        return f"COMPILE ERROR: {self.reason}"


class RuntimeException(SetCalcException):

    def __str__(self) -> str:
        return f"RUNTIME ERROR: {self.reason}"


__all__ = (
    SyntaxException.__name__,
    RuntimeException.__name__,
    CompileException.__name__,
    SetCalcException.__name__,
)
