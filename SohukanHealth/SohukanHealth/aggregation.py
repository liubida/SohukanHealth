# -*- coding: utf-8 -*-
'''
Created on Nov 13, 2012

@author: liubida
'''
from config.config import c
from monitor.models import SomeTotal
from statistics.biz import _is_test
from statistics.models import Aggregation
import MySQLdb
import anyjson
import datetime

jiathis = 'jiathis'
bshare = 'bshare'
webapp = 'webapp'
other = 'sohu_cms'
    
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
             'bshare':{'count':0, 'object_key':[]},
             'jiathis':{'count':0, 'object_key':[]},
             'webapp':{'count':0, 'object_key':[]},
             'sohu_cms':{'count':0, 'object_key':[]}}
        
        for d in results:
            user_id = int(d[0])
            object_key = anyjson.loads(d[1])
            object_key['user_id'] = user_id
            
#            # 去掉测试用户
            if not _is_test(user_id):
                if jiathis == object_key['from']:
                    m['jiathis']['object_key'].append(object_key)
                elif bshare == object_key['from']:
                    m['bshare']['object_key'].append(object_key)
                elif webapp == object_key['from']:
                    m['webapp']['object_key'].append(object_key)
                else:
                    m['sohu_cms']['object_key'].append(object_key)
        
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

        sql = "select distinct(user_id) from stats_oper where gmt_create >= '%s' and gmt_create <'%s' \
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

if __name__ == '__main__':
#    share_channels(datetime.datetime.now())
    activate_user(datetime.datetime.now())
    
#    r = redis.Redis(host='10.10.69.53', port=6379, db=4)
#    a = [1, 2, 3, ]
#    b = [3, 4, 5]
#    r.sadd('key1', *a)
#    r.sadd('key2', *b)
#    r1 = r.smembers('key1')
#    r2 = r.smembers('key2')
#    print r1, r2
#    print r1 | r2
