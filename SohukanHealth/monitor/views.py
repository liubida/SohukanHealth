# -*- coding: utf-8 -*-

from config.config import c
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.template import loader
from django.template.context import Context
from monitor.models import AppAvailableData, SysAlarm
from util import get_start_end_for_month, timediff, to_percent
import anyjson
import datetime

@login_required
def monitor(request):
    t = loader.get_template('monitor/monitor.html')

    username = str(request.user)
    if username not in c.monitor_user:
        return HttpResponse("<strong>Sry, u can not see this page</strong>", status=403)
    
    av = []
    this_month = datetime.datetime.now().month
    # 本年度从5月份开始
    for i in range(5, this_month + 1):
        # 本月的起止时间点
        start_time, end_time = get_start_end_for_month(i)

        alarm = SysAlarm.objects.filter(start_time__gte=start_time, start_time__lte=end_time)
        
        # 本月总时间
        all_min = timediff(start_time, end_time, 'minute')
        # 初始: 本月可用时间=本月总时间
        av_time = all_min
        # 初始: 本月可用时间(因自身原因导致故障)=本月总时间
        av_self_time = all_min
        
        for a in alarm:
            if a.type in c.self_alarm_type:
                av_self_time = av_time - timediff(a.start_time, a.end_time, 'minute')
            av_time = av_time - timediff(a.start_time, a.end_time, 'minute')
                 
        # 全部原因导致的系统可用率
        av_percent = round(((av_time + 0.0000000000001) / all_min), 6)
        # 自身原因导致的系统可用率
        av_self_percent = round(((av_self_time + 0.0000000000001) / all_min), 6)
        
        av_color = c.green if av_percent > 0.9999 else c.red
        av_self_color = c.green if av_self_percent > 0.9999 else c.red
        
        av_percent = to_percent(av_percent)
        av_self_percent = to_percent(av_self_percent)
        
        av.append({'month':i, 'time':av_time, 'self_time':av_self_time, 'percent':av_percent, 'self_percent':av_self_percent,
                   'color':av_color, 'self_color':av_self_color})
        
    response = HttpResponse(t.render(Context({
        'av':av,
        'user':request.user
    })))
    
    # 业务监控的系统可用率
    now = datetime.datetime.now()
    expire = now + datetime.timedelta(hours=8)
    response['Expires'] = expire.strftime('%a, %d %b %Y %H:%M:%S %Z')
    return response

@login_required
def sys_alarm(request, month=0):
    t = loader.get_template('monitor/sys_alarm_table.html')
    month = int(month)
    
    start_time, end_time = get_start_end_for_month(month)
    a = SysAlarm.objects.filter(start_time__gte=start_time, start_time__lte=end_time)
    alarm = []
    if a:
        for i in a:
            alarm.append({'type':i.type,
                     'start_time':i.start_time.strftime('%Y-%m-%d %H:%M:%S'),
                     'end_time':i.end_time.strftime('%Y-%m-%d %H:%M:%S'),
                     'duration': timediff(i.start_time, i.end_time, 'minute'),
                     'reason':i.reason if i.reason else '',
                     'wiki_url':i.wiki_url if i.wiki_url else '',
                     'comments':i.comments if i.comments else ''})
    
    response = HttpResponse(t.render(Context({'alarm':alarm})))
    
    # 业务监控的系统可用率
    now = datetime.datetime.now()
    expire = (now + datetime.timedelta(hours=8))
    response['Expires'] = expire.strftime('%a, %d %b %Y %H:%M:%S %Z')
    return response
    
@login_required
def read(request):
    s = {'list':[]}
    data = AppAvailableData.objects.filter(name='read').values('name', 'time_used', 'time')
    for d in data:
        s['list'].append({'name':d['name'], 'time_used':d['time_used'], 'time':d['time'].strftime('%Y.%m.%d %H:%M:%S')})
    
    response = HttpResponse(anyjson.dumps(s))
    response['Cache-Control'] = 'max-age=%d' % (300)
    
    return response

@login_required
def add(request):
    s = {'list':[]}
    data = AppAvailableData.objects.filter(name='add').values('name', 'time_used', 'time')
    for d in data:
        s['list'].append({'name':d['name'], 'time_used':d['time_used'], 'time':d['time'].strftime('%Y.%m.%d %H:%M:%S')})
    
    response = HttpResponse(anyjson.dumps(s))
    response['Cache-Control'] = 'max-age=%d' % (300)
    
    return response
