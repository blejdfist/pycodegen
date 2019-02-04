import argparse

from .parser_libclang import ParserLibClang


def register_arguments(argument_parser):
    argument_parser.add_argument("--args", nargs=argparse.REMAINDER, help="Arguments to pass to clang")


def run(filename, options):
    parser = ParserLibClang()
    return parser.parse(filename, options.args)
