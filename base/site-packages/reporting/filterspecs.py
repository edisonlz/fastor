from django.contrib.admin.filterspecs import FilterSpec
from django.db.models.fields.related import RelatedField
from django.template.defaultfilters import capfirst


class LookupFilterSpec(FilterSpec):
    def __init__(self, f, request, params, model, model_admin):
        FilterSpec.__init__(self, f, request, params, model, model_admin)
        self.model = model
        self.lookup_val = request.GET.get(f, None)
    
    def title(self):
        return capfirst(' '.join([i for i in self.field.split('__')]))

    def choices(self, cl):
        yield {'selected': self.lookup_val is None,
               'query_string': cl.get_query_string({}, [self.field]),
               'display': 'All'}
        values = self._values(self.model, self.field)
        for val in values:
            id, display = val
            yield {'selected': self.lookup_val == id,
                   'query_string': cl.get_query_string({self.field: id}),
                   'display': display}
    
    def _values(self, model, lookup):
        parts = lookup.split('__')
        field = model._meta.get_field(parts[0])
        if not isinstance(field, RelatedField):
            raise Exception('Invalid lookup "%s"' % self.field)
        rel_model = field.rel.to
        if len(parts) == 2:
            field2 = rel_model._meta.get_field(parts[1])
            ids = [i[0] for i in field.get_choices(include_blank=False)]
            values = set(rel_model.objects.filter(pk__in=ids).values_list(parts[1], flat=True))
            if field2.choices:
                labels = dict(field2.choices)
                return [(unicode(v), labels[v]) for v in values]
            return [(v,v) for v in values]
        next_lookup = '__'.join(parts[1:])
        return self._values(rel_model, next_lookup)

#FilterSpec.filter_specs.insert(0, (lambda f: '__' in f.name, LookupFilterSpec))
