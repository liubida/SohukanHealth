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

test_id = [2, 3, 3, 4, 5, 7, 8, 10, 11, 12, 13, 14, 15, 22, \
          23, 24, 25, 29, 32, 33, 35, 43, 46, 53, 58, 91, \
          108, 125, 165, 591, 1288, 1486, 2412, 3373]

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
    
    if user_id in test_id:
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
    max = len(color) - 1
    for d in raw_data:
        d['color'] = color[i if i <= max else max]
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
    max = len(color) - 1
    sum_count = 0
    for d in data:
        d['color'] = color[i if i <= max else max]
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

def get_bookmark_website(start_time=None, end_time=None, limit=100):
    data = get_bookmark_website_raw_data(start_time, end_time, limit);
    
    ret = {'list':data}
    return anyjson.dumps(ret)

def get_bookmark_website_for_user(start_time=None, end_time=None, limit=100):
    data = get_bookmark_website_for_user_raw_data(start_time, end_time, limit);

    ret = {'list':data}
    return anyjson.dumps(ret)

def get_user_platform(start_time=None, end_time=None):
    data = get_user_platform_raw_data(start_time, end_time)
    
    ret = {'list':data}
    return anyjson.dumps(ret)

def get_activate_user(start_time=None, end_time=None, data_grain='day'):

    # 获取注册用户数, 图中对比用
    raw_data = SomeTotal.objects.filter(name='user', time__gte=start_time, time__lte=end_time).values('time', 'count')
    # 每天取一个23点的数据
    reg_user = get_data_interval(raw_data, datetime.timedelta(days=1), time_format='datetime')
    
#    new_user = []
#    raw_data = DayReport.objects.filter(time__gte=start_time, time__lte=end_time).values('time', 'jsondata')
#    for d in raw_data:
#        jsondata = anyjson.loads(d['jsondata'])
#        new_user.append({'time':d['time'], 'new':jsondata['user']['total'] - jsondata['user']['total_yd']})
#    print 'new_user', new_user
    au_user = get_activate_user_raw_data(start_time, end_time, data_grain)

    data = []
    if data_grain == 'day':
        for a in au_user:
            for r in reg_user:
                if r['time'].year == a['time'].year and r['time'].month == a['time'].month and r['time'].day == a['time'].day:
                    percent = round((a['count'] + 0.00001) / r['count'], 4)
                    data.append({'time':a['time'].strftime("%m-%d"), 'reg':r['count'], 'au':a['count'], 'percent':percent})
            
    if data_grain == 'month':
        # 注意, 这里是 len(reg_user)-1    
        for i in range(0, len(reg_user) - 1):
            r = reg_user[i]
            r_n = reg_user[i + 1] 
            # 要保证是本月的最后一天的注册用户总数
            if r['time'].month == r_n['time'].month:
                continue
            else :
                for a in au_user:
                    if r['time'].year == a['time'].year and r['time'].month == a['time'].month:
                        percent = round((a['count'] + 0.00001) / r['count'], 4)
                        data.append({'time':a['time'].strftime("%Y-%m-%d"), 'reg':r['count'], 'au':a['count'], 'percent':percent})
        
    if data_grain == 'week':
        for a in au_user:
            au_week_num = int(a['time'].split('-')[1])
            for i in range(0, len(reg_user) - 1):
                r = reg_user[i]
                r_n = reg_user[i + 1] 
                # 要保证是本周的最后一天的注册用户总数
                if _get_week_num(r['time']) == _get_week_num(r_n['time']):
                    continue
                elif _get_week_num(r['time']) == au_week_num:
                    percent = round((a['count'] + 0.00001) / r['count'], 4)
                    data.append({'time':r['time'].strftime("%Y-%m-%d"), 'reg':r['count'], 'au':a['count'], 'percent':percent})
                
    data.sort(key=lambda x:x['time'], reverse=False)
    ret = {'list':data}
    return anyjson.dumps(ret)
    
def get_activate_user_raw_data(start_time=None, end_time=None, data_grain='day'):
    '''为[活跃用户统计]获取原始数据'''
    try:
        conn = MySQLdb.connect(**c.db_self_config)
        cursor = conn.cursor()

        ret = []
        # 去掉测试用户的id
        tmp = ' and user_id !='
        tmp += ' and user_id !='.join(map(lambda x:str(x), test_id))

        if data_grain == 'week':
            data_grain_format = r'%Y-%u'
        elif data_grain == 'month':
            data_grain_format = r'%Y-%m'
        else:
            data_grain_format = r'%Y-%m-%d'

        sql = "select count(u_id), tmp.data_grain from \
               (select distinct(user_id) as u_id, date_format(gmt_create,'%s') as data_grain from stats_oper \
               where gmt_create >= '%s' and gmt_create <='%s' %s) tmp group by tmp.data_grain" \
                % (data_grain_format, start_time, end_time, tmp)
        cursor.execute(sql)
        results = cursor.fetchall()
        
        if data_grain == 'day' or data_grain == 'month':
            for d in results:
                au = int(d[0])
                time = datetime.datetime.strptime(str(d[1]), data_grain_format)
                ret.append({'time':time, 'count':au})

        if data_grain == 'week':
            for d in results:
                au = int(d[0])
                time = str(d[1])
                ret.append({'time':time, 'count':au})
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
    '''为[收藏文章的域名统计]获取原始数据'''
    try:
        conn = MySQLdb.connect(**c.db_self_config)
        cursor = conn.cursor()
        
        # 去掉测试用户的id
        tmp = 'user_id !='
        tmp += ' and user_id !='.join(map(lambda x:str(x), test_id))

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
                
def get_bookmark_website_raw_data(start_time=None, end_time=None, limit=100):
    '''为[收藏文章的域名统计_PV]获取原始数据'''
    try:
        conn = MySQLdb.connect(**c.db_config)
        cursor = conn.cursor()
        
        having_fix, and_fix = _get_fix(start_time, end_time)
        mm = {}
        ret = []
        
        # 由于bookmark表以前没有gmt_create, 所以凡是查询bookmark表都要替换成create_time
        and_fix = and_fix.replace('gmt_create', 'create_time')
        # 这里不需要去掉guide, 因为后面会有专门的domain删除
        # remove_guide = " url not regexp '^http://kan.sohu.com/help/guide-' "
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
        for k in mm.keys():
            ret.append({'domain':k, 'count':mm[k]})
            
        ret.sort(key=lambda x:x['count'], reverse=True)
        
        # 需要去除domain='kan.sohu.com'的数据
        for r in ret:
            if r['domain'] == 'kan.sohu.com':
                ret.remove(r)
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
            sql = "select user_id, url from bookmark_bookmark_%s where 1=1 %s" % (i, and_fix)
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

def _get_week_num(date):
    '''获得给定日期是这一年的第几周。
    每周以周一为一周的开始，但1月1日不是周一时,算作上一年的最后一周,返回0'''
    year = date.year
    wd = date.replace(month=1, day=1).weekday()
    days = (date - datetime.datetime(year, 1, 1)).days
    nweek = 0
    if wd:
        nweek = (days + wd) / 7
    else:
        nweek = days / 7 + 1
    return nweek

def get_week_report_abstract(start_time, end_time):
    cur = start_time;
    step = datetime.timedelta(days=1)
    
if __name__ == '__main__':
#    b = get_bookmark_website_for_user_raw_data()
#    b = get_bookmark_website_for_user_raw_data('2012-01-01 00:00:00', '2222-06-10 00:00:00')
    
#    b = get_bookmark_website_for_user_raw_data()
#    print b
    pass
