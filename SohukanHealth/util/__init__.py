# -*- coding: utf-8 -*-
import anyjson
import datetime
import time
import urllib
import urllib2

def mytimer(func):
    def wrapper(*args, **kwargs):
        start = datetime.datetime.now()
        func(*args, **kwargs)
        end = datetime.datetime.now()
        return (end - start).seconds
    return wrapper

def print_info(name=''):
    def wrapper1(func):
        def wrapper2(*args, **kwargs):
            date, time = get_date_and_time()
            print '[%s %s] %s start' % (date, time, name)
            ret = func(*args, **kwargs)
            if ret:
                print '[%s %s] %s end result:%s' % (date, time, name, ret)
            else:
                print '[%s %s] %s end' % (date, time, name)
        return wrapper2
    return wrapper1;

def request(url, data=None, cookie=None):
    try:
        req = urllib2.Request(url=url, data=data);
        if None != cookie:
            req.add_header(*cookie);
            
        return urllib2.urlopen(req)
    except Exception, e:
        raise e

def query_ua(ua_string):
    ua_query_url = 'http://www.useragentstring.com'
    data = urllib.urlencode({"uas":ua_string.encode('utf8'), "getJSON":"agent_type-agent_name-os_type"});
    try:
        response = request(ua_query_url, data);
        
        if response.code == 200:
            s = response.read()
            j = anyjson.loads(s)
            return j
        else:
            return None 
    except Exception, e:
        raise e
    
def get_date_and_time():
    day_format = "%Y.%m.%d"
    time_format = "%H:%M:%S"
    
    now = datetime.datetime.now()
    time = now.strftime(time_format)
    date = now.strftime(day_format)
    
    return date, time

def get_start_end_for_month(month=1):
    now = datetime.datetime.now()
    
    # 这个月的第一天
    start = now.replace(month=month, day=1, hour=0, minute=0, second=0)
    
    # 下个月的第一天
    if month + 1 > 12:
        end = now.replace(month=month, day=31, hour=23, minute=59, second=59)
    else:
        next_month_first = now.replace(month=month + 1, day=1, hour=23, minute=59, second=59)
        end = next_month_first - datetime.timedelta(days=1)

    return start, end

def timediff(start, end, ft='second'):
    # end 必须大于 start
    diff = end - start
    seconds = diff.days * 24 * 3600 + diff.seconds
     
    if ft == 'second':
        return seconds
    if ft == 'minute':
        return round((diff.days * 24 * 60 + (diff.seconds + 0.0000000001) / 60), 0)
    
def to_percent(p):
    return '%.4f%%' % (p * 100)

def left_seconds(time, mod=5):
    # 离最近的整数5分钟还剩多少秒
    # a = 21:00:10; 距离a最近的整数5分钟是21:05:00
    # 则结果应该是 (4*60+50) 秒
    min = time.minute
    sec = time.second
    return (mod - 1 - min % mod) * 60 + (60 - sec)
    
if __name__ == '__main__':
    start_time = datetime.datetime.strptime("2012-08-17 10:35:08","%Y-%m-%d %H:%M:%S")
    end_time = datetime.datetime.strptime("2012-08-17 01:05:43","%Y-%m-%d %H:%M:%S")
    print start_time
    print end_time
    tdiff = timediff(start_time,end_time)
    print tdiff
    
#    while True:
#        now = datetime.datetime.now()
#        a = now.minute
#        b = now.second
#        print a%5
#        print a, ':', b, '|  ',(5 - 1 - a % 5) * 60 + (60 - b)
#        time.sleep(1)
#    
    
    
