from griffin.models import attendance
from griffin.models.skill import Skill, SkillRatio
from django.db import connection

import django

def get_max_days_attended(resume):
    db_name = SkillRatio._meta.db_table
    query = "SELECT MAX(days_attended) FROM %s"%(db_name)
    cursor = connection.cursor()
    cursor.execute(query)
    
    return cursor.fetchone()[0]

def calculate_skill_ratios(resume):
    for a in attendance.Attendance.objects.filter(resume=resume):
        for skill in a.skills.all():
            try:
                sr = SkillRatio.objects.get(resume__pk=resume.pk, skill__pk=skill.pk)
            except SkillRatio.DoesNotExist as e:
                sr = SkillRatio.objects.create(resume=resume, skill=skill)
            sr.days_attended = (sr.days_attended or 0) + a.get_days_attended()
            sr.save()
    max_attended = get_max_days_attended(resume)
    for sr in SkillRatio.objects.filter(resume=resume):
        ratio = (float(sr.days_attended) / float(max_attended)) * 100.0
        sr.ratio = ratio
        sr.save()