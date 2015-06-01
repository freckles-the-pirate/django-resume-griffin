
=======================================
{{ resume.applicant.first_name }}
=======================================

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

{{ a.title }}
-------------------------------------------------

{{ a.duties }}

{% endfor %}

Education
==========

{% for e in education %}

{{ e.corporate_entity.name }}
-----------------------------------------------------------

{% if e.date_end %}
Graduated {{ a.date_end|date:"F Y" }} {% if e.degree %} with a **{{ e.degree }}** in **{{ e.major }}** {% endif %}
{% endif %}

{% endfor %}

Projects
========
{% for p in projects %}
{% with pr=p.project %}
{{ pr.name }}
----------------------------------------------------------------------------
{% for u in pr.url_set %}
:{{ u.type}}:
    {{ u.url }}
{% endfor %}
{{ pr.description }}
{% endwith %}
{% endfor %}