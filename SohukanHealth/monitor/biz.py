# -*- coding: utf-8 -*-
'''
Created on Jun 19, 2012

@author: liubida
'''
from monitor.models import AppAvailableData
import datetime
import anyjson

def calc_app_available(duration='day'):
    '''duration=hour, day, week, month, sixmonths, year'''
    
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
    
if __name__ == '__main__':
    a = get_app_available()
    print a
