{% for client in clients %}
## {{ client.name }}

{{ client.doc }}

{% for method in client.methods %}
### {{ client.name }}.**{{ method.name }}**()

{{ method.doc }}
{%- endfor %}

{% for resource in client.resources %}
### {{ client.name }}.**{{ resource.name }}**

{{ resource.doc }}

{% for method in resource.methods %}
### {{ client.name }}.{{ resource.name }}.**{{ method.name }}**()

{{ method.doc }}

{% if method.params %}
Parameters:

{% for param in method.params %}
* `{{ param.name }}` - {{ param.description }}{% if param.required %} (required){% endif %}.
{%- endfor %}
{% endif %}

{%- endfor %}
{%- endfor %}

{% endfor %}
