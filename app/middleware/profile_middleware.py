# profile_middleware - a middleware that profiles views
#
# Inspired by udfalkso's http://www.djangosnippets.org/snippets/186/
# and the Shwagroo Team's http://www.djangosnippets.org/snippets/605/
#
# Install this by adding it to your MIDDLEWARE_CLASSES.  It is active
# if you are logged in as a superuser, or always when settings.DEBUG
# is True.
#
# To use it, pass 'profile=1' as a GET or POST parameter to any HTTP
# request.

from base64 import b64decode, b64encode
import cPickle
from cStringIO import StringIO
from decimal import Decimal
import hotshot, hotshot.stats
import pprint
import sys
import tempfile

from django.conf import settings
from django.core.exceptions import MiddlewareNotUsed
from django.db import connection, reset_queries
from django.http import HttpResponse
from django.utils import html

class StdoutWrapper(object):
    """Simple wrapper to capture and overload sys.stdout"""
    def __init__(self):
        self.stdout = sys.stdout
        self.stream = StringIO()
        sys.stdout = self.stream

    def __del__(self):
        if self.stdout is not None:
            sys.stdout = self.stdout

    def __str__(self):
        return self.stream.getvalue()


def render_stats(stats, sort, format):
    """
    Returns a StringIO containing the formatted statistics from _statsfile_.

    _sort_ is a list of fields to sort by.
    _format_ is the name of the method that pstats uses to format the data.
    """
    output = StdoutWrapper()
    if hasattr(stats, "stream"):
        stats.stream = output.stream
    stats.sort_stats(*sort)
    getattr(stats, format)()
    return output.stream

def render_queries(queries, sort):
    """
    Returns a StringIO containing the formatted SQL queries.

    _sort_ is a field to sort by.
    """
    output = StringIO()
    if sort == 'order':
        print >>output, "     time query"
        for query in queries:
            print >>output, " %8s %s" % (query["time"], query["sql"])
        return output
    if sort == 'time':
        def sorter(x, y):
            return cmp(x[1][1], y[1][1])
    elif sort == 'queries':
        def sorter(x, y):
            return cmp(x[1][0], y[1][0])
    else:
        raise RuntimeError("Unknown sort: %s" % sort)
    print >>output, "  queries     time query"
    results = {}
    for query in queries:
        try:
            result = results[query["sql"]]
            result[0] += 1
            result[1] += Decimal(query["time"])
        except KeyError:
            results[query["sql"]] = [1, Decimal(query["time"])]
    results = sorted(results.iteritems(), cmp=sorter, reverse=True)
    for result in results:
        print >>output, " %8d %8.3f %s" % (result[1][0],
                                           result[1][1],
                                           result[0])
    return output


def pickle_stats(stats):
    """Pickle a pstats.Stats object"""
    if hasattr(stats, "stream"):
        del stats.stream
    return cPickle.dumps(stats)

def unpickle_stats(stats):
    """Unpickle a pstats.Stats object"""
    stats = cPickle.loads(stats)
    stats.stream = True
    return stats


class RadioButton(object):
    """Generate the HTML for a radio button."""
    def __init__(self, name, value, description=None, checked=False):
        self.name = name
        self.value = value
        if description is None:
            self.description = value
        else:
            self.description = description
        self.checked = checked

    def __str__(self):
        checked = ""
        if self.checked:
            checked = "checked='checked'"
        return ("<input "
                "type='radio' "
                "name='%(name)s' "
                "value='%(value)s' "
                "%(checked)s>"
                "%(description)s"
                "</input><br />" %
                {'name': self.name,
                 'value': self.value,
                 'checked': checked,
                 'description': self.description})


class RadioButtons(object):
    """Generate the HTML for a list of radio buttons."""
    def __init__(self, name, checked, values):
        self.result = []
        for v in values:
            description = None
            if isinstance(v, (list, tuple)):
                value = v[0]
                description = v[1]
            else:
                value = v
            select = False
            if value == checked:
                select = True
            self.result.append(RadioButton(name, value, description, select))

    def __str__(self):
        return "\n".join([str(button) for button in self.result])


stats_template = """
<html>
    <head><title>Profile for %(url)s</title></head>
    <body>
        <form method='post' action='?profile=1'>
            <fieldset style='float: left'>
                <legend style='font-weight: bold'>Sort by</legend>
                %(sort_first_buttons)s
            </fieldset>
            <fieldset style='float: left'>
                <legend style='font-weight: bold'>then by</legend>
                %(sort_second_buttons)s
            </fieldset>
            <fieldset style='float: left'>
                <legend style='font-weight: bold'>Format</legend>
                %(format_buttons)s
            </fieldset>
            <div style='clear: both'></div>
            <input type='hidden' name='queries' value='%(rawqueries)s' />
            <input type='hidden' name='stats' value='%(rawstats)s' />
            <input type='hidden' name='show_stats' value='1' />
            <input type='submit' name='show_queries' value='Show Queries' />
            <input type='submit' name='sort' value='Sort' />
        </form>
        <hr />
        <pre>%(stats)s</pre>
    </body>
</html>
"""

sort_categories = (('time', 'internal time'),
                   ('cumulative', 'cumulative time'),
                   ('calls', 'call count'),
                   ('pcalls', 'primitive call count'),
                   ('file', 'file name'),
                   ('nfl', 'name/file/line'),
                   ('stdname', 'standard name'),
                   ('name', 'function name'))

