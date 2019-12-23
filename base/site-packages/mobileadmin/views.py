from django import template
from django.http import HttpResponseRedirect, HttpResponseNotFound, HttpResponseServerError
from django.views import defaults
from django.shortcuts import render_to_response
from django.core.exceptions import PermissionDenied
from django.template import Context, RequestContext, loader
from django.utils.translation import ugettext, ugettext_lazy as _

from mobileadmin import utils

def auth_add_view(self, request):
    if not self.has_change_permission(request):
        raise PermissionDenied
    template_list = ['admin/auth/user/add_form.html']
    user_agent = utils.get_user_agent(request)
    if user_agent:
        template_list = [
            'mobileadmin/%s/auth/user/add_form.html' % user_agent,
        ] + template_list
    if request.method == 'POST':
        form = self.add_form(request.POST)
        if form.is_valid():
            new_user = form.save()
            msg = _('The %(name)s "%(obj)s" was added successfully.') % {'name': 'user', 'obj': new_user}
            self.log_addition(request, new_user)
            if "_addanother" in request.POST:
                request.user.message_set.create(message=msg)
                return HttpResponseRedirect(request.path)
            elif '_popup' in request.REQUEST:
                return self.response_add(request, new_user)
            else:
                request.user.message_set.create(message=msg + ' ' + ugettext("You may edit it again below."))
                return HttpResponseRedirect('../%s/' % new_user.id)
    else:
        form = self.add_form()
    return render_to_response(template_list, {
        'title': _('Add user'),
        'form': form,
        'is_popup': '_popup' in request.REQUEST,
        'add': True,
        'change': False,
        'has_add_permission': True,
        'has_delete_permission': False,
        'has_change_permission': True,
        'has_file_field': False,
        'has_absolute_url': False,
        'auto_populated_fields': (),
        'opts': self.model._meta,
        'save_as': False,
        'username_help_text': self.model._meta.get_field('username').help_text,
        'root_path': self.admin_site.root_path,
        'app_label': self.model._meta.app_label,
    }, context_instance=template.RequestContext(request))

def page_not_found(request, template_name='404.html'):
    """
    Mobile 404 handler.

    Templates: `404.html`
    Context:
        request_path
            The path of the requested URL (e.g., '/app/pages/bad_page/')
    """
    user_agent = utils.get_user_agent(request)
    if user_agent:
        template_list = (
            'mobileadmin/%s/404.html' % user_agent,
            template_name,
        )
        return HttpResponseNotFound(loader.render_to_string(template_list, {
            'request_path': request.path,
        }, context_instance=RequestContext(request)))
    return defaults.page_not_found(request, template_name)

def server_error(request, template_name='500.html'):
    """
    Mobile 500 error handler.

    Templates: `500.html`
    Context: None
    """
    user_agent = utils.get_user_agent(request)
    if user_agent:
        template_list = (
            'mobileadmin/%s/500.html' % user_agent,
            template_name,
        )
        return HttpResponseServerError(loader.render_to_string(template_list))
    return defaults.server_error(request, template_name)
