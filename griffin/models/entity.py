from django.db import models
from django.utils.translation import ugettext_lazy as _
from polymorphic import PolymorphicModel, PolymorphicManager

#from griffin.managers.contactfield import ContactFieldManager
from griffin.models import contactfield

import logging, pprint, os
logger = logging.getLogger('test_contact')

# Create your models here.

class Entity(PolymorphicModel):
    
    objects = PolymorphicManager()
    #contact_fields = ContactFieldManager()

    def __init__(self, *args, **kwargs):
        super(Entity, self).__init__(*args, **kwargs)
        #self.contact_fields = ContactFieldManager(entity=self)
        
    def _get_contactfields(self, klass):
        r = contactfield.ContactFieldModel.objects.filter(entity=self).instance_of(klass)
        logger.debug("Got %s"%(r[:],))
        return r
        
    def get_contactfields(self):
        return self._get_contactfields(contactfield.ContactFieldModel)
    
    def get_streetaddress_fields(self):
        return self._get_contactfields(contactfield.StreetFieldModel)
    
    def get_emailaddress_fields(self):
        return self._get_contactfields(contactfield.EmailFieldModel)
        
    def __unicode__(self):
        s = ''
        contact_fields = contactfield.ContactFieldModel.objects.filter(
            entity=self)
        for cf in contact_fields:
            s = '%s%s\n'%(s, self.cf)
        return s
    
    def __str__(self):
        return unicode(self)

    class Meta:
        app_label='griffin'
        verbose_name = _("Entity")
        verbose_name_plural = _("Entities")

class CorporateEntity(Entity):
    """ An entity that's made up of people. Used to differentiate schools
    and businesses against people and applicants.
    """
    
    def __unicode__(self):
        return '%s'%super(CorporateEntity, self)
    
    def __str__(self):
        return unicode(self)

    class Meta:
        app_label = 'griffin'
        verbose_name = _('Corporate Entity')
        verbose_name_plural = _('Corporate Entities')

class SingleEntity(Entity):
    """ An entity that's a single person to itself.
    """

    class Meta:
        app_label = 'griffin'
        verbose_name = _('Single Entity')
        verbose_name_plural = _('Single Entities')

class Person(SingleEntity):

    first_name = models.CharField(max_length=200, blank=False)
    last_name = models.CharField(max_length=200, blank=True)
    title = models.CharField(max_length=200, blank=True)

    class Meta:
        app_label='griffin'
        verbose_name = _("Person")
        verbose_name_plural = _("People")
        
    def __unicode__(self):
        s = "%s %s"%(self.first_name, self.last_name)
        if self.title:
            s = "%s, %s"(s, title)
        contact_fields = contactfield.ContactFieldModel.objects.filter(
            entity=self)
        if (contact_fields.exists()):
            s = s + str([i.basic_value() for i in contact_fields])
        return s
        
    def __str__(self):
        return unicode(self)

class Applicant(Person):
    """ A person who has created a resume.
    
    :attr user: A Django user that has created the resume.
    :type user: django.contrib.auth.models.User
    
    """

    from django.contrib.auth.models import User

    user = models.OneToOneField(User, blank=False, null=False)

    class Meta:
        app_label='griffin'
        verbose_name = _("Applicant")
        verbose_name_plural = _("Applicants")
        
class Company(CorporateEntity):
    name = models.CharField(max_length=400)
    
    def __unicode__(self):
        s = '%s'%self.name
        contact_fields = contactfield.ContactFieldModel.objects.filter(
            entity=self)
        if len(contact_fields) > 0:
            s = s + ' [' + ','.join(['%s'%cf.value for cf in contact_fields]) \
                    + ']'
        return s
 
    def __str__(self):
        return unicode(self)

    class Meta:
        app_label='griffin'
        verbose_name = _("Company")
        verbose_name_plural = _("Companies")

class School (CorporateEntity):
    name = models.CharField(max_length=200)
    
    def __unicode__(self):
        return "%s - %s"%(self.name, self.get_streetaddress_fields())

    class Meta:
        app_label='griffin'
        verbose_name = _("School")
        verbose_name_plural = _("Schools")

class Project(CorporateEntity):
    """ Can be a landed entity, such as a volunteering project, or a non-landed
    entity, such as django project...hint hint.
    """
    name = models.CharField(max_length=200)
    description = models.TextField(blank=True, null=True)
    web_pages = models.ManyToManyField('WebPageFieldModel', blank=True,
                                       null=True)
    did_start = models.BooleanField(help_text=_('I started this project'),
                                    default=False)
    did_contribute = models.BooleanField( default=False,
        help_text=_('I contributed to this project'))

    class Meta:
        app_label='griffin'
        verbose_name = _("Project")
        verbose_name_plural = _("Projects")
