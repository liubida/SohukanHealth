# -*- coding: utf-8 -*-
'''
Created on Oct 31, 2012

@author: liubida
'''

from SohukanHealth.aggregation import bshare, jiathis, other, webapp, sohu_blog, sohu_news, baidu, iPhone, iPad, android, unknown, share, sohu_email
from statistics.models import Aggregation
import anyjson
import datetime

def get_share_channels(start_time, end_time, data_grain='day'):
    '''start_time, end_time is string'''
    raw_data = Aggregation.objects.filter(type='share_channels', time__gte=start_time, time__lte=end_time).values('time', 'content')

    data = {}
    for d in raw_data:
        Json = anyjson.loads(d['content'])
        if not Json.has_key(sohu_email):
            Json[sohu_email] = {'count': 0, 'object_key': []}
        data[d['time'].strftime("%Y-%m-%d")] = Json

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
                            sohu_email:data[key][sohu_email]['count'],
                            baidu:data[key][baidu]['count'],
                            share:data[key][share]['count']})
            else:
                if cur.date() == end.date():
                    break;
                else:
                    cur += step
                    continue;
            cur += step
    elif data_grain == 'week':
        step = datetime.timedelta(days=1)
        middle = {bshare:0, jiathis:0, webapp:0, sohu_blog:0, sohu_news:0,  baidu:0, share:0}
        
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
                                sohu_email:data[key][sohu_email],
                                baidu:middle[baidu],
                                share:middle[share]})
                    break;
                else:
                    cur += step
                    continue;
                
            middle[bshare] += data[key][bshare]['count']
            middle[jiathis] += data[key][jiathis]['count']
            middle[webapp] += data[key][webapp]['count']
            middle[sohu_blog] += data[key][sohu_blog]['count']
            middle[sohu_news] += data[key][sohu_news]['count']
            middle[sohu_email] += data[key][sohu_email]['count'],
            middle[baidu] += data[key][baidu]['count']
            middle[share] += data[key][share]['count']
            
            if cur.weekday() == 6 or cur.date() == end.date():
                # 这一天是周日
                ret.append({'time': cur.strftime("%m-%d"),
                            bshare:middle[bshare],
                            jiathis:middle[jiathis],
                            webapp:middle[webapp],
                            sohu_blog:middle[sohu_blog],
                            sohu_news:middle[sohu_news],
                            baidu:middle[baidu],
                            share:middle[share]})
                middle[bshare] = 0
                middle[jiathis] = 0
                middle[webapp] = 0
                middle[sohu_blog] = 0 
                middle[sohu_news] = 0
                middle[sohu_email] = 0
                middle[baidu] = 0
                middle[share] = 0
            cur += step
    elif data_grain == 'month':
        step = datetime.timedelta(days=1)
        middle = {bshare:0, jiathis:0, webapp:0, sohu_blog:0, sohu_news:0, baidu:0, share:0}
        
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
                                sohu_email:middle[sohu_email],
                                baidu:middle[baidu],
                                share:middle[share]})
                    break;
                else:
                    cur += step
                    continue;
            middle[bshare] += data[key][bshare]['count']
            middle[jiathis] += data[key][jiathis]['count']
            middle[webapp] += data[key][webapp]['count']
            middle[sohu_blog] += data[key][sohu_blog]['count']
            middle[sohu_news] += data[key][sohu_news]['count']
            middle[sohu_email] += data[key][sohu_email]['count'],
            middle[baidu] += data[key][baidu]['count']
            middle[share] += data[key][share]['count']
            
            if (cur + step).month != cur.month or cur.date() == end.date():
                ret.append({'time': cur.strftime("%Y-%m-%d"),
                            bshare:middle[bshare],
                            jiathis:middle[jiathis],
                            webapp:middle[webapp],
                            sohu_blog:middle[sohu_blog],
                            sohu_news:middle[sohu_news],
                            sohu_email:data[key][sohu_email],
                            baidu:middle[baidu],
                            share:middle[share]})
                middle[bshare] = 0
                middle[jiathis] = 0
                middle[webapp] = 0
                middle[sohu_blog] = 0 
                middle[sohu_news] = 0
                middle[sohu_email] = 0
                middle[baidu] = 0
                middle[share] = 0                            
            cur += step
    return ret

