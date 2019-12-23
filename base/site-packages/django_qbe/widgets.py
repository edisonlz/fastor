# -*- coding: utf-8 -*-
from django.forms.util import flatatt
from django.forms.widgets import MultiWidget, Select, TextInput, Widget
from django.utils.safestring import mark_safe
from django.utils.translation import ugettext as _


OPERATOR_CHOICES = (
    ('', ''),
    ('exact', _('is equal to')),
    ('contains', _('contains')),
    ('regex', _('matchs regex')),
    ('startswith', _('starts with')),
    ('endswith', _('ends with')),
    ('gt', _('is greater than')),
    ('gte', _('is greater than or equal to')),
    ('lt', _('is less than')),
    ('lte', _('is less than or equal to')),
    ('iexact', _('(i) is equal to')),
    ('icontains', _('(i) contains')),
    ('iregex', _('(i) matchs regex')),
    ('istartswith', _('(i) starts with')),
    ('endswith', _('(i) ends with')),
    ('join', _('joins to')),
)


class CheckboxLabelWidget(Widget):

    def __init__(self, attrs=None, label=None, prelabel=None, *args, **kwargs):
        super(CheckboxLabelWidget, self).__init__(*args, **kwargs)
        self.attrs = attrs or {}
        self.label = label or _('Check this')
        self.prelabel = prelabel

    def render(self, name, value=None, attrs=None, prelabel=None):
        self.attrs.update(attrs or {})
        final_attrs = self.build_attrs(self.attrs, name=name)
        prelabel = prelabel or self.prelabel
        if prelabel:
            out = u'<label for="%s" >%s</label><input type="checkbox"%s >' \
                  % (self.attrs.get("id", ""), value or self.label,
                     flatatt(final_attrs))
        else:
            out = u'<input type="checkbox"%s ><label for="%s" >%s</label>' \
                  % (flatatt(final_attrs), self.attrs.get("id", ""),
                     value or self.label)
        return mark_safe(out)


class CriteriaInput(MultiWidget):

    class Media:
        js = ('django_qbe/js/qbe.widgets.js', )

    def __init__(self, *args, **kwargs):
        # widgets = [CheckboxLabelWidget(label=_("Inverse")),
        #            Select(choices=OPERATOR_CHOICES), TextInput(),
        #            CheckboxLabelWidget(label=_("Nothing"))]
        widgets = [Select(choices=OPERATOR_CHOICES), TextInput()]
        super(CriteriaInput, self).__init__(widgets=widgets, *args, **kwargs)

    def decompress(self, value):
        if value:
            return value
        return (None, None)
