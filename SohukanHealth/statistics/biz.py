# -*- coding: utf-8 -*-
'''
Created on Jun 19, 2012

@author: liubida
'''
import sys
import os
root_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
print root_path
sys.path.append(root_path)
print sys.path

from django.core.management import setup_environ
from SohukanHealth import settings
print settings
setup_environ(settings)

from statistics.models import Aggregation
from config.config import c
from monitor.models import SomeTotal
from util import to_percent
import MySQLdb
import anyjson
import datetime
import urlparse


def get_data_interval(raw_data, delta=datetime.timedelta(days=1), time_format='str'):
    ret = []
    day_start = raw_data[0]['time']
    for d in raw_data:
            if d['time'].hour == 23 and \
               d['time'].year == day_start.year and \
               d['time'].month == day_start.month and \
               d['time'].day == day_start.day:
                if time_format == 'str':
                    ret.append({'time':d['time'].strftime('%m-%d'), 'count':d['count']})
                else:
                    ret.append({'time':d['time'], 'count':d['count']})
                day_start += delta
    return ret

def add_inc_for_data(data):
    list = data['list']
    if not list:
        return
    list[0]['inc'] = 0
    for i in range(1, len(list)):
        origin = list[i - 1]['count']
        later = list[i]['count']
        list[i]['inc'] = round(((later - origin) + 0.0000001) / origin, 4)
            
def _is_test(user_id):
    
    if user_id in c.test_id:
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

def _get_week_list(start=datetime.datetime(2012, 7, 16), end=None):
    now = datetime.datetime.now()
    start_time = start if start else now.replace(month=1, day=1)
    end_time = end if end else now.replace(month=12, day=31)
    
    week_list = [];
    
    cur = start_time
    step = datetime.timedelta(days=7)
    
    # 处理开始时间
    first_week_day = cur.isoweekday()
    if first_week_day != 1:
        week_list.append((cur.strftime('%Y-%m-%d'), (cur + datetime.timedelta(days=(7 - first_week_day))).strftime('%Y-%m-%d')))
        cur = cur + datetime.timedelta(days=(7 - first_week_day + 1))
    
    while cur <= end_time and (end_time - cur).days >= 7:
        week_list.append((cur.strftime('%Y-%m-%d'), (cur + datetime.timedelta(days=6)).strftime('%Y-%m-%d')))
        cur = cur + step
         
    return week_list
#_get_week_list(start=None, end=datetime.datetime(2012, 8, 30))
    
def _get_fix(start_time, end_time, start_delta=None, end_delta=None):
    having_fix = ''
    and_fix = ''
    
    if start_delta:
        start_time = start_time + start_delta
    if end_delta:
        end_time = end_time + end_delta
    
    #时间约束, 即某个时间区间
    if start_time:
        having_fix += " having create_time >= '%s' " % start_time
        and_fix += " and gmt_create >= '%s' " % start_time
    
    if end_time:
        if having_fix:
            having_fix += " and create_time <='%s' " % end_time
        else:
            having_fix = " having create_time <='%s' " % end_time
        
        and_fix += " and gmt_create <= '%s' " % end_time
    
    return having_fix, and_fix    

def get_bookmark_per_user(start_time=None, end_time=None, limit=100):
    '''返回jsondata'''
    raw_data = get_bookmark_per_user_raw_data(start_time, end_time, limit)
    
    # dd是获取的原始数据, 加入颜色值等其他信息
    i = 0 
    max = len(c.color) - 1
    for d in raw_data:
        d['color'] = c.color[i if i <= max else max]
        i += 1
        
    ret = {'list':raw_data}
    return anyjson.dumps(ret)

def get_bookmark_time(start_time=None, end_time=None):
    raw_data = get_bookmark_time_raw_data(start_time, end_time);
    
    # 按照时间段进行统计, 先设定24小时的count都为0
    # 这样做的目的, 避免因有的时段没有文章而无法展现
    data = [];
    for i in range(24):
        data.append({'hour':i, 'count':0})
    for d in raw_data:
        data[d['time'].hour]['count'] += 1
    
    # 先按照count排序, 目的是为了上色; 顺便计算下总文章数, 目的是为了后面计算percent
    data.sort(key=lambda x:x['count'], reverse=True)
    i = 0
    max = len(c.color) - 1
    sum_count = 0
    for d in data:
        d['color'] = c.color[i if i <= max else max]
        sum_count += d['count']
        i += 1
    # 再按照hour排序, 最后的展现顺序
    data.sort(key=lambda x:x['hour'], reverse=False)

    # 计算percent    
    for d in data:
        d['percent'] = round((d['count'] + 0.0000001) / sum_count, 4)
        
    ret = {'list':data}
    return anyjson.dumps(ret)

def get_bookmark_percent(start_time=None, end_time=None, raw=True):
    data, raw_data = get_bookmark_percent_raw_data(start_time, end_time);
    
    ret = {'list':data}
    if raw:
        ret['raw'] = raw_data
    return anyjson.dumps(ret)

