from textwrap import dedent

import pytest

try:
    import clang.cindex  # noqa: F401
except ImportError:
    pytest.skip("libclang not available", allow_module_level=True)


def test_generate_struct_header(driver):
    cpp_input = """
        struct Point {
            double x;
            double y;
        };
    """

    template = dedent("""\
        {% for item in items -%}
        // Generated from {{ item.name }}
        {% for field in item.fields -%}
        {{ field.type }} get_{{ field.name }}() const;
        {% endfor -%}
        {% endfor %}
    """)

    result = driver(cpp_input, frontend="cpp").render(template)

    assert "// Generated from Point" in result
    assert "double get_x() const;" in result
    assert "double get_y() const;" in result


def test_generate_enum_to_string(driver):
    cpp_input = dedent("""\
        enum Color {
            Red,
            Green,
            Blue
        };
    """)

    template = dedent("""\
        {% for item in items -%}
        {% for name in item.enum_values -%}
        {{ name }}
        {% endfor -%}
        {% endfor %}
    """)

    result = driver(cpp_input, frontend="cpp").render(template)

    assert result == dedent("""\
        Red
        Green
        Blue
    """)
