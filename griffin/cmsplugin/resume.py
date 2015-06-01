# -*- coding: utf-8 -*-

from django.db import models

from cms.models import CMSPlugin

class GriffinPluginModel(CMSPlugin):
    resume = models.ForeignKey('griffin.modesl.resume.Resume', related_name='plugins')

    def __unicode__(self):
        return str(self.resume)
