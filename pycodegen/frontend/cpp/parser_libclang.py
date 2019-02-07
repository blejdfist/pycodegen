import collections
import os

import clang.cindex
from clang.cindex import CursorKind
import logging
import glob

from . import helpers


def _detect_library_file():
    version = os.getenv("PYCODEGEN_LIBCLANG", "")
    candidates = glob.glob("/usr/lib/llvm-{version}*/lib/libclang*.so*".format(version=version))

    if not candidates:
        raise RuntimeError("Unable to find libclang")

    candidates.sort()
    return candidates[0]


ParserContext = collections.namedtuple("ParserContext", ["input_file"])


class ParserLibClang:
    _log = logging.getLogger(__name__)

    def __init__(self, library_file=None):
        self._context = None

        if not clang.cindex.Config.loaded:
            if library_file is None:
                library_file = _detect_library_file()

            self._log.debug("Using libclang from: %s", library_file)
            clang.cindex.Config.set_library_file(library_file)

        self._handlers = {
            CursorKind.TRANSLATION_UNIT: self._handle_recurse,
            CursorKind.NAMESPACE: self._handle_recurse,
            CursorKind.ENUM_DECL: self._handle_enum_decl
        }

    def dump(self, filename, arguments=None):
        """
        Generate a tree view of the AST

        :param filename: File to parse
        :param arguments: Extra arguments to pass to clang
        :return: String representation of the AST
        """
        import asciitree

        def format_node(c):
            return '{name:<10} ({extra})'.format(
                name=c.spelling or c.displayname,
                extra=c.kind.name)

        def get_children(c):
            return helpers.get_children(c, self._context)

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
            if type(child_data) == list:
                result += child_data
            else:
                result.append(child_data)

        return result

    def _handle_enum_decl(self, cursor, path):
        result = {
            "name": cursor.spelling or cursor.displayname,
            "type": "enum",
            "underlying_type": cursor.enum_type.spelling,
            "extent": helpers.get_extent(cursor),
            "enum_values": {}
        }

        if len(path) > 1:
            result["qualified_name"] = "::".join(path[1:]) + "::" + cursor.spelling
        else:
            result["qualified_name"] = result["name"]

        for value in helpers.get_children(cursor, self._context):
            if value.kind == CursorKind.ANNOTATE_ATTR:
                result["annotations"] = helpers.parse_annotation(value.spelling)
            elif value.kind == CursorKind.ENUM_CONSTANT_DECL:
                result["enum_values"][value.spelling] = value.enum_value
            else:
                self._log.debug("ENUM_DECL: Unhandled " + str(value.kind))

        return result

    def _traverse(self, cursor, path=None):
        handler = self._handlers.get(cursor.kind)
        if handler:
            return handler(cursor, path)
