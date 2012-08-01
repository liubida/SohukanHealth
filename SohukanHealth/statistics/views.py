# -*- coding: utf-8 -*-
# Create your views here.
from config.config import c
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.template import loader
from django.template.context import Context
from monitor.models import SomeTotal
from statistics.biz import get_bookmark_per_user, get_bookmark_time, \
    get_bookmark_percent, get_data_interval, add_inc_for_data, get_activate_user, \
    get_bookmark_website, _get_week_num, get_user_platform
from statistics.models import DayReport
import anyjson
import datetime

'''综合'''

# 综合页面首页
@login_required
def statistics(request):
    t = loader.get_template('statistics/statistics.html')
    c = Context({
        'name': 'liubida',
    })
    return HttpResponse(t.render(c))

# 综合 注册用户数统计
@login_required
def user_total(request):
    start_time = request.GET.get('start_time', c.MIN_TIME)
    end_time = request.GET.get('end_time', c.MAX_TIME)
    data_grain = request.GET.get('data_grain', 'day')
    data_grain = data_grain if data_grain else 'day'
    
    if start_time == 'NaN-aN-aN aN:aN:aN': 
        start_time = c.MIN_TIME
    if end_time == 'NaN-aN-aN aN:aN:aN': 
        end_time = c.MAX_TIME

    data = {'list':[]}
    raw_data = SomeTotal.objects.filter(name='user', time__gte=start_time, time__lte=end_time).values('time', 'count')
    
    if data_grain == 'hour':
        for d in raw_data:
            data['list'].append({'time':d['time'].strftime('%m-%d %H:%M:%S'), 'count':d['count']})
    elif data_grain == 'day':
        delta = datetime.timedelta(days=1)
        # 每天取一个23点的数据
        data['list'] = get_data_interval(raw_data, delta)
    elif data_grain == 'week':
        # 每隔7天取一个23点的数据
        delta = datetime.timedelta(days=7)
        data['list'] = get_data_interval(raw_data, delta)
    elif data_grain == 'month':
        # 每隔4周天取一个23点的数据
        delta = datetime.timedelta(weeks=4)
        data['list'] = get_data_interval(raw_data, delta)

    # 计算data的增长率
    add_inc_for_data(data)
    return HttpResponse(anyjson.dumps(data))

# 综合 收藏文章数统计
@login_required
def bookmark_total(request):
    start_time = request.GET.get('start_time', c.MIN_TIME)
    end_time = request.GET.get('end_time', c.MAX_TIME)
    data_grain = request.GET.get('data_grain', 'day')
    data_grain = data_grain if data_grain else 'day'
    
    if start_time == 'NaN-aN-aN aN:aN:aN': 
        start_time = c.MIN_TIME
    if end_time == 'NaN-aN-aN aN:aN:aN': 
        end_time = c.MAX_TIME

    data = {'list':[]}
    raw_data = SomeTotal.objects.filter(name='bookmark', time__gte=start_time, time__lte=end_time).values('time', 'count')
    if data_grain == 'hour':
        for d in raw_data:
            data['list'].append({'time':d['time'].strftime('%m-%d %H:%M:%S'), 'count':d['count']})
    elif data_grain == 'day':
        delta = datetime.timedelta(days=1)
        # 每天取一个23点的数据
        data['list'] = get_data_interval(raw_data, delta)
    elif data_grain == 'week':
        # 每隔7天取一个23点的数据
        delta = datetime.timedelta(days=7)
        data['list'] = get_data_interval(raw_data, delta)
    elif data_grain == 'month':
        # 每隔4周天取一个23点的数据
        delta = datetime.timedelta(weeks=4)
        data['list'] = get_data_interval(raw_data, delta)

    # 计算data的增长率
    add_inc_for_data(data)
    return HttpResponse(anyjson.dumps(data))

# 综合 收藏文章排行统计  
@login_required
def bookmark_per_user(request):
    start_time = request.GET.get('start_time', c.MIN_TIME)
    end_time = request.GET.get('end_time', c.MAX_TIME)
    limit = request.GET.get('data_size', '100')
    limit = int(limit if limit else 100)
    
    if start_time == 'NaN-aN-aN aN:aN:aN': 
        start_time = c.MIN_TIME
    if end_time == 'NaN-aN-aN aN:aN:aN': 
        end_time = c.MAX_TIME

    jsondata = get_bookmark_per_user(start_time, end_time, limit)
    return HttpResponse(jsondata)

