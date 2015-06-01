from django import template
from django.conf import settings
from django.core.urlresolvers import reverse
from griffin.models.skill import SkillRatio
from griffin.models.attendance import Attendance
from griffin.models.contactfield import ContactFieldModel
register = template.Library()

import logging
logger = logging.getLogger("griffin")

@register.simple_tag
def skill_fontsize(skill, resume, min_size=10.0, max_size=30.0, units='pt'):
    min_size = float(min_size)
    max_size = float(max_size)
    ratio = float(SkillRatio.objects.get(skill=skill, resume=resume).ratio)
    font_size = ((max_size-min_size)*(ratio/100.0))+min_size
    return 'font-size: %d%s;'%(font_size, units)

@register.filter
def get_contactfields(value, arg=None):
    """
    @brief Get all the contact fields of the corporate entity.
    
    :param corporate_entity: The corporate entity from which we want to get
    the contact fields.
    :type contactfields: CorporateEntity
    
    :param contactfield_type: The type of contactfield we want to obtain. None
    will return all the contact field types.
    :type contactfield: str.
    
    :returns: A list of contact fields, if any are found.
    """
    cfs = []
    contactfields = ContactFieldModel.objects.filter(entity=value)
    for contactfield in contactfields:
        if arg is not None:
            if arg in contactfield.__class__.__name__:
                cfs.append(contactfield)
        cfs.append(contactfield)
    return cfs

def _download_links(resume, *formats):
    from griffin.models.download import ResumeDownload
    downloads = ResumeDownload.objects.filter(resume=resume)
    for d in downloads:
        if (len(formats) == 0) or d.format.extension in formats:
            yield d.as_link_item()
        
@register.simple_tag
def resume_download_links(resume, *formats):
    """ Get a set of resume download links.
    
    :param resume: Resume for which we want the download links.
    :type resume: griffin.models.resume.Resume
    
    :param *formats: A list of formats to which we want to convert.
    :type *formats: str
    """
    return '\n'.join(list(_download_links(resume, *formats)))