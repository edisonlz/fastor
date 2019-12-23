import re
from django import template
from django.template.loader import render_to_string
register = template.Library()

admin_re = re.compile(r'^admin\/')

def prepopulated_fields_js(context):
    """
    Creates a list of prepopulated_fields that should render Javascript for
    the prepopulated fields for both the admin form and inlines.
    """
    prepopulated_fields = []
    if context['add'] and 'adminform' in context:
        prepopulated_fields.extend(context['adminform'].prepopulated_fields)
    if 'inline_admin_formsets' in context:
        for inline_admin_formset in context['inline_admin_formsets']:
            for inline_admin_form in inline_admin_formset:
                if inline_admin_form.original is None:
                    prepopulated_fields.extend(inline_admin_form.prepopulated_fields)
    context.update({'prepopulated_fields': prepopulated_fields})
    return context
prepopulated_fields_js = register.inclusion_tag('admin/prepopulated_fields_js.html', takes_context=True)(prepopulated_fields_js)

def mobile_inline_admin_formset(inline_admin_formset, user_agent):
    template_name = inline_admin_formset.opts.template
    if admin_re.match(template_name):
        # remove admin/ prefix to have a clean template name
        template_name = admin_re.sub('', template_name)
    return render_to_string((
        'mobileadmin/%s/%s' % (user_agent, template_name),
        'mobileadmin/%s' % template_name,
        'admin/%s' % template_name,
    ), {
        'inline_admin_formset': inline_admin_formset,
        'user_agent': user_agent,
    })
register.simple_tag(mobile_inline_admin_formset)

def mobile_inline_admin_fieldset(fieldset, user_agent):
    return render_to_string((
        'mobileadmin/%s/includes/fieldset.html' % user_agent,
        'mobileadmin/includes/fieldset.html',
        'admin/includes/fieldset.html',
    ), {
        'fieldset': fieldset,
    })
register.simple_tag(mobile_inline_admin_fieldset)
