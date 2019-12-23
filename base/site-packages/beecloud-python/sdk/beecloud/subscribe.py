# -*- coding: utf-8 -*-
"""
    beecloud.subscribe
    ~~~~~~~~~
    This module contains subscription API.
    :created by xuanzhui on 2016/8/25.
    :copyright (c) 2015 BeeCloud.
    :license: MIT, see LICENSE for more details.
"""

from beecloud.entity import BCPlan, BCSubscription
from beecloud.utils import get_rest_root_url, rest_add_object, rest_update_object, rest_delete_object


class BCSubscribe:
    def __init__(self):
        self.bc_app = None

    def register_app(self, bc_app):
        """
        register app, which is mandatory before calling other API
        :param bc_app: beecloud.entity.BCApp
        """
        self.bc_app = bc_app

    def _plan_url(self):
        return get_rest_root_url() + 'plan'

    def _subscription_url(self):
        return get_rest_root_url() + 'subscription'

    def create_plan(self, plan):
        """
        create subscription plan
        :param plan: beecloud.entity.BCPlan
        :return: beecloud.entity.BCResult
        """
        return rest_add_object(self.bc_app, self._plan_url(), plan, 'plan', BCPlan)

    def update_plan(self, plan_id, name=None, optional=None):
        """
        update subscription plan
        :param plan_id: plan object id
        :param name: plan name
        :param optional: dict -- key/value pairs
        :return: beecloud.entity.BCResult
        """
        return rest_update_object(self.bc_app, self._plan_url(), plan_id, name=name, optional=optional)

    def delete_plan(self, plan_id):
        """
        delete subscription plan
        :param plan_id: plan object id
        :return: beecloud.entity.BCResult
        """
        return rest_delete_object(self.bc_app, self._plan_url(), plan_id)

    def subscribe(self, subscription, sms_id, sms_code, coupon_code=None):
        """
        create subscription
        :param subscription: beecloud.entity.BCSubscription
                coupon_code should be used instead of coupon_id if there is a discount
                card_id or {bank_name, card_no, id_name, id_no, mobile} should be supplied
                card_id can be gotten from webhook provided that subscription is successful
                bank_name can be chosen from BCQuery.query_subscription_payment_supported_banks()
        :param sms_id: return by send_sms_passcode method
        :param sms_code: get from user phone
        :param coupon_code: the coupon code to apply to this subscription
        :return: beecloud.entity.BCResult
        """
        setattr(subscription, 'sms_id', sms_id)
        setattr(subscription, 'sms_code', sms_code)
        if coupon_code:
            setattr(subscription, 'coupon_code', coupon_code)
        return rest_add_object(self.bc_app, self._subscription_url(), subscription, 'subscription', BCSubscription)

    def update_subscription(self, sid, **kwargs):
        """
        create subscription
        :param sid: subscription id
        :param kwargs: items can updated, like amount=2
        :return: beecloud.entity.BCResult
        """
        return rest_update_object(self.bc_app, self._subscription_url(), sid, **kwargs)

    def cancel_subscription(self, sid):
        """
        create subscription
        :param sid: subscription id
        :return: beecloud.entity.BCResult
        """
        return rest_delete_object(self.bc_app, self._subscription_url(), sid)
