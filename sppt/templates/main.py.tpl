
{% if executable %}
def {{executable_entry_point.split(":")|last}}():
    pass
{% endif %}

