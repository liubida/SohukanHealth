'''
Created on Jun 14, 2012

@author: liubida
'''
from config.config import c
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.template import loader
from django.template.context import Context
from django.shortcuts import render_to_response

from timer.job import add_job, read_job
from statistics.biz import get_notice_args, get_token_list
from statistics.models import Notice

import random
import json
import urllib, urllib2

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
def push(request):
    submit, title, content, users, user_list = get_notice_args(request)
    flag = ''
    if submit:
        if not (title and content):
            flag = 'miss params!'
            return render_to_response('push.html', locals())
        data = Notice(title=title, content=content, group=0 if users=='all' else 1, users=';'.join(user_list))
        data.save()
        if users == 'all':
            #return render_to_response('push.html', locals())
            token_list = get_token_list()
        else:
            token_list = get_token_list(user_list=user_list)
        for token in token_list:
            http_request_add(token=token, title=title, content=content)
        user_list = ','.join(user_list)
        flag = 'Done!'
    return render_to_response('push.html', locals())

def http_request_add(token, title, content):
    url = 'http://kan.sohu.com/api/2/bookmarks/add'
    body = urllib.urlencode({'url': 'http://e.weibo.com/suishenkan', 'title': title, 'content': content, 'content_source': 'partial'})
    try:
        req = urllib2.Request(url, body)
        req.add_header('Cookie', 'access_token=%s' % token)
        resp = urllib2.urlopen(req).read()
        print resp
    except Exception, e:
        raise e

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
