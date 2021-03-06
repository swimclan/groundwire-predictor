# utils module with functions from lodash and other nice little diddys
from datetime import datetime, timedelta, date
from pydash import collections
from pydash import numerical
import pytz

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

def current_market_times(dt):
    ret = []
    marketday = set_market_time(dt)
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

def average(list):
    return numerical.mean(list)

def map(arr, iteratee):
    ret = []
    for key, item in enumerate(arr):
        ret.append(iteratee(item, key, arr))
    return ret

def isMorning(epoch):
    dt = datetime.utcfromtimestamp(epoch)
    if dt.hour >= 16:
        return False
    return True

def parsePubDate(d):
    # 2017-09-26 13:35:00 +0000
    ret = datetime.strptime(d[0:19], "%Y-%m-%d %H:%M:%S").replace(tzinfo=pytz.UTC)
    return ret

def serializeNews(newsitems):
    ret = []
    for item in newsitems:
        item['publication_date'] = parsePubDate(item['publication_date'])
        ret.append(item)
    return ret

def dictList(obj):
    keystr = '('
    valstr = '('
    for key, value in obj.iteritems():
      keystr += (str(key) + ", ")
      valstr += ("'" + str(value) + "', ")
    keystr = keystr[0:-2]
    valstr = valstr[0:-2]
    keystr += ')'
    valstr += ')'
    return (keystr, valstr)

def parseISODate(d):
  d_arr = d.split('-')
  if len(d_arr) < 3:
    print 'ERROR! Invalid date string supplied!'
  else:
    return datetime(int(d_arr[0]), int(d_arr[1]), int(d_arr[2]))
    
def filterNoNews(observations):
    print observations[0]
    ret = []
    for item in observations:
        if item['age_recent_news'] < 8760:
            ret.append(item)
    return ret