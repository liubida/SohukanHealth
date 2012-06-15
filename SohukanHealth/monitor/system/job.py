# -*- coding: utf-8 -*-
'''
Created on Jun 7, 2012

@author: liubida
'''

from config import constant
from config.constant import cookie
from exception import JobException
from log import logger
from monitor.models import AppAvailableData, UserTotal
from monitor.system.worker import add_worker, read_worker
from util.random_spider import RandomSpider
import config
import datetime

def read_job():
    value = read_worker(cookie).test()
    data = AppAvailableData(name='read', category='', result=value.get('result', False), \
                            time=datetime.datetime.now(), time_used=value.get('time_used', constant.read_time_limit), comments='')
    data.save()

def add_job():
    url = RandomSpider().get_valid_url()
    value = add_worker(url, cookie).test()
    data = AppAvailableData(name='add', category='', result=value.get('result', False), \
                            time=datetime.datetime.now(), time_used=value.get('time_used', constant.add_time_limit), comments=url)
    data.save()

def user_total_job():
    try:
        conn = config.conn;
        cursor = conn.cursor()
        cursor.execute('select count(*) from account_user')
        result = cursor.fetchone()
        data = UserTotal(time=datetime.datetime.now(), count=result[0])
        data.save()
    except JobException as e:
        logger.error(e)
    finally:
        try:
            if cursor:
                cursor.close()
        except JobException as e:
            logger.error(e)
        finally:
            pass
#            if conn:
#                conn.close()

#def user_register_job():
#    try:
#        now = datetime.datetime.now()
#        min_time = now - datetime.timedelta(minutes=12)
#        delta = UserTotal.objects.filter(time__gte=min_time, time__lte=now)
#        delta = delta.count()
#        if delta > 0:
#            data = 
#        conn = config.conn;
#        cursor = conn.cursor()
#        cursor.execute('select passport_userid from account_user where gmt_create > ')
#        count = cursor.fetchone()
#        data = RegisterUser(passport=)
#    data = AppAvailableData(name='add', category='', result=value.get('result', False), \
#                            time=datetime.datetime.now(), time_used=value.get('time_used', constant.add_time_limit), comments=url)
#    data.save()
#        
#        
#        print 'count:', count[0]
#    except JobException as e:
#        logger.error(e)
#    finally:
#        try:
#            if cursor:
#                cursor.close()
#        except JobException as e:
#            logger.error(e)
#        finally:
#            if conn:
#                conn.close()

        
if __name__ == '__main__':
    user_total_job()
#    url = RandomSpider().get_valid_url()
#        
#    add = add_worker(url, cookie)
#    add_value = add.test()
    
#    read = read_worker(cookie)
#    read_value = read.test()
#    monitor_read(cookie)
    

