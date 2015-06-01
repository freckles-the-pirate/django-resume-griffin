from django.db import models
#from griffin.models.skill import Skill

#class ResumeSkillManager(models.Manager):

    #def get_queryset(self):
        #r = super(ResumeSkillManager, self).get_queryset()
        #skills = models.query.QuerySet()
        #for resume in r.all():
            #attendnace_set = resume.attendance_set
            #skills = Skill.objects.filter(attendance_set=attendance_set)
        #return skills

class PositionManager(models.Manager):

    def __init__(self, resume, *args, **kwargs):
        self.resume = resume
        super(PositionManager, self).__init__(*args, **kwargs)

    def get_queryset(self):
        from griffin.models.attendance import Position
        return self.resume.attendance_set.instance_of(Position)
