# -*- coding: utf-8 -*-
from django import forms
from django.db import connections
from django.db.models.fields import Field
from django.core.urlresolvers import reverse, NoReverseMatch
from django.conf import settings
from django.forms.formsets import BaseFormSet, formset_factory
from django.utils.importlib import import_module
from django.utils.translation import ugettext as _

from django_qbe.utils import get_models
from django_qbe.widgets import CriteriaInput


DATABASES = None
try:
    DATABASES = settings.DATABASES
except AttributeError:
    # Backwards compatibility for Django versions prior to 1.1.
    DATABASES = {
        'default': {
            'ENGINE': "django.db.backends.%s" % settings.DATABASE_ENGINE,
            'NAME': settings.DATABASE_NAME,
        }
    }

SORT_CHOICES = (
    ("", ""),
    ("asc", _("Ascending")),
    ("des", _("Descending")),
)


class QueryByExampleForm(forms.Form):
    show = forms.BooleanField(label=_("Show"), required=False)
    model = forms.CharField(label=_("Model"))
    field = forms.CharField(label=_("Field"))
    criteria = forms.CharField(label=_("Criteria"), required=False)
    sort = forms.ChoiceField(label=_("Sort"), choices=SORT_CHOICES,
                             required=False)

    def __init__(self, *args, **kwargs):
        super(QueryByExampleForm, self).__init__(*args, **kwargs)
        model_widget = forms.Select(attrs={'class': "qbeFillModels to:field"})
        self.fields['model'].widget = model_widget
        sort_widget = forms.Select(attrs={'disabled': "disabled",
                                          'class': 'submitIfChecked'},
                                   choices=SORT_CHOICES)
        self.fields['sort'].widget = sort_widget
        criteria_widget = CriteriaInput(attrs={'disabled': "disabled"})
        self.fields['criteria'].widget = criteria_widget
        criteria_widgets = getattr(criteria_widget, "widgets", [])
        if criteria_widgets:
            criteria_len = len(criteria_widgets)
            criteria_names = ",".join([("criteria_%s" % s)
                                       for s in range(0, criteria_len)])
            field_attr_class = "qbeFillFields enable:sort,%s" % criteria_names
        else:
            field_attr_class = "qbeFillFields enable:sort,criteria"
        field_widget = forms.Select(attrs={'class': field_attr_class})
        self.fields['field'].widget = field_widget

    def clean_model(self):
        model = self.cleaned_data['model']
        return model.lower().replace(".", "_")

    def clean_criteria(self):
        criteria = self.cleaned_data['criteria']
        try:
            operator, over = eval(criteria, {}, {})
            return (operator, over)
        except:
            return (None, None)


