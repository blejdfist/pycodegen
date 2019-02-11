import logging
from clang.cindex import CursorKind, AccessSpecifier

from . import helpers

_log = logging.getLogger(__name__)

ACCESS_PRIVATE = "private"
ACCESS_PUBLIC = "public"
ACCESS_PROTECTED = "protected"


def visit(cursor, qualified_path, context):
    result = {
        "name": cursor.spelling or cursor.displayname,
        "type": "class",
        "extent": helpers.get_extent(cursor),
        "fields": [],
        "methods": [],
    }

    if len(qualified_path) > 1:
        result["qualified_name"] = helpers.make_qualified_name(qualified_path, cursor.spelling)
    else:
        result["qualified_name"] = result["name"]

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
            _log.warning("Unhandled " + str(child.kind))

    return result


def visit_field(cursor, qualified_path):
    field_desc = {
        "name": cursor.spelling or cursor.displayname,
        "qualified_name": helpers.make_qualified_name(qualified_path, cursor.spelling),
        "type": cursor.type.spelling,
    }

    if cursor.access_specifier == AccessSpecifier.PUBLIC:
        field_desc["access"] = ACCESS_PUBLIC
    elif cursor.access_specifier == AccessSpecifier.PRIVATE:
        field_desc["access"] = ACCESS_PRIVATE
    elif cursor.access_specifier == AccessSpecifier.PROTECTED:
        field_desc["access"] = ACCESS_PROTECTED

    return field_desc


def visit_method(cursor, qualified_path):
    method_desc = {
        "name": cursor.spelling or cursor.displayname,
        "qualified_name": helpers.make_qualified_name(qualified_path, cursor.spelling),
        "return_type": cursor.result_type.spelling,
        "arguments": []
    }
    if cursor.access_specifier == AccessSpecifier.PUBLIC:
        method_desc["access"] = ACCESS_PUBLIC
    elif cursor.access_specifier == AccessSpecifier.PRIVATE:
        method_desc["access"] = ACCESS_PRIVATE
    elif cursor.access_specifier == AccessSpecifier.PROTECTED:
        method_desc["access"] = ACCESS_PROTECTED

    for child in cursor.get_children():
        if child.kind == CursorKind.PARM_DECL:
            method_desc["arguments"].append(child.spelling)

    return method_desc
