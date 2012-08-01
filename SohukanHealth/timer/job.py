# -*- coding: utf-8 -*-
'''
Created on Jun 7, 2012

@author: liubida
'''

import sys
import os
root_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
print root_path
sys.path.append(root_path)
print sys.path

from django.core.management import setup_environ
from SohukanHealth import settings
print settings
setup_environ(settings)

from config.config import c
from monitor.models import AppAvailableData, SomeTotal, SysAlarm
from monitor.system.worker import add_worker, read_worker
from statistics.biz import get_userdata_for_day_report, \
    get_bookmarkdata_for_day_report, get_bookmark_website_raw_data, \
    get_bookmark_percent_raw_data, test_id, _is_test
from statistics.models import DayReport, UA
from timer.sms import sms
from util import print_info, query_ua
from util.random_spider import RandomSpider
import MySQLdb
import anyjson
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
    try:
        # TODO: there should be a dbhelper
        conn = MySQLdb.connect(**c.db_config)
        cursor = conn.cursor()

        #去掉测试用户的id
        tmp = ' where id > 100 and id !='
        tmp += ' and id !='.join(map(lambda x:str(x), test_id))
        print tmp
        cursor.execute('select count(*) from account_user %s' % tmp)
        result = cursor.fetchone()
        now = datetime.datetime.now()
        data = SomeTotal(name='user', time=now, count=result[0])
        data.save()
        return result[0]
    except Exception, e:
        c.logger.error(e)
        return str(e)
    finally:
        try:
            if cursor:
                cursor.close()
        except Exception, e:
            c.logger.error(e)
        finally:
            if conn:
                conn.close()

@print_info(name='bookmark_total_job')
def bookmark_total_job():
    try:
        conn = MySQLdb.connect(**c.db_config)
        cursor = conn.cursor()
        sum = 0
        for i in range(64):
            cursor.execute ("select user_id, count(*) from bookmark_bookmark_%s group by user_id" % i)
            results = cursor.fetchall()
            for d in results:
                user_id = int(d[0])
                count = int(d[1])
                # 去掉测试用户添加的文章
                if not _is_test(user_id):
                    sum += count
        now = datetime.datetime.now()
        data = SomeTotal(name='bookmark', time=now, count=sum)
        data.save()
        return sum
    except Exception, e:
        c.logger.error(e)
        return str(e)
    finally:
        try:
            if cursor:
                cursor.close()
        except Exception, e:
            c.logger.error(e)
        finally:
            if conn:
                conn.close()

@print_info(name='add_alarm_job')
def add_alarm_job():
    start_time = datetime.datetime.now() - datetime.timedelta(hours=0.5) 
    add_failure_data = AppAvailableData.objects.filter(name='add', result=False, time__gte=start_time).values('time')
    failure_count = len(add_failure_data)
    
    if failure_count >= c.add_alarm_time: 
        try:
            start_time = add_failure_data[0]['time']
            end_time = add_failure_data[failure_count - 1]['time']
            type = 'add_bookmark'
            msg = 'add failure count(30min):%s' % str(failure_count)
            sms(mobile_list=c.mobile_list, message_post=msg)

            latest = SysAlarm.objects.order_by('-gmt_create')[0]
            if (not latest) or start_time > latest.end_time and (start_time - latest.end_time).total_seconds() > 600:
                # 一次新故障
                alarm = SysAlarm(type=type, start_time=start_time, end_time=end_time)
                alarm.save()
            else:
                # 添加-报警的定时任务是每10min执行一次, 如果本次报警的时间和上次开始的时间<10min, 则认为是同一次故障
                # 同一次故障的持续报警, 只需修改上次的结束时间即可
                latest.end_time = end_time
                latest.save()
        except Exception, e:
            c.logger.error(e)
            c.logger.error(msg)
            print msg