def get_bookmark_website(start_time, end_time, limit=100):
    '''start_time, end_time is string'''
    raw_data = Aggregation.objects.filter(type='bookmark_website', time__gte=start_time, time__lte=end_time).values('time', 'content')

    data = {}
    for d in raw_data:
        data[d['time'].strftime("%Y-%m-%d")] = anyjson.loads(d['content'])

    step = datetime.timedelta(days=1)
    start = datetime.datetime.strptime(start_time, "%Y-%m-%d %H:%M:%S")
    end = datetime.datetime.strptime(end_time, "%Y-%m-%d %H:%M:%S")
    cur = start
    
    ret = []
    urls = {} 
    mm = {}   
    while cur <= end:
        key = cur.strftime("%Y-%m-%d")

        if key not in data.keys():
            cur += step
            continue
        
        for d in data[key]:
            domain_key = d['domain']
            if domain_key in mm.keys():
                mm[domain_key] += d['count']
            else:
                mm[domain_key] = d['count']
        cur += step

    for k in mm:
        ret.append({'count':mm[k], 'domain':k})
        
    ret.sort(key=lambda x:x['count'], reverse=True)

    return ret[:limit]

def get_bookmark_website_detail(start_time, end_time, limit=100, urls_limit=24):
    '''start_time, end_time is string'''
    raw_data = Aggregation.objects.filter(type='bookmark_website', time__gte=start_time, time__lte=end_time).values('time', 'content')

    data = {}
    for d in raw_data:
        data[d['time'].strftime("%Y-%m-%d")] = anyjson.loads(d['content'])

    step = datetime.timedelta(days=1)
    start = datetime.datetime.strptime(start_time, "%Y-%m-%d %H:%M:%S")
    end = datetime.datetime.strptime(end_time, "%Y-%m-%d %H:%M:%S")
    cur = start
    
    ret = []
    urls = {} 
    mm = {}   
    while cur <= end:
        key = cur.strftime("%Y-%m-%d")

        if key not in data.keys():
            cur += step
            continue
        
        for d in data[key]:
            if d['domain'] in mm.keys():
                mm[d['domain']] += d['count']
                if len(urls[d['domain']]) <= 30:
                    urls[d['domain']].extend(d['urls'])
            else:
                mm[d['domain']] = d['count']
                urls[d['domain']] = d['urls']
        cur += step

    for k in mm:
        ret.append({'count':mm[k], 'domain':k, 'urls':urls[k][:urls_limit]})
        
    ret.sort(key=lambda x:x['count'], reverse=True)
    return ret[:limit]
    
    
def get_bookmark_website_for_user(start_time=None, end_time=None, limit=100):
    data = get_bookmark_website_for_user_raw_data(start_time, end_time, limit);

    ret = {'list':data}
    return anyjson.dumps(ret)

def get_user_platform(start_time=None, end_time=None):
    '''start_time, end_time is string'''
    raw_data = Aggregation.objects.filter(type='user_platform', time__gte=start_time, time__lte=end_time).values('time', 'content')

    data = []
    for d in raw_data:
        data.append(anyjson.loads(d['content'])['platform'])
    
    return anyjson.dumps(data)

def get_conversion(start_time, end_time, data_grain='day'):
    '''start_time, end_time is string'''
    raw_data = Aggregation.objects.filter(type='conversion_%s' % data_grain, time__gte=start_time, time__lte=end_time).values('time', 'content')

    data = {}
    for d in raw_data:
        data[d['time'].strftime("%Y-%m-%d")] = anyjson.loads(d['content'])

    ret = []
    start = datetime.datetime.strptime(start_time, "%Y-%m-%d %H:%M:%S")
    end = datetime.datetime.strptime(end_time, "%Y-%m-%d %H:%M:%S")
    cur = start
    step = datetime.timedelta(days=1)
    while cur <= end:
        key = cur.strftime("%Y-%m-%d")
        if key in data.keys():
            ret.append({'time': cur.strftime("%m-%d"), 'share':data[key]['share']['conversion'], 'plug_in':data[key]['plug_in']['conversion'], 'mobile':data[key]['mobile']['conversion']})
        else:
            if cur.date() == end.date():
                break;
            else:
                cur += step
                continue;
        cur += step
    return anyjson.dumps(ret)
    
