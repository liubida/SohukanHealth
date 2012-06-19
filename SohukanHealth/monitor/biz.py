# -*- coding: utf-8 -*-
'''
Created on Jun 19, 2012

@author: liubida
'''
import datetime

def calc_app_available(duration='day'):
    '''duration=hour, day, week, month, sixmonths, year'''
    
    now = datetime.datetime.now()

    if 'hour' == duration:
        delta = datetime.timedelta(hours=1)
    elif 'day' == duration:
        delta = datetime.timedelta(days=1)
    elif 'week' == duration:
        delta = datetime.timedelta(weeks=1)
    elif 'month' == duration:
        datetime.date()
        delta = datetime.timedelta(weeks=4)
    elif 'sixmonths' == duration:
        pass
    elif 'year' == duration:
        pass
    start_time = now - delta
    print start_time

if __name__ == '__main__':
#    calc_app_available('hour')
    now = datetime.datetime.now()
    print now
