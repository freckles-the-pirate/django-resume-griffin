from django.db import models
from datetime import date

from griffin.fuzzy_date import FuzzyDate
from griffin.fields import FuzzyDateInput

import logging, pprint
logger = logging.getLogger('to_terminal')

class FuzzyDateField(models.DateField):

    def __init__(self, *args, **kwargs):
        """ A date field that contains just the month and the year, but
        not the day.
        """
        #logger.debug("Creating new FuzzyDateField.")
        #logger.debug(" - args: %s"%(', '.join(args)))
        #logger.debug(" - kwargs: %s"%(kwargs))
        super(FuzzyDateField, self).__init__( *args, **kwargs)

    def deconstruct(self, *args, **kwargs):
        deconstructed = super(FuzzyDateField, self).deconstruct()
        logger.debug("Deconstructed FuzzyDateField is" + 
                pprint.pformat(deconstructed))
        return (
            deconstructed[0],
            'django.db.models.DateField',
            deconstructed[2],
            deconstructed[3],
        )

    def to_python(self, value):
        logger.debug("FuzzyDateField -> python: %s"%value)
        return FuzzyDate.from_sql(value)
    
    def formfield(self, **kwargs):
        defaults = {'form_class': FuzzyDateInput, }
        defaults.update(kwargs)
        return super(FuzzyDateField, self).formfield(**defaults)

    def get_prep_value(self, value):
        logger.debug("Prep value type is %s"%type(value))
        if not value:
            return
        return value.as_sql()
