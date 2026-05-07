from textwrap import dedent

INPUT_DATA = [
    {"name": "Alice", "role": "admin"},
    {"name": "Bob", "role": "user"},
]


def test_full_generation(driver):
    result = driver(INPUT_DATA, frontend="json").render(dedent("""\
        {% for item in items -%}
        Name: {{ item.name }}
        Role: {{ item.role }}
        {% endfor %}
    """))

    assert result == dedent("""\
        Name: Alice
        Role: admin
        Name: Bob
        Role: user
    """)


def test_generation_with_filter(driver):
    result = driver(INPUT_DATA, frontend="json").render(dedent("""\
        {% for item in items -%}
        {{ item.name | upper }}: {{ item.role }}
        {% endfor %}
    """))

    assert result == dedent("""\
        ALICE: admin
        BOB: user
    """)
