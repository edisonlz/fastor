from django.db.models.fields.related import RelatedField
from django.db.models.fields import DateField
import datetime
from django.utils.translation import get_date_formats, get_partial_date_formats, ugettext as _
from django.utils import dateformat
from django.utils.safestring import mark_safe
from django.template import Library

register = Library()

def get_date_model_field(model, lookup):
    parts = lookup.split('__')
    field = model._meta.get_field(parts[0])
    if not isinstance(field, RelatedField):
        if not isinstance(field, DateField):
            raise Exception('%s is not a date field' % lookup)
        return model, lookup
    rel_model = field.rel.to
    if len(parts) == 1:
        raise Exception('%s is not a date field' % lookup) 
    next_lookup = '__'.join(parts[1:])
    return get_date_model_field(rel_model, next_lookup)


def report_date_hierarchy(cl):
    if cl.date_hierarchy:
        model, field_name = get_date_model_field(cl.model, cl.date_hierarchy)
        rel_query_set = model.objects.all()
         
        year_field = '%s__year' % cl.date_hierarchy
        month_field = '%s__month' % cl.date_hierarchy
        day_field = '%s__day' % cl.date_hierarchy
        field_generic = '%s__' % cl.date_hierarchy
        year_lookup = cl.params.get(year_field)
        month_lookup = cl.params.get(month_field)
        day_lookup = cl.params.get(day_field)
        year_month_format, month_day_format = get_partial_date_formats()

        link = lambda d: mark_safe(cl.get_query_string(d, [field_generic]))

        if year_lookup and month_lookup and day_lookup:
            day = datetime.date(int(year_lookup), int(month_lookup), int(day_lookup))
            return {
                'show': True,
                'back': {
                    'link': link({year_field: year_lookup, month_field: month_lookup}),
                    'title': dateformat.format(day, year_month_format)
                },
                'choices': [{'title': dateformat.format(day, month_day_format)}]
            }
        elif year_lookup and month_lookup:
            days = rel_query_set.filter(**{'%s__year' % field_name: year_lookup, '%s__month' % field_name: month_lookup}).dates(field_name, 'day')
            return {
                'show': True,
                'back': {
                    'link': link({year_field: year_lookup}),
                    'title': year_lookup
                },
                'choices': [{
                    'link': link({year_field: year_lookup, month_field: month_lookup, day_field: day.day}),
                    'title': dateformat.format(day, month_day_format)
                } for day in days]
            }
        elif year_lookup:
            months = rel_query_set.filter(**{'%s__year' % field_name: year_lookup}).dates(field_name, 'month')
            return {
                'show' : True,
                'back': {
                    'link' : link({}),
                    'title': _('All dates')
                },
                'choices': [{
                    'link': link({year_field: year_lookup, month_field: month.month}),
                    'title': dateformat.format(month, year_month_format)
                } for month in months]
            }
        else:
            years = rel_query_set.dates(field_name, 'year')
            return {
                'show': True,
                'choices': [{
                    'link': link({year_field: year.year}),
                    'title': year.year
                } for year in years]
            }
report_date_hierarchy = register.inclusion_tag('admin/date_hierarchy.html')(report_date_hierarchy)