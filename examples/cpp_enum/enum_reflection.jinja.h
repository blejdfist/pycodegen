#include <array>

template<typename T>
struct enum_info {};

{% for enum in enums %}
template<>
struct enum_info<{{ enum.qualified_name }}>
{
    using underlying_type = {{ enum.underlying_type }};

    static const char* name(const {{ enum.qualified_name }} value)
    {
        switch (value) {
        {%- for name, _ in enum.enum_values.items() %}
            case {{ enum.qualified_name }}::{{ name }}: return "{{ name }}";
        {%- endfor %}
        }

        return "<unknown>";
    }

    static const char* qualified_name(const {{ enum.qualified_name }} value)
    {
        switch (value) {
        {%- for name, _ in enum.enum_values.items() %}
            case {{ enum.qualified_name }}::{{ name }}: return "{{ enum.qualified_name }}::{{ name }}";
        {%- endfor %}
        }

        return "<unknown>";
    }
};
{% endfor %}
