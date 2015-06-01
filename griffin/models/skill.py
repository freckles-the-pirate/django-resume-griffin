from django.db import models
from mptt.models import MPTTModel, TreeForeignKey
from datetime import date, timedelta
from django.utils.safestring import mark_safe
from django.utils.translation import ugettext_lazy as _
from django import template

from griffin.models.resume import Resume

import logging, pprint, os
logger = logging.getLogger('test_logger')

register=template.Library()

class Skill(MPTTModel):
    name = models.CharField(max_length=50, unique=True)
    description = models.TextField(max_length=1000, blank=True, null=True)
    parent = TreeForeignKey('self', null=True, blank=True,
                            related_name='children', db_index=True)

    def __unicode__(self):
        if self.parent:
            return "%s > %s"%(self.parent, self.name)
        return "%s"%self.name

    class MPTTMeta:
        order_insertion_by = ['name']

    class Meta:
        app_label='griffin'
        verbose_name = _("Skill")
        verbose_name_plural = _("Skills")

class SkillRatio(models.Model):
    resume = models.ForeignKey('Resume')
    skill = models.ForeignKey('Skill')
    days_attended = models.IntegerField(blank=True, null=True)
    ratio = models.IntegerField(blank=True, null=True)