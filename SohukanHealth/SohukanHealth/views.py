'''
Created on Jun 14, 2012

@author: liubida
'''
from django.http import HttpResponse, Http404
import datetime


def home_page(request):
    return HttpResponse("hi, i'm at home!")

def hello(request):
    return HttpResponse("hello liubida")

def now(request):
    now = datetime.datetime.now()
    return HttpResponse("now is : %s " % now)

def now_plus(request, offset):
    try:
        offset = int(offset)
    except ValueError:
        raise Http404()
    assert True
    dt = datetime.datetime.now() + datetime.timedelta(hours=offset)
    return HttpResponse("now + %s is : %s " % (offset, dt))