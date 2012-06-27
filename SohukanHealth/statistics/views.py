# Create your views here.
from django.http import HttpResponse
from django.template import loader
from django.template.context import Context
from monitor.models import SomeTotal
from statistics.biz import get_bookmark_per_user, get_bookmark_time
import anyjson


def statistics(request):
    t = loader.get_template('statistics/statistics.html')
    c = Context({
        'name': 'liubida&&zww',
    })
    return HttpResponse(t.render(c))

def user_total(request):
    data = SomeTotal.objects.filter(name='user').values('time', 'count')
    return HttpResponse(someTotal_to_json(data))
    
def bookmark_total(request):
    data = SomeTotal.objects.filter(name='bookmark').values('time', 'count')
    return HttpResponse(someTotal_to_json(data))

def bookmark_per_user(request):
    o = request.GET.get('includeTest', 'true')
    if 'true' == o:
        include_test = True
    elif 'false' == o:
        include_test = False
    jsondata = get_bookmark_per_user(include_test);
    return HttpResponse(jsondata)

def bookmark_time(request):
    o = request.GET.get('start_time', '')
    jsondata = get_bookmark_time(str(o))
        
    return HttpResponse(jsondata)
        
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
