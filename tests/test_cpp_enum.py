import tempfile
from pycodegen import get_frontend_by_name


def test_parse_enum_class():
    with tempfile.NamedTemporaryFile() as f:
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
    with tempfile.NamedTemporaryFile() as f:
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
    with tempfile.NamedTemporaryFile() as f:
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


def test_parse_enum_values():
    with tempfile.NamedTemporaryFile() as f:
        f.write(b"""
            enum Values {
                A = 0xABCD,
                B = 0755,
                C = 1234
            };
        """)
        f.file.flush()

        frontend = get_frontend_by_name("cpp")
        result = frontend.run(f.name)

        assert result[0]['enum_values']['A'] == 0xABCD
        assert result[0]['enum_values']['B'] == 0o755
        assert result[0]['enum_values']['C'] == 1234


def test_parse_enum_annotation_simple():
    with tempfile.NamedTemporaryFile() as f:
        f.write(b"""
            enum __attribute__((annotate("hello world"))) Color {
            };
        """)
        f.file.flush()

        frontend = get_frontend_by_name("cpp")
        result = frontend.run(f.name)

        assert result[0]['annotations'].get("hello world")


def test_parse_enum_annotation_key_value():
    with tempfile.NamedTemporaryFile() as f:
        f.write(b"""
            enum __attribute__((annotate("greeting=hello,what=world"))) Color {
            };
        """)
        f.file.flush()

        frontend = get_frontend_by_name("cpp")
        result = frontend.run(f.name)

        assert result[0]['annotations'].get("greeting") == "hello"
        assert result[0]['annotations'].get("what") == "world"


