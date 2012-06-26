# -*- coding: utf-8 -*-
'''
Created on Jun 19, 2012

@author: liubida
'''
from config.config import lock, c
from monitor.models import AppAvailableData
import MySQLdb
import datetime
import json

#ring = HashRing([str(i) for i in range(64)])

color = ['#FF0F00', '#FF6600', '#FF9E01', '#FCD202', '#F8FF01', '#B0DE09', \
         '#04D215', '#0D8ECF', '#0D52D1', '#2A0CD0', '#8A0CCF', '#CD0D74']

def _is_test(user_id):
    test_id = [108, 165, 591]
    
    if user_id < 100 or user_id in test_id:
        return True;
    else:
        return False;
    
def get_bookmark_per_user(include_test=True):
    dd = get_bookmark_per_user_raw_data(include_test)

    s = {}
    s['success'] = True
    s['info'] = 'get_bookmark_per_user'
    s['code'] = 0
    s['total'] = len(dd)
    s['list'] = []
    
    i = 0
    max = len(color) - 1
    for d in dd[0:100]:
        tmp = {}
        tmp['user_id'] = d['user_id']
        tmp['count'] = d['count']
        if i >= max:
            tmp['color'] = color[max]
        else:
            tmp['color'] = color[i]
        s['list'].append(tmp)
        i += 1

    return json.dumps(s)

def get_bookmark_time(start_time=None):
    dd = calc_bookmark_time(start_time);
    
    s = {}
    s['success'] = True
    s['info'] = 'get_bookmark_time'
    s['code'] = 0
    s['total'] = len(dd)
    s['list'] = dd
    
    return json.dumps(s)

def calc_bookmark_time(start_time=None):
    raw_data = get_bookmark_time_raw_data(start_time);
    
#    filter(lambda x: x['time']>=start_time and x['time']<=end_time, raw_data)
    
    
    ret = [];
    for i in range(24):
        kv = {};
        kv['hour'] = i;
        kv['count'] = 0;
        ret.append(kv)
        
    for d in raw_data:
        ret[d['time'].hour]['count'] += 1
    
    # fix the color
    ret.sort(key=lambda x:x['count'], reverse=True)
    
    i = 0
    max = len(color) - 1
    for d in ret:
        if i >= max:
            d['color'] = color[max]
        else:
            d['color'] = color[i]
        i += 1
    ret.sort(key=lambda x:x['hour'], reverse=False)
    
    return ret
    
def get_bookmark_time_raw_data(start_time=None):
    locked = False;
    try:
        if lock.acquire():
            locked = True
            conn = MySQLdb.connect(**c.db_config)
            cursor = conn.cursor()
            
            if start_time:
                prefix = "where create_time > '%s'" % start_time
            else:
                prefix = ''
            ret = []
            for i in range(64):
                cursor.execute("select id, create_time from bookmark_bookmark_%s %s" % (i, prefix))
                results = cursor.fetchall()
                for d in results:
                    kv = {}
                    kv['id'] = '%d_%d' % (i, int(d[0]))
                    kv['time'] = d[1]
                    ret.append(kv)
                                
            ret.sort(key=lambda x:x['time'], reverse=True)
            return ret;
    except Exception as e:
        c.logger.error(e)
        return str(e)
    finally:
        if locked:
            lock.release()
        try:
            if cursor:
                cursor.close()
        except Exception as e:
            c.logger.error(e)
        finally:
            if conn:
                conn.close()
    
def get_bookmark_per_user_raw_data(include_test=True):
    locked = False;
    try:
        if lock.acquire():
            locked = True
            conn = MySQLdb.connect(**c.db_config)
            cursor = conn.cursor()
            
            ret = []
            for i in range(64):
                cursor.execute("select user_id, count(*) from bookmark_bookmark_%s group by user_id" % i)
                results = cursor.fetchall()
                for d in results:
                    kv = {}
                    kv['user_id'] = int(d[0])
                    kv['count'] = int(d[1])
                    if include_test or not _is_test(kv['user_id']):
                        ret.append(kv)
                                
            ret.sort(key=lambda x:x['count'], reverse=True)
            return ret;
    except Exception as e:
        c.logger.error(e)
        return str(e)
    finally:
        if locked:
            lock.release()
        try:
            if cursor:
                cursor.close()
        except Exception as e:
            c.logger.error(e)
        finally:
            if conn:
                conn.close()

def calc_app_available(duration='day'):
    '''duration=hour, day, week, month, sixmonths, year'''
    
    now = datetime.datetime.now()

    if 'hour' == duration:
        delta = datetime.timedelta(hours=1)
    elif 'day' == duration:
        delta = datetime.timedelta(days=1)
    elif 'week' == duration:
        delta = datetime.timedelta(weeks=1)
    elif 'month' == duration:
        delta = datetime.timedelta(weeks=4)
    elif 'sixmonths' == duration:
        delta = datetime.timedelta(weeks=4 * 6)
    elif 'year' == duration:
        delta = datetime.timedelta(weeks=4 * 52)
    start_time = now - delta
    print start_time
    
    success_data = AppAvailableData.objects.filter(result=True, time__gte=start_time).count()
    failure_data = AppAvailableData.objects.filter(result=False, time__gte=start_time).count()

    if success_data or failure_data:
        ret = 100 * (success_data + 0.00001) / (success_data + failure_data)
        return format(ret, '.2f')
    else:
        return 'None'

def get_app_available():
    hour_available = calc_app_available('hour')
    day_available = calc_app_available('day')
    week_available = calc_app_available('week')
    month_available = calc_app_available('month')
    sixmonths_available = calc_app_available('sixmonths')
    year_available = calc_app_available('year')
    
    ret = {};
    ret['hour'] = hour_available
    ret['day'] = day_available
    ret['week'] = week_available
    ret['month'] = month_available
    ret['sixmonths'] = sixmonths_available
    ret['year'] = year_available
    
    return ret
#    return dict_to_json(ret)
    
def dict_to_json(data):
    s = {}
    s['success'] = True
    s['info'] = ''
    s['code'] = 0
    s['total'] = 1
    s['list'] = []
    s['list'].append(data)
    return s
    
def appAvailableData_to_json(data):
    s = {}
    s['success'] = True
    s['info'] = ''
    s['code'] = 0
    s['total'] = data.count()
    s['list'] = []
    for d in data:
        tmp = {}
        tmp['name'] = d['name']
        tmp['time_used'] = d['time_used']
        tmp['time'] = d['time'].strftime('%Y.%m.%d %H:%M:%S')
        s['list'].append(tmp)
    return json.dumps(s)   
    
if __name__ == '__main__':
#    a = get_app_available()
#    print a
#    get_bookmark_per_user()
    calc_bookmark_time(0, 0)
