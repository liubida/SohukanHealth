#-*- coding: utf-8 -*-

'''
Created on May 19, 2013

@author: cescgao
'''

from config.config import c
from django.contrib.auth.decorators import login_required
from django.htt import HttpResponse
from statistics.models import *
from monitor.models import *
import datetime

def sys_alarm():
    raw_data = SysAlarm.objects.filter(name='', time__gte=start_time, time__lte=end_time)
    for d in raw_data
