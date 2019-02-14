"""C/C++ parser frontend based on libclang"""
import argparse
import logging
import sys

_LOGGER = logging.getLogger(__name__)


def register_arguments(argument_parser):
    argument_parser.add_argument("--args", nargs=argparse.REMAINDER,
                                 help="Arguments to pass to clang")

    argument_parser.add_argument("--print-ast", action="store_true",
                                 help="Print AST to console")


def run(filename, options=None):
    try:
        import clang.cindex
    except ModuleNotFoundError:
        _LOGGER.error("To use the C++ frontend you must have clang>=6.0.0 installed.")
        _LOGGER.error("Try installing it using: pip install 'pycodegen[CPP]'")
        sys.exit(1)

    from .parser_libclang import ParserLibClang

    if options is None:
        options = {}

    parser = ParserLibClang()

    if options.get('print_ast'):
        print(parser.dump(filename, options.get('args')))

    return parser.parse(filename, options.get('args'))
