# -*- coding: utf-8 -*-

from config.config import c
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.template import loader
from django.template.context import Context
from monitor.biz import appAvailableData_to_json
from monitor.models import AppAvailableData, SysAlarm
from util import get_start_end_for_month, timediff
import datetime

@login_required
def monitor(request):
    t = loader.get_template('monitor/monitor.html')

    username = str(request.user)
    if username not in c.monitor_user:
        return HttpResponse("<strong>Sry, u can not see this page</strong>", status=403)
    
    av = []
    this_month = datetime.datetime.now().month
    for i in range(5, this_month):
        start_time, end_time = get_start_end_for_month(i)

        alarm = SysAlarm.objects.filter(start_time__gte=start_time, start_time__lte=end_time)
        
        all_min = timediff(start_time, end_time, 'minute')
        av_time = all_min
        
        for a in alarm:
            av_time = av_time - timediff(a.start_time, a.end_time, 'minute')
        
        av_percent = round(((av_time + 0.0000000000001) / all_min), 6)
        av_color = c.green if av_percent > 0.9999 else c.red
        av.append({'month':i, 'time':av_time, 'percent':av_percent, 'color':av_color})
        
    return HttpResponse(t.render(Context({
        'av':av
    })))

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
    
    return HttpResponse(t.render(Context({'alarm':alarm})))
    
@login_required
def read(request):
    data = AppAvailableData.objects.filter(name='read').values('name', 'time_used', 'time')
    return HttpResponse(appAvailableData_to_json(data))

@login_required
def add(request):
    data = AppAvailableData.objects.filter(name='add').values('name', 'time_used', 'time')
    return HttpResponse(appAvailableData_to_json(data))
