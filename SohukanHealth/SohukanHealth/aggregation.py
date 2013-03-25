# -*- coding: utf-8 -*-
'''
Created on Nov 13, 2012

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

from config.config import c
from monitor.models import SomeTotal
from statistics.biz import _is_test, _get_fix
from statistics.models import Aggregation
import MySQLdb
import anyjson
import datetime
import urlparse

jiathis = 'jiathis'
bshare = 'bshare'
webapp = 'webapp'
sohu_blog = 'sohu_blog'
sohu_news = 'sohu_news'
baidu = 'baidu'
other = 'share'

iPhone = 'iPhone'
iPad = 'iPad'
android = 'android'
unknown = 'unknown'

def share_channels(start_time):
    '''为[收藏渠道统计]聚合数据
    '''
    
    start_time = start_time.replace(hour=0, minute=0, second=0)
    step = datetime.timedelta(days=1)
    end_time = start_time + step
    
    try:
        conn = MySQLdb.connect(**c.db_self_config)
        cursor = conn.cursor()

        # 去掉测试用户的id
        exclude_test_user_id = ' and o.user_id !='
        exclude_test_user_id += ' and o.user_id !='.join(map(lambda x:str(x), c.test_id))

        sql = """select o.user_id, oo.object_key from stats_oper o  
        left join stats_operobject oo on oo.oper_id = o.id 
        where o.oper_type_id in (1,35) %s and oo.gmt_create >= '%s' and oo.gmt_create < '%s'  
        and oo.object_key like '%%\"from\":%%' """ % (exclude_test_user_id, start_time, end_time)
        cursor.execute(sql)
        results = cursor.fetchall()

        user_id = None
        object_key = None
        
        m = {'time':datetime.datetime.strftime(start_time, "%Y-%m-%d"),
             jiathis:{'count':0, 'object_key':[]},
             bshare:{'count':0, 'object_key':[]},
             webapp:{'count':0, 'object_key':[]},
             sohu_blog:{'count':0, 'object_key':[]},
             sohu_news:{'count':0, 'object_key':[]},
             baidu:{'count':0, 'object_key':[]},
             other:{'count':0, 'object_key':[]}}

        for d in results:
            user_id = int(d[0])
            object_key = anyjson.loads(d[1])
            object_key['user_id'] = user_id
            
            # 去掉测试用户
            if not _is_test(user_id):
                if jiathis == object_key['from']:
                    m[jiathis]['object_key'].append(object_key)
                elif bshare == object_key['from']:
                    m[bshare]['object_key'].append(object_key)
                elif webapp == object_key['from']:
                    m[webapp]['object_key'].append(object_key)
                elif sohu_blog == object_key['from']:
                    m[sohu_blog]['object_key'].append(object_key)
                elif sohu_news == object_key['from']:
                    m[sohu_news]['object_key'].append(object_key)
                elif baidu == object_key['from']:
                    m[baidu]['object_key'].append(object_key)
                else:
                    m[other]['object_key'].append(object_key)
        
        for k in m:
            if k != 'time':
                m[k]['count'] = len(m[k]['object_key'])
                
        data = Aggregation(type='share_channels', time=start_time.date(), content=anyjson.dumps(m))
        data.save()
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


def public_client(start_time):
    '''为[收藏渠道统计]聚合数据
    '''
    
    start_time = start_time.replace(hour=0, minute=0, second=0)
    step = datetime.timedelta(days=1)
    end_time = start_time + step
    
    try:
        conn = MySQLdb.connect(**c.db_self_config)
        cursor = conn.cursor()
        
        sql = '''select o.object_key from stats_oper s, stats_operobject o, stats_opertype t 
                    where s.oper_type_id=t.id and s.id=o.oper_id and (t.id=64 or t.id=65 or t.id=67) 
                    and o.gmt_create >= '%s' and o.gmt_create < '%s';''' % (start_time, end_time)
        cursor.execute(sql)
        results = cursor.fetchall()

        m = {'time':datetime.datetime.strftime(start_time, "%Y-%m-%d"),
             iPhone:{'count': 0},
             iPad:{'count': 0},
             android:{'count': 0},
             unknown:{'count': 0}}

        for d in results:
            object_key = anyjson.loads(d[0])
            if object_key.has_key('client_type'):
                m[object_key['client_type']]['count'] += 1
            else:
                m[unknown]['count'] += 1
             
        data = Aggregation(type='public_client', time=start_time.date(), content=anyjson.dumps(m))
        data.save()
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


def conversion(end_time=None):
    '''为[收藏渠道统计]聚合数据
    ''' 
    end_time = datetime.datetime.now()
    end_time = end_time.replace(hour=0, minute=0, second=0)
    end_time = end_time - datetime.timedelta(days=0)
    start_time = end_time - datetime.timedelta(days=1)
    conversion_core(start_time, end_time, 'conversion_day')
    if end_time.isoweekday() == 1:
        start_time = end_time - datetime.timedelta(days=7)
        conversion_core(start_time, end_time, 'conversion_week')


def conversion_core(start_time, end_time, type_name):
    try:
        conn = MySQLdb.connect(**c.db_self_config)
        cursor = conn.cursor()
        sql = """select o.user_id, oo.gmt_create from stats_oper o left join stats_operobject oo on oo.oper_id = o.id 
                where o.oper_type_id = 1 and oo.gmt_create >= '%s' and oo.gmt_create < '%s' 
                and oo.object_key like '%%\"from\":%%'""" % (start_time, end_time)
        cursor.execute(sql)
        results = cursor.fetchall()
        m = {}
        for d in results:
            if m.has_key(d[0]):
                if m[d[0]] > d[1]:
                    m[d[0]] = d[1]
            else:
                m[d[0]] = d[1]
        share_add = len(m)
        share_custom = {'phone': 0, 'pad': 0, 'pc': 0, 'unknown': 0}
        for k in m.keys():
            sql = """select oo.object_key from stats_operobject oo, stats_oper o where o.id=oo.oper_id 
                and o.oper_type_id=7 and oo.user_id = %s and (object_key like '%%\"iPhone\"%%' or object_key like '%%\"android\"%%') 
                and gmt_create > '%s' and gmt_create < '%s' limit 1""" % (k, m[k], end_time)
            cursor.execute(sql)
            result = cursor.fetchall()
            if len(result) > 0:
                share_custom['phone'] += 1
        for k in m.keys():
            sql = """select oo.object_key from stats_operobject oo, stats_oper o where o.id=oo.oper_id 
                and o.oper_type_id=7 and oo.user_id = %s and object_key like '%%\"iPad\"%%'
                and gmt_create > '%s' and gmt_create < '%s' limit 1""" % (k, m[k], end_time)
            cursor.execute(sql)
            result = cursor.fetchall()
            if len(result) > 0:
                share_custom['pad'] += 1
        for k in m.keys():
            sql = """select oo.object_key from stats_operobject oo, stats_oper o where o.id=oo.oper_id 
                and o.oper_type_id=7 and oo.user_id = %s and object_key like '%%\"reader\"%%' 
                and gmt_create > '%s' and gmt_create < '%s' limit 1""" % (k, m[k], end_time)
            cursor.execute(sql)
            result = cursor.fetchall()
            if len(result) > 0:
                share_custom['pc'] += 1
        for k in m.keys():
            sql = """select oo.object_key from stats_operobject oo, stats_oper o where o.id=oo.oper_id 
                and o.oper_type_id=7 and oo.user_id = %s and object_key not like '%%\"client_type\"%%' 
                and gmt_create > '%s' and gmt_create < '%s' limit 1""" % (k, m[k], end_time)
            cursor.execute(sql)
            result = cursor.fetchall()
            if len(result) > 0:
                share_custom['unknown'] += 1

        sql = """select o.user_id, oo.gmt_create from stats_oper o left join stats_operobject oo on oo.oper_id = o.id 
                where o.oper_type_id = 1 and oo.gmt_create >= '%s' and oo.gmt_create < '%s' 
                and oo.object_key like '%%\"from2\":%%'""" % (start_time, end_time)
        cursor.execute(sql)
        results = cursor.fetchall()
        m = {}
        for d in results:
            if m.has_key(d[0]):
                if m[d[0]] > d[1]:
                    m[d[0]] = d[1]
            else:
                m[d[0]] = d[1]
        plug_in_add = len(m)
        plug_in_custom = {'phone': 0, 'pad': 0, 'pc': 0}
        for k in m.keys():
            sql = """select oo.object_key from stats_operobject oo, stats_oper o where o.id=oo.oper_id 
                and o.oper_type_id=7 and oo.user_id = %s and (object_key like '%%\"iPhone\"%%' or object_key like '%%\"android\"%%') 
                and gmt_create > '%s' and gmt_create < '%s' limit 1""" % (k, m[k], end_time)
            cursor.execute(sql)
            result = cursor.fetchall()
            if len(result) > 0:
                plug_in_custom['phone'] += 1
        for k in m.keys():
            sql = """select oo.object_key from stats_operobject oo, stats_oper o where o.id=oo.oper_id 
                and o.oper_type_id=7 and oo.user_id = %s and object_key like '%%\"iPad\"%%'
                and gmt_create > '%s' and gmt_create < '%s' limit 1""" % (k, m[k], end_time)
            cursor.execute(sql)
            result = cursor.fetchall()
            if len(result) > 0:
                plug_in_custom['pad'] += 1
        for k in m.keys():
            sql = """select oo.object_key from stats_operobject oo, stats_oper o where o.id=oo.oper_id 
                and o.oper_type_id=7 and oo.user_id = %s and object_key like '%%\"reader\"%%' 
                and gmt_create > '%s' and gmt_create < '%s' limit 1""" % (k, m[k], end_time)
            cursor.execute(sql)
            result = cursor.fetchall()
            if len(result) > 0:
                plug_in_custom['pc'] += 1
        for k in m.keys():
            sql = """select oo.object_key from stats_operobject oo, stats_oper o where o.id=oo.oper_id 
                and o.oper_type_id=7 and oo.user_id = %s and object_key not like '%%\"client_type\"%%' 
                and gmt_create > '%s' and gmt_create < '%s' limit 1""" % (k, m[k], end_time)
            cursor.execute(sql)
            result = cursor.fetchall()
            if len(result) > 0:
                plug_in_custom['unknown'] += 1

        sql = """select o.user_id, oo.gmt_create from stats_oper o left join stats_operobject oo on oo.oper_id = o.id 
                where o.oper_type_id = 1 and oo.gmt_create >= '%s' and oo.gmt_create < '%s' 
                and oo.object_key like '%%\"from3\":%%'""" % (start_time, end_time)
        cursor.execute(sql)
        results = cursor.fetchall()
        m = {}
        for d in results:
            if m.has_key(d[0]):
                if m[d[0]] > d[1]:
                    m[d[0]] = d[1]
            else:
                m[d[0]] = d[1]
        mobile_add = len(m)
        mobile_custom = {'phone': 0, 'pad': 0, 'pc': 0}
        for k in m.keys():
            sql = """select oo.object_key from stats_operobject oo, stats_oper o where o.id=oo.oper_id 
                and o.oper_type_id=7 and oo.user_id = %s and (object_key like '%%\"iPhone\"%%' or object_key like '%%\"android\"%%') 
                and gmt_create > '%s' and gmt_create < '%s' limit 1""" % (k, m[k], end_time)
            cursor.execute(sql)
            result = cursor.fetchall()
            if len(result) > 0:
                mobile_custom['phone'] += 1
        for k in m.keys():
            sql = """select oo.object_key from stats_operobject oo, stats_oper o where o.id=oo.oper_id 
                and o.oper_type_id=7 and oo.user_id = %s and object_key like '%%\"iPad\"%%'
                and gmt_create > '%s' and gmt_create < '%s' limit 1""" % (k, m[k], end_time)
            cursor.execute(sql)
            result = cursor.fetchall()
            if len(result) > 0:
                mobile_custom['pad'] += 1
        for k in m.keys():
            sql = """select oo.object_key from stats_operobject oo, stats_oper o where o.id=oo.oper_id 
                and o.oper_type_id=7 and oo.user_id = %s and object_key like '%%\"reader\"%%' 
                and gmt_create > '%s' and gmt_create < '%s' limit 1""" % (k, m[k], end_time)
            cursor.execute(sql)
            result = cursor.fetchall()
            if len(result) > 0:
                mobile_custom['pc'] += 1
        for k in m.keys():
            sql = """select oo.object_key from stats_operobject oo, stats_oper o where o.id=oo.oper_id 
                and o.oper_type_id=7 and oo.user_id = %s and object_key not like '%%\"client_type\"%%' 
                and gmt_create > '%s' and gmt_create < '%s' limit 1""" % (k, m[k], end_time)
            cursor.execute(sql)
            result = cursor.fetchall()
            if len(result) > 0:
                mobile_custom['unknown'] += 1

        share = {'phone': 0, 'pad': 0, 'pc': 0, 'unknown': 0}
        plug_in = {'phone': 0, 'pad': 0, 'pc': 0, 'unknown': 0}
        mobile = {'phone': 0, 'pad': 0, 'pc': 0, 'unknown': 0}
        if share_add > 0:
            share['phone'] = round(float(share_custom['phone']) / share_add, 4)
            share['pad'] = round(float(share_custom['pad']) / share_add, 4)
            share['pc'] = round(float(share_custom['pc']) / share_add, 4)
            share['unknown'] = round(float(share_custom['unknown']) / share_add, 4)
        if plug_in_add > 0:
            plug_in['phone'] = round(float(plug_in_custom['phone']) / plug_in_add, 4)
            plug_in['pad'] = round(float(plug_in_custom['pad']) / plug_in_add, 4)
            plug_in['pc'] = round(float(plug_in_custom['pc']) / plug_in_add, 4)
            plug_in['unknown'] = round(float(plug_in_custom['unknown']) / plug_in_add, 4)
        if mobile_add > 0: 
            mobile['phone'] = round(float(mobile_custom['phone']) / mobile_add, 4)
            mobile['pad'] = round(float(mobile_custom['pad']) / mobile_add, 4)
            mobile['pc'] = round(float(mobile_custom['pc']) / mobile_add, 4)
            mobile['unknown'] = round(float(mobile_custom['unknown']) / mobile_add, 4)
        m = {"time":datetime.datetime.strftime(end_time, "%Y-%m-%d"),
             "share":{"conversion": share, "add": share_add, "customer": share_custom},
             "plug_in":{"conversion": plug_in, "add": plug_in_add, "customer": plug_in_custom},
             "mobile":{"conversion": mobile, "add": mobile_add, "customer": mobile_custom}}
        data = Aggregation(type=type_name, time=end_time.date(), content=anyjson.dumps(m))
        data.save()
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


def activate_user(start_time):

    start_time = start_time.replace(hour=0, minute=0, second=0)
    step = datetime.timedelta(days=1)
    end_time = start_time + step
    
    try:
        conn = MySQLdb.connect(**c.db_self_config)
        cursor = conn.cursor()

        # 去掉测试用户的id
        exclude_test_user_id = ' and user_id !='
        exclude_test_user_id += ' and user_id !='.join(map(lambda x:str(x), c.test_id))

        sql = "select distinct(user_id) from stats_oper where gmt_create >= '%s' and gmt_create < '%s' \
               and oper_type_id != 28 and user_id is not null %s" \
               % (start_time, end_time, exclude_test_user_id)
        cursor.execute(sql)
        results = cursor.fetchall()
        
        user_ids = []
        for d in results:
            user_ids.append(int(d[0]))
        
        c.redis_instance.sadd('activate:user:id:%s' % datetime.datetime.strftime(start_time, "%Y-%m-%d"), *user_ids)

        au = len(user_ids)
        
        # 获取注册用户数
        reg = SomeTotal.objects.filter(name='user', time__gte=start_time, time__lte=end_time).\
                   order_by('-gmt_create')[0].count
        percent = round((au + 0.00001) / reg, 4)
        
        m = {'time':datetime.datetime.strftime(start_time, "%Y-%m-%d"), 'percent': percent, 'au':au, 'reg':reg}
        
        data = Aggregation(type='active_user', time=start_time.date(), content=anyjson.dumps(m))
        data.save()
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

def bookmark_website(start_time):
    '''为[收藏文章的域名统计_PV]聚合数据'''
    
    start_time = start_time.replace(hour=0, minute=0, second=0)
    step = datetime.timedelta(days=1)
    end_time = start_time + step
    
    try:
        conn = MySQLdb.connect(**c.db_config)
        cursor = conn.cursor()
        
        having_fix, and_fix = _get_fix(start_time, end_time)
        mm = {}   # mm = {'www.douban.com':100, 'www.dapenti.com':80}
        urls = {} #	urls = {'www.douban.com':['http://www.douban.com/1','http://www.douban.com/2'], 'www.dapenti.com':[...]}

        ret = []
        
        # 由于bookmark表以前没有gmt_create, 所以凡是查询bookmark表都要替换成create_time
        and_fix = and_fix.replace('gmt_create', 'create_time')
        
        for i in range(64):
            cursor.execute("select user_id, url from bookmark_bookmark_%s where 1=1 %s " % (i, and_fix))
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
                        urls[domain] = [] 
                    if len(urls[domain]) <= 50:
                        urls[domain].append(url)
        
        for k in mm:
            # 需要去除domain='kan.sohu.com'的数据
            if k == 'kan.sohu.com':
                continue
            ret.append({'domain':k, 'count':mm[k], 'urls':urls[k]})
                
            
        ret.sort(key=lambda x:x['count'], reverse=True)
        # 只存储每日排名前100的domain
        #print ret[:100]
        data = Aggregation(type='bookmark_website', time=start_time.date(), content=anyjson.dumps(ret[:100]))
        data.save()
        
#        pp = []
#        ssum = 0
#        for r in ret:
#            if r['domain'].find('.sohu.com') != -1:
#                pp.append({'domain':r['domain'], 'count':r['count']})
#                ssum += r['count']                        
#        print pp
#        print ssum
        return ret
    except Exception, e:
        c.logger.error(e)
        print e
        return None
    finally:
        try:
            if cursor:
                cursor.close()
        except Exception, e:
            c.logger.error(e)
        finally:
            if conn:
                conn.close()
                
def user_platform(start_time):
    '''为[用户使用平台]聚合数据: 每天用户的使用平台数据分布
       start_time is datetime
    '''
    start_time = start_time.replace(hour=0, minute=0, second=0)
    step = datetime.timedelta(days=1)
    end_time = start_time + step
    start_time_str = datetime.datetime.strftime(start_time, "%Y-%m-%d")
    
    try:
        conn = MySQLdb.connect(**c.db_self_config)
        cursor = conn.cursor()

        # 去掉测试用户的id
        exclude_test_user_id = ' and user_id !='
        exclude_test_user_id += ' and user_id !='.join(map(lambda x:str(x), c.test_id))
               
        sql_platform = "select count(distinct a.user_id), b.platform from stats_oper a \
                        left join stats_ua b on a.ua_id =b.id where a.user_id is not null %s \
                        and a.gmt_create >= '%s' and a.gmt_create < '%s' group by b.platform" \
                        % (exclude_test_user_id, start_time, end_time)
        cursor.execute(sql_platform)
        results = cursor.fetchall()
        platform = {'time':start_time_str}
        for d in results:
            platform[str(d[1])] = int(d[0])
        
        sql_browser = "select count(distinct a.user_id), b.browser from stats_oper a \
                        left join stats_ua b on a.ua_id =b.id where a.user_id is not null %s \
                        and a.gmt_create >= '%s' and a.gmt_create < '%s' group by b.browser" \
                        % (exclude_test_user_id, start_time, end_time)
        cursor.execute(sql_browser)
        results = cursor.fetchall()
        browser = {'time':start_time_str}
        for d in results:
            browser[str(d[1])] = int(d[0])
                        
        m = {'time':start_time_str, 'platform': platform, 'browser':browser}
        data = Aggregation(type='user_platform', time=start_time.date(), content=anyjson.dumps(m))
        data.save()
        return m
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
                
if __name__ == '__main__':
    
    
#    result = user_platform(start)
#    print result

#    start = datetime.datetime(2012, 7, 21, 23, 52, 0)
    start = datetime.datetime(2012, 11, 16, 23, 52, 0)
    step = datetime.timedelta(days=1)
    
    now = datetime.datetime.now()
    while start < now:
        result = share_channels(start)
        if result:
            print "success -- ", start.strftime("%Y-%m-%d")
        start += step
    print 'over'
#    r = redis.Redis(host='10.10.69.53', port=6379, db=4)
#    a = [1, 2, 3, ]
#    b = [3, 4, 5]
#    r.sadd('key1', *a)
#    r.sadd('key2', *b)
#    r1 = r.smembers('key1')
#    r2 = r.smembers('key2')
#    print r1, r2
#    print r1 | r2
