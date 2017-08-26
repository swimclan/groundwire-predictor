# utils module with functions from lodash and other nice little diddys
from datetime import datetime, timedelta, date
from pydash import collections

def last_weekday(dt=datetime.now()):
    found = False
    c = 1
    while not found:
        test_date = dt - timedelta(days=c)
        yesterday = date.weekday(test_date)
        if not yesterday == 5 and not yesterday == 6:
            found = True
            break
        else:
            c += 1
    return test_date

def set_market_time(dt):
    open = dt
    close = dt
    return [open.replace(hour=13, minute=30, second=0, microsecond=0), close.replace(hour=20, minute=0, second=0, microsecond=0)]

def epoch(dt):
    epoch = datetime.utcfromtimestamp(0)
    return int((dt - epoch).total_seconds())

def previous_market_times(dt):
    ret = []
    marketday = set_market_time(last_weekday(dt))
    for t in marketday:
        ret.append(epoch(t))
    return ret


def has(obj, target):
    ret = False
    for key, val in obj.iteritems():
        if target == key:
            ret = True
    return ret

def index_of(arr, target):
    ret = -1
    for idx, val in enumerate(arr):
        if target == val:
            ret = idx
    return ret

def parse_env(file):
    ret = {}
    for line in file.readlines():   
        line_list = line.split('=')
        ret[line_list[0]] = line_list[1][0:-1]

    return ret

def each(collection, f):
    collections.for_each(collection, f)