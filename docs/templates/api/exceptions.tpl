{% for exc in exceptions %}
## {{ exc.name }}

Bases: {% for name in exc.bases -%}
    [{{ name }}](#{{ name | lower }})
    {%- if not loop.last %}, {% endif %}
{%- endfor %}

{{ exc.doc }}
{% endfor %}
