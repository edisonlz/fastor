# -*- coding: utf-8 -*-
"""
    beecloud.sales
    ~~~~~~~~~
    This module contains coupon sales API.
    :created by xuanzhui on 2017/8/18.
    :copyright (c) 2015 BeeCloud.
    :license: MIT, see LICENSE for more details.
"""
from beecloud.entity import BCCouponTemplate, BCCoupon, _TmpObject
from beecloud.utils import get_rest_root_url, rest_query_object_by_id, rest_query_objects, parse_dict_to_obj, \
    rest_add_object


def query_coupon_template(bc_app, id):
    """
    query coupon template by id
    :param bc_app: beecloud.entity.BCApp
    :param id: template id
    :return: beecloud.entity.BCCouponTemplate
    """
    url = get_rest_root_url() + 'rest/coupon/template'
    return rest_query_object_by_id(bc_app, url, id, 'coupon_template', BCCouponTemplate, True)


def query_coupon_templates(bc_app, query_criteria):
    """
    query coupon template by condition
    :param bc_app: beecloud.entity.BCApp
    :param query_criteria: query condition object beecloud.entity.BCQueryCriteria
                            attach more condition like obj.name = 'my_name'
    :return: beecloud.entity.BCCouponTemplate
    """
    url = get_rest_root_url() + 'rest/coupon/template'
    return rest_query_objects(bc_app, url, query_criteria, 'coupon_templates', BCCouponTemplate, True)


def query_coupon(bc_app, id):
    """
    query coupon by id
    :param bc_app: beecloud.entity.BCApp
    :param id: coupon id
    :return: beecloud.entity.BCCoupon
    """
    url = get_rest_root_url() + 'rest/coupon'
    result = rest_query_object_by_id(bc_app, url, id, 'coupon', BCCoupon, True)

    if hasattr(result, 'coupon'):
        coupon = result.coupon

        if coupon and hasattr(coupon, 'template'):
            template_dict = coupon.template
            if isinstance(template_dict, dict):
                setattr(coupon, 'template', parse_dict_to_obj(template_dict, BCCouponTemplate))

    return result


def query_coupons(bc_app, query_criteria):
    """
    query coupon template by condition
    :param bc_app: beecloud.entity.BCApp
    :param query_criteria: query condition object beecloud.entity.BCQueryCriteria
                            attach more condition like obj.name = 'my_name'
    :return: beecloud.entity.BCCouponTemplate
    """
    url = get_rest_root_url() + 'rest/coupon'
    result = rest_query_objects(bc_app, url, query_criteria, 'coupons', BCCoupon, True)

    if hasattr(result, 'coupons'):
        coupons = result.coupons

        if coupons and isinstance(coupons, list) and len(coupons) > 0:
            for coupon in coupons:
                if hasattr(coupon, 'template'):
                    template_dict = coupon.template
                    if isinstance(template_dict, dict):
                        setattr(coupon, 'template', parse_dict_to_obj(template_dict, BCCouponTemplate))

    return result


def create_coupon(bc_app, template_id, user_id):
    """
    distribute coupon to buyer
    :param bc_app: beecloud.entity.BCApp
    :param template_id: coupon template id
    :param user_id: user who would use the coupon
    :return: beecloud.entity.BCCoupon
    """
    url = get_rest_root_url() + 'rest/coupon'

    obj = _TmpObject()
    obj.template_id = template_id
    obj.user_id = user_id

    result = rest_add_object(bc_app, url, obj, 'coupon', BCCoupon)

    if hasattr(result, 'coupon'):
        coupon = result.coupon

        if coupon and hasattr(coupon, 'template'):
            template_dict = coupon.template
            if isinstance(template_dict, dict):
                setattr(coupon, 'template', parse_dict_to_obj(template_dict, BCCouponTemplate))

    return result