def get_activate_user(start_time, end_time, data_grain='day'):
    '''start_time, end_time is string'''
    raw_data = Aggregation.objects.filter(type='active_user', time__gte=start_time, time__lte=end_time).values('time', 'content')

    data = {}
    for d in raw_data:
        data[d['time'].strftime("%Y-%m-%d")] = anyjson.loads(d['content'])

    ret = []
    start = datetime.datetime.strptime(start_time, "%Y-%m-%d %H:%M:%S")
    end = datetime.datetime.strptime(end_time, "%Y-%m-%d %H:%M:%S")
    cur = start
    if data_grain == 'day':
        step = datetime.timedelta(days=1)
        while cur <= end:
            key = cur.strftime("%Y-%m-%d")
            if key in data.keys():
                ret.append({'time': cur.strftime("%m-%d"),
                            'au':data[key]['au'],
                            'reg':data[key]['reg']})
            else:
                break;
            cur += step
    elif data_grain == 'week':
        step = datetime.timedelta(days=1)
        tmp_au = 0
        user_ids = set()
        
        while cur <= end:
            key = cur.strftime("%Y-%m-%d")
            if key not in data.keys():
                if (cur - step).weekday() != 6:
                    ret.append({'time': (cur - step).strftime("%m-%d"),
                                'au':tmp_au,
                                'reg':data[(cur - step).strftime("%Y-%m-%d")]['reg']})
                break;
            
            user_ids = user_ids | c.redis_instance.smembers('activate:user:id:%s' % cur.strftime("%Y-%m-%d"))
            tmp_au = len(user_ids)
            
            if cur.weekday() == 6 or cur.date() == end.date():
                # 这一天是周日
                ret.append({'time': cur.strftime("%m-%d"),
                            'au':tmp_au,
                            'reg':data[key]['reg']})
                tmp_au = 0
                user_ids = set()
            cur += step
    elif data_grain == 'month':
        step = datetime.timedelta(days=1)
        tmp_au = 0
        user_ids = set()
        
        while cur <= end:
            key = cur.strftime("%Y-%m-%d")
            if key not in data.keys():
                ret.append({'time': (cur - step).strftime("%m-%d"),
                            'au':tmp_au,
                            'reg':data[(cur - step).strftime("%Y-%m-%d")]['reg']})
                break;
            
            user_ids = user_ids | c.redis_instance.smembers('activate:user:id:%s' % cur.strftime("%Y-%m-%d"))
            tmp_au = len(user_ids)
            
            if (cur + step).month != cur.month or cur.date() == end.date():
                # 这一天是月末
                ret.append({'time': cur.strftime("%Y-%m-%d"),
                            'au':tmp_au,
                            'reg':data[key]['reg']})
                tmp_au = 0
                user_ids = set()
            cur += step
    return anyjson.dumps(ret)
    
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
        raw = {}
        
        
        # 去掉测试用户的id, 因为要查询用户总数, 所以单独指定tmp
#        tmp = ' and id !='
#        tmp += ' and id !='.join(map(lambda x:str(x), test_id))

        having_fix, and_fix = _get_fix(start_time, end_time)
#        if not user_total:        
#            sql_total = "select count(*) from account_user where id > 100 %s %s" % (tmp, and_fix)
#            cursor.execute(sql_total)
#            result = cursor.fetchone()
#            user_total = result[0]
#        print 'user_total:', user_total

        remove_guide = " url not regexp '^http://kan.sohu.com/help/guide-' "
        and_fix = and_fix.replace('gmt_create', 'create_time')
        for i in range(64):
            sql = "select user_id, count(*) from bookmark_bookmark_%s where 1=1 \
                   and %s %s group by user_id" % (i, remove_guide, and_fix)
            cursor.execute(sql)
            results = cursor.fetchall()
            for d in results:
                user_id = int(d[0])
                count = int(d[1])
                if not _is_test(user_id):
                    '''根据用户的文章数情况, 把相应的范围数的用户数+1'''
                    ret[_which_index(count)]['count'] += 1
                    
                    if count in raw.keys():
                        raw[count] += 1
                    else:
                        raw[count] = 1
        # 原始的数值
        ret_raw = []
        for k in raw.keys():
            tmp = {}
            tmp['p_count'] = k
            tmp['u_count'] = raw[k]
            ret_raw.append(tmp)
        
        # 为了计算为文章数为0的用户数
#        user_used = 0
#        for r in ret:
#            user_used += r['count']

#        ret_raw.append({'p_count':0, 'u_count':user_total - user_used})        
#        ret.append({'name':'0篇', 'count':user_total - user_used})
        
        ret_raw.sort(key=lambda x:x['p_count'], reverse=True)
        ret.sort(key=lambda x:x['count'], reverse=True)
        return ret, ret_raw[:limit];
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

def get_user_platform_raw_data(start_time=None, end_time=None):
    '''为[收藏文章的平台统计]获取原始数据'''
    try:
        conn = MySQLdb.connect(**c.db_self_config)
        cursor = conn.cursor()
        
        # 去掉测试用户的id
        tmp = 'user_id !='
        tmp += ' and user_id !='.join(map(lambda x:str(x), c.test_id))

        ret = []
        data_grain_format = r'%Y-%m-%d'
        
        sql = '''select o.data_grain, u.platform, count(u.platform) from (
           select user_id, ua_id, date_format(gmt_create,'%s') as data_grain from stats_oper
           where gmt_create >= '%s' and gmt_create <='%s' and  %s ) o 
           left join stats_ua u on o.ua_id = u.id group by u.platform, o.data_grain order by o.data_grain''' \
           % (data_grain_format, start_time, end_time, tmp)

        cursor.execute(sql)
        results = cursor.fetchall()
        mm = {'time':''};
        for d in results:
            time = str(d[0])
            platform = str(d[1])
            count = int(d[2])
            if mm['time'] != time:
                if mm['time']:
                    ret.append(mm)
                mm = {'time':time};
            mm[platform] = count
        ret.append(mm)
        
        return ret
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
                
