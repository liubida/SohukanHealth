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

def get_start_end_for_month(d):
    '''d是某一天, 计算出d所在的某一个月的第一天和最后一天'''
#    now = datetime.datetime.now()
    
    # 这个月的第一天
    month = int(d.month)
    start = d.replace(month=month, day=1, hour=0, minute=0, second=0)
    
    # 下个月的第一天
    if month + 1 > 12:
        end = d.replace(month=month, day=31, hour=23, minute=59, second=59)
    else:
        next_month_first = d.replace(month=month + 1, day=1, hour=23, minute=59, second=59)
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
          
def read_file(filename):
    if not filename:
        return None
    
    f = open(filename, "r")  #  Opens file for reading
    lines = [] 
    for line in f:
        lines.append(line)
    f.close()
    return lines      

def get_week_num(date):
    '''某个日期是属于这一年的第几周, 返回那个周的周数
    以周一为一周的开始，但1月1日不是周一时,算作上一年的最后一周,返回0'''
    year = date.year
    wd = date.replace(month=1, day=1).weekday()
    days = (date - datetime.datetime(year, 1, 1)).days
    nweek = 0
    if wd:
        nweek = (days + wd) / 7
    else:
        nweek = days / 7 + 1
    return nweek

def get_week_sun(date):
    '''某个日期所在周的周日的日期
    以周一为一周的开始，但1月1日不是周一时,算作上一年的最后一周,返回0'''
    diff = 6 - date.weekday()
    step = datetime.timedelta(days=diff)
    return date + step 
        
if __name__ == '__main__':
    start_time = datetime.datetime.strptime("2012-10-24 10:35:08", "%Y-%m-%d %H:%M:%S")
    end_time = datetime.datetime.strptime("2012-10-27 01:05:43", "%Y-%m-%d %H:%M:%S")
    a = datetime.datetime.strptime("2012-10-21 01:05:43", "%Y-%m-%d %H:%M:%S")
    b = datetime.datetime.strptime("2012-10-28 01:05:43", "%Y-%m-%d %H:%M:%S")
    print start_time
    print end_time
#    tdiff = timediff(start_time,end_time)
#    print tdiff
    print get_week_num(start_time)
    print start_time.weekday()
    step = datetime.timedelta(days=(6 - start_time.weekday()))
    print get_week_sun(start_time)
    print get_week_sun(end_time)
    print get_week_sun(a)
    print get_week_sun(b)
    
    print '((((((((((((((((((('
    
    final_start = datetime.datetime(2012, 5, 1, 0, 0, 0)
    start = final_start
    end = datetime.datetime.now()
    one_day = datetime.timedelta(days=1)
    
    while start < end:
        # 本月(start)的起止时间点
        start_time, end_time = get_start_end_for_month(start)
        print start_time, end_time
        start = end_time + one_day
    
#    while True:
#        now = datetime.datetime.now()
#        a = now.minute
#        b = now.second
#        print a%5
#        print a, ':', b, '|  ',(5 - 1 - a % 5) * 60 + (60 - b)
#        time.sleep(1)
#    
    
    
