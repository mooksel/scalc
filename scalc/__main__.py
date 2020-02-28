import typing as t

from scalc.expressions import Expression
from scalc.tokens import TokenParser
from scalc.exceptions import SetCalcException
from scalc.compiler import Compiler
from scalc.executor import Executor
from scalc.functions import load_functions, SetCalcFunc


if __name__ == "__main__":
    source_str = "[ SUM [ DIF a.txt b.txt c.txt ] [ INT b.txt c.txt ] ]"
    token_parser = TokenParser(source_str=source_str)
    try:
        tokens = token_parser.parse()
        functions_mapping = load_functions()
        compiler = Compiler(
            tokens=tokens,
            functions_mapping=functions_mapping,
        )

        root_expression = compiler.compile()
        executor = Executor(
            root_expression=root_expression,
            functions_mapping=functions_mapping,
        )

        result = list(executor.execute())
        result.sort()
        for i in result:
            print(i)

    except SetCalcException as e:
        print(e)

