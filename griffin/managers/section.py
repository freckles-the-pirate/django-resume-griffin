from django.db import models

class ResumeSectionManager(models.Manager):
    def __init__(self, entity_instance):
        self.entity_instance = entity_instance
        
    def get_queryset(self):
        from griffin.models.contactfield import ContactFieldModel
        return ContactFieldModel.objects.filter(entity=entity_instance).as_manager()
