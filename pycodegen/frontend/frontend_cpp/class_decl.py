import logging
from clang.cindex import CursorKind, AccessSpecifier

from . import helpers

_LOGGER = logging.getLogger(__name__)

ACCESS_PRIVATE = "private"
ACCESS_PUBLIC = "public"
ACCESS_PROTECTED = "protected"


def _get_access(cursor):
    if cursor.access_specifier == AccessSpecifier.PUBLIC:
        return ACCESS_PUBLIC
    if cursor.access_specifier == AccessSpecifier.PRIVATE:
        return ACCESS_PRIVATE
    if cursor.access_specifier == AccessSpecifier.PROTECTED:
        return ACCESS_PROTECTED
    return None


def visit(cursor, qualified_path, context):
    result = {
        "name": cursor.spelling or cursor.displayname,
        "qualified_name": helpers.make_qualified_name(qualified_path, cursor),
        "type": "class",
        "extent": helpers.get_extent(cursor),
        "fields": [],
        "methods": [],
    }

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
        "access": _get_access(cursor),
        "type": cursor.type.spelling,
    }

    return field_desc


def visit_method(cursor, qualified_path):
    method_desc = {
        "name": cursor.spelling or cursor.displayname,
        "qualified_name": helpers.make_qualified_name(qualified_path, cursor),
        "return_type": cursor.result_type.spelling,
        "access": _get_access(cursor),
        "arguments": []
    }

    for child in cursor.get_children():
        if child.kind == CursorKind.PARM_DECL:
            method_desc["arguments"].append(child.spelling)

    return method_desc
