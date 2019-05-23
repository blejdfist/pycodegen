import tempfile
from pycodegen import get_frontend_by_name


def group_by_name(objects):
    return dict([(obj['name'], obj) for obj in objects])


def test_basic():
    with tempfile.NamedTemporaryFile() as f:
        f.write(b"""
            struct MyStruct {};
        """)
        f.file.flush()

        frontend = get_frontend_by_name("cpp")
        result = frontend.run(f.name)

        assert len(result) == 1
        assert result[0].get('name') == 'MyStruct'
        assert result[0].get('type') == 'struct'
        assert result[0].get('qualified_name') == 'MyStruct'


def test_fields():
    with tempfile.NamedTemporaryFile() as f:
        f.write(b"""
            struct MyStruct {
                double public_field_1;
            public: 
                double public_field_2;
            private: 
                bool private_field;
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

        assert fields['public_field_1']['access'] == 'public'
        assert fields['public_field_2']['access'] == 'public'
        assert fields['private_field']['access'] == 'private'
        assert fields['protected_field']['access'] == 'protected'

        assert fields['public_field_1']['type'] == 'double'
        assert fields['public_field_2']['type'] == 'double'
        assert fields['private_field']['type'] == 'bool'
        assert fields['protected_field']['type'] == 'bool'


def test_methods():
    with tempfile.NamedTemporaryFile() as f:
        f.write(b"""
            struct MyStruct {
                bool public_method_1();
            public: 
                double public_method_2();
            private: 
                bool private_method();
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

        assert methods['public_method_1']['access'] == 'public'
        assert methods['public_method_2']['access'] == 'public'
        assert methods['private_method']['access'] == 'private'
        assert methods['protected_method']['access'] == 'protected'

        assert methods['public_method_1']['return_type'] == 'bool'
        assert methods['public_method_2']['return_type'] == 'double'
        assert methods['private_method']['return_type'] == 'bool'
        assert methods['protected_method']['return_type'] == 'char'


def test_method_params():
    with tempfile.NamedTemporaryFile() as f:
        f.write(b"""
            struct MyStruct {
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
                struct MyStruct {
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
        assert result[0]['name'] == 'MyStruct'
        assert result[0]['qualified_name'] == 'Foo::Bar::MyStruct'

        assert len(result[0]['methods']) == 1
        assert result[0]['methods'][0]['qualified_name'] == 'Foo::Bar::MyStruct::my_method'

        assert len(result[0]['fields']) == 1
        assert result[0]['fields'][0]['qualified_name'] == 'Foo::Bar::MyStruct::my_member'


def test_annotations():
    with tempfile.NamedTemporaryFile() as f:
        f.write(b"""
            struct __attribute__((annotate("foo=bar"))) MyStruct {
            };
        """)
        f.file.flush()

        frontend = get_frontend_by_name("cpp")
        result = frontend.run(f.name)

        assert len(result) == 1
        assert result[0]['annotations'].get("foo") == "bar"
