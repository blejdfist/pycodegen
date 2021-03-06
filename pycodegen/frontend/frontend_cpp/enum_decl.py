"""Visitor for C/C++ enums"""
import logging
from clang.cindex import CursorKind

from . import helpers

_LOGGER = logging.getLogger(__name__)


def visit(cursor, qualified_path, context):
    """
    Visit CursorKind.ENUM_DECL

    :param cursor: Current cursor
    :param qualified_path: Qualified path (namespaces)
    :param context: ParserContext
    :return: Enum description
    """
    result = {
        "name": cursor.spelling or cursor.displayname,
        "qualified_name": helpers.make_qualified_name(qualified_path, cursor),
        "type": "enum",
        "underlying_type": cursor.enum_type.spelling,
        "extent": helpers.get_extent(cursor),
        "enum_values": {}
    }

    for value in helpers.get_children(cursor, context):
        if value.kind == CursorKind.ANNOTATE_ATTR:
            result["annotations"] = helpers.parse_annotation(value.spelling)
        elif value.kind == CursorKind.ENUM_CONSTANT_DECL:
            result["enum_values"][value.spelling] = value.enum_value
        else:
            _LOGGER.warning("Unhandled %s", str(value.kind))

    return result
