if __name__ == '__main__' and __package__ is None:
    from os import sys, path
    sys.path.append(path.dirname(path.dirname(path.abspath(__file__))))

from unittest import skip
from datetime import date

from django import test as unittest
from django.test import Client
from django.contrib.auth.models import User, UserManager
from django.core.urlresolvers import reverse
from django.contrib.auth.models import User

import logging, pprint, os
logger = logging.getLogger('griffin')

from griffin.templatetags import resume
from griffin.models.resume import Resume
from griffin.models.entity import Applicant
from griffin.models.download import ResumeDownload, DownloadFormat

class TestTemplateTags(unittest.TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create()
        self.applicant = Applicant.objects.create(user=self.user)
        self.resume = Resume.objects.create(applicant=self.applicant)
        
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

    def test_resume_links_simple(self):
        out_set = list(resume._download_links(self.resume))
        self.assertEqual(len(out_set), 2) # should have 2 "formats" + ul and /ul
        logger.debug("Links: %s"%(out_set,))
        
    def test_resume_links_special(self):
        out_set = list(resume._download_links(self.resume, 'pdf'))
        self.assertEqual(len(out_set), 1) # should have 2 "formats" + ul and /ul
        logger.debug("Links: %s"%(out_set,))