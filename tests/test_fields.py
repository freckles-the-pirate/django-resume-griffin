if __name__ == '__main__' and __package__ is None:
    from os import sys, path
    sys.path.append(path.dirname(path.dirname(path.abspath(__file__))))

from django import test as unittest
from django.contrib.auth.models import User, UserManager

from unittest import skip
from datetime import date

import logging, pprint, os
logger = logging.getLogger('to_terminal')

from griffin.fields import FuzzyDateInput
from griffin.models.fields import FuzzyDateField, FuzzyDate
from griffin.widgets import FuzzyDateWidget

from django.test import Client
from django.core.urlresolvers import reverse

class TestFields(unittest.TestCase):
    def setUp(self):
        pass
    
    def test_fuzzy_date_model_field(self):
        FuzzyDateField()

    def test_fuzzy_date_widget(self):
        """ FuzzyDateWidget decompresses a date string to a [month, year]
        list.
        """
        fdw = FuzzyDateWidget(attrs={'required' : False})
        tests = (
            (None, [None, None]),
            ('', [None, None]),
            (FuzzyDate(9, 2013), [9, 2013]),
        )
        for t in tests:
            decomp = fdw.decompress(t[0])
            self.assertEqual(decomp, t[1])

    def test_fuzzy_date_input(self):
        """ Compression compresses a [month, year] list to a date string.
        """
        fdi = FuzzyDateInput(required=False)

        tests = (
            ([None, None], None),
            ([], None),
            ([9, 2013], FuzzyDate(9,2013)),
        )
        for t in tests:
            comp = fdi.compress(t[0])
            self.assertEqual(comp, t[1])

    def test_fuzzy_date_field(self):
        """ A FuzzyDateField can be assigned a value without anything blowing
        up
        """
        fdf = FuzzyDateField(FuzzyDate(10, 2013))

    def test_fuzzy_date_field_exception(self):
        """ We should not be able to assign an invalid date.
        """
        with self.assertRaises(ValueError):
            fdf = FuzzyDateField(FuzzyDate(59, 2013))
