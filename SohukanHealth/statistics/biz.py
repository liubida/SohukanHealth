# -*- coding: utf-8 -*-
'''
Created on Jun 19, 2012

@author: liubida
'''
from config.config import c
from monitor.models import AppAvailableData
import MySQLdb
import anyjson
import datetime

#ring = HashRing([str(i) for i in range(64)])

#color = ['#FF0F00', '#FF6600', '#FF9E01', '#FCD202', '#F8FF01', '#B0DE09', \
#         '#04D215', '#0D8ECF', '#0D52D1', '#2A0CD0', '#8A0CCF', '#CD0D74']
color = ['#FF0F00', '#FF9E01', '#FCD202', '#F8FF01', '#B0DE09', \
         '#04D215', '#0D8ECF', '#0D52D1', '#2A0CD0', '#8A0CCF', '#CD0D74']
test_id = [108, 165, 591]

def _is_test(user_id):
    
    if user_id < 100 or user_id in test_id:
        return True;
    else:
        return False;
    
def _which_index(count):
#    if count < 0:
#        return 0;
    if count == 1:
        return 0;
    if count <= 5:
        return 1;
    if count <= 50:
        return 2;
    if count <= 100:
        return 3;
    if count <= 200:
        return 4;
    if count > 200:
        return 5;
    
    return None;

def get_bookmark_per_user(include_test=False):
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

    return anyjson.dumps(s)

def get_bookmark_time(start_time=None):
    dd = calc_bookmark_time(start_time);
    
    s = {}
    s['success'] = True
    s['info'] = 'get_bookmark_time'
    s['code'] = 0
    s['total'] = len(dd)
    s['list'] = dd
    
    return anyjson.dumps(s)

def get_bookmark_percent(include_test=False):
    dd = get_bookmark_percent_raw_data(include_test);
    
    s = {}
    s['success'] = True
    s['info'] = 'get_bookmark_percent'
    s['code'] = 0
    s['total'] = len(dd)
    s['list'] = dd
    
    return anyjson.dumps(s)

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

def get_bookmark_percent_raw_data(include_test=False):
    try:
        conn = MySQLdb.connect(**c.db_config)
        cursor = conn.cursor()

        ret = [{'name':'1篇', 'count':0},
               {'name':'2-5篇', 'count':0},
               {'name':'6-50篇', 'count':0},
               {'name':'51-100篇', 'count':0},
               {'name':'101-200篇', 'count':0},
               {'name':'>200篇', 'count':0}]
        
#            if start_time:
#                prefix = "where create_time > '%s'" % start_time
#            else:
#                prefix = ''
        prefix = ''
        print include_test
        
        if include_test:
            sql_total = "select count(*) from account_user"
        else:
            tmp = ' and id !='
            tmp += ' and id !='.join(map(lambda x:str(x), test_id))
            print tmp
            sql_total = "select count(*) from account_user where id > 100 %s" % tmp
            print sql_total
            
        cursor.execute(sql_total)
        result = cursor.fetchone()
        user_total = result[0]
        print user_total
        
        for i in range(64):
#                cursor.execute("select id, create_time from bookmark_bookmark_%s %s" % (i, prefix))
            cursor.execute("select user_id, count(*) from bookmark_bookmark_%s group by user_id %s" % (i, prefix))
            results = cursor.fetchall()
            for d in results:
                if include_test or not _is_test(int(d[0])):
                    ret[_which_index(int(d[1]))]['count'] += 1
        
# TODO:     a = reduce(lambda x, y:x['count'] + y['count'], ret)

        user_used = 0
        for r in ret:
            user_used += r['count']
        
        ret.append({'name':'0篇', 'count':user_total - user_used})
        
        ret.sort(key=lambda x:x['count'], reverse=True)
        return ret;
    except Exception, e:
        c.logger.error(e)
        raise e
    finally:
        try:
            if cursor:
                cursor.close()
        except Exception, e:
            c.logger.error(e)
        finally:
            if conn:
                conn.close()
                        
def get_bookmark_time_raw_data(start_time=None):
    '''为[收藏文章时间段]获取原始数据'''
    try:
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
    except Exception, e:
        c.logger.error(e)
        return str(e)
    finally:
        try:
            if cursor:
                cursor.close()
        except Exception, e:
            c.logger.error(e)
        finally:
            if conn:
                conn.close()
    
def get_bookmark_per_user_raw_data(include_test=False):
    '''为[用户收藏文章数排行]获取原始数据'''
    try:
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
    except Exception, e:
        c.logger.error(e)
        return str(e)
    finally:
        try:
            if cursor:
                cursor.close()
        except Exception, e:
            c.logger.error(e)
        finally:
            if conn:
                conn.close()

def calc_app_available(duration='day'):
    '''
    计算系统可用率
    duration=hour, day, week, month, sixmonths, year
    '''
    
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
    return anyjson.dumps(s)   

def tmp_raw_data(include_test=False):
    try:
        conn = MySQLdb.connect(**c.db_config)
        cursor = conn.cursor()
        
        ret = []
        for i in range(64):
            cursor.execute("select user_id, url from bookmark_bookmark_%s where gmt_create > '2012-07-04 20:00:00' \
            and gmt_create < '2012-07-04 22:20:00'" % i)
            results = cursor.fetchall()
            for d in results:
                if d[0]:
                    kv = {}
                    kv['user_id'] = int(d[0])
                    kv['url'] = str(d[1])
                    kv['bookmark'] = i
                    print kv['user_id'], kv['url']
#                    if include_test or not _is_test(kv['user_id']):
#                        ret.append(kv)
                    ret.append(kv)
        ret.sort(key=lambda x:x['user_id'], reverse=True)
        return ret;
    except Exception, e:
        c.logger.error(e)
        return str(e)
    finally:
        try:
            if cursor:
                cursor.close()
        except Exception, e:
            c.logger.error(e)
        finally:
            if conn:
                conn.close()
    
if __name__ == '__main__':
#    a = get_app_available()
#    print a
#    get_bookmark_per_user()
#    calc_bookmark_time(0, 0)
#    print get_bookmark_per_user_raw_data()
#    get_bookmark_percent_raw_data()
#    a = get_bookmark_percent(include_test=True)
#    a = get_bookmark_percent()
#    print a
#    tmp = 'or id = '
#    tmp += " or id=".join(map(lambda x:str(x), test_id))
##        tmp += 'or id='.join(str(i))
#    print tmp        

    a = tmp_raw_data()
    print a
