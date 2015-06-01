from django.db import models
from django.utils.translation import ugettext_lazy as _

from polymorphic import PolymorphicModel, PolymorphicManager
from phonenumber_field.modelfields import PhoneNumberField
import phonenumbers
from django.utils.html import mark_safe

from django.db.models.loading import cache as model_cache

import logging
logger = logging.getLogger('test_logger')

import pprint

from griffin.managers.contactfield import ContactFieldManager

APP_LABEL = 'griffin'

class ContactFieldModel(PolymorphicModel):

    field_type = models.CharField(max_length=20, blank=False, null=True,
            help_text=_("Type of contact field, e.g. \"Home\", \"Business\"," +
                " etc."))

    entity = models.ForeignKey('Entity',
            related_query_name='contactfield')

    objects = PolymorphicManager()

    def __init__(self, *args, **kwargs):
        super(ContactFieldModel, self).__init__(*args, **kwargs)
        
    def basic_value(self):
        return unicode(self)
    
    def render(self):
        return {
            'field_type' : self.field_type,
            'value' : self.value,
        }
    
    def _render(self, type_id, value):
        return {
            'field_type' : type_id,
            'value' : value,
        }
    
    def get_type(self):
        return self.type_name or None

    class Meta:
        app_label = APP_LABEL
        verbose_name = _("Contact Field")
        verbose_name_plural = _("Contact Fields")

class State(models.Model):
    name = models.CharField(max_length=100)
    abbreviation = models.CharField(max_length=3)

    def __unicode__(self):
        return "%s (%s)"%(self.name, self.abbreviation)

class City(models.Model):
    name = models.CharField(max_length=100)
    state = models.ForeignKey('State', related_name='+')
    zip_code = models.CharField(max_length=11, blank=True, null=True)

    def __unicode__(self):
        return '%s, %s'%(self.name, self.state.abbreviation)

class StreetFieldModel(ContactFieldModel):
    street = models.CharField(max_length=1000, blank=True, null=True)
    city = models.ForeignKey(City, related_name='+')
    type_name="Address"

    @property
    def value(self):
        return self.__unicode__()
    
    def __unicode__(self):
        if self.city.zip_code:
            return "%s %s %s"%(self.street, self.city, self.city.zip_code)
        return "%s %s"%(self.street, self.city)

class EmailFieldModel(ContactFieldModel):

    value = models.EmailField(max_length=200)
    type_name="Email"

    class Meta:
        app_label = APP_LABEL
        verbose_name = _("Email Field")
        verbose_name_plural = _("Email Fields")
        
    def render(self):
        return super(EmailFieldModel, self)._render(
            "Email",
            mark_safe('<a href="mailto:%s">%s</a>'%(self.value, self.value)),
        )
        
    def __unicode__(self):
        return "%s Email: %s"%(self.field_type, self.value)
    
    def __str__(self):
        return unicode(self)

class PhoneFieldModel(ContactFieldModel):

    value = PhoneNumberField(max_length=200)
    type_name="Phone"
    
    def render(self):
        # [+1](123)(4567)"-"(890)
        v = self.basic_value()
        return super(PhoneFieldModel, self)._render(
            "Phone",
            v
        )

    class Meta:
        app_label = APP_LABEL
        verbose_name = _("Phone Field")
        verbose_name_plural = _("Phone Fields")
        
    def basic_value(self):
        return str(phonenumbers.format_number(self.value,
                    phonenumbers.PhoneNumberFormat.NATIONAL))
        
    def __str__(self):
        return unicode(self)
    
    def __unicode__(self):
        return "%s Phone: %s"%(self.field_type, self.value)

class AddressFieldModel(ContactFieldModel):

    street = models.CharField(max_length=200)
    type_name="Address"

    #TODO: make a choice field
    country = models.CharField(max_length=3, blank=False) 

    # TODO: Make a choice field and make it dynamic
    # Can be a state, province, area, etc.
    region = models.CharField(max_length=3, blank=True)

    city = models.CharField(max_length=100, blank=False)

    class Meta:
        app_label = APP_LABEL
        verbose_name = _("Address")
        verbose_name_plural = _("Addresses")

class WebPageFieldModel(ContactFieldModel):

    value = models.URLField()
    type_name="Web page"

    def __init__(self, *args, **kwargs):
        super(WebPageFieldModel, self).__init__(*args, **kwargs)

    def __unicode__(self):
        return "%s's %s Web Page: %s"%(self.entity.name, self.field_type,
                self.value)

    class Meta:
        app_label = APP_LABEL
        verbose_name = _("Web Page")
        verbose_name_plural = _("Web Pages")

class OtherContactFieldModel(ContactFieldModel):

    value = models.CharField(max_length=1000)
    type_name="Other"

    class Meta:
        app_label = APP_LABEL
        verbose_name = _("Other Contact Field")
        verbose_name_plural = _("Other Contact Fields")
