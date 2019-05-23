"""Visitor for C/C++ functions"""
import logging
from clang.cindex import CursorKind

from . import helpers

_LOGGER = logging.getLogger(__name__)


def visit(cursor, qualified_path, context):
    """
    Visit CursorKind.FUNCTION_DECL

    :param cursor: Current cursor
    :param qualified_path: Qualified path (namespaces)
    :param context: ParserContext
    :return: Function description
    """
    result = {
        "name": cursor.spelling or cursor.displayname,
        "qualified_name": helpers.make_qualified_name(qualified_path, cursor),
        "type": "function",
        "return_type": cursor.result_type.spelling,
        "extent": helpers.get_extent(cursor),
    }

    for value in helpers.get_children(cursor, context):
        if value.kind == CursorKind.ANNOTATE_ATTR:
            result["annotations"] = helpers.parse_annotation(value.spelling)
        else:
            _LOGGER.warning("Unhandled %s", str(value.kind))

    return result