#def get_bookmark_website_raw_data(start_time=None, end_time=None, limit=100):
#    '''为[收藏文章的域名统计_PV]获取原始数据'''
#    try:
#        conn = MySQLdb.connect(**c.db_config)
#        cursor = conn.cursor()
#        
#        having_fix, and_fix = _get_fix(start_time, end_time)
#        mm = {}
#        urls = {}
#        ret = []
#        
#        # 由于bookmark表以前没有gmt_create, 所以凡是查询bookmark表都要替换成create_time
#        and_fix = and_fix.replace('gmt_create', 'create_time')
#        
#        for i in range(64):
#            cursor.execute("select user_id, url from bookmark_bookmark_%s where 1=1 %s " % (i, and_fix))
#            results = cursor.fetchall()
#            for d in results:
#                user_id = int(d[0])
#                url = str(d[1])
#                domain = urlparse.urlparse(url)[1]
#                if not _is_test(user_id):
#                    if domain in mm.keys():
#                        mm[domain] += 1
#                    else:
#                        mm[domain] = 1
#                        urls[domain] = [] 
#                    if(len(urls[domain]) <= 100):
#                        urls[domain].append(url)
#                    
#        for k in mm.keys():
#            ret.append({'domain':k, 'count':mm[k], 'urls':urls[k]})
#            
#        ret.sort(key=lambda x:x['count'], reverse=True)
#        
#        # 需要去除domain='kan.sohu.com'的数据
#        for r in ret:
#            if r['domain'] == 'kan.sohu.com':
#                ret.remove(r)
#        
##        pp = []
##        ssum = 0
##        for r in ret:
##            if r['domain'].find('.sohu.com') != -1:
##                pp.append({'domain':r['domain'], 'count':r['count']})
##                ssum += r['count']                        
##        print pp
##        print ssum
#        
#        return ret[:limit];
#    except Exception, e:
#        c.logger.error(e)
#        raise e
#    finally:
#        try:
#            if cursor:
#                cursor.close()
#        except Exception, e:
#            c.logger.error(e)
#        finally:
#            if conn:
#                conn.close()

def get_bookmark_website_for_user_raw_data(start_time=None, end_time=None, limit=100):
    '''为[收藏文章的域名统计_UV]获取原始数据'''
    try:
        conn = MySQLdb.connect(**c.db_config)
        cursor = conn.cursor()
        
        having_fix, and_fix = _get_fix(start_time, end_time)
        
        data_list = []
        mm = {}
        ret = []
        
        # 由于bookmark表以前没有gmt_create, 所以凡是查询bookmark表都要替换成create_time
        and_fix = and_fix.replace('gmt_create', 'create_time')
        # 这里不需要去掉guide, 因为后面会有专门的domain删除
        # remove_guide = " url not regexp '^http://kan.sohu.com/help/guide-' "
        # 先取得原始数据, 
        for i in range(64):
            sql = "select user_id, url from bookmark_bookmark_%s where 1=1 %s " % (i, and_fix)
            cursor.execute(sql)
            results = cursor.fetchall()
            for d in results:
                user_id = int(d[0])
                url = str(d[1])
                domain = urlparse.urlparse(url)[1]
                if not _is_test(user_id):
                    # 把收藏文章的每一条记录整理成domain,u_id的形式
                    data_list.append({'domain':domain, 'u_id':user_id})
        
        for a in data_list:
            if a['domain'] in mm.keys():
                mm[a['domain']].add(a['u_id'])
            else:
                mm[a['domain']] = set([a['u_id']])
        
        for k in mm.keys():
            ret.append({'domain':k, 'count':len(mm[k])})

        ret.sort(key=lambda x:x['count'], reverse=True)
        
        # 需要去除domain='kan.sohu.com'的数据
        for r in ret:
            if r['domain'] == 'kan.sohu.com':
                ret.remove(r)
        return ret[:limit]
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
                        
def get_bookmark_time_raw_data(start_time=None, end_time=None):
    '''为[收藏文章时间段]获取原始数据'''
    try:
        conn = MySQLdb.connect(**c.db_config)
        cursor = conn.cursor()
        
        having_fix, and_fix = _get_fix(start_time, end_time)
        and_fix = and_fix.replace('gmt_create', 'create_time')
        remove_guide = " url not regexp '^http://kan.sohu.com/help/guide-' "
        ret = []
        for i in range(64):
            sql = "select create_time, user_id from bookmark_bookmark_%s where 1=1 and %s %s" % (i, remove_guide, and_fix)
            cursor.execute(sql)
            results = cursor.fetchall()
            for d in results:
                if not _is_test(int(d[1])):
                    ret.append({'time':d[0]})
                            
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
    
