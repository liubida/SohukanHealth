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
other = 'share'
    
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
    
    
#    start = datetime.datetime(2012, 11, 16, 23, 52, 0)
#    result = user_platform(start)
#    print result

    start = datetime.datetime(2012, 7, 21, 23, 52, 0)
    step = datetime.timedelta(days=1)
    
    now = datetime.datetime.now()
    while start < now:
        result = user_platform(start)
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
