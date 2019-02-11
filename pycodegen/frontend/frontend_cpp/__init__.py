"""C/C++ parser frontend based on libclang"""
import argparse
from .parser_libclang import ParserLibClang


def register_arguments(argument_parser):
    argument_parser.add_argument("--args", nargs=argparse.REMAINDER, help="Arguments to pass to clang")
    argument_parser.add_argument("--print-ast", action="store_true", default=False, help="Print AST to console")


def run(filename, options=None):
    if options is None:
        options = {}

    parser = ParserLibClang()

    if options.get('print_ast'):
        print(parser.dump(filename, options.get('args')))

    return parser.parse(filename, options.get('args'))