def get_add_channels(start_time, end_time, data_grain='day'):
    '''start_time, end_time is string'''
    raw_data = Aggregation.objects.filter(type='add_channels', time__gte=start_time, time__lte=end_time).values('time', 'content')

    data = {}
    for d in raw_data:
        data[d['time'].strftime("%Y-%m-%d")] = anyjson.loads(d['content'])
        print data
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
                            'share':data[key]['share']['count'],
                            'chrome':data[key]['chrome']['count'],
                            'sogou':data[key]['sogou']['count'],
                            'iPhone':data[key]['iPhone']['count'],
                            'iPad':data[key]['iPad']['count'],
                            'android':data[key]['android']['count'],
                            'other':data[key]['other']['count']})
            else:
                if cur.date() == end.date():
                    break;
                else:
                    cur += step
                    continue;
            cur += step
    elif data_grain == 'week':
        step = datetime.timedelta(days=1)
        middle = {'share': 0, 'chrome': 0, 'sogou': 0, 'iPhone': 0, 'iPad': 0, 'android': 0, 'other': 0}
        
        while cur <= end:
            key = cur.strftime("%Y-%m-%d")
            if key not in data.keys():
                if cur.date() == end.date():
                    ret.append({'time': (cur-step).strftime("%m-%d"),
                                'share':data[key]['share']['count'],
                                'chrome':data[key]['chrome']['count'],
                                'sogou':data[key]['sogou']['count'],
                                'iPhone':data[key]['iPhone']['count'],
                                'iPad':data[key]['iPad']['count'],
                                'android':data[key]['baidu']['count'],
                                'other':data[key]['other']['count']})
                    break;
                else:
                    cur += step
                    continue;
                
            middle['share'] += data[key]['share']['count']
            middle['chrome'] += data[key]['chrome']['count']
            middle['sogou'] += data[key]['sogou']['count']
            middle['iPhone'] += data[key]['iPhone']['count']
            middle['iPad'] += data[key]['iPad']['count']
            middle['android'] += data[key]['baidu']['count']
            middle['other'] += data[key]['other']['count']
            
            if cur.weekday() == 6 or cur.date() == end.date():
                # 这一天是周日
                ret.append({'time': cur.strftime("%m-%d"),
                            'share':middle['share'],
                            'chrome':middle['chrome'],
                            'sogou':middle['sogou'],
                            'iPhone':middle['iPhone'],
                            'iPad':middle['iPad'],
                            'android':middle['android'],
                            'other':middle['other']})
                middle['share'] = 0
                middle['chrome'] = 0
                middle['sogou'] = 0
                middle['iPhone'] = 0 
                middle['iPad'] = 0
                middle['android'] = 0
                middle['other'] = 0
            cur += step
    elif data_grain == 'month':
        step = datetime.timedelta(days=1)
        middle = {bshare:0, jiathis:0, webapp:0, sohu_blog:0, sohu_news:0, baidu:0, other:0}
        
        while cur <= end:
            key = cur.strftime("%Y-%m-%d")
            if key not in data.keys():
                if cur.date() == end.date():
                    ret.append({'time': (cur-step).strftime("%m-%d"),
                                'share':data[key]['share']['count'],
                                'chrome':data[key]['chrome']['count'],
                                'sogou':data[key]['sogou']['count'],
                                'iPhone':data[key]['iPhone']['count'],
                                'iPad':data[key]['iPad']['count'],
                                'android':data[key]['baidu']['count'],
                                'other':data[key]['other']['count']})
                    break;
                else:
                    cur += step
                    continue;
            middle['share'] += data[key]['share']['count']
            middle['chrome'] += data[key]['chrome']['count']
            middle['sogou'] += data[key]['sogou']['count']
            middle['iPhone'] += data[key]['iPhone']['count']
            middle['iPad'] += data[key]['iPad']['count']
            middle['android'] += data[key]['baidu']['count']
            middle['other'] += data[key]['other']['count']
            
            if (cur + step).month != cur.month or cur.date() == end.date():
                ret.append({'time': cur.strftime("%Y-%m-%d"),
                            bshare:middle['share'],
                            jiathis:middle['chrome'],
                            webapp:middle['sogou'],
                            sohu_blog:middle['iPhone'],
                            sohu_news:middle['iPad'],
                            baidu:middle['android'],
                            other:middle['other']})
                middle['share'] = 0
                middle['chrome'] = 0
                middle['sogou'] = 0
                middle['iPhone'] = 0 
                middle['iPad'] = 0
                middle['android'] = 0
                middle['other'] = 0
            cur += step
    return ret