def get_bookmark_per_user_raw_data(start_time=None, end_time=None, limit=100):
    '''为[用户收藏文章数排行]获取原始数据'''
    try:
        conn = MySQLdb.connect(**c.db_config)
        cursor = conn.cursor()
        
        having_fix, and_fix = _get_fix(start_time, end_time)    
        and_fix = and_fix.replace('gmt_create', 'create_time')
        remove_guide = " url not regexp '^http://kan.sohu.com/help/guide-' "    
        
        ret = []
        for i in range(64):
            sql = "select user_id, count(*) from bookmark_bookmark_%s where 1=1 and %s %s \
                   group by user_id " % (i, remove_guide, and_fix)
            cursor.execute(sql)
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
    
def get_folder_name_per_user_raw_data(start_time=None, end_time=None, limit=100):
    '''为[统计用户创建的分类名]获取原始数据'''
    try:
        conn = MySQLdb.connect(**c.db_config)
        cursor = conn.cursor()
        
        having_fix, and_fix = _get_fix(start_time, end_time)
#        remove_guide = " url not regexp '^http://kan.sohu.com/help/guide-' "    
        
        ret = []
        m = {}
        cursor.execute("set names utf8");
        num = 0
        for i in range(64):
            sql = "select user_id, name from folder_folder_%s where 1=1 %s " % (i, and_fix)
#            print sql
            cursor.execute(sql)
            results = cursor.fetchall()
            for d in results:
                user_id = int(d[0])
                name = str(d[1])
                num += 1
                if not _is_test(user_id):
                    if name not in m.keys():
                        m[name] = 1
                    else:
                        m[name] += 1
        
        items = m.items()
        items.sort(key=lambda x:x[1], reverse=True)
        ret = [{'name':key, 'count':value} for key, value in items]                            
        for r in ret:
            pass
#            print r['name'], r['count']
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

def get_userdata_for_day_report(today_start, today_end):
    # 针对some_total的机制对时间做点处理
    # 用户总数是在整点时间+5分钟统计的, 当天的最后一个数据需要在第二天的00:06:00取得
    # 因为是取最后一个总数数据, 所以只需要对today_end进行处理即可
    today_end = today_end + datetime.timedelta(minutes=8)
    
    # 昨天
    yd_start = today_start - datetime.timedelta(days=1)
    yd_end = today_end - datetime.timedelta(days=1)
    
    # 前天
    b_yd_start = today_start - datetime.timedelta(days=2)
    b_yd_end = today_end - datetime.timedelta(days=2)
    
#    print today_start
#    print today_end
#    print yd_start
#    print yd_end
#    print b_yd_start
#    print b_yd_end
    
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
    
    # 昨日用户总数_增长率
    user_total_inc_yd = (abs(user_new_yd) + 0.00000001) / user_total_b_yd
    user_total_inc_yd = round(user_total_inc_yd, 4)
        
    # 环比新增用户_(本期新增用户-上期新增用户)/上期新增用户
    user_new_inc = (user_new - user_new_yd + 0.00000001) / user_new_yd 
    user_new_inc = round(user_new_inc, 4)
    
    ret = {}
    ret['total'] = user_total;
    ret['total_yd'] = user_total_yd;
    ret['total_b_yd'] = user_total_b_yd;
    ret['total_inc'] = user_total_inc;
    ret['total_inc_yd'] = user_total_inc_yd;
    ret['new_inc'] = user_new_inc;
    
    return ret

def get_email_for_day_report(today_start, today_end):
    today_end = today_end + datetime.timedelta(minutes=8)
    
    # 昨天
    yd_start = today_start - datetime.timedelta(days=1)
    yd_end = today_end - datetime.timedelta(days=1)
    
    # 前天
    b_yd_start = today_start - datetime.timedelta(days=2)
    b_yd_end = today_end - datetime.timedelta(days=2)
    
    # 今日邮件总数
    email_total = int(SomeTotal.objects.filter(name='email', time__gte=today_start, time__lte=today_end).values('count').\
                            reverse()[0]['count'])
    # 昨日邮件总数
    email_total_yd = int(SomeTotal.objects.filter(name='email', time__gte=yd_start, time__lte=yd_end).\
                            values('count').reverse()[0]['count'])
    # 前日邮件总数
    email_total_b_yd = int(SomeTotal.objects.filter(name='email', time__gte=b_yd_start, time__lte=b_yd_end).\
                            values('count').reverse()[0]['count'])
    
    # 今日新增邮件数
    email_new = email_total - email_total_yd
    
    # 昨日新增邮件数
    email_new_yd = email_total_yd - email_total_b_yd
    
    # 今日邮件总数_增长率
    email_total_inc = (abs(email_new) + 0.00000001) / email_total_yd
    email_total_inc = round(email_total_inc, 4)
    
    # 昨日邮件总数_增长率
    email_total_inc_yd = (abs(email_new_yd) + 0.00000001) / email_total_b_yd
    email_total_inc_yd = round(email_total_inc_yd, 4)
        
    if email_new_yd > 0:
        email_new_inc = (email_new - email_new_yd + 0.00000001) / email_new_yd 
        email_new_inc = round(email_new_inc, 4)
    else:
        email_new_inc = 0.0

    ret = {}
    ret['total'] = email_total;
    ret['total_yd'] = email_total_yd;
    ret['total_b_yd'] = email_total_b_yd;
    ret['total_inc'] = email_total_inc;
    ret['total_inc_yd'] = email_total_inc_yd;
    ret['new_inc'] = email_new_inc 
    return ret