# 综合 收藏文章时段统计
@login_required
def bookmark_time(request):
    start_time = request.GET.get('start_time', c.MIN_TIME)
    end_time = request.GET.get('end_time', c.MAX_TIME)
    
    if start_time == 'NaN-aN-aN aN:aN:aN': 
        start_time = c.MIN_TIME
    if end_time == 'NaN-aN-aN aN:aN:aN': 
        end_time = c.MAX_TIME
        
    jsondata = get_bookmark_time(start_time, end_time)
    return HttpResponse(jsondata)

# 综合 收藏文章百分比(pie)统计
@login_required
def user_bookmark_percent(request):
    start_time = request.GET.get('start_time', c.MIN_TIME)
    end_time = request.GET.get('end_time', c.MAX_TIME)
    
    if start_time == 'NaN-aN-aN aN:aN:aN': 
        start_time = c.MIN_TIME
    if end_time == 'NaN-aN-aN aN:aN:aN': 
        end_time = c.MAX_TIME
        
    jsondata = get_bookmark_percent(start_time, end_time, raw=False)
    return HttpResponse(jsondata)

'''深度统计'''

# 深度统计页面首页
@login_required
def depth(request):
    template = loader.get_template('statistics/depth.html')
    c = Context({
        'name': 'liubida'})
        
    return HttpResponse(template.render(c))

# 深度 活跃用户统计    
@login_required
def activate_user(request):
    start_time = request.GET.get('start_time', c.MIN_TIME)
    end_time = request.GET.get('end_time', c.MAX_TIME)
    data_grain = request.GET.get('data_grain', 'day')
    data_grain = data_grain if data_grain else 'day'
    
    if start_time == 'NaN-aN-aN aN:aN:aN': 
        start_time = c.MIN_TIME
    if end_time == 'NaN-aN-aN aN:aN:aN': 
        end_time = c.MAX_TIME

    jsondata = get_activate_user(start_time, end_time, data_grain=data_grain)
    return HttpResponse(jsondata)

# 深度 收藏文章来源网站统计
@login_required
def bookmark_website(request):
    start_time = request.GET.get('start_time', c.MIN_TIME)
    end_time = request.GET.get('end_time', c.MAX_TIME)
    limit = request.GET.get('size', '100')
    limit = int(limit if limit else 100)
    
    if start_time == 'NaN-aN-aN aN:aN:aN': 
        start_time = c.MIN_TIME
    if end_time == 'NaN-aN-aN aN:aN:aN': 
        end_time = c.MAX_TIME
    jsondata = get_bookmark_website(start_time, end_time, limit=limit)
    return HttpResponse(jsondata)

# 深度 用户使用平台统计
@login_required
def user_platform(request):
    start_time = request.GET.get('start_time', c.MIN_TIME)
    end_time = request.GET.get('end_time', c.MAX_TIME)
    
    if start_time == 'NaN-aN-aN aN:aN:aN': 
        start_time = c.MIN_TIME
    if end_time == 'NaN-aN-aN aN:aN:aN': 
        end_time = c.MAX_TIME
        
    jsondata = get_user_platform(start_time, end_time)
    print jsondata
    return HttpResponse(jsondata)

'''日报'''
# 日报首页页面
@login_required
def day_report(request):
    template = loader.get_template('statistics/day_report.html')
    c = Context({
        'name': 'liubida'})
        
    return HttpResponse(template.render(c))

# 日报日期
@login_required
def day_report_date(request):
    time_array = DayReport.objects.filter().values('time')
    
    day_array = []
    day_format = "%m-%d"
    for t in time_array:
        print t
        print t['time']
        day_array.append(t['time'].strftime(day_format))

    s = {}
    s['success'] = True
    s['info'] = ''
    s['code'] = 0
    s['total'] = len(day_array)
    s['list'] = day_array
    return HttpResponse(anyjson.dumps(s))