@print_info(name='read_alarm_job')
def read_alarm_job():
    start_time = datetime.datetime.now() - datetime.timedelta(hours=0.5) 
    read_failure_data = AppAvailableData.objects.filter(name='read', result=False, time__gte=start_time).values('time')
    failure_count = len(read_failure_data)
    
    if failure_count >= c.read_alarm_time: 
        try:
            start_time = read_failure_data[0]['time']
            end_time = read_failure_data[failure_count - 1]['time']
            print start_time
            print end_time
            type = 'read_bookmark'
            msg = 'read failure count(30min):%s' % str(failure_count)
            sms(mobile_list=c.mobile_list, message_post=msg)

            # 获取上一次的报警信息
            latest = SysAlarm.objects.order_by('-gmt_create')[0]
            if (not latest) or start_time > latest.end_time and (start_time - latest.end_time).total_seconds() > 600:
                # 一次新故障
                alarm = SysAlarm(type=type, start_time=start_time, end_time=end_time)
                alarm.save()
            else:
                # 添加-报警的定时任务是每10min执行一次, 如果本次报警的时间和上次开始的时间<10min, 则认为是同一次故障
                # 同一次故障的持续报警, 只需修改上次的结束时间即可
                latest.end_time = end_time
                latest.save()
        except Exception, e:
            c.logger.error(e)
            c.logger.error(msg)
            print msg
        
#    read_failure_data = AppAvailableData.objects.filter(name='read', result=False, time__gte=start_time)
#        if len(read_failure_data) >= c.read_alarm_time:
#            msg = 'read failure count(30min):%s' % str(len(read_failure_data))
#            type = 'read_bookmark'

@print_info(name='day_report_job')
def day_report_job(now=None):
    '''day_report created at 23:58:00'''
    
    # 今天
    if not now:
        now = datetime.datetime.now()
    
    today_start = now.replace(hour=0, minute=0, second=0, microsecond=0)
    today_end = now.replace(hour=23, minute=59, second=59, microsecond=0)
    
    user = get_userdata_for_day_report(today_start, today_end);
    bookmark = get_bookmarkdata_for_day_report(today_start, today_end);
    
    bookmark_count = {}
    bookmark_count['percent'], bookmark_count['data'] = get_bookmark_percent_raw_data(today_start, today_end, limit=20)
    bookmark_website = {}
    bookmark_website['data'] = get_bookmark_website_raw_data(today_start, today_end, limit=20)
    
    jsondata = {}
    jsondata['user'] = user
    jsondata['bookmark'] = bookmark
    jsondata['bookmark_website'] = bookmark_website
    jsondata['bookmark_count'] = bookmark_count
    
    day_report = DayReport(time=datetime.datetime.now(), version=c.day_report_version, jsondata=anyjson.dumps(jsondata))
    day_report.save();
    
@print_info(name='fix_ua_job')
def fix_ua_job():
    try:
        ua = UA.objects.filter(is_crawler=False)
        for u in ua:
            if u.ua_string.startswith(u'搜狐随身看'):
                u.platform = 'Darwin'
                u.is_crawler = True
            else:
                ret = query_ua(u.ua_string)
                if ret:
                    u.platform = ret['os_type']
                    u.is_crawler = True
            u.save()
    except Exception, e:
        c.logger.error(e)

if __name__ == '__main__':
    add_alarm_job()
    read_alarm_job()
#    read_job()
#    add_job()
#    now = datetime.datetime.now()
#    start = datetime.datetime(2012, 7, 16, 23, 58, 4)
#    while start < now:
#        print start
#        day_report_job(start)
#        start += datetime.timedelta(days=1)
#    today = datetime.date.today()
#    today = today.replace(day=31)
#    print today
#    d = datetime.timedelta(days=1)
#    print today + d
#    
#    fix_ua_job()
#    mysql_ping_job();
#    user_total_job()
#    bookmark_total_job()
#    add_and_read_alarm_job()
#    url = RandomSpider().get_valid_url()
