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
from timer.alarm_job import web_alarm_job

import random
import json
import urllib

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
    if value['result'] == True:
        code = 200
        message = 'Read is OK!'
    else:
        code = 202
        message = 'Read job is error!!! Reason:' + value['comments']
    res = {'code': code, 'message': message}
    return HttpResponse(json.dumps(res))

def web_job_monitor(request):
    code = 200
    kanMess = 'OK!'
    readerMess = 'OK!'
    message = 'Web site is OK!'
    weburl = 'http://kan.sohu.com/'
    readerurl = 'http://kan.sohu.com/reader/'
    try:
        kan = urllib.urlopen(weburl).read()
        if(len(kan) < 1000):
            kanMess = 'Web is Error!!!'
            code = 202
    except:
        kanMess = 'Web is Error!!!'
        code = 202
    try:
        reader = urllib.urlopen(readerurl).read()
        if(len(reader) < 1000):
            readerMess = 'Reader is Error!!!'
            code = 202
    except:
        readerMess = 'Reader is Error!!!'
        code = 202
    if code == 202:
        if kanMess == 'OK!':
            message = readerMess
        elif readerMess == 'OK!':
            message = kanMess
        else:
            message = 'Web and Reader are both Error!!!'
    res = {'code': code, 'message': message}
    return HttpResponse(json.dumps(res))
