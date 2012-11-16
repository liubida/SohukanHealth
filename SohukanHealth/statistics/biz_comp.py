# -*- coding: utf-8 -*-
'''
Created on Oct 31, 2012

@author: liubida
'''

from SohukanHealth.aggregation import bshare, jiathis, other, webapp, sohu_blog, sohu_news
from statistics.models import Aggregation
import anyjson
import datetime

def get_share_channels(start_time, end_time, data_grain='day'):
    '''start_time, end_time is string'''
    raw_data = Aggregation.objects.filter(type='share_channels', time__gte=start_time, time__lte=end_time).values('time', 'content')

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
                            bshare:data[key][bshare]['count'],
                            jiathis:data[key][jiathis]['count'],
                            webapp:data[key][webapp]['count'],
                            sohu_blog:data[key][sohu_blog]['count'],
                            sohu_news:data[key][sohu_news]['count'],
                            other:data[key][other]['count']})
            else:
                if cur.date() == end.date():
                    break;
                else:
                    cur += step
                    continue;
            cur += step
    elif data_grain == 'week':
        step = datetime.timedelta(days=1)
        middle = {bshare:0, jiathis:0, webapp:0, sohu_blog:0, sohu_news:0,  other:0}
        
        while cur <= end:
            key = cur.strftime("%Y-%m-%d")
            if key not in data.keys():
                if cur.date() == end.date():
                    ret.append({'time': (cur-step).strftime("%m-%d"),
                                bshare:middle[bshare],
                                jiathis:middle[jiathis],
                                webapp:middle[webapp],
                                sohu_blog:middle[sohu_blog],
                                sohu_news:middle[sohu_news],
                                other:middle[other]})
                    break;
                else:
                    cur += step
                    continue;
                
            middle[bshare] += data[key][bshare]['count']
            middle[jiathis] += data[key][jiathis]['count']
            middle[webapp] += data[key][webapp]['count']
            middle[sohu_blog] += data[key][sohu_blog]['count']
            middle[sohu_news] += data[key][sohu_news]['count']
            middle[other] += data[key][other]['count']
            
            if cur.weekday() == 6 or cur.date() == end.date():
                # 这一天是周日
                ret.append({'time': cur.strftime("%m-%d"),
                            bshare:middle[bshare],
                            jiathis:middle[jiathis],
                            webapp:middle[webapp],
                            sohu_blog:middle[sohu_blog],
                            sohu_news:middle[sohu_news],
                            other:middle[other]})
                middle[bshare] = 0
                middle[jiathis] = 0
                middle[webapp] = 0
                middle[sohu_blog] = 0 
                middle[sohu_news] = 0
                middle[other] = 0
            cur += step
    elif data_grain == 'month':
        step = datetime.timedelta(days=1)
        middle = {bshare:0, jiathis:0, webapp:0, sohu_blog:0, sohu_news:0,  other:0}
        
        while cur <= end:
            key = cur.strftime("%Y-%m-%d")
            if key not in data.keys():
                if cur.date() == end.date():
                    ret.append({'time': (cur-step).strftime("%m-%d"),
                                bshare:middle[bshare],
                                jiathis:middle[jiathis],
                                webapp:middle[webapp],
                                sohu_blog:middle[sohu_blog],
                                sohu_news:middle[sohu_news],
                                other:middle[other]})
                    break;
                else:
                    cur += step
                    continue;
            middle[bshare] += data[key][bshare]['count']
            middle[jiathis] += data[key][jiathis]['count']
            middle[webapp] += data[key][webapp]['count']
            middle[sohu_blog] += data[key][sohu_blog]['count']
            middle[sohu_news] += data[key][sohu_news]['count']
            middle[other] += data[key][other]['count']
            
            if (cur + step).month != cur.month or cur.date() == end.date():
                ret.append({'time': cur.strftime("%Y-%m-%d"),
                            bshare:middle[bshare],
                            jiathis:middle[jiathis],
                            webapp:middle[webapp],
                            sohu_blog:middle[sohu_blog],
                            sohu_news:middle[sohu_news],
                            other:middle[other]})
                middle[bshare] = 0
                middle[jiathis] = 0
                middle[webapp] = 0
                middle[sohu_blog] = 0 
                middle[sohu_news] = 0
                middle[other] = 0                            
            cur += step
    return ret

if __name__ == '__main__':
#    start_time = datetime.datetime(2012, 11, 9, 0, 0, 0)
#    end_time = datetime.datetime(2012, 11, 11, 23, 59, 59)
    b = get_share_channels('2012-10-30 00:00:00', '2012-11-13 23:59:59', data_grain='month')
    print b
#    b = get_bookmark_website_for_user_raw_data(start_time,end_time)
#    print b
#    get_bookmark_website_raw_data('2012-08-20 00:00:00', '2012-08-26 23:59:59')
    
#    b = get_bookmark_website_for_user_raw_data()
    
#    b = get_bookmark_website_for_user_raw_data()
#    print b
    pass
