# Create your views here.
from django.http import HttpResponse
from django.template import loader
from django.template.context import Context
from monitor.biz import appAvailableData_to_json, get_app_available
from monitor.models import AppAvailableData

def monitor(request):
#    latest_poll_list = Poll.objects.all().order_by('-pub_date')[:5]
    
    t = loader.get_template('monitor/monitor.html')
    c = Context({
        'app_available': get_app_available(),
    })
    return HttpResponse(t.render(c))

def app_available(request):
    
    return HttpResponse(get_app_available())

def read(request):
    data = AppAvailableData.objects.filter(name='read').values('name', 'time_used', 'time')
    return HttpResponse(appAvailableData_to_json(data))

def add(request):
    data = AppAvailableData.objects.filter(name='add').values('name', 'time_used', 'time')
    return HttpResponse(appAvailableData_to_json(data))
