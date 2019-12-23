from mobileadmin.utils import get_user_agent

def user_agent(request):
    return {'user_agent': get_user_agent(request)}
