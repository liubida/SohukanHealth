# Create your views here.
from django.http import HttpResponse
from django.template import loader
from django.template.context import Context
from monitor.models import AppAvailableData
import json

def monitor(request):
#    latest_poll_list = Poll.objects.all().order_by('-pub_date')[:5]
    
    t = loader.get_template('monitor/monitor.html')
    c = Context({
        'name': 'liubida&&zww',
    })
    return HttpResponse(t.render(c))

def all(request):
    t = loader.get_template('all.html')
    c = Context({
        'name': 'liubida&&zww',
    })
    return HttpResponse(t.render(c))

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
    return json.dumps(s)

def read(request):
    data = AppAvailableData.objects.filter(name='read').values('name', 'time_used', 'time')
    return HttpResponse(appAvailableData_to_json(data))

def add(request):
    data = AppAvailableData.objects.filter(name='add').values('name', 'time_used', 'time')
    return HttpResponse(appAvailableData_to_json(data))
