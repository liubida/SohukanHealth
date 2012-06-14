# -*- coding: utf-8 -*-
'''
Created on Jun 7, 2012

@author: liubida
'''

from config import constant
from config.constant import cookie
from dao.models import AppAvailableData
from monitor.system.worker import add_worker, read_worker
from util.random_spider import RandomSpider
import datetime

def monitor_read():
    value = read_worker(cookie).test()
    data = AppAvailableData(name='read', category='', result=value.get('result', False), \
                            time=datetime.datetime.now(), time_used=value.get('time_used', constant.read_time_limit), comments='')
    data.save()

def monitor_add():
    url = RandomSpider().get_valid_url()
    value = add_worker(url, cookie).test()
    data = AppAvailableData(name='add', category='', result=value.get('result', False), \
                            time=datetime.datetime.now(), time_used=value.get('time_used', constant.add_time_limit), comments=url)
    data.save()
    
if __name__ == '__main__':
    monitor_add()
#    url = RandomSpider().get_valid_url()
#        
#    add = add_worker(url, cookie)
#    add_value = add.test()
    
#    read = read_worker(cookie)
#    read_value = read.test()
#    monitor_read(cookie)
    

