import anyjson
import datetime
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

if __name__ == '__main__':
    get_date_and_time()
