from django.template import Library

register = Library()

def mobileadmin_media_prefix():
    """
    Returns the string contained in the setting MOBILEADMIN_MEDIA_PREFIX.
    """
    try:
        from mobileadmin.conf import settings
    except ImportError:
        return ''
    return settings.MEDIA_PREFIX
mobileadmin_media_prefix = register.simple_tag(mobileadmin_media_prefix)
