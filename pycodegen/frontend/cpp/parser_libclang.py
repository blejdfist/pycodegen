import clang.cindex
from clang.cindex import CursorKind
import logging


def _parse_annotation(annotation):
    parts = annotation.split(",")

    if parts:
        values = [p.split("=") for p in parts]
    else:
        values = [(annotation, True)]

    result = {}

    for value in values:
        if len(value) == 2:
            result[value[0]] = value[1]
        else:
            result[value[0]] = True

    return result


def _get_extent(cursor):
    return {
        "file": cursor.extent.start.file.name,
        "start": {
            "offset": cursor.extent.start.offset,
            "line": cursor.extent.start.line,
            "column": cursor.extent.start.column,
        },
        "end": {
            "offset": cursor.extent.end.offset,
            "line": cursor.extent.end.line,
            "column": cursor.extent.end.column
        },
    }


class ParserLibClang:
    _log = logging.getLogger(__name__)

    def __init__(self, library_file=None):
        self._current_filename = None

        if not clang.cindex.Config.loaded:
            if library_file is None:
                library_file = self._detect_library_file()

            clang.cindex.Config.set_library_file(library_file)

        self._handlers = {
            CursorKind.TRANSLATION_UNIT: self._handle_recurse,
            CursorKind.NAMESPACE: self._handle_recurse,
            CursorKind.ENUM_DECL: self._handle_enum_decl
        }

    def _detect_library_file(self):
        return "/usr/lib/x86_64-linux-gnu/libclang-7.so.1"

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

        translation_unit = self._parse_file(filename, extra_arguments=arguments)
        return asciitree.draw_tree(translation_unit.cursor, self._get_children, format_node)

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
        self._current_filename = filename
        index = clang.cindex.Index.create()

        arguments = ["-x", "c++", "-D__CODEGEN__"]
        if extra_arguments is not None:
            arguments += extra_arguments

        translation_unit = index.parse(filename, args=arguments, options=0)
        return translation_unit

    def _get_children(self, cursor):
        return [c for c in cursor.get_children() if c.location.file and c.location.file.name == self._current_filename]

    def _handle_recurse(self, cursor, path=None):
        if path is None:
            path = []

        result = []
        for child in self._get_children(cursor, ):
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
            "extent": _get_extent(cursor),
            "enum_values": {}
        }

        if len(path) > 1:
            result["qualified_name"] = "::".join(path[1:]) + "::" + cursor.spelling

        for value in self._get_children(cursor):
            if value.kind == CursorKind.ANNOTATE_ATTR:
                result["annotations"] = _parse_annotation(value.spelling)
            elif value.kind == CursorKind.ENUM_CONSTANT_DECL:
                result["enum_values"][value.spelling] = value.enum_value
            else:
                self._log.debug("ENUM_DECL: Unhandled " + str(value.kind))

        return result

    def _traverse(self, cursor, path=None):
        handler = self._handlers.get(cursor.kind)
        if handler:
            return handler(cursor, path)
