import datetime
import urllib2

def mytimer(func):
    def wrapper(*args, **kwargs):
        start = datetime.datetime.now()
        func(*args, **kwargs)
        end = datetime.datetime.now()
        return (end - start).seconds
    return wrapper

def request(url, data=None, cookie=None):
    try:
        req = urllib2.Request(url=url, data=data);
        if None != cookie:
            req.add_header(*cookie);
            
        return urllib2.urlopen(req)
    except Exception as e:
        return e

def get_date_and_time():
    day_format = "%Y.%m.%d"
    time_format = "%H:%M:%S"
    
    now = datetime.datetime.now()
    time = now.strftime(time_format)
    date = now.strftime(day_format)
    
    return date, time

if __name__ == '__main__':
    pass