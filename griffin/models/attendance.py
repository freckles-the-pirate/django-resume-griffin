if __name__ == '__main__' and __package__ is None:
    from os import sys, path
    sys.path.append(path.dirname(path.dirname(path.abspath(__file__))))

from django.db import models
from django.core.exceptions import FieldError
from django.utils.translation import ugettext_lazy as _
from polymorphic import PolymorphicModel

from datetime import date

from griffin.fuzzy_date import FuzzyDate
from griffin.widgets import FuzzyDateWidget
from griffin.models.fields import FuzzyDateField

from griffin.models.skill import Skill

import logging
logger = logging.getLogger('griffin')

import pprint

APP_LABEL = 'griffin'

class Attendance(PolymorphicModel):
    """ If an applicant has attended any entity, this references the entity.
    This is simply to be a superclass for times of employment, when the
    applicant went to school, etc.

    :param resume: The resume associated with attendance. Note this will also
        be associated with a user
    :type resume: Resume
    
    :param corporate_entity: The corporate entity associated with the
        Attendance
    :type corporate_entity: CorporateEntity

    :param date_begin: The start date of the attendance.
    :type date_begin: datetime.date

    :param date_end: The end date of the attendance. If left blank it's assumed
        the applicant is still attending the corporate entity.
    :type date_end: datetime.date
    :optional date_end:

    """

    resume = models.ForeignKey('Resume', related_query_name='attendance')

    title = models.CharField(max_length=1000, blank=True, null=True)
    duties = models.TextField(blank=True, null=True)

    skills = models.ManyToManyField('Skill', blank=True, null=True)
    
    date_begin = None
    date_end = None
    
    def _get_raw_dates(self):
        from django.db import connection
        
        table = self.__class__._meta.db_table
        fields = ('date_begin', 'date_end')
        query = """SELECT date_begin,date_end
        FROM %s
        WHERE attendance_ptr_id=%d"""%(table, self.id)
        
        #logger.debug("Executing \"%s\""%query)
        
        cursor = connection.cursor()
        cursor.execute(query)
        
        row = cursor.fetchone()
        
        return row

    def get_days_attended(self):
        """ Return the total number of days spent at an entity.
        """
        
        (date_begin, date_end) = self._get_raw_dates()
        if not date_begin:
            date_begin = date.today()
        if not date_end:
            date_end = date.today()

        try:
            return (date_end - date_begin).days
        except ValueError as ve:
            logger.error("When getting days attended: %s - %s"%(
                self.date_begin, 
                self.date_end))
            raise ve
        
    def date_range(self, date_format="%b %Y", present="Present", separator=" - "):
        start = self.date_begin.strftime(date_format)
        end=present
        if self.date_end:
            end = self.date_end.strftime(date_format)
        return "%s%s%s"%(start, separator, end)
    
    class Meta:
        app_label = APP_LABEL
        #abstract=True
        verbose_name = _("Atendance")
        verbose_name_plural = _("Atendances")
        
class LocatableAttendance(models.Model):
    corporate_entity = models.ForeignKey('CorporateEntity')
        
    #def __unicode__(self):
        #if self.title: return "%s at %s"%(self.title, self.corporate_entity)
        #else: return "at %s"%(self.corporate_entity)
    
    class Meta:
        app_label = APP_LABEL
        abstract=True
        
class HardAttendance(Attendance):
    date_begin = FuzzyDateField()
    date_end = FuzzyDateField(blank=True, null=True, auto_now=False,
            auto_now_add=False)
    class Meta:
        app_label = APP_LABEL
        abstract=True
        
class SoftAttendance(Attendance):
    date_begin = FuzzyDateField(blank=True, null=True)
    date_end = FuzzyDateField(blank=True, null=True)
    
    def get_days_attended(self):
        if self.date_begin == None and self.date_end == None:
            return 1
        return super(SoftAttendance, self).get_days_attended()
        
    class Meta:
        app_label = APP_LABEL
        abstract = True
        verbose_name = _("Atendance (Soft)")
        verbose_name_plural = _("Atendances (Soft)")
    

class Position(HardAttendance, LocatableAttendance):
    """ A time period where the applicant was employed.
    
    :param managers: people who were managers of the position
    """

    managers = models.ManyToManyField('Person', blank=True, null=True)
    
    def __unicode__(self):
        return '%s at %s'%(self.title, self.corporate_entity)

    class Meta:
        app_label = APP_LABEL
        abstract=False
        verbose_name = _("Position")
        verbose_name_plural = _("Positions")

class Student(HardAttendance, LocatableAttendance):
    """ A time period when an applicant went to a school.
    """
    def __str__(self):
        return "%s: %s"%(self.corporate_entity.name,
                              self.date_range())

    class Meta:
        app_label = APP_LABEL
        abstract=False
        verbose_name = _("School Attended")
        verbose_name_plural = _("Schools Attended")

class CollegeStudent(Student):

    class Meta:
        app_label = APP_LABEL
        abstract=False
        verbose_name = _("College Attended")
        verbose_name_plural = _("College Attended")
        
class AbbreviatedChoice(models.Model):
    name = models.CharField(max_length=100)
    abbreviation = models.CharField(max_length=10)
    
    def __unicode__(self):
        return '%s (%s)'%(self.name, self.abbreviation)
    
    class Meta:
        abstract = True
        app_label = APP_LABEL
        
class Degree(AbbreviatedChoice):
    class Meta:
        app_label = APP_LABEL
        abstract=False
        verbose_name = _("Degree")
        verbose_name_plural = _("Degrees")
        
class Major(AbbreviatedChoice):
    class Meta:
        app_label = APP_LABEL
        abstract=False
        verbose_name = _("Major")
        verbose_name_plural = _("Majors")

class UniversityStudent(Student):

    degree = models.ForeignKey(Degree)
    major = models.ForeignKey(Major)

    class Meta:
        app_label = APP_LABEL
        abstract=False
        verbose_name = _("University Attended")
        verbose_name_plural = _("Universities Attended")

GOBLIN_URL='https://pypi.python.org/pypi/django-project-goblin/'
try:
    import goblin
    goblin_available = True
except ImportError as ie:
    logger.debug("Project Goblin <%s>"%GOBLIN_URL +
        "Has not been installed, so the GoblinProject model will not be " +
        "available.")
    goblin_available = True
    
if goblin_available:
    from goblin.models import Project
    class GoblinProject(SoftAttendance):
        
        project = models.ForeignKey(Project)
        
        def __init__(self, *args, **kwargs):
            super(GoblinProject, self).__init__(*args, **kwargs)
        
        class Meta:
            app_label = 'griffin'
            verbose_name = _("Project (Goblin Plug-in)")
            verbose_name_plural = _("Projects (Goblin Plug-In)")
            
        def __unicode__(self):
            return unicode(self.project)