def get_shorturl_for_day_report(today_start, today_end):
    today_end = today_end + datetime.timedelta(minutes=8)
    
    # 昨天
    yd_start = today_start - datetime.timedelta(days=1)
    yd_end = today_end - datetime.timedelta(days=1)
    
    # 前天
    b_yd_start = today_start - datetime.timedelta(days=2)
    b_yd_end = today_end - datetime.timedelta(days=2)
    
    # 今日短链接总数
    shorturl_total = int(SomeTotal.objects.filter(name='shorturl', time__gte=today_start, time__lte=today_end).values('count').\
                            reverse()[0]['count'])
    # 昨日短链接总数
    shorturl_total_yd = int(SomeTotal.objects.filter(name='shorturl', time__gte=yd_start, time__lte=yd_end).\
                            values('count').reverse()[0]['count'])
    # 前日短链接总数
    shorturl_total_b_yd = int(SomeTotal.objects.filter(name='shorturl', time__gte=b_yd_start, time__lte=b_yd_end).\
                            values('count').reverse()[0]['count'])
    
    # 今日新增短链接数
    shorturl_new = shorturl_total - shorturl_total_yd
    
    # 昨日新增链接数
    shorturl_new_yd = shorturl_total_yd - shorturl_total_b_yd
    
    # 今日短链接总数_增长率
    shorturl_total_inc = (abs(shorturl_new) + 0.00000001) / shorturl_total_yd
    shorturl_total_inc = round(shorturl_total_inc, 4)
    
    # 昨日短链接总数_增长率
    shorturl_total_inc_yd = (abs(shorturl_new_yd) + 0.00000001) / shorturl_total_b_yd
    shorturl_total_inc_yd = round(shorturl_total_inc_yd, 4)
        
    if shorturl_new_yd > 0:
        shorturl_new_inc = (shorturl_new - shorturl_new_yd + 0.00000001) / shorturl_new_yd 
        shorturl_new_inc = round(shorturl_new_inc, 4)
    else:
        shorturl_new_inc = 0.0

    ret = {}
    ret['total'] = shorturl_total;
    ret['total_yd'] = shorturl_total_yd;
    ret['total_b_yd'] = shorturl_total_b_yd;
    ret['total_inc'] = shorturl_total_inc;
    ret['total_inc_yd'] = shorturl_total_inc_yd;
    ret['new_inc'] = shorturl_new_inc 
    return ret

def get_fiction_for_day_report(today_start, today_end):
    today_end = today_end + datetime.timedelta(minutes=8)
    
    # 昨天
    yd_start = today_start - datetime.timedelta(days=1)
    yd_end = today_end - datetime.timedelta(days=1)
    
    # 前天
    b_yd_start = today_start - datetime.timedelta(days=2)
    b_yd_end = today_end - datetime.timedelta(days=2)
    
    # 今日小说总数
    fiction_total = int(SomeTotal.objects.filter(name='fiction', time__gte=today_start, time__lte=today_end).values('count').\
                            reverse()[0]['count'])
    # 昨日小说总数
    fiction_total_yd = int(SomeTotal.objects.filter(name='fiction', time__gte=yd_start, time__lte=yd_end).\
                            values('count').reverse()[0]['count'])
    # 前日小说总数
    fiction_total_b_yd = int(SomeTotal.objects.filter(name='fiction', time__gte=b_yd_start, time__lte=b_yd_end).\
                            values('count').reverse()[0]['count'])
    
    # 今日新增小说数
    fiction_new = fiction_total - fiction_total_yd
    
    # 昨日新增小说数
    fiction_new_yd = fiction_total_yd - fiction_total_b_yd
    
    # 今日小说总数_增长率
    fiction_total_inc = (abs(fiction_new) + 0.00000001) / fiction_total_yd
    fiction_total_inc = round(fiction_total_inc, 4)
    
    # 昨日小说总数_增长率
    fiction_total_inc_yd = (abs(fiction_new_yd) + 0.00000001) / fiction_total_b_yd
    fiction_total_inc_yd = round(fiction_total_inc_yd, 4)
       
    if fiction_new_yd > 0:
        fiction_new_inc = (fiction_new - fiction_new_yd + 0.00000001) / fiction_new_yd 
        fiction_new_inc = round(fiction_new_inc, 4)
    else:
        fiction_new_inc = 0.0

    ret = {}
    ret['total'] = fiction_total;
    ret['total_yd'] = fiction_total_yd;
    ret['total_b_yd'] = fiction_total_b_yd;
    ret['total_inc'] = fiction_total_inc;
    ret['total_inc_yd'] = fiction_total_inc_yd;
    ret['new_inc'] = fiction_new_inc; 
    return ret

