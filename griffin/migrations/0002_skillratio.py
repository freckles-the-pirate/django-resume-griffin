# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('griffin', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='SkillRatio',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('days_attended', models.IntegerField(null=True, blank=True)),
                ('ratio', models.IntegerField(null=True, blank=True)),
                ('resume', models.ForeignKey(to='griffin.Resume')),
                ('skill', models.ForeignKey(to='griffin.Skill')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
