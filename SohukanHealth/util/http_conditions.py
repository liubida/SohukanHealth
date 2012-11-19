# -*- coding: utf-8 -*-
'''
Created on Nov 16, 2012

@author: liubida
'''
from config.config import c
import datetime


def share_channels_last_modified(request):
    start_time = request.GET.get('start_time', c.SHARE_CHANNEL_MIN_TIME)
    end_time = request.GET.get('end_time', datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
    data_grain = request.GET.get('data_grain', 'day')
    data_grain = data_grain if data_grain else 'day'
    
    if start_time == 'NaN-aN-aN aN:aN:aN': 
        start_time = c.SHARE_CHANNEL_MIN_TIME
    if end_time == 'NaN-aN-aN aN:aN:aN': 
        end_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    
    
    
    pass
