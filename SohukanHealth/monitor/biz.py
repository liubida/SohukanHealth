# -*- coding: utf-8 -*-
'''
Created on Jun 19, 2012

@author: liubida
'''
from monitor.models import AppAvailableData
import datetime
import anyjson

def dict_to_json(data):
    s = {}
    s['success'] = True
    s['info'] = ''
    s['code'] = 0
    s['total'] = 1
    s['list'] = []
    s['list'].append(data)
    return s
    
def appAvailableData_to_json(data):
    s = {}
    s['success'] = True
    s['info'] = ''
    s['code'] = 0
    s['total'] = data.count()
    s['list'] = []
    for d in data:
        tmp = {}
        tmp['name'] = d['name']
        tmp['time_used'] = d['time_used']
        tmp['time'] = d['time'].strftime('%Y.%m.%d %H:%M:%S')
        s['list'].append(tmp)
    return anyjson.dumps(s)   
    
if __name__ == '__main__':
    pass
