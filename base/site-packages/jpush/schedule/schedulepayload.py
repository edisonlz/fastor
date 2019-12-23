import re
from jpush import push

def schedulepayload(name=None, enabled=None, trigger=None, push=None):
    schedulepayload = {}
    if name is not None:
        schedulepayload['name'] = name
    if enabled is not None:
        schedulepayload['enabled'] = enabled
    if trigger is not None:
        schedulepayload['trigger'] = trigger
    if push is not None:
        schedulepayload['push'] = push
    if not schedulepayload:
        raise ValueError("schedule payload may not be empty")
    return schedulepayload


def trigger(time, start=None, end=None,time_unit=None,frequency=None,point=None):
    if(start==None and end==None and time_unit==None and frequency==None):
        trigger={}
        single={}
        single["time"]=time
        trigger["single"]=single
        return trigger
    else:
        trigger={}
        periodical={}
        if time is not None:
            periodical['time'] = time
        if start is not None:
            periodical['start'] = start
        if end is not None:
            periodical['end'] = end
        if time_unit is not None:
            periodical['time_unit'] = time_unit
        if frequency is not None:
            periodical['frequency'] = frequency
        if point is not None:
            periodical['point'] = point
        trigger["periodical"]=periodical
        return trigger



