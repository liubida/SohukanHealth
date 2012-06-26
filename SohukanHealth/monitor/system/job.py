# -*- coding: utf-8 -*-
'''
Created on Jun 7, 2012

@author: liubida
'''

from config.config import c, lock
from monitor.models import AppAvailableData, SomeTotal
from monitor.system.worker import add_worker, read_worker
from util import print_info
from util.random_spider import RandomSpider
import MySQLdb
import datetime

@print_info(name='read_job')
def read_job():
    value = read_worker(c.cookie).test()
    data = AppAvailableData(name='read', category='', result=value.get('result', False), \
                            time=datetime.datetime.now(), time_used=value.get('time_used', c.read_time_limit), \
                            comments=value.get('comments', ''))
    data.save()
    return value

@print_info(name='add_job')
def add_job():
    url = RandomSpider().get_valid_url()
    value = add_worker(url, c.cookie).test()
    data = AppAvailableData(name='add', category='', result=value.get('result', False), \
                            time=datetime.datetime.now(), time_used=value.get('time_used', c.add_time_limit), \
                            comments=value.get('comments', url))
    data.save()
    return value

@print_info(name='user_total_job')
def user_total_job():
    # TODO: this is a tmp job, it will be deleted
    locked = False
    try:
        if lock.acquire():
            locked = True
            # TODO: there should be a dbhelper
            conn = MySQLdb.connect(**c.db_config)
            cursor = conn.cursor()
            cursor.execute('select count(*) from account_user')
            result = cursor.fetchone()
            now = datetime.datetime.now()
            data = SomeTotal(name='user', time=now, count=result[0])
            data.save()
            return result[0]
    except Exception as e:
        c.logger.error(e)
        return str(e)
    finally:
        if locked:
            lock.release()
        try:
            if cursor:
                cursor.close()
        except Exception as e:
            c.logger.error(e)
        finally:
            if conn:
                conn.close()

@print_info(name='bookmark_total_job')
def bookmark_total_job():
    # TODO: this is a tmp job, it will be deleted
    locked = False;
    try:
        if lock.acquire():
            locked = True
            conn = MySQLdb.connect(**c.db_config)
            cursor = conn.cursor()
            sum = 0
            for i in range(64):
                cursor.execute ("select count(*) from bookmark_bookmark_%s" % i)
                result = cursor.fetchone()
                sum += result[0]
            now = datetime.datetime.now()
            data = SomeTotal(name='bookmark', time=now, count=sum)
            data.save()
            return sum
    except Exception as e:
        c.logger.error(e)
        return str(e)
    finally:
        if locked:
            lock.release()
        try:
            if cursor:
                cursor.close()
        except Exception as e:
            c.logger.error(e)
        finally:
            if conn:
                conn.close()
        
if __name__ == '__main__':
#    mysql_ping_job();
    user_total_job()
    bookmark_total_job()

#    url = RandomSpider().get_valid_url()
#        
#    add = add_worker(url, c.cookie)
#    add_value = add.test()
    
#    read = read_worker(c.cookie)
#    read_value = read.test()
#    monitor_read(c.cookie)
    


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
