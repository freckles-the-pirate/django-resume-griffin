if __name__ == '__main__' and __package__ is None:
    from os import sys, path
    sys.path.append(path.dirname(path.dirname(path.abspath(__file__))))

from django import test as unittest
from django.contrib.auth.models import User, UserManager

from unittest import skip
from datetime import date


from griffin.models.contactfield import *
from griffin.models.entity import *
from griffin.models.resume import *
from griffin.models.attendance import *
from griffin.models.skill import *
from griffin.models.fields import FuzzyDate

from griffin.utils import skill_ratio

from django.db import connection

import logging, pprint, os
logger = logging.getLogger('griffin')

class TestModels(unittest.TestCase):

    def setUp(self):
        self.user = User.objects.create() 
        self.user.username='test_user'

        self.person = Person.objects.create(first_name='Simon',
                last_name='Willison')

        self.applicant = Applicant.objects.create(first_name='Simon',
                last_name='Willison', user=self.user)

        self.companies = {
            'mozilla' : Company.objects.create(name='Mozilla'),
            'redhat' : Company.objects.create(name='Red Hat'),
            'django' : Company.objects.create(name='Django'),
        }

        self.skills = {
            'python' : Skill.objects.create(name='Python'),
            'c' : Skill.objects.create(name='C'),
            'coffee' : Skill.objects.create(name='Drinking Coffee'),
        }

        self.resume = Resume.objects.create(applicant=self.applicant,
                objective="To test a resume!")
        
        pos_list = (
            ('mozilla', FuzzyDate(1, 1999), FuzzyDate(2, 2001),),
            ('redhat', FuzzyDate(2, 2001), FuzzyDate(4, 2008),),
            ('django', FuzzyDate(4, 2008), None),
        )

        self.positions = {}
        
        self.skill_days = {}

        skill_assignments = {
            'c' : ('mozilla', 'redhat',),
            'python' : ('django',), # Obviously!
            'coffee' : ('mozilla', 'redhat', 'django',),
        }

        for company,start,end in pos_list:
            self.positions.update({
                company : Position.objects.create(resume=self.resume,
                    corporate_entity=self.companies[company],
                    date_begin=start, date_end=end),})
            for (skill,comp) in skill_assignments.items():
                if company in comp:
                    da = self.positions[company].get_days_attended()
                    
                    self.skill_days[skill] = self.skill_days.pop(skill, 0) + da
        
        # Days attended
        # mozilla: 760
        # redhat: 2615
        # c: 3375
        # coffee: 3375

        for (skill,companies) in skill_assignments.items():
            for company in companies:
                self.skills[skill].attendance_set.add(self.positions[company])
                
    def test_skillratio_initialize(self):
        skill_ratio.calculate_skill_ratios(self.resume)
        logger.debug("\bDays attended:")
        expected_max = 0
        for (s,d) in self.skill_days.items():
            if int(d) > expected_max:
                expected_max = int(d)
            logger.debug("%-30s %d"%(s,d))
            
        logger.debug("Database results: ")
        for sr in SkillRatio.objects.filter(resume=self.resume):
            logger.debug("%-30s %-10d %-10d"%(sr.skill.name, sr.days_attended,
                                     sr.ratio))
        
        max_days = skill_ratio.get_max_days_attended(self.resume)
        self.assertEqual(max_days, expected_max)
