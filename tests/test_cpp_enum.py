import tempfile
from pycodegen.frontend import get_frontend_by_name


def test_parse_enum_class():
    with tempfile.NamedTemporaryFile(suffix=".h") as f:
        f.write(b"""
            enum class Color : char {
                Red,Green,Blue
            };
        """)
        f.file.flush()

        frontend = get_frontend_by_name("cpp")
        result = frontend.run(f.name)

        assert len(result) == 1
        assert result[0].get('name') == 'Color'
        assert result[0].get('type') == 'enum'
        assert result[0].get('underlying_type') == 'char'
        assert result[0].get('qualified_name') == 'Color'
        assert len(result[0]['enum_values'].keys()) == 3


def test_parse_enum():
    with tempfile.NamedTemporaryFile(suffix=".h") as f:
        f.write(b"""
            enum Color {
                Red,Green,Blue
            };
        """)
        f.file.flush()

        frontend = get_frontend_by_name("cpp")
        result = frontend.run(f.name)

        assert len(result) == 1
        assert result[0].get('name') == 'Color'
        assert result[0].get('type') == 'enum'
        assert result[0].get('qualified_name') == 'Color'
        assert len(result[0]['enum_values'].keys()) == 3


def test_parse_enum_in_namespace():
    with tempfile.NamedTemporaryFile(suffix=".h") as f:
        f.write(b"""
            namespace MyEnums {
                enum Color {
                    Red,Green,Blue
                };
            }
        """)
        f.file.flush()

        frontend = get_frontend_by_name("cpp")
        result = frontend.run(f.name)

        assert len(result) == 1
        assert result[0].get('name') == 'Color'
        assert result[0].get('type') == 'enum'
        assert result[0].get('qualified_name') == 'MyEnums::Color'
        assert len(result[0]['enum_values'].keys()) == 3