class BaseQueryByExampleFormSet(BaseFormSet):
    _selects = []
    _froms = []
    _wheres = []
    _sorts = []
    _params = []
    _models = {}
    _raw_query = None
    _db_alias = "default"
    _db_operators = {}
    _db_table_names = []
    _db_operations = None

    def __init__(self, *args, **kwargs):
        self._db_alias = kwargs.pop("using", "default")
        self._db_connection = connections["default"]
        database_properties = DATABASES.get(self._db_alias, "default")
        module = database_properties['ENGINE']
        try:
            base_mod = import_module("%s.base" % module)
            intros_mod = import_module("%s.introspection" % module)
        except ImportError:
            pass
        if base_mod and intros_mod:
            self._db_operators = base_mod.DatabaseWrapper.operators
            DatabaseOperations = base_mod.DatabaseOperations
            try:
                self._db_operations = DatabaseOperations(self._db_connection)
            except TypeError:
                # Some engines have no params to instance DatabaseOperations 
                self._db_operations = DatabaseOperations()
            intros_db = intros_mod.DatabaseIntrospection(self._db_connection)
            django_table_names = intros_db.django_table_names()
            table_names = intros_db.table_names()
            self._db_table_names = list(django_table_names.union(table_names))
        super(BaseQueryByExampleFormSet, self).__init__(*args, **kwargs)

    def clean(self):
        """
        Checks that there is almost one field to select
        """
        if any(self.errors):
            # Don't bother validating the formset unless each form is valid on
            # its own
            return
        selects, froms, wheres, sorts, params = self.get_query_parts()
        if not selects:
            validation_message = _(u"At least you must check a row to get.")
            raise forms.ValidationError, validation_message
        self._selects = selects
        self._froms = froms
        self._wheres = wheres
        self._sorts = sorts
        self._params = params

    def get_query_parts(self):
        """
        Return SQL query for cleaned data
        """
        selects = []
        froms = []
        wheres = []
        sorts = []
        params = []
        app_model_labels = None
        lookup_cast = self._db_operations.lookup_cast
        qn = self._db_operations.quote_name
        uqn = self._unquote_name
        for data in self.cleaned_data:
            if not ("model" in data and "field" in data):
                break
            model = data["model"]
            # HACK: Workaround to handle tables created
            #       by django for its own
            if not app_model_labels:
                app_models = get_models(include_auto_created=True,
                                        include_deferred=True)
                app_model_labels = [u"%s_%s" % (a._meta.app_label,
                                                a._meta.module_name)
                                    for a in app_models]
            if model in app_model_labels:
                position = app_model_labels.index(model)
                model = app_models[position]._meta.db_table
                self._models[model] = app_models[position]
            field = data["field"]
            show = data["show"]
            criteria = data["criteria"]
            sort = data["sort"]
            db_field = u"%s.%s" % (qn(model), qn(field))
            operator, over = criteria
            is_join = operator.lower() == 'join'
            if show and not is_join:
                selects.append(db_field)
            if sort:
                sorts.append(db_field)
            if all(criteria):
                if is_join:
                    over_split = over.lower().rsplit(".", 1)
                    join_model = qn(over_split[0].replace(".", "_"))
                    join_field = qn(over_split[1])
                    if model in self._models:
                        _field = self._models[model]._meta.get_field(field)
                        join = u"%s.%s = %s.%s" \
                               % (join_model, join_field, qn(model),
                                  qn(_field.attname))
                    else:
                        join = u"%s.%s = %s" \
                               % (join_model, join_field,
                                  u"%s_id" % db_field)
                    if (join not in wheres
                        and uqn(join_model) in self._db_table_names):
                        wheres.append(join)
                        if join_model not in froms:
                            froms.append(join_model)
                    # join_select = u"%s.%s" % (join_model, join_field)
                    # if join_select not in selects:
                    #     selects.append(join_select)
                elif operator in self._db_operators:
                    # db_operator = self._db_operators[operator] % over
                    db_operator = self._db_operators[operator]
                    lookup = self._get_lookup(operator, over)
                    params.append(lookup)
                    wheres.append(u"%s %s" \
                                  % (lookup_cast(operator) % db_field,
                                     db_operator))
            if qn(model) not in froms and model in self._db_table_names:
                froms.append(qn(model))
        return selects, froms, wheres, sorts, params

    def get_raw_query(self, limit=None, offset=None, count=False,
                      add_extra_ids=False, add_params=False):
        if self._raw_query:
            return self._raw_query
        if self._sorts:
            order_by = u"ORDER BY %s" % (", ".join(self._sorts))
        else:
            order_by = u""
        if self._wheres:
            wheres = u"WHERE %s" % (" AND ".join(self._wheres))
        else:
            wheres = u""
        if count:
            selects = (u"COUNT(*) as count", )
            order_by = u""
        elif add_extra_ids:
            selects = self._get_selects_with_extra_ids()
        else:
            selects = self._selects
        limits = u""
        if limit:
            try:
                limits = u"LIMIT %s" % int(limit)
            except ValueError:
                pass
        offsets = u""
        if offset:
            try:
                offsets = u"OFFSET %s" % int(offset)
            except ValueError:
                pass
        sql = u"""SELECT %s FROM %s %s %s %s %s;""" \
              % (", ".join(selects),
                 ", ".join(self._froms),
                 wheres,
                 order_by,
                 limits,
                 offsets)
        if add_params:
            return u"%s /* %s */" % (sql, ", ".join(self._params))
        else:
            return sql

    def get_results(self, limit=None, offset=None, query=None, admin_name=None,
                    row_number=False):
        """
        Fetch all results after perform SQL query and
        """
        add_extra_ids = (admin_name != None)
        if not query:
            sql = self.get_raw_query(limit=limit, offset=offset,
                                     add_extra_ids=add_extra_ids)
        else:
            sql = query
        if settings.DEBUG:
            print sql
        cursor = self._db_connection.cursor()
        cursor.execute(sql, tuple(self._params))
        query_results = cursor.fetchall()
        if admin_name:
            selects = self._get_selects_with_extra_ids()
            results = []
            try:
                offset = int(offset)
            except ValueError:
                offset = 0
            for r, row in enumerate(query_results):
                i = 0
                l = len(row)
                if row_number:
                    result = [(r + offset + 1, u"#row%s" % (r + offset + 1))]
                else:
                    result = []
                while i < l:
                    appmodel, field = selects[i].split(".")
                    appmodel = self._unquote_name(appmodel)
                    field = self._unquote_name(field)
                    try:
                        if appmodel in self._models:
                            _model = self._models[appmodel]
                            _appmodel = u"%s_%s" % (_model._meta.app_label,
                                                    _model._meta.module_name)
                        else:
                            _appmodel = appmodel
                        admin_url = reverse("%s:%s_change" % (admin_name,
                                                              _appmodel),
                                             args=[row[i + 1]])
                    except NoReverseMatch:
                        admin_url = None
                    result.append((row[i], admin_url))
                    i += 2
                results.append(result)
            return results
        else:
            if row_number:
                results = []
                for r, row in enumerate(query_results):
                    result = [r + 1]
                    for cell in row:
                        result.append(cell)
                    results.append(result)
                return results
            else:
                return query_results

    def get_count(self):
        query = self.get_raw_query(count=True)
        results = self.get_results(query=query)
        if results:
            return float(results[0][0])
        else:
            return len(self.get_results())

    def get_labels(self, add_extra_ids=False, row_number=False):
        if row_number:
            labels = [_(u"#")]
        else:
            labels = []
        if add_extra_ids:
            selects = self._get_selects_with_extra_ids()
        else:
            selects = self._selects
        if selects and isinstance(selects, (tuple, list)):
            for select in selects:
                label_splits = select.replace("_", ".").split(".")
                label_splits_field = " ".join(label_splits[2:]).capitalize()
                label = u"%s.%s: %s" % (label_splits[0].capitalize(),
                                        label_splits[1].capitalize(),
                                        label_splits_field)
                labels.append(label)
        return labels

    def _unquote_name(self, name):
        quoted_space = self._db_operations.quote_name("")
        if name.startswith(quoted_space[0]) and name.endswith(quoted_space[1]):
            return name[1:-1]
        return name

    def _get_lookup(self, operator, over):
        lookup = Field().get_db_prep_lookup(operator, over,
                                            connection=self._db_connection,
                                            prepared=True)
        if isinstance(lookup, (tuple, list)):
            return lookup[0]
        return lookup

    def _get_selects_with_extra_ids(self):
        qn = self._db_operations.quote_name
        selects = []
        for select in self._selects:
            appmodel, field = select.split(".")
            appmodel = self._unquote_name(appmodel)
            field = self._unquote_name(field)
            selects.append(select)
            if appmodel in self._models:
                pk_name = self._models[appmodel]._meta.pk.name
            else:
                pk_name = u"id"
            selects.append("%s.%s" % (qn(appmodel), qn(pk_name)))
        return selects

QueryByExampleFormSet = formset_factory(QueryByExampleForm,
                                        formset=BaseQueryByExampleFormSet,
                                        extra=1,
                                        can_delete=True)
