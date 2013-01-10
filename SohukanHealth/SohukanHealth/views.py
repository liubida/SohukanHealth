'''
Created on Jun 14, 2012

@author: liubida
'''
from config.config import c
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.template import loader
from django.template.context import Context

from timer.job import add_job, read_job

import random
import json

@login_required
def index(request):
    t = loader.get_template('index.html')
    c = Context({
        'user': request.user
    })
    return HttpResponse(t.render(c))

@login_required
def about(request):
    t = loader.get_template('about.html')
    c = Context()
    return HttpResponse(t.render(c)) 

@login_required
def logtest(request):
    a = random.randint(0, 10)
    if a % 2:
        c.logger.info("SohukanHealth logtest info")
    else:
        c.logger.error("SohukanHealth logtest error")
    return HttpResponse("hehe")        

def add_job_monitor(request):
    value = add_job()
    print '2: ', value
    if value['result'] == True:
        code = 200
        message = 'Add is OK!'
    else:
        code = 202
        message = 'Add job is error!!! Reason:' + value['comments']
    res = {'code': code, 'message': message}
    return HttpResponse(json.dumps(res))

def read_job_monitor(request):
    value = read_job()
    print '2: ', value
    if value['result'] == True:
        code = 200
        message = 'Read is OK!'
    else:
        code = 202
        message = 'Read job is error!!! Reason:' + value['comments']
    res = {'code': code, 'message': message}
    return HttpResponse(json.dumps(res))
