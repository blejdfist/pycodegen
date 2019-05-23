"""Visitor for C++ classes"""
import logging
from clang.cindex import CursorKind

from . import helpers

_LOGGER = logging.getLogger(__name__)


def visit(cursor, qualified_path, context):
    result = {
        "name": cursor.spelling or cursor.displayname,
        "qualified_name": helpers.make_qualified_name(qualified_path, cursor),
        "extent": helpers.get_extent(cursor),
        "fields": [],
        "methods": [],
    }

    if cursor.kind == CursorKind.CLASS_DECL:
        result["type"] = "class"
    elif cursor.kind == CursorKind.STRUCT_DECL:
        result["type"] = "struct"

    for child in helpers.get_children(cursor, context):
        if child.kind == CursorKind.ANNOTATE_ATTR:
            result["annotations"] = helpers.parse_annotation(child.spelling)
        elif child.kind == CursorKind.CXX_METHOD:
            result["methods"].append(visit_method(child, qualified_path + [cursor.spelling]))
        elif child.kind == CursorKind.FIELD_DECL:
            result["fields"].append(visit_field(child, qualified_path + [cursor.spelling]))
        elif child.kind == CursorKind.CXX_ACCESS_SPEC_DECL:
            pass
        else:
            _LOGGER.warning("Unhandled %s", str(child.kind))

    return result


def visit_field(cursor, qualified_path):
    field_desc = {
        "name": cursor.spelling or cursor.displayname,
        "qualified_name": helpers.make_qualified_name(qualified_path, cursor),
        "access": cursor.access_specifier.name.lower(),
        "type": cursor.type.spelling,
    }

    return field_desc


def visit_method(cursor, qualified_path):
    method_desc = {
        "name": cursor.spelling or cursor.displayname,
        "qualified_name": helpers.make_qualified_name(qualified_path, cursor),
        "return_type": cursor.result_type.spelling,
        "access": cursor.access_specifier.name.lower(),
        "arguments": []
    }

    for child in cursor.get_children():
        if child.kind == CursorKind.PARM_DECL:
            method_desc["arguments"].append(child.spelling)

    return method_desc
