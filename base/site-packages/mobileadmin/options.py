from django.contrib.admin import options
from mobileadmin import decorators

class MobileModelAdmin(options.ModelAdmin):
    """
    A custom model admin class to override the used templates depending on the
    user agent of the request.
    
    Please use it in case you want to create you own mobileadmin.
    """
    def render_change_form(self, request, context, add=False, change=False, form_url='', obj=None):
        return super(MobileModelAdmin, self).render_change_form(request, context, add, change, form_url, obj)
    render_change_form = decorators.mobile_templates(render_change_form)

    def changelist_view(self, request, extra_context=None):
        return super(MobileModelAdmin, self).changelist_view(request, extra_context)
    changelist_view = decorators.mobile_templates(changelist_view)

    def delete_view(self, request, object_id, extra_context=None):
        return super(MobileModelAdmin, self).delete_view(request, object_id, extra_context)
    delete_view = decorators.mobile_templates(delete_view)

    def history_view(self, request, object_id, extra_context=None):
        return super(MobileModelAdmin, self).history_view(request, object_id, extra_context)
    history_view = decorators.mobile_templates(history_view)

class MobileStackedInline(options.StackedInline):
    template = 'edit_inline/stacked.html'

class MobileTabularInline(options.InlineModelAdmin):
    template = 'edit_inline/tabular.html'