def get_public_client(start_time, end_time, data_grain='day'):
    '''start_time, end_time is string'''
    raw_data = Aggregation.objects.filter(type='public_client', time__gte=start_time, time__lte=end_time).values('time', 'content')

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
                            iPhone:data[key][iPhone]['count'],
                            iPad:data[key][iPad]['count'],
                            android:data[key][android]['count'],
                            unknown:data[key][unknown]['count']})
            else:
                if cur.date() == end.date():
                    break;
                else:
                    cur += step
                    continue;
            cur += step
    elif data_grain == 'week':
        step = datetime.timedelta(days=1)
        middle = {iPhone:0, iPad:0,  android:0, unknown:0}
        
        while cur <= end:
            key = cur.strftime("%Y-%m-%d")
            if key not in data.keys():
                if cur.date() == end.date():
                    ret.append({'time': (cur-step).strftime("%m-%d"),
                                iPhone:middle[iPhone],
                                iPad:middle[iPad],
                                android:middle[android],
                                unknown:middle[unknown]})
                    break;
                else:
                    cur += step
                    continue;
                
            middle[iPhone] += data[key][iPhone]['count']
            middle[iPad] += data[key][iPad]['count']
            middle[android] += data[key][android]['count']
            middle[unknown] += data[key][unknown]['count']
            
            if cur.weekday() == 6 or cur.date() == end.date():
                # 这一天是周日
                ret.append({'time': cur.strftime("%m-%d"),
                            iPhone:middle[iPhone],
                            iPad:middle[iPad],
                            android:middle[android],
                            unknown:middle[unknown]})
                middle[iPhone] = 0
                middle[iPad] = 0
                middle[android] = 0
                middle[unknown] = 0 
            cur += step
    elif data_grain == 'month':
        step = datetime.timedelta(days=1)
        middle = {iPhone:0, iPad:0,  android:0, unknown:0}
        
        while cur <= end:
            key = cur.strftime("%Y-%m-%d")
            if key not in data.keys():
                if cur.date() == end.date():
                    ret.append({'time': (cur-step).strftime("%m-%d"),
                            iPhone:middle[iPhone],
                            iPad:middle[iPad],
                            android:middle[android],
                            unknown:middle[unknown]})
                    break;
                else:
                    cur += step
                    continue;
            middle[iPhone] += data[key][iPhone]['count']
            middle[iPad] += data[key][iPad]['count']
            middle[android] += data[key][android]['count']
            middle[unknown] += data[key][unknown]['count']
            
            if (cur + step).month != cur.month or cur.date() == end.date():
                ret.append({'time': cur.strftime("%Y-%m-%d"),
                            iPhone:middle[iPhone],
                            iPad:middle[iPad],
                            android:middle[android],
                            unknown:middle[unknown]})
                middle[iPhone] = 0
                middle[iPad] = 0
                middle[android] = 0
                middle[unknown] = 0 
            cur += step
    print ret
    return ret

if __name__ == '__main__':
#    start_time = datetime.datetime(2012, 11, 9, 0, 0, 0)
#    end_time = datetime.datetime(2012, 11, 11, 23, 59, 59)
    b = get_share_channels('2013-01-01 00:00:00', '2013-01-03 23:59:59', data_grain='day')
    print b
#    b = get_bookmark_website_for_user_raw_data(start_time,end_time)
#    print b
#    get_bookmark_website_raw_data('2012-08-20 00:00:00', '2012-08-26 23:59:59')
    
#    b = get_bookmark_website_for_user_raw_data()
    
#    b = get_bookmark_website_for_user_raw_data()
#    print b
    pass