def display_stats(request, stats, queries):
    """
    Generate a HttpResponse of functions for a profiling run.

    _stats_ should contain a pstats.Stats of a hotshot session.
    _queries_ should contain a list of SQL queries.
    """
    sort = [request.REQUEST.get('sort_first', 'time'),
            request.REQUEST.get('sort_second', 'calls')]
    format = request.REQUEST.get('format', 'print_stats')
    sort_first_buttons = RadioButtons('sort_first', sort[0],
                                      sort_categories)
    sort_second_buttons = RadioButtons('sort_second', sort[1],
                                       sort_categories)
    format_buttons = RadioButtons('format', format,
                                  (('print_stats', 'by function'),
                                   ('print_callers', 'by callers'),
                                   ('print_callees', 'by callees')))
    output = render_stats(stats, sort, format)
    output.reset()
    output = [html.escape(unicode(line)) for line in output.readlines()]
    response = HttpResponse(mimetype='text/html; charset=utf-8')
    response.content = (stats_template %
                        {'format_buttons': format_buttons,
                         'sort_first_buttons': sort_first_buttons,
                         'sort_second_buttons': sort_second_buttons,
                         'rawqueries' : b64encode(cPickle.dumps(queries)),
                         'rawstats': b64encode(pickle_stats(stats)),
                         'stats': "".join(output),
                         'url': request.path})
    return response


queries_template = """
<html>
    <head><title>SQL Queries for %(url)s</title></head>
    <body>
        <form method='post' action='?profile=1'>
            <fieldset style='float: left'>
                <legend style='font-weight: bold'>Sort by</legend>
                %(sort_buttons)s
            </fieldset>
            <div style='clear: both'></div>
            <input type='hidden' name='queries' value='%(rawqueries)s' />
            <input type='hidden' name='stats' value='%(rawstats)s' />
            <input type='hidden' name='show_queries' value='1' />
            <input type='submit' name='show_stats' value='Show Profile' />
            <input type='submit' name='sort' value='Sort' />
        </form>
        <hr />
        %(num_queries)d SQL queries:
        <pre>%(queries)s</pre>
    </body>
</html>
"""


def display_queries(request, stats, queries):
    """
    Generate a HttpResponse of SQL queries for a profiling run.

    _stats_ should contain a pstats.Stats of a hotshot session.
    _queries_ should contain a list of SQL queries.
    """
    sort = request.REQUEST.get('sort_by', 'time')
    sort_buttons = RadioButtons('sort_by', sort,
                                (('order', 'by order'),
                                 ('time', 'time'),
                                 ('queries', 'query count')))
    output = render_queries(queries, sort)
    output.reset()
    output = [html.escape(unicode(line))
              for line in output.readlines()]
    response = HttpResponse(mimetype='text/html; charset=utf-8')
    response.content = (queries_template %
                        {'sort_buttons': sort_buttons,
                         'num_queries': len(queries),
                         'queries': "".join(output),
                         'rawqueries' : b64encode(cPickle.dumps(queries)),
                         'rawstats': b64encode(pickle_stats(stats)),
                         'url': request.path})
    return response


class ProfileMiddleware(object):
    """
    Displays hotshot profiling for any view.
    http://yoursite.com/yourview/?profile=1

    WARNING: It uses hotshot profiler which is not thread safe.
    """
    def process_request(self, request):
        """
	Setup the profiler for a profiling run and clear the SQL query log.

	If this is a resort of an existing profiling run, just return
	the resorted list.
	"""
        def unpickle(params):
            stats = unpickle_stats(b64decode(params.get('stats', '')))
            queries = cPickle.loads(b64decode(params.get('queries', '')))
            return stats, queries

        if request.method != 'GET' and \
           not (request.META.get('HTTP_CONTENT_TYPE',
                                 request.META.get('CONTENT_TYPE', '')) in
                ['multipart/form-data', 'application/x-www-form-urlencoded']):
            return
        if (request.REQUEST.get('profile', False) and
            (settings.DEBUG == True or request.user.is_staff)):
            request.statsfile = tempfile.NamedTemporaryFile()
            params = request.REQUEST
            if (params.get('show_stats', False)
                and params.get('show_queries', '1') == '1'):
                # Instantly re-sort the existing stats data
                stats, queries = unpickle(params)
                return display_stats(request, stats, queries)
            elif (params.get('show_queries', False)
                  and params.get('show_stats', '1') == '1'):
                stats, queries = unpickle(params)
                return display_queries(request, stats, queries)
            else:
                # We don't have previous data, so initialize the profiler
                request.profiler = hotshot.Profile(request.statsfile.name)
                reset_queries()

    def process_view(self, request, view_func, view_args, view_kwargs):
        """Run the profiler on _view_func_."""
        profiler = getattr(request, 'profiler', None)
        if profiler:
            # Make sure profiler variables don't get passed into view_func
            original_get = request.GET
            request.GET = original_get.copy()
            request.GET.pop('profile', None)
            request.GET.pop('show_queries', None)
            request.GET.pop('show_stats', None)
            try:
                return profiler.runcall(view_func,
                                        request, *view_args, **view_kwargs)
            finally:
                request.GET = original_get


    def process_response(self, request, response):
        """Finish profiling and render the results."""
        profiler = getattr(request, 'profiler', None)
        if profiler:
            profiler.close()
            params = request.REQUEST
            stats = hotshot.stats.load(request.statsfile.name)
            queries = connection.queries
            if (params.get('show_queries', False)
                and params.get('show_stats', '1') == '1'):
                response = display_queries(request, stats, queries)
            else:
                response = display_stats(request, stats, queries)
        return response
