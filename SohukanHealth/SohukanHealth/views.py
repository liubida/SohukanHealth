'''
Created on Jun 14, 2012

@author: liubida
'''
from config.config import c
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.template import loader
from django.template.context import Context
import random

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

