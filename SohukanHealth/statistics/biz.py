# -*- coding: utf-8 -*-
'''
Created on Jun 19, 2012

@author: liubida
'''
from config.config import c
from monitor.models import AppAvailableData, SomeTotal
import MySQLdb
import anyjson
import datetime
import urlparse

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
    if count <= 10:
        return 2;
    if count <= 20:
        return 3;
    if count <= 50:
        return 4;
    if count <= 100:
        return 5;
    if count <= 200:
        return 6;
    if count > 200:
        return 7;
    
    return None;

def _get_fix(start_time, end_time):
    having_fix = ''
    and_fix = ''
    
    #时间约束, 即某个时间之前的非测试用户数
    if start_time:
        having_fix += "having create_time >= '%s'" % start_time
        and_fix += "and gmt_create >= '%s'" % start_time
    
    if end_time:
        if having_fix:
            having_fix += " and create_time <='%s'" % end_time
        else:
            having_fix = "having create_time <='%s'" % end_time
        
        and_fix += "and gmt_create <= '%s'" % end_time
    
    return having_fix, and_fix    

def get_bookmark_per_user(start_time=None):
    dd = get_bookmark_per_user_raw_data(start_time)

    s = {}
    s['success'] = True
    s['info'] = 'get_bookmark_per_user'
    s['code'] = 0
    s['total'] = len(dd)
    s['list'] = []
    
    i = 0
    max = len(color) - 1
    for d in dd:
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

def get_bookmark_percent(start_time=None, end_time=None):
    data, raw_data = get_bookmark_percent_raw_data(start_time, end_time);
    
    s = {}
    s['success'] = True
    s['info'] = 'get_bookmark_percent'
    s['code'] = 0
    s['total'] = len(data)
    s['list'] = data
    s['raw'] = raw_data
    
    return anyjson.dumps(s)

def get_bookmark_website(start_time=None, end_time=None):
    data = get_bookmark_website_raw_data(start_time, end_time);
    
    s = {}
    s['success'] = True
    s['info'] = 'get_bookmark_website'
    s['code'] = 0
    s['total'] = len(data)
    s['list'] = data
    
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

def get_bookmark_percent_raw_data(start_time=None, end_time=None, limit=100):
    '''为[用户收藏文章数统计]获取原始数据'''
    try:
        conn = MySQLdb.connect(**c.db_config)
        cursor = conn.cursor()

        ret = [{'name':'1篇', 'count':0},
               {'name':'2-5篇', 'count':0},
               {'name':'6-10篇', 'count':0},
               {'name':'11-20篇', 'count':0},
               {'name':'21-50篇', 'count':0},
               {'name':'51-100篇', 'count':0},
               {'name':'101-200篇', 'count':0},
               {'name':'>200篇', 'count':0}]
        mm = {}
        
        having_fix, and_fix = _get_fix(start_time, end_time)
        
        #去掉测试用户的id
        tmp = ' and id !='
        tmp += ' and id !='.join(map(lambda x:str(x), test_id))
        
        sql_total = "select count(*) from account_user where id > 100 %s %s" % (tmp, and_fix)        
        print 'sql_total:', sql_total
        
        cursor.execute(sql_total)
        result = cursor.fetchone()
        user_total = result[0]
        print user_total
        
        for i in range(64):
            cursor.execute("select user_id, count(*), create_time from bookmark_bookmark_%s group by user_id %s" % (i, having_fix))
            results = cursor.fetchall()
            for d in results:
                user_id = int(d[0])
                count = int(d[1])
                if not _is_test(user_id):
                    '''根据用户的文章数情况, 把相应的范围数+1'''
                    ret[_which_index(count)]['count'] += 1
                    
                    if count in mm.keys():
                        mm[count] += 1
                    else:
                        mm[count] = 1
        ret_mm = []
        for k in mm.keys():
            tmp = {}
            tmp['p_count'] = k
            tmp['u_count'] = mm[k]
            ret_mm.append(tmp)
        
        user_used = 0
        for r in ret:
            user_used += r['count']

        ret_mm.append({'p_count':0, 'u_count':user_total - user_used})        
        ret.append({'name':'0篇', 'count':user_total - user_used})
        
        ret_mm.sort(key=lambda x:x['p_count'], reverse=True)
        ret.sort(key=lambda x:x['count'], reverse=True)
        return ret[:limit], ret_mm[:limit];
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
                
