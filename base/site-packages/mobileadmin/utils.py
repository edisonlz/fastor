import re
from mobileadmin.conf import settings

def get_user_agent(request):
    """
    Checks if the given user agent string matches one of the valid user
    agents.
    """
    name = request.META.get('HTTP_USER_AGENT', None)
    if not name:
        return False
    for platform, regex in settings.USER_AGENTS.iteritems():
        if re.compile(regex).search(name) is not None:
            return platform.lower()
    return False
