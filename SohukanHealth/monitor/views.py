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

    username1 = str(request.user.username)
    print username1
    
    username = str(request.user)
    if username not in c.monitor_user:
        return HttpResponse("<strong>Sry, u can not see this page</strong>", status=403)
    
    av = []
    this_month = datetime.datetime.now().month
    for i in range(5, this_month + 1):
        start_time, end_time = get_start_end_for_month(i)

        alarm = SysAlarm.objects.filter(start_time__gte=start_time, start_time__lte=end_time)
        
        all_min = timediff(start_time, end_time, 'minute')
        av_time = all_min
        
        for a in alarm:
            av_time = av_time - timediff(a.start_time, a.end_time, 'minute')
        
        av_percent = round(((av_time + 0.0000000000001) / all_min), 6) 
        av_color = c.green if av_percent > 0.9999 else c.red
        av_percent = to_percent(av_percent)
        av.append({'month':i, 'time':av_time, 'percent':av_percent, 'color':av_color})
        
    response = HttpResponse(t.render(Context({
        'av':av,
        'user':request.user
    })))
    
    # 业务监控的系统可用率
    now = datetime.datetime.now()
    expire = now + datetime.timedelta(hours=8)
    print now
    print expire
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
    print expire
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
