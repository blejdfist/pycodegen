import tempfile
from pycodegen import get_frontend_by_name


def test_global_function():
    with tempfile.NamedTemporaryFile() as f:
        f.write(b"""
            void func_1() {};
            int func_2() {};
        """)
        f.file.flush()

        frontend = get_frontend_by_name("cpp")
        result = frontend.run(f.name)

        assert len(result) == 2

        assert result[0]["type"] == "function"
        assert result[1]["type"] == "function"

        assert result[0]["name"] == "func_1"
        assert result[1]["name"] == "func_2"

        assert result[0]["qualified_name"] == "func_1"
        assert result[1]["qualified_name"] == "func_2"

        assert result[0]["return_type"] == "void"
        assert result[1]["return_type"] == "int"


def test_global_function_namespace():
    with tempfile.NamedTemporaryFile() as f:
        f.write(b"""
            namespace Foo {
                namespace Bar {
                    int func() {}
                }
            }
        """)
        f.file.flush()

        frontend = get_frontend_by_name("cpp")
        result = frontend.run(f.name)

        assert len(result) == 1

        assert result[0]["type"] == "function"
        assert result[0]["name"] == "func"
        assert result[0]["qualified_name"] == "Foo::Bar::func"


def test_global_function_annotation():
    with tempfile.NamedTemporaryFile() as f:
        f.write(b"""
            int __attribute__((annotate("foo=bar"))) func() {};
        """)
        f.file.flush()

        frontend = get_frontend_by_name("cpp")
        result = frontend.run(f.name)

        assert len(result) == 1

        assert result[0]["type"] == "function"
        assert result[0]['annotations'].get("foo") == "bar"
