# -*- coding: utf-8 -*-
'''
Created on Oct 31, 2012

@author: liubida
'''

from config.config import c
from statistics.biz import _is_test
from util import get_week_sun
import MySQLdb
import datetime

def get_share_channels(start_time, end_time, data_grain='day'):
    '''为[收藏渠道统计]获取原始数据
        [params] data_grain: the time_interval of the statistics
        [return] 
    '''
    jiathis = '"from": "jiathis"'
    bshare =  '"from": "bshare"'
    try:
        conn = MySQLdb.connect(**c.db_self_config)
        cursor = conn.cursor()

        ret = []
        # 去掉测试用户的id
        exclude_test_user_id = ' and o.user_id !='
        exclude_test_user_id += ' and o.user_id !='.join(map(lambda x:str(x), c.test_id))

        sql = """select o.user_id, oo.object_key, oo.gmt_create from stats_oper o  
        left join stats_operobject oo on oo.oper_id = o.id 
        where o.oper_type_id in (1,35) %s and oo.gmt_create >= '%s' and oo.gmt_create <= '%s'  
        and oo.object_key like '%%\"from\"%%' """ % (exclude_test_user_id, start_time, end_time)
        cursor.execute(sql)
        results = cursor.fetchall()

        user_id = None
        object_key = None
        gmt_create = None
        
        m = {}
        for d in results:
            user_id = int(d[0])
            object_key = str(d[1])
            gmt_create = datetime.datetime.strptime(str(d[2]), "%Y-%m-%d %H:%M:%S")

            # 去掉测试用户
            if not _is_test(user_id):
                if data_grain == 'day':
                    key = gmt_create.strftime("%Y-%m-%d")
                elif data_grain == 'week':
                    key = get_week_sun(gmt_create).strftime("%Y-%m-%d")
                elif data_grain == 'month':
                    key = gmt_create.strftime("%Y-%m")

                if key not in m.keys():
                    m[key] = {'bshare':0, 'jiathis':0, 'other':0}
                if -1 != object_key.find(bshare):
                    m[key]['bshare'] += 1
                elif -1 != object_key.find(jiathis):
                    m[key]['jiathis'] += 1
                else:
                    m[key]['other'] += 1
                    
        # 数据整理, 防止有一天/一周没有数据
        ret = []
        start = datetime.datetime.strptime(start_time, "%Y-%m-%d %H:%M:%S")
        end = datetime.datetime.strptime(end_time, "%Y-%m-%d %H:%M:%S")
        cur = datetime.datetime(start.year, start.month, start.day)
        if data_grain == 'day':
            step = datetime.timedelta(days=1)
            while cur <= end:
                key = cur.strftime("%Y-%m-%d")
                if key in m.keys():
                    ret.append({'time': cur.strftime("%m-%d"), 'bshare':m[key]['bshare'], 'jiathis':m[key]['jiathis'], 'other':m[key]['other']})
                else:
                    ret.append({'time': cur.strftime("%m-%d"), 'bshare':0, 'jiathis':0, 'other':0})
                cur += step
        elif data_grain == 'week':
            step = datetime.timedelta(days=7)
            end_sun = get_week_sun(end)
            while cur <= end_sun:
                key = get_week_sun(cur).strftime("%Y-%m-%d")
                if key in m.keys():
                    ret.append({'time': key, 'bshare':m[key]['bshare'], 'jiathis':m[key]['jiathis'], 'other':m[key]['other']})
                else:
                    ret.append({'time': key, 'bshare':0, 'jiathis':0, 'other':0})
                cur += step
        elif data_grain == 'month':
            # 月的不需要做这种逻辑
            for r in m.keys():
                ret.append({'time': r, 'bshare':m[r]['bshare'], 'jiathis':m[r]['jiathis'], 'other':m[r]['other']})
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

if __name__ == '__main__':
#    start_time = datetime.datetime(2012, 11, 9, 0, 0, 0)
#    end_time = datetime.datetime(2012, 11, 11, 23, 59, 59)
    b = get_share_channels('2012-11-09 00:00:00', '2012-11-11 23:59:59', data_grain='day')
    print b
#    b = get_bookmark_website_for_user_raw_data(start_time,end_time)
#    print b
#    get_bookmark_website_raw_data('2012-08-20 00:00:00', '2012-08-26 23:59:59')
    
#    b = get_bookmark_website_for_user_raw_data()
    
#    b = get_bookmark_website_for_user_raw_data()
#    print b
    pass
