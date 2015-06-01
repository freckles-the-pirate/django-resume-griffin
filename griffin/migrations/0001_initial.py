# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings
import phonenumber_field.modelfields
import mptt.fields


class Migration(migrations.Migration):

    dependencies = [
        ('goblin', '__first__'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('contenttypes', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Attendance',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('title', models.CharField(max_length=1000, null=True, blank=True)),
                ('duties', models.TextField(null=True, blank=True)),
            ],
            options={
                'verbose_name': 'Atendance',
                'verbose_name_plural': 'Atendances',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='City',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=100)),
                ('zip_code', models.CharField(max_length=11, null=True, blank=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='ContactFieldModel',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('field_type', models.CharField(help_text='Type of contact field, e.g. "Home", "Business", etc.', max_length=20, null=True)),
            ],
            options={
                'verbose_name': 'Contact Field',
                'verbose_name_plural': 'Contact Fields',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='AddressFieldModel',
            fields=[
                ('contactfieldmodel_ptr', models.OneToOneField(parent_link=True, auto_created=True, primary_key=True, serialize=False, to='griffin.ContactFieldModel')),
                ('street', models.CharField(max_length=200)),
                ('country', models.CharField(max_length=3)),
                ('region', models.CharField(max_length=3, blank=True)),
                ('city', models.CharField(max_length=100)),
            ],
            options={
                'verbose_name': 'Address',
                'verbose_name_plural': 'Addresses',
            },
            bases=('griffin.contactfieldmodel',),
        ),
        migrations.CreateModel(
            name='Degree',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=100)),
                ('abbreviation', models.CharField(max_length=10)),
            ],
            options={
                'abstract': False,
                'verbose_name': 'Degree',
                'verbose_name_plural': 'Degrees',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='EmailFieldModel',
            fields=[
                ('contactfieldmodel_ptr', models.OneToOneField(parent_link=True, auto_created=True, primary_key=True, serialize=False, to='griffin.ContactFieldModel')),
                ('value', models.EmailField(max_length=200)),
            ],
            options={
                'verbose_name': 'Email Field',
                'verbose_name_plural': 'Email Fields',
            },
            bases=('griffin.contactfieldmodel',),
        ),
        migrations.CreateModel(
            name='Entity',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
            ],
            options={
                'verbose_name': 'Entity',
                'verbose_name_plural': 'Entities',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='CorporateEntity',
            fields=[
                ('entity_ptr', models.OneToOneField(parent_link=True, auto_created=True, primary_key=True, serialize=False, to='griffin.Entity')),
            ],
            options={
                'verbose_name': 'Corporate Entity',
                'verbose_name_plural': 'Corporate Entities',
            },
            bases=('griffin.entity',),
        ),
        migrations.CreateModel(
            name='Company',
            fields=[
                ('corporateentity_ptr', models.OneToOneField(parent_link=True, auto_created=True, primary_key=True, serialize=False, to='griffin.CorporateEntity')),
                ('name', models.CharField(max_length=400)),
            ],
            options={
                'verbose_name': 'Company',
                'verbose_name_plural': 'Companies',
            },
            bases=('griffin.corporateentity',),
        ),
        migrations.CreateModel(
            name='GoblinProject',
            fields=[
                ('attendance_ptr', models.OneToOneField(parent_link=True, auto_created=True, primary_key=True, serialize=False, to='griffin.Attendance')),
                ('date_begin', models.DateField(null=True, blank=True)),
                ('date_end', models.DateField(null=True, blank=True)),
            ],
            options={
                'abstract': False,
                'verbose_name': 'Project (Goblin Plug-in)',
                'verbose_name_plural': 'Projects (Goblin Plug-In)',
            },
            bases=('griffin.attendance',),
        ),
        migrations.CreateModel(
            name='Major',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=100)),
                ('abbreviation', models.CharField(max_length=10)),
            ],
            options={
                'abstract': False,
                'verbose_name': 'Major',
                'verbose_name_plural': 'Majors',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='OtherContactFieldModel',
            fields=[
                ('contactfieldmodel_ptr', models.OneToOneField(parent_link=True, auto_created=True, primary_key=True, serialize=False, to='griffin.ContactFieldModel')),
                ('value', models.CharField(max_length=1000)),
            ],
            options={
                'verbose_name': 'Other Contact Field',
                'verbose_name_plural': 'Other Contact Fields',
            },
            bases=('griffin.contactfieldmodel',),
        ),
        migrations.CreateModel(
            name='PhoneFieldModel',
            fields=[
                ('contactfieldmodel_ptr', models.OneToOneField(parent_link=True, auto_created=True, primary_key=True, serialize=False, to='griffin.ContactFieldModel')),
                ('value', phonenumber_field.modelfields.PhoneNumberField(max_length=200)),
            ],
            options={
                'verbose_name': 'Phone Field',
                'verbose_name_plural': 'Phone Fields',
            },
            bases=('griffin.contactfieldmodel',),
        ),
        migrations.CreateModel(
            name='Position',
            fields=[
                ('attendance_ptr', models.OneToOneField(parent_link=True, auto_created=True, primary_key=True, serialize=False, to='griffin.Attendance')),
                ('date_begin', models.DateField()),
                ('date_end', models.DateField(null=True, blank=True)),
            ],
            options={
                'abstract': False,
                'verbose_name': 'Position',
                'verbose_name_plural': 'Positions',
            },
            bases=('griffin.attendance', models.Model),
        ),
        migrations.CreateModel(
            name='Project',
            fields=[
                ('corporateentity_ptr', models.OneToOneField(parent_link=True, auto_created=True, primary_key=True, serialize=False, to='griffin.CorporateEntity')),
                ('name', models.CharField(max_length=200)),
                ('description', models.TextField(null=True, blank=True)),
                ('did_start', models.BooleanField(default=False, help_text='I started this project')),
                ('did_contribute', models.BooleanField(default=False, help_text='I contributed to this project')),
            ],
            options={
                'verbose_name': 'Project',
                'verbose_name_plural': 'Projects',
            },
            bases=('griffin.corporateentity',),
        ),
        migrations.CreateModel(
            name='Resume',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('objective', models.TextField(help_text=b'What do you want your focus to be?', null=True, verbose_name=b'Objective', blank=True)),
            ],
            options={
                'verbose_name': 'Resume',
                'verbose_name_plural': 'Resumes',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='School',
            fields=[
                ('corporateentity_ptr', models.OneToOneField(parent_link=True, auto_created=True, primary_key=True, serialize=False, to='griffin.CorporateEntity')),
                ('name', models.CharField(max_length=200)),
            ],
            options={
                'verbose_name': 'School',
                'verbose_name_plural': 'Schools',
            },
            bases=('griffin.corporateentity',),
        ),
        migrations.CreateModel(
            name='SingleEntity',
            fields=[
                ('entity_ptr', models.OneToOneField(parent_link=True, auto_created=True, primary_key=True, serialize=False, to='griffin.Entity')),
            ],
            options={
                'verbose_name': 'Single Entity',
                'verbose_name_plural': 'Single Entities',
            },
            bases=('griffin.entity',),
        ),
        migrations.CreateModel(
            name='Person',
            fields=[
                ('singleentity_ptr', models.OneToOneField(parent_link=True, auto_created=True, primary_key=True, serialize=False, to='griffin.SingleEntity')),
                ('first_name', models.CharField(max_length=200)),
                ('last_name', models.CharField(max_length=200, blank=True)),
                ('title', models.CharField(max_length=200, blank=True)),
            ],
            options={
                'verbose_name': 'Person',
                'verbose_name_plural': 'People',
            },
            bases=('griffin.singleentity',),
        ),
        migrations.CreateModel(
            name='Applicant',
            fields=[
                ('person_ptr', models.OneToOneField(parent_link=True, auto_created=True, primary_key=True, serialize=False, to='griffin.Person')),
                ('user', models.OneToOneField(to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Applicant',
                'verbose_name_plural': 'Applicants',
            },
            bases=('griffin.person',),
        ),
        migrations.CreateModel(
            name='Skill',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(unique=True, max_length=50)),
                ('description', models.TextField(max_length=1000, null=True, blank=True)),
                ('lft', models.PositiveIntegerField(editable=False, db_index=True)),
                ('rght', models.PositiveIntegerField(editable=False, db_index=True)),
                ('tree_id', models.PositiveIntegerField(editable=False, db_index=True)),
                ('level', models.PositiveIntegerField(editable=False, db_index=True)),
                ('parent', mptt.fields.TreeForeignKey(related_name='children', blank=True, to='griffin.Skill', null=True)),
            ],
            options={
                'verbose_name': 'Skill',
                'verbose_name_plural': 'Skills',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='State',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=100)),
                ('abbreviation', models.CharField(max_length=3)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='StreetFieldModel',
            fields=[
                ('contactfieldmodel_ptr', models.OneToOneField(parent_link=True, auto_created=True, primary_key=True, serialize=False, to='griffin.ContactFieldModel')),
                ('street', models.CharField(max_length=1000, null=True, blank=True)),
                ('city', models.ForeignKey(related_name='+', to='griffin.City')),
            ],
            options={
                'abstract': False,
            },
            bases=('griffin.contactfieldmodel',),
        ),
        migrations.CreateModel(
            name='Student',
            fields=[
                ('attendance_ptr', models.OneToOneField(parent_link=True, auto_created=True, primary_key=True, serialize=False, to='griffin.Attendance')),
                ('date_begin', models.DateField()),
                ('date_end', models.DateField(null=True, blank=True)),
            ],
            options={
                'abstract': False,
                'verbose_name': 'School Attended',
                'verbose_name_plural': 'Schools Attended',
            },
            bases=('griffin.attendance', models.Model),
        ),
        migrations.CreateModel(
            name='CollegeStudent',
            fields=[
                ('student_ptr', models.OneToOneField(parent_link=True, auto_created=True, primary_key=True, serialize=False, to='griffin.Student')),
            ],
            options={
                'abstract': False,
                'verbose_name': 'College Attended',
                'verbose_name_plural': 'College Attended',
            },
            bases=('griffin.student',),
        ),
        migrations.CreateModel(
            name='UniversityStudent',
            fields=[
                ('student_ptr', models.OneToOneField(parent_link=True, auto_created=True, primary_key=True, serialize=False, to='griffin.Student')),
                ('degree', models.ForeignKey(to='griffin.Degree')),
                ('major', models.ForeignKey(to='griffin.Major')),
            ],
            options={
                'abstract': False,
                'verbose_name': 'University Attended',
                'verbose_name_plural': 'Universities Attended',
            },
            bases=('griffin.student',),
        ),
        migrations.CreateModel(
            name='WebPageFieldModel',
            fields=[
                ('contactfieldmodel_ptr', models.OneToOneField(parent_link=True, auto_created=True, primary_key=True, serialize=False, to='griffin.ContactFieldModel')),
                ('value', models.URLField()),
            ],
            options={
                'verbose_name': 'Web Page',
                'verbose_name_plural': 'Web Pages',
            },
            bases=('griffin.contactfieldmodel',),
        ),
        migrations.AddField(
            model_name='student',
            name='corporate_entity',
            field=models.ForeignKey(to='griffin.CorporateEntity'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='resume',
            name='applicant',
            field=models.ForeignKey(related_query_name=b'resume', to='griffin.Applicant'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='project',
            name='web_pages',
            field=models.ManyToManyField(to='griffin.WebPageFieldModel', null=True, blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='position',
            name='corporate_entity',
            field=models.ForeignKey(to='griffin.CorporateEntity'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='position',
            name='managers',
            field=models.ManyToManyField(to='griffin.Person', null=True, blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='goblinproject',
            name='project',
            field=models.ForeignKey(to='goblin.Project'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='entity',
            name='polymorphic_ctype',
            field=models.ForeignKey(related_name='polymorphic_griffin.entity_set', editable=False, to='contenttypes.ContentType', null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='contactfieldmodel',
            name='entity',
            field=models.ForeignKey(related_query_name=b'contactfield', to='griffin.Entity'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='contactfieldmodel',
            name='polymorphic_ctype',
            field=models.ForeignKey(related_name='polymorphic_griffin.contactfieldmodel_set', editable=False, to='contenttypes.ContentType', null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='city',
            name='state',
            field=models.ForeignKey(related_name='+', to='griffin.State'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='attendance',
            name='polymorphic_ctype',
            field=models.ForeignKey(related_name='polymorphic_griffin.attendance_set', editable=False, to='contenttypes.ContentType', null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='attendance',
            name='resume',
            field=models.ForeignKey(related_query_name=b'attendance', to='griffin.Resume'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='attendance',
            name='skills',
            field=models.ManyToManyField(to='griffin.Skill', null=True, blank=True),
            preserve_default=True,
        ),
    ]
