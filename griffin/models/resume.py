if __name__ == '__main__' and __package__ is None:
    from os import sys, path
    sys.path.append(path.dirname(path.dirname(path.abspath(__file__))))

from django.db import models
from django.utils.translation import ugettext_lazy as _
from polymorphic import PolymorphicModel

from griffin.managers.resume import *
#from griffin.models.skill import Skill

APP_LABEL = 'griffin'

import logging, pprint, os
logger = logging.getLogger('test_logger')

GOBLIN_URL='https://pypi.python.org/pypi/django-project-goblin/'
try:
    import goblin
    goblin_available = True
except ImportError as ie:
    logger.debug("Project Goblin <%s>"%GOBLIN_URL +
        "Has not been installed, so the GoblinProject model will not be " +
        "available.")
    goblin_available = True

class Resume(models.Model):
    """
    @brief A document that shows work and education history.
    
    :attr applicant: A person that has published the resume.
    :type applicant: griffin.models.entity.Applicant
    
    :attr objective: Why the person has uploaded the resume.
    :type objective: str
    """
    
    applicant = models.ForeignKey('Applicant', related_query_name="resume")
    objective = models.TextField('Objective', blank=True, null=True,
            help_text="What do you want your focus to be?")
    
    def get_all_skills(self):
        from griffin.models.attendance import Attendance
        all_skills = []
        for attendance in Attendance.objects.filter(resume=self):
            for skill in attendance.skills.all():
                if skill not in all_skills:
                    all_skills.append(skill)
        return all_skills
    
    def all_goblin_projects(self):
        from griffin.models.attendance import GoblinProject
        return self.attendance_set.instance_of(GoblinProject)
    
    def all_projects(self):
        from griffin.models.attendance import Project
        return self.attendance_set.instance_of(Project)
    
    def get_absolute_url(self):
        return '/resume/%d'%self.pk

    def __init__(self, *args, **kwargs):
        super(Resume, self).__init__(*args, **kwargs)
        self.position_set = PositionManager(self)
    
    def __unicode__(self):
        if self.applicant.last_name:
            return "%s %s's Resume"%(self.applicant.first_name, 
                self.applicant.last_name)
        return "%s's Resume"%(self.applicant.first_name)
    
    def __str__(self):
        return unicode(self)

    class Meta:
        app_label = APP_LABEL
        verbose_name = _("Resume")
        verbose_name_plural = _("Resumes")
