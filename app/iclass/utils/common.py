# -*- coding:utf-8 -*-
import base64


def force_to_str(_id):
    return "%s" % _id


def _decode_video_id(vid):
    if isinstance(vid, (int, long)) or str(vid).isdigit():
        return long(vid)
    try:
        return long(base64.b64decode(vid[1:])) >> 2
    except:
        return 0


def decode_video_id(vid, to_str=False):
    decoded_vid = _decode_video_id(vid)
    return force_to_str(decoded_vid) if to_str else decoded_vid


def _decode_user_id(uid):
    if isinstance(uid, unicode):
        uid = uid.encode('utf-8')
    if isinstance(uid, (int, long)) or str(uid).isdigit():
        return long(uid)
    try:
        return long(base64.b64decode(uid[1:])) >> 2
    except:
        return 0


def encode_utf8(val):
    if isinstance(val, unicode):
        return val.encode("utf8")
    return val


def decode_user_id(uid, to_str=False):
    decoded_uid = _decode_user_id(uid)
    return force_to_str(decoded_uid) if to_str else decoded_uid

def get_paged_dict(item_list, page_pos=1, one_page_count=20, item_name='items'):
    from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
    p = Paginator(item_list, one_page_count)
    display_pages = []
    try:
        items = p.page(page_pos)
        now_page = int(page_pos)
    except (PageNotAnInteger, EmptyPage, ValueError):
        items = p.page(1)
        now_page = 1
    if p.num_pages <= 5:
        display_pages = map(str, range(1, p.num_pages+1))
    else:
        if now_page - 4 > 1:
            display_pages += ['1', '...', ] + map(str, range(now_page-2, now_page+1))
        else:
            display_pages += map(str, range(1, now_page+1))
        if now_page + 4 < p.num_pages:
            display_pages += map(str, range(now_page+1, now_page+3)) + ['...', str(p.num_pages)]
        else:
            display_pages += map(str, range(now_page+1, p.num_pages+1))
    page_info_dict = {item_name: items, 'page_range': p.page_range, 'num_pages': str(p.num_pages),
                      'now_page': str(now_page), 'display_pages': display_pages, 'previous_page': now_page-1,
                      'next_page': now_page+1,'num_count': p._count}
    return page_info_dict