# 日报概要信息    
@login_required
def day_report_abstract(request):
    start_time = request.GET.get('start_time', '')
    end_time = request.GET.get('end_time', '')
    
    jsondata_array = DayReport.objects.filter(time__gte=start_time, time__lt=end_time).values('jsondata')
    if jsondata_array:
        jsondata = jsondata_array[0]['jsondata']
        data = anyjson.loads(jsondata)

        s = {
            'name': 'liubida',
            'user_total'    : data['user']['total'],
            'user_total_inc': data['user']['total_inc'],
            'user_new'      : data['user']['total'] - data['user']['total_yd'],
            'user_new_inc'  : data['user']['new_inc'],
            'user_new_inc_color': c.red if data['user']['new_inc'] > 0  else c.green,
            'bookmark_total'    : data['bookmark']['total'],
            'bookmark_total_inc': data['bookmark']['total_inc'],
            'bookmark_new'      : data['bookmark']['total'] - data['bookmark']['total_yd'],
            'bookmark_new_inc'  : data['bookmark']['new_inc'],
            'bookmark_new_inc_color': c.red if data['bookmark']['new_inc'] > 0  else c.green,
        }
        
        return HttpResponse(anyjson.dumps(s))
    
# 日报收藏文章比例        
@login_required
def day_report_bookmark_percent(request):
    start_time = request.GET.get('start_time', '')
    end_time = request.GET.get('end_time', '')
    
    jsondata_array = DayReport.objects.filter(time__gte=start_time, time__lt=end_time).values('jsondata')
    print jsondata_array
    if jsondata_array:
        jsondata = jsondata_array[0]['jsondata']
        data = anyjson.loads(jsondata)
        return HttpResponse(anyjson.dumps(data['bookmark_count']))        

# 日报收藏文章来源网站    
@login_required
def day_report_bookmark_website(request):
    start_time = request.GET.get('start_time', '')
    end_time = request.GET.get('end_time', '')
    
    jsondata_array = DayReport.objects.filter(time__gte=start_time, time__lt=end_time).values('jsondata')
    print jsondata_array
    if jsondata_array:
        jsondata = jsondata_array[0]['jsondata']
        data = anyjson.loads(jsondata)
        return HttpResponse(anyjson.dumps(data['bookmark_website']))        

'''周报'''
  
# 周报首页
@login_required
def week_report(request):
    template = loader.get_template('statistics/week_report.html')
    c = Context({
        'name': 'liubida'})
        
    return HttpResponse(template.render(c))

# 编码时测试用
@login_required
def test(start_time, end_time, data_grain='day'):
    if start_time == 'NaN-aN-aN aN:aN:aN': 
        start_time = c.MIN_TIME
    if end_time == 'NaN-aN-aN aN:aN:aN': 
        end_time = c.MAX_TIME
    data = {'list':[]}
    raw_data = SomeTotal.objects.filter(name='user', time__gte=start_time, time__lte=end_time).values('time', 'count')
    
    if data_grain == 'hour':
        for d in raw_data:
            data['list'].append({'time':d['time'].strftime('%m-%d %H:%M:%S'), 'count':d['count']})
    elif data_grain == 'day':
        delta = datetime.timedelta(days=1)
        # 每天取一个23点的数据
        data['list'] = get_data_interval(raw_data, delta)
    elif data_grain == 'week':
        week_start = _get_week_num(raw_data[0]['time'])
        
        first_day = datetime.date.today().replace(month=1, day=1)
        day = first_day + datetime.timedelta(weeks=week_start)
        print raw_data[0]['time']
        print week_start
        print day
        
        for d in raw_data:
            if d['time'].hour == 23 and \
               d['time'].year == day['time'].year and \
               d['time'].month == day['time'].month and \
               d['time'].day == day['time'].day:
                data['list'].append({'time':d['time'].strftime('%Y-%m-%d'), 'count':d['count']})
                day += delta
        
#        # 每隔7天取一个23点的数据
#        delta = datetime.timedelta(days=7)
#        data['list'] = get_data_interval(raw_data, delta)
    elif data_grain == 'month':
        # 每隔4周天取一个23点的数据
        delta = datetime.timedelta(weeks=4)
        data['list'] = get_data_interval(raw_data, delta)
    
if __name__ == '__main__':
    test('NaN-aN-aN aN:aN:aN', 'NaN-aN-aN aN:aN:aN', 'week')
#    test('2012-07-12', '2012-07-17')
#    day_report_job()
#    mysql_ping_job();
#    user_total_job()
#    bookmark_total_job()
#    add_and_read_alarm_job()
#    url = RandomSpider().get_valid_url()
