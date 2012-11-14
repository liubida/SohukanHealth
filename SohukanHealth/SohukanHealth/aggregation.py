# -*- coding: utf-8 -*-
'''
Created on Nov 13, 2012

@author: liubida
'''
from config.config import c
from monitor.models import AppAvailableData
from monitor.system.worker import add_worker
from statistics.biz import _is_test
from statistics.models import Aggregation
from util import print_info, get_week_sun
from util.random_spider import RandomSpider
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

        ret = []
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

@print_info(name='add_job')
def add_job():
    url = RandomSpider().get_valid_url()
    value = add_worker(url, c.cookie).test()
    data = AppAvailableData(name='add', category='', result=value.get('result', False), \
                            time=datetime.datetime.now(), time_used=value.get('time_used', c.add_time_limit), \
                            comments=value.get('comments', url))
    data.save()
    return value

if __name__ == '__main__':
    share_channels(datetime.datetime.now())
