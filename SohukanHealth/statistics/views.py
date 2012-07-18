# Create your views here.
from django.http import HttpResponse
from django.template import loader
from django.template.context import Context
from monitor.models import SomeTotal
from statistics.biz import get_bookmark_per_user, get_bookmark_time, \
    get_bookmark_percent, get_bookmark_website
from statistics.models import DayReport
import anyjson
import datetime
import pickle


def statistics(request):
    t = loader.get_template('statistics/statistics.html')
    c = Context({
        'name': 'liubida',
    })
    return HttpResponse(t.render(c))

def user_total(request):
    data = SomeTotal.objects.filter(name='user').values('time', 'count')
    return HttpResponse(someTotal_to_json(data))

    
def bookmark_total(request):
    data = SomeTotal.objects.filter(name='bookmark').values('time', 'count')
    return HttpResponse(someTotal_to_json(data))

def user_bookmark_percent(request):
    o = request.GET.get('before_time', '')
    jsondata = get_bookmark_percent(str(o))
    return HttpResponse(jsondata)

def bookmark_per_user(request):
    o = request.GET.get('start_time', '')
    jsondata = get_bookmark_per_user(str(o))
    return HttpResponse(jsondata)

def bookmark_time(request):
    o = request.GET.get('start_time', '')
    jsondata = get_bookmark_time(str(o))
        
    return HttpResponse(jsondata)

def day_report(request):
    template = loader.get_template('statistics/day_report.html')
    c = Context({
        'name': 'liubida'})
        
    return HttpResponse(template.render(c))
    
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
            'user_new_inc_color': '#c00' if data['user']['new_inc'] > 0  else '#008000',
            'bookmark_total'    : data['bookmark']['total'],
            'bookmark_total_inc': data['bookmark']['total_inc'],
            'bookmark_new'      : data['bookmark']['total'] - data['bookmark']['total_yd'],
            'bookmark_new_inc'  : data['bookmark']['new_inc'],
            'bookmark_new_inc_color': '#c00' if data['bookmark']['new_inc'] > 0  else '#008000',
        }
        
        return HttpResponse(anyjson.dumps(s))
        
def day_report_bookmark_percent(request):
    start_time = request.GET.get('start_time', '')
    end_time = request.GET.get('end_time', '')
    
    jsondata_array = DayReport.objects.filter(time__gte=start_time, time__lt=end_time).values('jsondata')
    print jsondata_array
    if jsondata_array:
        jsondata = jsondata_array[0]['jsondata']
        data = anyjson.loads(jsondata)
        return HttpResponse(anyjson.dumps(data['bookmark_count']))        
    
def day_report_bookmark_website(request):
    start_time = request.GET.get('start_time', '')
    end_time = request.GET.get('end_time', '')
    
    jsondata_array = DayReport.objects.filter(time__gte=start_time, time__lt=end_time).values('jsondata')
    print jsondata_array
    if jsondata_array:
        jsondata = jsondata_array[0]['jsondata']
        data = anyjson.loads(jsondata)
        return HttpResponse(anyjson.dumps(data['bookmark_website']))        
   
def someTotal_to_json(data):
    s = {}
    s['success'] = True
    s['info'] = ''
    s['code'] = 0
    s['total'] = data.count()
    s['list'] = []
    for d in data:
        tmp = {}
        tmp['time'] = d['time'].strftime('%Y.%m.%d %H:%M:%S')
        tmp['count'] = d['count']
        s['list'].append(tmp)
    return anyjson.dumps(s)
