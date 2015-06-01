from django.core.management.base import BaseCommand, CommandError
from griffin.models.resume import Resume
from griffin.models.skill import Skill, SkillRatio

from griffin.utils.skill_ratio import calculate_skill_ratios

class Command(BaseCommand):
    args = '[resume_id, resume_id, ...]'
    help = 'Syncronizes the skill ratios for the given resumes'

    def handle(self, *args, **options):
        if len(args) == 0:
            resumes = Resume.objects.all()
        for resume_pk in args:
            resumes.append(Resume.objects.get(resume__pk=resume_pk))
            
        for resume in resumes:
            self.stdout.write("Updating skill ratios for %s"%resume)
            calculate_skill_ratios(resume)