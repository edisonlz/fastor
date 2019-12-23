import os
from django.conf import settings

# PLEASE: Don't change anything here, use your site settings.py

MEDIA_PATH = os.path.join(os.path.abspath(os.path.dirname(__file__)), '..', 'media')
MEDIA_PREFIX = getattr(settings, 'MOBILEADMIN_MEDIA_PREFIX', '/mobileadmin_media/')
MEDIA_REGEX = r'^%s(?P<path>.*)$' % MEDIA_PREFIX.lstrip('/')

USER_AGENTS = {
    'mobile_safari': r'AppleWebKit/.*Mobile/',
    'blackberry': r'^BlackBerry',
    'opera_mini': r'[Oo]pera [Mm]ini',
}
USER_AGENTS.update(getattr(settings, 'MOBILEADMIN_USER_AGENTS', {}))

TEMPLATE_MAPPING = {
    'index': ('index_template', 'index.html'),
    'display_login_form': ('login_template', 'login.html'),
    'app_index': ('app_index_template', 'app_index.html'),
    'render_change_form': ('change_form_template', 'change_form.html'),
    'changelist_view': ('change_list_template', 'change_list.html'),
    'delete_view': ('delete_confirmation_template', 'delete_confirmation.html'),
    'history_view': ('object_history_template', 'object_history.html'),
    'logout': ('logout_template', 'registration/logged_out.html'),
    'password_change': ('password_change_template', 'registration/password_change_form.html'),
    'password_change_done': ('password_change_done_template', 'registration/password_change_done.html'),
}
TEMPLATE_MAPPING.update(getattr(settings, 'MOBILEADMIN_TEMPLATE_MAPPING', {}))