def get_bookmarkdata_for_day_report(today_start, today_end):
    # 针对some_total的机制对时间做点处理
    # 文章总数是在整点时间+10分钟统计的, 当天的最后一个数据需要在第二天的00:10:00取得
    # 因为是取最后一个总数数据, 所以只需要对today_end进行处理即可
    today_end = today_end + datetime.timedelta(minutes=15)
        
    # 昨天
    yd_start = today_start - datetime.timedelta(days=1)
    yd_end = today_end - datetime.timedelta(days=1)
    
    # 前天
    b_yd_start = today_start - datetime.timedelta(days=2)
    b_yd_end = today_end - datetime.timedelta(days=2)
    
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
    
    # 昨日文章总数_增长率
    bookmark_total_inc_yd = (abs(bookmark_new_yd) + 0.00000001) / bookmark_total_b_yd
    bookmark_total_inc_yd = round(bookmark_total_inc_yd, 4)
        
    # 环比新增文章=(本期新增文章-上期新增文章)/上期新增文章
    bookmark_new_inc = (bookmark_new - bookmark_new_yd + 0.00000001) / bookmark_new_yd 
    bookmark_new_inc = round(bookmark_new_inc, 4)
    
    # 今日收藏失败文章
    bookmark_failed = get_bookmark_failed(today_start, today_end)
    
    ret = {}
    ret['total'] = bookmark_total;
    ret['total_yd'] = bookmark_total_yd;
    ret['total_b_yd'] = bookmark_total_b_yd;
    ret['total_inc'] = bookmark_total_inc;
    ret['total_inc_yd'] = bookmark_total_inc_yd;
    ret['new_inc'] = bookmark_new_inc;
    ret['failed'] = bookmark_failed
    
    return ret

def get_bookmark_failed(start, end):
    try:
        purify_timeout = 'connect purify timeout'
        conn = MySQLdb.connect(**c.db_self_config)
        cursor = conn.cursor()
        
        bookmark_fail = [];
        sql = "select user_id, url, reason, id from stats_failcase where gmt_create >= '%s' and gmt_create <= '%s'" % (start, end)
        cursor.execute(sql)
        results = cursor.fetchall()
        for d in results:
            user_id = int(d[0])
            url = str(d[1])
            if not _is_test(user_id):
                if (not d[2]) or (purify_timeout == str(d[2])):
                    reason = purify_timeout
                else:
                    reason = "purify error | table stats_failure id: %s" % str(d[3])                    
                bookmark_fail.append({'user_id':user_id, 'url':url, 'reason': reason})
        return bookmark_fail;
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
                
def tmp_raw_data(include_test=False):
    try:
        conn = MySQLdb.connect(**c.db_config)
        cursor = conn.cursor()
        
        ret = []
        for i in range(64):
            cursor.execute("select user_id, url from bookmark_bookmark_%s where gmt_create > '2012-09-10 00:00:00' \
            and gmt_create < '2012-09-16 23:59:59'" % i)
            results = cursor.fetchall()
            for d in results:
#                if d[0]:
#                    kv = {}
#                    kv['user_id'] = int(d[0])
#                    kv['url'] = str(d[1])
#                    kv['bookmark'] = i
                if include_test or not _is_test(int(d[0])):
                    domain = urlparse.urlparse(str(d[1]))[1]
                    kv = {}
                    kv['domain'] = domain
                    kv['url'] = str(d[1])
                    ret.append(kv)
#        ret.sort(key=lambda x:x['user_id'], reverse=True)
        i = 0
        for r in ret:
            if r['domain'] == "www.google.com":
                i = i + 1
                pass
#                print i, r['url']
            
        return None;
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

def get_week_report_add_way_and_platform(start_time, end_time):
    '''为[周报_收藏方式&&平台]获取数据'''
    try:
        conn = MySQLdb.connect(**c.db_self_config)
        cursor = conn.cursor()
        
        having_fix, and_fix = _get_fix(start_time, end_time)
        and_fix = and_fix.replace("gmt_create", "o.gmt_create")    
        #remove_guide = " url not regexp '^http://kan.sohu.com/help/guide-' "    

        # 去掉测试用户的id
        tmp = ' and user_id !='
        tmp += ' and user_id !='.join(map(lambda x:str(x), c.test_id))
        tmp = tmp.replace("user_id", "o.user_id")

        # 收藏总数       
        sql_total = "select count(oo.object_key) from stats_oper o left join stats_operobject oo on oo.oper_id = o.id\
               where 1=1 %s %s and o.oper_type_id in (1,35)" % (and_fix, tmp)
        cursor.execute(sql_total)
        result = cursor.fetchone()
        total = int(result[0])
        print total
        
        # 段落收藏
        sql_partial_total = "select count(oo.object_key) from stats_oper o left join stats_operobject oo on oo.oper_id = o.id\
               where 1=1 %s %s and o.oper_type_id in (1,35) \
               and object_key regexp '.*\"content\":.*\"content_source\".*partial.*' " % (and_fix, tmp)
        cursor.execute(sql_partial_total)
        result = cursor.fetchone()
        partial = int(result[0])
        print partial 
        
        # 所有通过链接收藏的文章, 这一项包括chrome链接收藏+手机链接收藏
        sql_url_total = "select count(oo.object_key) from stats_oper o left join stats_operobject oo on oo.oper_id = o.id\
               where 1=1 %s %s and o.oper_type_id in (1,35) and object_key not regexp '.*\"content\".*'" % (and_fix, tmp)
