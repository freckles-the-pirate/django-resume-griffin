from django.db import models

from polymorphic import PolymorphicModel, PolymorphicManager, PolymorphicQuerySet

import logging, pprint, os
logger = logging.getLogger('test_contact')

class ContactFieldManager(PolymorphicManager):

    def __init__(self, entity, *args, **kwargs):
        return super(ContactFieldManager, self).__init__(*args, **kwargs)
        self.entity = entity
    
    def get_queryset(self):
        from griffin.models.contactfield import ContactFieldModel
        return ContactFieldModel.objects.filter( entity=self.entity )
