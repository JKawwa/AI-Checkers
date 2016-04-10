{{ fullname }}
{{ underline }}

.. currentmodule:: {{ module }}

.. autoclass:: {{ objname }}


   {% block attributes %}
   {% if attributes %}
   .. rubric:: Attributes

   .. autosummary::
      :toctree:
   {% for item in attributes %}
      ~{{ name }}.{{ item }}
   {%- endfor %}
   {% endif %}
   {% endblock %}

   {% block methods %}
   ..	.. automethod:: __init__

   {% if methods %}
   .. rubric:: Methods

   .. autosummary::
      :toctree:
   {% for item in methods %}
   {% if not item == "__init__" %}
      ~{{ name }}.{{ item }}
   {% endif %}
   {%- endfor %}
   {% endif %}
   {% endblock %}

   {% if attributes %}

   {% for item in attributes %}
   .. autoattribute:: {{ name }}.{{ item }}
      :noindex:
   {%- endfor %}

   {% endif %}

   {% if methods %}

   {% for item in methods %}
   {% if not item == "__init__" %}
   .. automethod:: {{ name }}.{{ item }}
      :noindex:
   {% endif %}
   {%- endfor %}

   {% endif %}
