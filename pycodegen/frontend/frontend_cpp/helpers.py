def parse_annotation(annotation):
    parts = annotation.split(",")

    values = [part.split("=") for part in parts]

    result = {}

    for value in values:
        if len(value) == 2:
            result[value[0]] = value[1]
        else:
            result[value[0]] = True

    return result


def get_extent(cursor):
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


def get_children(cursor, context):
    return [c for c in cursor.get_children() if c.location.file and c.location.file.name == context.input_file]


def make_qualified_name(qualified_path, node):
    if len(qualified_path) > 1:
        return "::".join(qualified_path[1:]) + "::" + node.spelling

    return node.spelling
