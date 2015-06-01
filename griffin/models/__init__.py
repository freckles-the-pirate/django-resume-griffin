import sys, os
BASE_DIR=os.path.basename(os.path.abspath(__file__))
from django.conf import settings
sys.path.insert(0, BASE_DIR)
from . import (
    attendance,
    contactfield,
    entity,
    resume,
    skill,
    download,
)