def get_bookmark_website_raw_data(start_time=None, end_time=None, limit=20):
    '''为[收藏文章的域名统计]获取原始数据'''
    try:
        conn = MySQLdb.connect(**c.db_config)
        cursor = conn.cursor()
        
        having_fix, and_fix = _get_fix(start_time, end_time)

        mm = {}
        ret = []
        
        for i in range(64):
            cursor.execute("select user_id, url from bookmark_bookmark_%s where 1=1 %s" % (i, and_fix))
            results = cursor.fetchall()
            for d in results:
                user_id = int(d[0])
                url = str(d[1])
                domain = urlparse.urlparse(url)[1]
                if not _is_test(user_id):
                    if domain in mm.keys():
                        mm[domain] += 1
                    else:
                        mm[domain] = 1
        print mm

        for k in mm.keys():
            tmp = {}
            tmp['domain'] = k
            tmp['count'] = mm[k]
            ret.append(tmp)
        ret.sort(key=lambda x:x['count'], reverse=True)

        return ret[:limit];
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
            cursor.execute("select id, create_time, user_id from bookmark_bookmark_%s %s" % (i, prefix))
            results = cursor.fetchall()
            for d in results:
                kv = {}
                kv['id'] = '%d_%d' % (i, int(d[0]))
                kv['time'] = d[1]
                if not _is_test(int(d[2])):
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
    
def get_bookmark_per_user_raw_data(start_time=None, limit=100):
    '''为[用户收藏文章数排行]获取原始数据'''
    try:
        conn = MySQLdb.connect(**c.db_config)
        cursor = conn.cursor()
        
        if start_time:
            prefix = "having create_time > '%s'" % start_time
        else:
            prefix = ''
        ret = []
        for i in range(64):
            cursor.execute("select user_id, count(*), create_time from bookmark_bookmark_%s group by user_id %s" % (i, prefix))
            results = cursor.fetchall()
            for d in results:
                kv = {}
                kv['user_id'] = int(d[0])
                kv['count'] = int(d[1])
                if not _is_test(kv['user_id']):
                    ret.append(kv)
                            
        ret.sort(key=lambda x:x['count'], reverse=True)
        return ret[:limit];
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

def get_userdata_for_day_report(today_start,today_end):
    
    # 昨天
    yd_start = today_start - datetime.timedelta(days=1)
    yd_end = today_end - datetime.timedelta(days=1)
    
    # 前天
    b_yd_start = today_start - datetime.timedelta(days=2)
    b_yd_end = today_end - datetime.timedelta(days=2)
    
    print today_start
    print today_end
    print yd_start
    print yd_end
    print b_yd_start
    print b_yd_end
    
    # 今日用户总数
    user_total = int(SomeTotal.objects.filter(name='user', time__gte=today_start, time__lte=today_end).values('count').\
                            reverse()[0]['count'])
    # 昨日用户总数
    user_total_yd = int(SomeTotal.objects.filter(name='user', time__gte=yd_start, time__lte=yd_end).\
                            values('count').reverse()[0]['count'])
    # 前日用户总数
    user_total_b_yd = int(SomeTotal.objects.filter(name='user', time__gte=b_yd_start, time__lte=b_yd_end).\
                            values('count').reverse()[0]['count'])
    
    # 今日新增用户数
    user_new = user_total - user_total_yd
    
    # 昨日新增用户数
    user_new_yd = user_total_yd - user_total_b_yd
    
    # 今日用户总数_增长率
    user_total_inc = (abs(user_new) + 0.00000001) / user_total_yd
    user_total_inc = round(user_total_inc, 4)
