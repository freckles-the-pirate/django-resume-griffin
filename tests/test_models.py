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
from griffin.models.download import *
from griffin.models.fields import FuzzyDate

import logging, pprint, os
logger = logging.getLogger('to_terminal')

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
        
        self.addresses = {}
        
        self.addresses['mozilla'] = StreetFieldModel.objects.create(
            city=City.objects.create(name="New York",
                state=State.objects.create(name="NY")
            ),
            entity=self.companies['mozilla']
        )
            
        self.addresses['redhat'] = StreetFieldModel.objects.create(
            city=City.objects.create(name="Dallas",
                state=State.objects.create(name="TX")
            ),
            entity=self.companies['redhat']
        )

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

        for company,start,end in pos_list:
            self.positions.update({
                company : Position.objects.create(resume=self.resume,
                    corporate_entity=self.companies[company],
                    date_begin=start, date_end=end),})

        skill_assignments = {
            'c' : ('mozilla', 'redhat',),
            'python' : ('django',), # Obviously!
            'coffee' : ('mozilla', 'redhat', 'django',),
        }

        for (skill,companies) in skill_assignments.items():
            for company in companies:
                self.skills[skill].attendance_set.add(self.positions[company])
        
        self.format_pdf = DownloadFormat.objects.create(
                description='PDF',
                extension='pdf'
            )
        self.format_odt = DownloadFormat.objects.create(
                description='LibreOffice Document',
                extension='odt'
            )
        self.download_pdf = ResumeDownload.objects.create(resume=self.resume, format=self.format_pdf)
        self.download_odt = ResumeDownload.objects.create(resume=self.resume, format=self.format_odt)


    def test_relations(self):
        self.assertEqual(self.resume.attendance_set.count(), 3)
        self.assertEqual(self.resume.position_set.count(), 3)

    def test_street_address(self):
        california = State.objects.create(name="California", abbreviation="CA")
        massachusetts = State.objects.create(name="Massachusetts",
                                             abbreviation="MA")
        sacramento = City.objects.create(name="Sacramento", state=california)
        boston = City.objects.create(name="Boston", state=massachusetts)

        self.assertEqual(str(sacramento), "Sacramento, CA")
        self.assertEqual(str(boston), "Boston, MA")
    
    def test_relations_2(self):
        self.assertEqual(len(self.resume.get_all_skills()), 3)
        
    def test_contactfields(self):
        self.assertEqual(len(self.companies['mozilla'].get_streetaddress_fields()), 1)
        
    def test_download(self):
        downloads = ResumeDownload.objects.filter(resume=self.resume)
        self.assertEqual(len(downloads), 2)
