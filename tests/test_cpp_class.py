import tempfile
from pycodegen.frontend import get_frontend_by_name


def group_by_name(objects):
    return dict([(obj['name'], obj) for obj in objects])


def test_basic():
    with tempfile.NamedTemporaryFile() as f:
        f.write(b"""
            class MyClass {};
        """)
        f.file.flush()

        frontend = get_frontend_by_name("cpp")
        result = frontend.run(f.name)

        assert len(result) == 1
        assert result[0].get('name') == 'MyClass'
        assert result[0].get('type') == 'class'
        assert result[0].get('qualified_name') == 'MyClass'


def test_fields():
    with tempfile.NamedTemporaryFile() as f:
        f.write(b"""
            class MyClass {
                double private_field_1;
            public: 
                double public_field;
            private: 
                bool private_field_2;
            protected: 
                bool protected_field;
            };
        """)
        f.file.flush()

        frontend = get_frontend_by_name("cpp")
        result = frontend.run(f.name)

        assert len(result) == 1
        assert len(result[0]['fields']) == 4

        fields = group_by_name(result[0]['fields'])

        assert fields['private_field_1']['access'] == 'private'
        assert fields['private_field_2']['access'] == 'private'
        assert fields['public_field']['access'] == 'public'
        assert fields['protected_field']['access'] == 'protected'

        assert fields['private_field_1']['type'] == 'double'
        assert fields['private_field_2']['type'] == 'bool'
        assert fields['public_field']['type'] == 'double'
        assert fields['protected_field']['type'] == 'bool'


def test_methods():
    with tempfile.NamedTemporaryFile() as f:
        f.write(b"""
            class MyClass {
                bool private_method_1();
            public: 
                double public_method();
            private: 
                bool private_method_2();
            protected: 
                char protected_method();
            };
        """)
        f.file.flush()

        frontend = get_frontend_by_name("cpp")
        result = frontend.run(f.name)

        assert len(result) == 1
        assert len(result[0]['methods']) == 4

        methods = group_by_name(result[0]['methods'])

        assert methods['private_method_1']['access'] == 'private'
        assert methods['private_method_2']['access'] == 'private'
        assert methods['public_method']['access'] == 'public'
        assert methods['protected_method']['access'] == 'protected'

        assert methods['private_method_1']['return_type'] == 'bool'
        assert methods['private_method_2']['return_type'] == 'bool'
        assert methods['public_method']['return_type'] == 'double'
        assert methods['protected_method']['return_type'] == 'char'


def test_method_params():
    with tempfile.NamedTemporaryFile() as f:
        f.write(b"""
            class MyClass {
                void my_method(int a, char b, bool d);
            };
        """)
        f.file.flush()

        frontend = get_frontend_by_name("cpp")
        result = frontend.run(f.name)

        assert len(result) == 1
        assert len(result[0]['methods']) == 1

        method = result[0]['methods'][0]
        assert len(method['arguments']) == 3


def test_namespace():
    with tempfile.NamedTemporaryFile() as f:
        f.write(b"""
            namespace Foo {
              namespace Bar {
                class MyClass {
                    int my_method() const;
                    int my_member;
                };
              }
            }
        """)
        f.file.flush()

        frontend = get_frontend_by_name("cpp")
        result = frontend.run(f.name)

        assert len(result) == 1
        assert result[0]['name'] == 'MyClass'
        assert result[0]['qualified_name'] == 'Foo::Bar::MyClass'

        assert len(result[0]['methods']) == 1
        assert result[0]['methods'][0]['qualified_name'] == 'Foo::Bar::MyClass::my_method'

        assert len(result[0]['fields']) == 1
        assert result[0]['fields'][0]['qualified_name'] == 'Foo::Bar::MyClass::my_member'


def test_annotations():
    with tempfile.NamedTemporaryFile() as f:
        f.write(b"""
            class __attribute__((annotate("foo=bar"))) MyClass {
            };
        """)
        f.file.flush()

        frontend = get_frontend_by_name("cpp")
        result = frontend.run(f.name)

        assert len(result) == 1
        assert result[0]['annotations'].get("foo") == "bar"