#    user_total_inc_color = '#c00' if user_new > 0  else '#008000'
    
    # 昨日用户总数_增长率
    user_total_inc_yd = (abs(user_new_yd) + 0.00000001) / user_total_b_yd
    user_total_inc_yd = round(user_total_inc_yd, 4)
        
    # 环比新增用户_增长率_百分点
    user_new_inc = user_total_inc - user_total_inc_yd 
    user_new_inc = round(user_new_inc, 4)
#    user_new_inc_color = '#c00' if user_new_inc > 0  else '#008000'
    
    ret = {}
    ret['total'] = user_total;
    ret['total_yd'] = user_total_yd;
    ret['total_b_yd'] = user_total_b_yd;
    ret['total_inc'] = user_total_inc;
    ret['total_inc_yd'] = user_total_inc_yd;
    ret['new_inc'] = user_new_inc;
    
    return ret


def get_bookmarkdata_for_day_report(today_start,today_end):
    
    # 昨天
    yd_start = today_start - datetime.timedelta(days=1)
    yd_end = today_end - datetime.timedelta(days=1)
    
    # 前天
    b_yd_start = today_start - datetime.timedelta(days=2)
    b_yd_end = today_end - datetime.timedelta(days=2)
    
    print today_start
    print today_end
    print yd_start
    print yd_end
    print b_yd_start
    print b_yd_end
    
    # 今日文章总数
    bookmark_total = int(SomeTotal.objects.filter(name='bookmark', time__gte=today_start, time__lte=today_end).values('count').\
                            reverse()[0]['count'])
    # 昨日文章总数
    bookmark_total_yd = int(SomeTotal.objects.filter(name='bookmark', time__gte=yd_start, time__lte=yd_end).\
                            values('count').reverse()[0]['count'])
    # 前日文章总数
    bookmark_total_b_yd = int(SomeTotal.objects.filter(name='bookmark', time__gte=b_yd_start, time__lte=b_yd_end).\
                            values('count').reverse()[0]['count'])
    
    # 今日新增文章数
    bookmark_new = bookmark_total - bookmark_total_yd
    
    # 昨日新增文章数
    bookmark_new_yd = bookmark_total_yd - bookmark_total_b_yd
    
    # 今日文章总数_增长率
    bookmark_total_inc = (abs(bookmark_new) + 0.00000001) / bookmark_total_yd
    bookmark_total_inc = round(bookmark_total_inc, 4)
#    bookmark_total_inc_color = '#c00' if bookmark_new > 0  else '#008000'
    
    # 昨日文章总数_增长率
    bookmark_total_inc_yd = (abs(bookmark_new_yd) + 0.00000001) / bookmark_total_b_yd
    bookmark_total_inc_yd = round(bookmark_total_inc_yd, 4)
#    bookmark_total_inc_yd_color = '#c00' if bookmark_new_yd > 0  else '#008000'
        
    # 环比新增文章_增长率_百分点
    bookmark_new_inc = bookmark_total_inc - bookmark_total_inc_yd 
    bookmark_new_inc = round(bookmark_new_inc, 4)
#    bookmark_new_inc_color = '#c00' if bookmark_new_inc > 0  else '#008000'
    
    ret = {}
    ret['total'] = bookmark_total;
    ret['total_yd'] = bookmark_total_yd;
    ret['total_b_yd'] = bookmark_total_b_yd;
    ret['total_inc'] = bookmark_total_inc;
    ret['total_inc_yd'] = bookmark_total_inc_yd;
    ret['new_inc'] = bookmark_new_inc;
    
    return ret
    
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

#    a = get_bookmark_percent_raw_data('2012.06.05 16:54:10')
#    a = tmp_raw_data()
    b = get_bookmark_website_raw_data('2012.07.10', '2012.07.12')
    print b
