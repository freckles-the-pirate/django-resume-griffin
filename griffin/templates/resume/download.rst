
=======================================
{{ resume.applicant.first_name }}
=======================================

.. include <isonum.txt>

Basic Info
===========

{% for e in resume.applicant.get_contactfields.all %}
    {{ e }}
{% endfor %}

Skills
=======

{% for s in resume.get_all_skills %}
* {{ s.name }}{% endfor %}
    
Work History
============

{% for a in resume.position_set.all %}

{{ a.title }} {% if a.corporate_entity %}| {% for s in a.corporate_entity.get_streetaddress_fields %}{{ s.city }}{% endfor %}{% endif %}
------------------------------------------------------------------------------

{{ a.duties }}

{% endfor %}

Education
==========

{% for e in resume.all_education %}

{{ e.corporate_entity.name }} {% if e.corporate_entity %}| {% for s in e.corporate_entity.get_streetaddress_fields %}{{ s.city }}{% endfor %}{% endif %}
-----------------------------------------------------------

{% if e.date_end %}
Graduated {{ e.date_end|date:"F Y" }} {% if e.degree %} with a **{{ e.degree }}** in **{{ e.major }}** {% endif %}
{% endif %}

{% endfor %}

Projects
========
{% for p in resume.all_goblin_projects.all %}
{% if p %}
{% if p.project.status.status == "Public" %}
{{ p.project.name|escape }}
--------------------------------------------------
{{ p.project.description|escape }}
{% for u in p.project.projectlink_set.all %}
* `{{p.project.name}}: {{ u.type }} <{{ u.url }}>`_
{% endfor %}
{% endif %}
{% endif %}
{% endfor %}

Contributions
==============
{% for p in resume.all_goblin_projects.all %}
{% if p %}
{% if p.project.status.status == "Contribution" %}
{{ p.project.name|escape }}
--------------------------------------------------
{{ p.project.description|escape }}
{% for u in p.project.projectlink_set.all %}
* `{{p.project.name}}: {{ u.type }} <{{ u.url }}>`_
{% endfor %}
{% endif %}
{% endif %}
{% endfor %}