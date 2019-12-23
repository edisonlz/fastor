#encoding = utf-8
import sys, os
import time
import math

def redis_pager(obj, field, start, page_count, context=True, withscores=False, only_ids=False):
	""" redis panigator """

	if obj:
		try:
			if start == -1:
				total_count = field.zcard(obj)
				start = (math.ceil(float(total_count) / page_count) - 1) * page_count

			qs = field.zrevrange(obj, start, start + page_count, withscores=withscores, only_ids=only_ids)
			if context:
				total_count = field.zcard(obj)
				page_context = {}
				page_context["total_count"] = total_count
				return page_context, qs
			else:
				return {}, qs
		except Exception, e:
			if context:
				return None, None
	else:
		return {"total_count": 0}, []


def mongo_pager(queryset, start, page_count, context=True):
	""" mongodb panigator """

	if queryset:
		page_context = {}
		total_count = None
		if start == -1:
			total_count = queryset.count()
			start = (math.ceil(float(total_count) / page_count) - 1) * page_count

		if context:
			if not total_count:
				total_count = queryset.count()

		qs = queryset[start:start + page_count]
		if context:
			page_context['total_count'] = total_count
			return page_context, qs
		else:
			return {}, qs
	else:
		return {"total_count": 0}, []

