import logging
import glob
import collections
import os

import clang.cindex
from clang.cindex import CursorKind

from . import helpers
from . import enum_decl
from . import class_struct_decl
from . import function_decl

_LOGGER = logging.getLogger(__name__)


def _detect_library_file():
    version = os.getenv("PYCODEGEN_LIBCLANG", "")
    candidates = glob.glob("/usr/lib/llvm-{version}*/lib/libclang*.so*".format(version=version))

    if not candidates:
        raise RuntimeError("Unable to find libclang")

    # Select the latest libclang version
    candidates.sort()
    return candidates[-1]


ParserContext = collections.namedtuple("ParserContext", ["input_file"])


class ParserLibClang:

    def __init__(self, library_file=None):
        self._context = None

        if not clang.cindex.Config.loaded:
            if library_file is None:
                library_file = _detect_library_file()

            _LOGGER.debug("Using libclang from: %s", library_file)
            clang.cindex.Config.set_library_file(library_file)

    def dump(self, filename, arguments=None):
        """
        Generate a tree view of the AST

        :param filename: File to parse
        :param arguments: Extra arguments to pass to clang
        :return: String representation of the AST
        """
        import asciitree

        def format_node(cursor):
            return '{name:<10} ({extra})'.format(
                name=cursor.spelling or cursor.displayname,
                extra=cursor.kind.name)

        def get_children(cursor):
            return helpers.get_children(cursor, self._context)

        translation_unit = self._parse_file(filename, extra_arguments=arguments)
        return asciitree.draw_tree(translation_unit.cursor, get_children, format_node)

    def parse(self, filename, arguments=None):
        """
        Parse and return a simplified version of the AST

        :param filename: File to parse
        :param arguments: Extra arguments to pass to clang
        :return: AST representation
        """
        translation_unit = self._parse_file(filename, extra_arguments=arguments)
        return self._traverse(translation_unit.cursor)

    def _parse_file(self, filename, extra_arguments):
        self._context = ParserContext(input_file=filename)
        index = clang.cindex.Index.create()

        arguments = ["-x", "c++", "-D__CODEGEN__"]
        if extra_arguments is not None:
            arguments += extra_arguments

        options = clang.cindex.TranslationUnit.PARSE_SKIP_FUNCTION_BODIES

        translation_unit = index.parse(filename, args=arguments, options=options)
        return translation_unit

    def _handle_recurse(self, cursor, path=None):
        if path is None:
            path = []

        result = []
        for child in helpers.get_children(cursor, self._context):
            child_data = self._traverse(child, path + [cursor.spelling])
            if child_data is not None:
                if isinstance(child_data, list):
                    result += child_data
                else:
                    result.append(child_data)

        return result

    def _traverse(self, cursor, qualified_path=None):
        if cursor.kind in [CursorKind.TRANSLATION_UNIT,
                           CursorKind.NAMESPACE]:
            return self._handle_recurse(cursor, qualified_path)

        if cursor.kind == CursorKind.ENUM_DECL:
            return enum_decl.visit(cursor, qualified_path, self._context)

        if cursor.kind in [CursorKind.CLASS_DECL, CursorKind.STRUCT_DECL]:
            return class_struct_decl.visit(cursor, qualified_path, self._context)

        if cursor.kind in [CursorKind.FUNCTION_DECL]:
            return function_decl.visit(cursor, qualified_path, self._context)

        _LOGGER.warning("Unhandled %s", str(cursor.kind))
        return None