#        print sql_url_total
        cursor.execute(sql_url_total)
        result = cursor.fetchone()
        url_total = int(result[0])
#        print url_total
        
        # 收藏平台
        platform_total = 0;
        platforms = {'Android':0, 'Darwin':0, 'Linux':0, 'Macintosh':0, 'unknown':0, 'Windows':0}
        for p in platforms.keys():
            sql = "select count(*) from stats_oper o left join stats_ua u on o.ua_id = u.id \
                          where 1=1 %s and oper_type_id in (1,35) and platform = '%s' %s" % (tmp, p, and_fix)
            cursor.execute(sql)
            result = cursor.fetchone()
            platforms[p] = int(result[0])
            platform_total += platforms[p]
#            print p
            
        # chrome通过链接收藏
        phone_url = platforms['Android'] + platforms['Darwin']
        chrome_url = url_total - phone_url

        # page整页收藏
        page = total - url_total - partial

        way = {}
        way_page = round((page + 0.001) / total, 6)
        way_chrome_url = round((chrome_url + 0.001) / total, 6)
        way_phone_url = round((phone_url + 0.001) / total, 6)
        way_partial = round((partial + 0.001) / total, 6)
        way['total'] = [total, 1, "收藏方式总数", to_percent(1) ]
        way['page'] = [page, way_page, "chrome+bookmarklet整页收藏", to_percent(way_page)]
        way['chrome_url'] = [chrome_url, way_chrome_url, "chrome链接收藏", to_percent(way_chrome_url)]
        way['phone_url'] = [phone_url, way_phone_url , "手机收藏", to_percent(way_phone_url)]
        way['partial'] = [partial, way_partial , "chrome段落收藏", to_percent(way_partial)]
        
        platform = {}
        platform_windows = round((platforms['Windows'] + 0.001) / platform_total, 6)
        platform_macintosh = round((platforms['Macintosh'] + 0.001) / platform_total, 6)
        platform_linux = round((platforms['Linux'] + 0.001) / platform_total, 6)
        platform_unknown = round((platforms['unknown'] + 0.001) / platform_total, 6)
        platform_android = round((platforms['Android'] + 0.001) / platform_total, 6)
        platform_darwin = round((platforms['Darwin'] + 0.001) / platform_total, 6)
        platform['total'] = [platform_total, 1, "收藏平台总数"]
        platform['Windows'] = [platforms['Windows'], platform_windows, "Windows", to_percent(platform_windows)]
        platform['Macintosh'] = [platforms['Macintosh'], platform_macintosh, "Macintosh", to_percent(platform_macintosh)]
        platform['Linux'] = [platforms['Linux'], platform_linux, "Linux", to_percent(platform_linux)]
        platform['unknown'] = [platforms['unknown'], platform_unknown, "unknown", to_percent(platform_unknown)]
        platform['Android'] = [platforms['Android'], platform_android, "Android", to_percent(platform_android)]
        platform['Darwin'] = [platforms['Darwin'], platform_darwin, "Darwin", to_percent(platform_darwin)]
        
        ret = {'way':way, 'platform':platform}
        return ret
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
        
def get_week_report_abstract(start_time, end_time):
    cur = start_time;
    step = datetime.timedelta(days=1)
    
if __name__ == '__main__':
#    start_time = datetime.datetime(2012, 11, 5, 0, 0, 20)
#    end_time = datetime.datetime(2012, 11, 11, 23, 59, 59)
##    b = get_bookmark_website('2012-06-15 00:00:00', '2012-11-11 23:59:59')
#    b = get_activate_user('2012-11-16 00:00:00', '2012-11-21 23:59:59', data_grain='week')
#    print b
    
    b = get_user_platform('2012-11-16 00:00:00', '2012-12-21 23:59:59')
    print b
    
#    cur1 = datetime.datetime(2012, 11, 20, 0, 0, 0)
#    cur2 = datetime.datetime(2012, 11, 21, 0, 0, 0)
#    user_ids_1 = c.redis_instance.smembers('activate:user:id:%s' % cur1.strftime("%Y-%m-%d"))
#    user_ids_2 = c.redis_instance.smembers('activate:user:id:%s' % cur2.strftime("%Y-%m-%d"))
#    
#    print len(user_ids_1), user_ids_1
#    print len(user_ids_2), user_ids_2
    
#    b = get_bookmarkdata_for_day_report(start_time, end_time)
#    print b
#    b = get_bookmark_website_for_user_raw_data(start_time,end_time)
#    print b
#    get_bookmark_website_raw_data('2012-08-20 00:00:00', '2012-08-26 23:59:59')
    
#    b = get_bookmark_website_for_user_raw_data()
    
#    b = get_bookmark_website_for_user_raw_data()
#    print b
    pass
