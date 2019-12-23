from django import template
from django.template.loader import render_to_string
from django.contrib.admin.views.main import ALL_VAR, PAGE_VAR, SEARCH_VAR

register = template.Library()

def paginator_number(cl, i):
    if i == cl.page_num:
        classname = "active"
    else:
        classname = "inactive"
    return u'<a href="%s" class="%s float-left">%d</a> ' % (cl.get_query_string({PAGE_VAR: i}), classname, i+1)
paginator_number = register.simple_tag(paginator_number)

def pagination(cl, user_agent):
    paginator, page_num = cl.paginator, cl.page_num

    pagination_required = (not cl.show_all or not cl.can_show_all) and cl.multi_page
    if not pagination_required:
        page_range = []
    else:
        ON_EACH_SIDE = 1

        # If there are 4 or fewer pages, display links to every page.
        # Otherwise, do some fancy
        if paginator.num_pages <= 3:
            page_range = range(paginator.num_pages)
        else:
            # Insert "smart" pagination links, so that there are always ON_ENDS
            # links at either end of the list of pages, and there are always
            # ON_EACH_SIDE links at either end of the "current page" link.
            page_range = []
            if page_num > ON_EACH_SIDE:
                page_range.extend(range(0, ON_EACH_SIDE - 1))
                page_range.extend(range(page_num - ON_EACH_SIDE, page_num + 1))
            else:
                page_range.extend(range(0, page_num + 1))
            if page_num < (paginator.num_pages - ON_EACH_SIDE - 1):
                page_range.extend(range(page_num + 1, page_num + ON_EACH_SIDE + 1))
                page_range.extend(range(paginator.num_pages, paginator.num_pages))
            else:
                page_range.extend(range(page_num + 1, paginator.num_pages))

    need_show_all_link = cl.can_show_all and not cl.show_all and cl.multi_page
    return render_to_string((
        'mobileadmin/%s/pagination.html' % user_agent,
        'mobileadmin/pagination.html',
        'admin/pagination.html'
    ), {
        'cl': cl,
        'pagination_required': pagination_required,
        'show_all_url': need_show_all_link and cl.get_query_string({ALL_VAR: ''}),
        'page_range': page_range,
        'ALL_VAR': ALL_VAR,
        '1': 1,
    })
register.simple_tag(pagination)

def search_form(cl, user_agent):
    return render_to_string((
        'mobileadmin/%s/search_form.html' % user_agent,
        'mobileadmin/search_form.html',
        'admin/search_form.html'
    ), {
        'cl': cl,
        'show_result_count': cl.result_count != cl.full_result_count and not cl.opts.one_to_one_field,
        'search_var': SEARCH_VAR
    })
register.simple_tag(search_form)

def admin_list_filter(cl, spec, user_agent):
    return render_to_string((
        'mobileadmin/%s/filter.html' % user_agent,
        'mobileadmin/filter.html',
        'admin/filter.html'
    ), {
        'title': spec.title(),
        'choices': list(spec.choices(cl)),
    })
register.simple_tag(admin_list_filter)
