#encoding=utf-8
import  datetime, time
import re


def get_year_start_end():
    import calendar
    day_now = time.localtime()
    day_begin = '%d-01-01' % (day_now.tm_year)  # 月初肯定是1号
    wday, monthRange = calendar.monthrange(day_now.tm_year, 12)
    day_end = '%d-12-%02d' % (day_now.tm_year,monthRange)
    return day_begin,day_end


def get_month_start_end():
    import calendar
    day_now = time.localtime()
    day_begin = '%d-%02d-01' % (day_now.tm_year, day_now.tm_mon)  # 月初肯定是1号
    wday, monthRange = calendar.monthrange(day_now.tm_year, day_now.tm_mon)  # 得到本月的天数 第一返回为月第一日为星期几（0-6）, 第二返回为此月天数
    day_end = '%d-%02d-%02d' % (day_now.tm_year, day_now.tm_mon, monthRange)
    return day_begin,day_end


def get_month_start_end_by_month(sdate):
    import calendar
    day_now = time.localtime()
    day_begin = '%d-%02d-01 00:00:00' % (sdate.year, sdate.month)  # 月初肯定是1号
    wday, monthRange = calendar.monthrange(sdate.year, sdate.month)  # 得到本月的天数 第一返回为月第一日为星期几（0-6）, 第二返回为此月天数
    day_end = '%d-%02d-%02d 23:59:59' % (sdate.year, sdate.month, monthRange)

    date_day_begin = datetime.datetime.strptime(day_begin,"%Y-%m-%d %H:%M:%S")
    date_day_end = datetime.datetime.strptime(day_end,"%Y-%m-%d %H:%M:%S")
    next_day_begin = date_day_end+datetime.timedelta(seconds=120)

    return date_day_begin , date_day_end, next_day_begin



def get_week_start_end(d=None):
    if not d:
        d = datetime.datetime.now()


    this_week_start = d - datetime.timedelta(days=d.weekday())
    this_week_end = this_week_start + datetime.timedelta(days=6)

    return this_week_start.strftime("%Y-%m-%d") + " 00:00:00",this_week_end.strftime("%Y-%m-%d")+ " 23:59:59"





def get_week_start_end_day(d=None):
    if not d:
        d = datetime.datetime.now()


    this_week_start = d - datetime.timedelta(days=d.weekday())
    this_week_end = this_week_start + datetime.timedelta(days=6)

    return this_week_start.strftime("%m月%d日"),this_week_end.strftime("%m月%d日")




def humanreadable_mseconds(mseconds):
    seconds = int(mseconds) / 1000
    s = seconds % 60
    h = seconds / 60 / 60

    if h:
        m = seconds / 60 % 60
        ret = u"%02d:%02d:%02d" % (h,m,s)

    else:
        m = seconds / 60
        ret = u"%02d:%02d" % (m,s)

    return ret


def zero_date():
    d = datetime.datetime.today()
    return datetime.datetime(d.year, d.month, d.day)


def datetime_to_timestamp(d):
    return int(time.mktime(d.timetuple()))


def timestamp_to_datetime(response):
    "Converts a unix timestamp to a Python datetime object"
    if not response:
        return None
    try:
        response = int(response)
    except ValueError:
        return None
    return datetime.datetime.fromtimestamp(response)


def days_ago(day=30):
    return datetime.datetime.now() - datetime.timedelta(day)


def nature_days_ago(day=30):
    return zero_date() - datetime.timedelta(day)


def after_days(day=30):
    return datetime.datetime.now() + datetime.timedelta(day)

def after_from_days(dd,day=1):
    return dd + datetime.timedelta(day)


def nature_after_days(day=30):
    return zero_date() + datetime.timedelta(day)

def nature_after_days_end(day=30):
    return zero_date() + datetime.timedelta(day) - datetime.timedelta(seconds=60)


def seconds_to_zero():
    d = nature_after_days(1)
    return int(datetime_to_timestamp(d) - int(time.time()))


def is_weekend(d=datetime.datetime.today()):
    return d.weekday() in (0, 6)


def minutes_ago(seconds=300):
    return datetime.datetime.now() - datetime.timedelta(seconds=seconds)


def after_minutes(seconds=300):
    return datetime.datetime.now() + datetime.timedelta(seconds=seconds)


def int_day(d=None):
    if d is None:
        d = datetime.datetime.today()
    return int("%s%d%d" % (d.year,d.month, d.day))

def int_days(d=None):
    if d is None:
        d = datetime.datetime.today()
    return int("%s%02d%02d" % (d.year,d.month, d.day))


def int_month(d=None):
    if d is None:
        d = datetime.datetime.today()
    return int("%s%d" % (d.year, d.month))


def int_week(d=None):
    if d is None:
        d = datetime.datetime.today()

    monday = d.weekday()
    d = d - datetime.timedelta(monday)

    return int("%s%d%d" % (d.year, d.month, d.day))


def int_weeks(d=None):
    if d is None:
        d = datetime.datetime.today()

    monday = d.weekday()
    d = d - datetime.timedelta(monday)

    return int("%s%02d%02d" % (d.year, d.month, d.day))


def int_last_weeks(d=None):
    if d is None:
        d = datetime.datetime.today() - datetime.timedelta(7)

    monday = d.weekday()
    d = d - datetime.timedelta(monday)

    return int("%s%02d%02d" % (d.year, d.month, d.day))


def is_legal_date(d):
    timere = "^(\d{2}|\d{4})-((0([1-9]{1}))|(1[0|1|2]))-(([0-2]([0-9]{1}))|(3[0|1]))$"
    return re.match(timere, d) != None



def out_week_date(year,day):
    fir_day = datetime.datetime(year,1,1)
    zone = datetime.timedelta(days=day-1)
    return datetime.datetime.strftime(fir_day + zone, "%Y-%m-%d")


